from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as lazy_text

# Create your models here.

# class CustomAccountManager(BaseUserManager):
#     def create_superuser(self, email, username, password, **other_fields):
#         other_fields.setdefault('is_staff', True)
#         other_fields.setdefault('is_superuser', True)
#         other_fields.setdefault('is_active', True)
#
#         if other_fields.get('is_staff') is not True:
#             raise ValueError("Superuser must be assigned to is_staff=True.")
#         if other_fields.get('is_superuser') is not True:
#             raise ValueError("Superuser must be assigned to is_superuser=True.")
#
#         return self.create_user(email, username, password, **other_fields)
#
#     def create_user(self, email, username, password, **other_fields):
#         if not email:
#             raise ValueError(lazy_text('You must provide an email address'))
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, **other_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
# class NewUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(lazy_text("Email address"), unique=True)
#     username = models.CharField(max_length=150, unique=True)
#     creation_date = models.DateTimeField(default=timezone.now)
#     about = models.TextField(lazy_text("About"), max_length=500, blank=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#
#     objects = CustomAccountManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        unique_together = ('menuitem', 'user')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User,
                                      on_delete=models.SET_NULL, related_name='delivery_crew', null=True)
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self) -> str:
        return self.user.username


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menuitem')
