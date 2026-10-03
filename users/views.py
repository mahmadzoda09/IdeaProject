from sqlite3 import IntegrityError
from django.db import IntegrityError

from django.contrib.auth import login 
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView , ListView ,DetailView , DeleteView
from django.views import View
from .forms import *
from .models import *
from .permission import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")

class UserLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True
    next_page = reverse_lazy("users")

class UserLogoutView(LoginRequiredMixin ,LogoutView):
    next_page = reverse_lazy("login")

class all_users(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class UserDetailView(LoginRequiredMixin ,DetailView):
    model = User
    template_name = "users/user_detail.html"
    context_object_name = "user"

class BrandCreateView(LoginRequiredMixin ,CreateView):
    form_class = BrandForm
    template_name = 'cars/add_brand.html'
    success_url = reverse_lazy('brands')


class BrandShowView(LoginRequiredMixin ,ListView):
    model = Brand
    template_name = 'cars/brands.html'
    context_object_name = 'brands'


class CarModelCreateView(LoginRequiredMixin ,CreateView):
    form_class = CarModelForm
    template_name = 'cars/add_model.html'
    success_url = reverse_lazy('models')


class CarModelView(LoginRequiredMixin ,ListView):
    model = CarModel
    template_name = 'cars/models.html'
    context_object_name = 'models'

class CarCreateView(LoginRequiredMixin, CreateView):
    form_class = CarForm
    template_name = 'cars/add_car.html'
    success_url = reverse_lazy('cars')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CarView(LoginRequiredMixin ,ListView):
    model = Car
    template_name = 'cars/cars.html'
    context_object_name = 'cars'
    paginate_by = 12
 
    SORT_OPTIONS = {
        "newest": "-id",
        "price_asc": "price",
        "price_desc": "-price",
        "year_desc": "-year",
    }
 
    def get_queryset(self):
        qs = Car.objects.select_related("brand", "model")
        g = self.request.GET
 
        # --- search (brand, model, description) ---
        q = g.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(model__name__icontains=q)
                | Q(brand__name__icontains=q)
                | Q(description__icontains=q)
            )
 
        # --- checkbox filters (several values allowed) ---
        brands = g.getlist("brand")
        if brands:
            qs = qs.filter(brand_id__in=brands)
 
        fuels = g.getlist("fuel")
        if fuels:
            qs = qs.filter(fuel_type__in=fuels)
 
        transmissions = g.getlist("transmission")
        if transmissions:
            qs = qs.filter(transmission__in=transmissions)
 
        colors = g.getlist("color")
        if colors:
            qs = qs.filter(color__in=colors)
 
        # --- ranges ---
        if g.get("min_price"):
            qs = qs.filter(price__gte=g["min_price"])
        if g.get("max_price"):
            qs = qs.filter(price__lte=g["max_price"])
        if g.get("min_year"):
            qs = qs.filter(year__gte=g["min_year"])
        if g.get("max_year"):
            qs = qs.filter(year__lte=g["max_year"])
 
        return qs.order_by(self.SORT_OPTIONS.get(g.get("sort"), "-id"))
 
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        g = self.request.GET
 
        # options for the sidebar
        ctx["brands"] = Brand.objects.all()
        ctx["fuel_choices"] = Car._meta.get_field("fuel_type").choices
        ctx["transmission_choices"] = Car._meta.get_field("transmission").choices
        ctx["colors"] = (
            Car.objects.exclude(color="")
            .values_list("color", flat=True)
            .distinct()
            .order_by("color")
        )
 
        # what is currently selected
        ctx["values"] = g
        ctx["sel_brands"] = g.getlist("brand")
        ctx["sel_fuel"] = g.getlist("fuel")
        ctx["sel_trans"] = g.getlist("transmission")
        ctx["sel_colors"] = g.getlist("color")
        ctx["current_sort"] = g.get("sort", "newest")
 
        # query strings that keep filters while changing sort / page
        params = g.copy()
        params.pop("page", None)
        ctx["querystring"] = params.urlencode()
        params.pop("sort", None)
        ctx["qs_nosort"] = params.urlencode()
        return ctx
 


class CarDetailView(LoginRequiredMixin ,DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["is_favorite"] = Favorite.objects.filter( user=self.request.user, car=self.object).exists()

        return context

class CarImageCreateView(LoginRequiredMixin , CreateView):
    model = CarImage
    form_class = CarImageForm
    template_name = "cars/image_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["owner"] = self.request.user
        kwargs["car"] = Car.objects.get(id=self.kwargs["car_id"])

        return kwargs

    def form_valid(self, form):
        form.instance.car = form.car
        return super().form_valid(form)

    def get_success_url(self):
        return f"/cars/{self.kwargs['car_id']}/"


class CarDeleteView(LoginRequiredMixin ,DeleteView):
    model = Car
    template_name = 'cars/car_delete.html'
    success_url = reverse_lazy('cars')

class StartChatView(LoginRequiredMixin, View):
    def get(self, request, owner_id):
        owner = User.objects.get(id=owner_id)
        if request.user == owner:
            return redirect("cars")
        
        chat = Chat.objects.filter( user1=request.user, user2=owner).first()

        if not chat:
            chat = Chat.objects.filter( user1=owner, user2=request.user).first()

        if not chat:
            chat = Chat.objects.create( user1=request.user, user2=owner)

        return redirect("chat", chat.id)


class ChatView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = "cars/chat.html"
    context_object_name = "chat"

    def get_queryset(self):
        return Chat.objects.filter( Q(user1=self.request.user) | Q(user2=self.request.user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MessageForm()
        return context


class SendMessageView(LoginRequiredMixin, CreateView):
    form_class = MessageForm
    def form_valid(self, form):
        chat = Chat.objects.get(id=self.kwargs["chat_id"])
        form.instance.chat = chat
        form.instance.sender = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return f"/chat/{self.kwargs['chat_id']}/"

class MyChatsView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = "cars/my_chats.html"
    context_object_name = "chats"

    def get_queryset(self):
        return Chat.objects.filter(user1=self.request.user) | Chat.objects.filter( user2=self.request.user )

class FavoriteCarView(LoginRequiredMixin,View):
    def post(self, request, pk):
        car = Car.objects.get(id=pk)
        favorite = Favorite.objects.filter(user=request.user,car=car).first()
        if favorite:
            favorite.delete()
        else:
            Favorite.objects.create(user=request.user, car=car)
        
        return redirect("car_detail", pk=pk)

class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = "cars/favorites.html"
    context_object_name = "favorites"

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class OrderCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        car = Car.objects.get(id=pk)

        if car.owner == request.user:
            return redirect("car_detail", pk=pk)
        
        if Order.objects.filter(user=request.user, car=car).exists():
            return redirect("car_detail", pk=pk)

        try:
            Order.objects.create(user=request.user, car=car)
        except IntegrityError:
            return redirect("car_detail", pk=pk)

        Notification.objects.create( user=car.owner, car=car, message=f"{request.user.username} wants to buy your {car.model}.")
        return redirect("car_detail", pk=pk)
    
class MyOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "cars/orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "cars/notifications.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")

class DeleteOrderView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = "cars/delete_order.html"
    success_url = reverse_lazy("my_orders")

    def get_queryset(self):
        return Order.objects.filter(
            Q(user=self.request.user) | Q(car__owner=self.request.user)
        )

class SellCarView(LoginRequiredMixin, View):
    def post(self, request, car_id, notification_id):
        car = Car.objects.get(id=car_id)
        notification = Notification.objects.get(id=notification_id)
        if car.owner == request.user and notification.user == request.user:
            car.status = "sold"
            car.save()
            notification.is_read = True
            notification.save()
            car.delete()

        return redirect("notifications")

class DeleteNotificationView(LoginRequiredMixin, DeleteView):
    model = Notification
    template_name = "cars/notification_delete.html"
    success_url = reverse_lazy("notifications")

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)