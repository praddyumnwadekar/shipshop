from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password = None):
        """
        Create and return a regular user with the given details.
        
        This method creates a new user account with the provided information.
        It validates that email and username are provided, normalizes the email,
        and sets the password.
        
        Args:
            first_name (str): User's first name
            last_name (str): User's last name
            username (str): Unique username for the user
            email (str): User's email address
            password (str, optional): User's password
        
        Returns:
            Account: The created user instance
        
        Raises:
            ValueError: If email or username is not provided
        """
        if not email:
            raise ValueError("User must provide an Email Address")
        
        if not username:
            raise ValueError("User must have username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, first_name,  last_name, email, username, password):
        """
        Create and return a superuser with admin privileges.
        
        This method creates a superuser account with full administrative
        privileges. It sets all admin flags to True and saves the user.
        
        Args:
            first_name (str): Superuser's first name
            last_name (str): Superuser's last name
            email (str): Superuser's email address
            username (str): Unique username for the superuser
            password (str): Superuser's password
        
        Returns:
            Account: The created superuser instance
        """
        user = self.create_user(
            email= self.normalize_email(email),
            username= username,
            password= password,
            first_name= first_name,
            last_name= last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user


# Create your models here.
class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField( max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)

    # REQUIRED_FIELDS
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False) 
    is_staff        = models.BooleanField(default=False) 
    is_active       = models.BooleanField(default=False) 
    is_superadmin   = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
            'username', 
            'first_name', 
            'last_name'
        ]
    
    objects = MyAccountManager()

    def __str__(self):
        """
        Return a string representation of the Account instance.
        
        Returns:
            str: The user's email address
        """
        return self.email 
    
    def has_perm(self, perm, obj = None):
        """
        Check if the user has a specific permission.
        
        This method determines if the user has the given permission.
        For this implementation, it returns True if the user is an admin.
        
        Args:
            perm (str): The permission to check
            obj (object, optional): The object to check permission against
        
        Returns:
            bool: True if user is admin, False otherwise
        """
        return self.is_admin

    def has_module_perms(self, add_label):
        """
        Check if the user has permissions for a specific app module.
        
        This method determines if the user has permissions for the given
        Django app label. For this implementation, it always returns True.
        
        Args:
            add_label (str): The Django app label to check permissions for
        
        Returns:
            bool: Always returns True
        """
        return True