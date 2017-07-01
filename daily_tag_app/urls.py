from django.conf.urls import url

from . import views
from . import api
urlpatterns = [
	url(r'^$',views.index, name='index'),
	url(r'^detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.detail, name='detail'),

	# API
	url(r'^api/check_session_init/$', api.check_session_init),
	url(r'^api/post_head_tag/$', api.post_head_tag),
	url(r'^api/get_head_tags/$', api.get_head_tags),
	url(r'^api/get_head_tags/(?P<country>\w+)/$', api.get_head_tags),
	url(r'^api/get_head_tags/(?P<country>\w+)/(?P<city>\d+)/$', api.get_head_tags),
	url(r'^api/get_tag_detail/(?P<id>\d+)/$', api.get_tag_detail),
	url(r'^api/page_view_record/(?P<id>\d+)/$', api.page_view_record),
]