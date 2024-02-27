from django.shortcuts import render
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

BLOG_POSTS_PER_PAGE = 10

def home_screen_view(request, *args, **kwargs):
	
	context = {}

	# Search
	query = ""
	if request.GET:
		query = request.GET.get('q', '')
		context['query'] = str(query)


	# Pagination
	page = request.GET.get('page', 1)

	return render(request, "personal/home.html", context)
