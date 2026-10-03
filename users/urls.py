from django.urls import path
from .views import *


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path('users/', all_users.as_view(), name='users'),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("add_brand/" , BrandCreateView.as_view() , name='add_brand'),
    path("brands/" , BrandShowView.as_view() , name='brands'),
    path("add_model/" , CarModelCreateView.as_view() , name='add_model'),
    path("models/" , CarModelView.as_view() , name='models'),
    path("add_car/" , CarCreateView.as_view() , name='add_car'),
    path("" , CarView.as_view() , name='cars'),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car_detail"),
    path("cars/<int:car_id>/add-image/",CarImageCreateView.as_view(),name="car_image_add"),
    path("cars/<int:pk>/delete", CarDeleteView.as_view(), name="car_delete"),
    path("chat/start/<int:owner_id>/",StartChatView.as_view(),name="start_chat"),
    path("chat/<int:pk>/",ChatView.as_view(),name="chat"),
    path("chat/<int:chat_id>/send/",SendMessageView.as_view(),name="send_message"),
    path("chats/",MyChatsView.as_view(),name="my_chats"),
    path("cars/<int:pk>/favorite/", FavoriteCarView.as_view(), name="favorite"),
    path("favorites/", FavoriteListView.as_view(), name="favorites"),
    path("cars/<int:pk>/buy/", OrderCreateView.as_view(), name="buy_car"),
    path("orders/", MyOrdersView.as_view(), name="my_orders"),
    path("notifications/", NotificationListView.as_view(), name="notifications"),
    path("orders/<int:pk>/delete/",DeleteOrderView.as_view(),name="order_delete"),
    path("sell/<int:car_id>/<int:notification_id>/", SellCarView.as_view(), name="sell"),
    path("notifications/<int:pk>/delete/",DeleteNotificationView.as_view(),name="notification_delete"),
]