from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to='profile_photos/', 
        null=True, 
        blank=True, 
        default='static/images/profile_photo.png'
    )
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    INTENSITY_CHOICES = [
        ('0.3', 'Gentle (0.3kg / week)'),
        ('0.6', 'Light (0.6kg / week)'),
        ('0.7', 'Moderate (0.75kg / week)'),
        ('0.8', 'Aggressive (1kg / week)'),
        ('0.9', 'High Intensity (1.25kg / week)')
    ]
    
    intensity = models.CharField(
        max_length=10, 
        choices=INTENSITY_CHOICES, 
        blank=True, 
        null=True
    )
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    
    BODY_GOAL_CHOICES = [
        ('victoria-secret-thin', 'Victoria-Secret Thin'),
        ('slim', 'Slim'),
        ('muscular', 'Muscular'),
        ('athletic', 'Athletic'),
        ('sumo-wrestler', 'Sumo Wrestler'),
    ]
    body_goal = models.CharField(max_length=30, choices=BODY_GOAL_CHOICES, blank=True)
    
    receive_emails = models.BooleanField(default=False)
    agree_to_terms = models.BooleanField(default=False)
    
    # Add these new fields
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    def has_perm(self, perm, obj=None):
        """Does the user have specific permissions?"""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return self.is_superuser

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
      
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )

    def __str__(self):
        return self.email