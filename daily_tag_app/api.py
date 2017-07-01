from requests import get
from django.contrib.gis.geoip2 import GeoIP2
from django.core.exceptions import ObjectDoesNotExist
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache

from .models import Country, City, HeadTag
from .serializers import HeadTagSerializer
from .public_methods import check_init

# init session
@api_view(['GET'])
def check_session_init(request):
	# 初始化session
	check_init(request)
	return Response(status=status.HTTP_200_OK)


# post_head_tag
@api_view(['POST'])
@csrf_protect
def post_head_tag(request):
	# get ip and ip_city
	ip = get('https://api.ipify.org').text
	session_address = request.session['address'].split('_')
	city_region = session_address[0]
	country_code = session_address[1]
	country = Country.objects.get(code=country_code)
	city = City.objects.get(region=city_region, belong_to_country=country)

	serialziers = HeadTagSerializer(data=request.data)
	if serialziers.is_valid():
		title = serialziers.initial_data['title']
		desc = serialziers.initial_data['desc']
		head_tag = HeadTag.objects.create(title=title, desc=desc, ip=ip, belong_to_city=city)
		# 重新序列化创建的对象
		# 刚才出错的原因在于，当使用序列化器进行output的时候，缺少必要的参数，所以报的就是keyerror
		# input的时候只需要提供非read_only_fileds内的参数，但是output的时候需要提供所有的参数
		serialziers = HeadTagSerializer(head_tag, many=False)
		return Response(serialziers.data,status=status.HTTP_200_OK)
	return Response(serialziers.errors, status=status.HTTP_400_BAD_REQUEST)

# get_head_tag
@api_view(['GET'])
def get_head_tags(request,country=None,city=None):

	# 如果参数都为none 说明是在做初始化的请求
	if country == None and city == None:
		session_address = request.session['address'].split('_')
		city_region = session_address[0]
		country_code = session_address[1]

		country = Country.objects.get(code=country_code)
		city = City.objects.get(region=city_region, belong_to_country=country)

		head_tags = HeadTag.objects.filter(belong_to_city=city)

	# 如果没有city参数，说明是在做国家的切换，这就是在做国家数据的请求
	elif country != None and city == None:
		country = Country.objects.get(code=country)
		# 查询country下的所有city
		head_tags = HeadTag.objects.filter(belong_to_city__in=country.cities.all())

	# 如果两个参数都包含，说明在查询特定城市的数据
	elif country != None and city != None:
		country = Country.objects.get(code=country)
		city = City.objects.get(region=city, belong_to_country=country)

		head_tags = HeadTag.objects.filter(belong_to_city=city)

	# 判断有没有查询到数据
	if head_tags.count() == 1 :

		serializer = HeadTagSerializer(head_tags, many=False)
		return Response(serializer.data, status=status.HTTP_200_OK)

	elif head_tags.count() > 1:

		serializer = HeadTagSerializer(head_tags, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	else:
		body = {
			'msg':'sorry,the query is empty'
		}
		return Response(body, status=status.HTTP_404_NOT_FOUND)


# head_tag详情接口
@api_view(['GET'])
def get_tag_detail(request,id):
	try:
		head_tag = HeadTag.objects.get(id=id)
	except ObjectDoesNotExist:
		body = {
			'msg':'headtag not found'
		}
		return Response(body, status=status.HTTP_404_NOT_FOUND)

	serializer = HeadTagSerializer(head_tag, many=False)
	return Response(serializer.data, status=status.HTTP_200_OK)


# 统计阅读数的接口
@api_view(['GET'])
def page_view_record(request,id):

	try:
		# 检查有没有这个帖子
		head_tag = HeadTag.objects.get(id=id)
	except ObjectDoesNotExist:
		body = {
			'msg':'head_tag not found',
		}
		# 没有就返回404
		return Response(body, status=status.HTTP_404_NOT_FOUND)

	key = 'htpv_{}'.format(head_tag.id)
	# 如果key存在 就读取key
	if cache.has_key(key):
		cache.incr(key)
		count = cache.get(key)

	# 如果key不存在 就设置缓存
	else:
		count = 1
		cache.set(key, count)

	body = {
		'head_tag_pv_count':count,
	}

	return Response(body, status=status.HTTP_200_OK)





