from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=20,blank=True)
    
    def __str__(self):
        return self.username

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

FUEL_TYPE = (
    ("petrol", "Бензин"),
    ("diesel", "Дизель"),
    ("electric", "Электричество"),
    ("hybrid", "Гибрид"),
    ("gas", "Газ"),
)

TRANSMISSION = (
    ("manual", "Механика"),
    ("automatic", "Автомат"),
)

class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='owners')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE , related_name='brands')
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE , related_name='models') 
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    fuel_type = models.CharField(choices=FUEL_TYPE, max_length=50)
    transmission = models.CharField(choices=TRANSMISSION, max_length=50)
    color = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=20, default="available") 
    
    def __str__(self):
        return self.model.name

class CarImage(models.Model):
    car = models.ForeignKey( Car, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="media/")

    def __str__(self):
        return f"Image of {self.car}"

class Chat(models.Model):
    user1 = models.ForeignKey( User, on_delete=models.CASCADE, related_name="chats_as_user1")
    user2 = models.ForeignKey( User, on_delete=models.CASCADE, related_name="chats_as_user2")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1} - {self.user2}"
    
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text[:30]}"

class Favorite(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="favorites")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_by")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.car}"

class Order(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="orders")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.car}"
    
class Notification(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE, related_name="notifications")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="notifications" , null=True, blank=True)
    order = models.ForeignKey( Order, on_delete=models.CASCADE, related_name="notification", null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username