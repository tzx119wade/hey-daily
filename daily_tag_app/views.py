from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import HeadTag

# Create your views here.
@ensure_csrf_cookie
def index(request):
	return render(request, 'index.html')

@ensure_csrf_cookie
def detail(request):
	head_tag = HeadTag.objects.get(id=1)
	detail_url = head_tag.get_absolute_url()
	
	return HttpResponse(detail_url)
	