from django.shortcuts import render
from my_page.models import Question
#We need to import our model too

# Create your views here.

def my_page_view(request):

	print(request.headers)

	context={}
	
	questions = Question.objects.all()
	#What this does is, basically selects all the query inside our database
	
	context['questions'] = questions
	#So this is getting added to the context of the view whenever there is a request.

	return render(request, "my_page/home.html", context)