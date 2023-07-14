from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("user must have a email")
        user = self.model(
            email=email,
        )
        user.role = "Customer"
        user.is_superuser = False
        user.is_staff = False
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
        )
        user.role = "Admin"
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User_Profile(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=250, null=True)
    role = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    USERNAME_FIELD = 'email'
    objects = MyAccountManager()

    class Meta:
      get_latest_by = 'created_on'

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    total_tickets = models.IntegerField()
    available_tickets = models.IntegerField()#
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    description = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        managed = True
        db_table = 'event'

class BookingMaster(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User_Profile,on_delete=models.CASCADE,related_name="user", null=False)
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name="event", null=False)
    tickets = models.IntegerField(null=True)
    booking_date = models.DateField(null=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'booking_master'