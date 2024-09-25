from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
#we need these two imports for certain functions of our custom user model


#We also need to create a custom account manager, and this needs to stay at the top.
#Basically whenever we create a custom user model, we need to overwrite the create
#user and create super user methods too. And it will require that BaseUserManager
#module.

class MyAccountManager(BaseUserManager):
	#This one is for regular users
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError("Users must have an email address.")
		if not username:
			raise ValueError("Users must have a username.")
		#We basically created the exceptions at the beginning if the fields are
		#empty.

		#So, we create the user like this if there are no problems.
		user = self.model(
			email = self.normalize_email(email),
			#normalize_email just converts all the characters to lower case,
			#it's also only available with BaseUserManager

			username = username,
			)
		user.set_password(password) #sets the entered password to the user object
		user.save(using=self._db) #saves the user to the database
		return user
	
	#And this one will be for the super users
	def create_superuser(self, email, username, password):
		#Here, we do "self.create_user" instead of "self.model", because 
		#creating a super user is just another variation of creating a user.
		user = self.create_user(
			email = self.normalize_email(email),
			username = username,
			password = password, 
			#Apparently we accept the password parameter here
			#because a super user is created through the console, maybe?
			)
		user.is_admin=True
		user.is_staff=True
		user.is_superuser=True
		#We set the necessary privileges for the super user
		user.save(using=self._db)
		return user

# Create your models here.

#Here's our account, and it needs to be extended by the AbstractBaseUser
class Account(AbstractBaseUser):

	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	#Here's our email field for our user model, and it needs to be "unique".

	username = models.CharField(max_length=30, unique=True)
	#And username field should be unique as well.

	#These next 6 fields, along with "username", that we are going to add are required for
	#the "AbstractBaseUser" class that we are using, btw.

	date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
	last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	#Along with this, depending on our user model, we could add more fields too, like
	#"first_name" and "last_name" and whatnot.

	#Here is an important point with the Django framework, we have a django specific
	#variable called "USERNAME_FIELD" and even though it's name is "USERNAME", you have
	#to assign that to whatever field that you are going to use as the login parameter.
	#As such:

	USERNAME_FIELD = "email"
	#The built-in user model uses the "username" parameter for it.
	#This basically swaps the logic used for USERNAME_FIELD on django.
	#So, while "username" used to be one of the required parameters for the 
	#"AbstractBaseUser" class, now it's become the "email" field instead.

	#With that, we need to enter any other additional fields that are a requirement for 
	#a user to register:
	
	REQUIRED_FIELDS = ["username"]

	#This is how we set up that our parameters will know where to look for 
	#the manager we created earlier by referencing it here
	objects = MyAccountManager()

	#Then, we will do the self referencing stuff that will print the stuff

	def __str__(self):
		return self.email
		#you can also make it print out anything you want, you can even concatanate like
		#return self.email + ", " + self.username

	#Now, we have a couple more functions that we have to define for our custom user model
	#to be able to work.

	#Basically this gets the permissions for a particular user
	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True