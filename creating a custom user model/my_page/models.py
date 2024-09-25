from django.db import models

# Create your models here.

#Let's create a variable named PRIORITY here that we will use for the priority field below later.
#It's gonna be a list of tuples.
PRIORITY = [
	("H", "High"),
	("M", "Medium"),
	("L", "Low")
]

#The name is up to us. We create the data field as a class everytime.
#And inside the paranthesis has to be models.Model so program understands that this is
#a Django specific data model.

class Question(models.Model):

	#Let's say we want to hold a title for our users' questions. The variable name is
	#up to us.
	title = models.CharField(max_length=60)
	#We use character field (which you can see from the documentation above) for this,
	#which has a required attribute called max length, so we declare that too.

	#Then let's say we want a field for the actual question.
	question = models.TextField()
	#Text field is another type of field that we can use.

	#Then let's say we create a field called priority.
	priority = models.CharField(max_length=1, choices=PRIORITY)
	#We also assigned an optional field called choices here.

	def __str__(self):
		return self.title
	#Then, we declare a private method like this inside our class, what this does is,
	#basically when our data is called into view, this "self.title" shows as the default
	#field.