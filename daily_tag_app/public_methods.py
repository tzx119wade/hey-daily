from requests import get
from django.contrib.gis.geoip2 import GeoIP2
from django.core.exceptions import ObjectDoesNotExist

from .models import Country, City

# handle_ip_address
def check_init(request):
	g = GeoIP2()
	if request.session.get('address',False):
		# 如果已经初始化过
		session_list = request.session['address'].split('_')
		session_data = {
			'city_region':session_list[0],
			'country_code':session_list[1]
		}

	else:
		# 如果没有初始化
		# 1.获取公共IP
		# 2.通过公共IP去查询地理位置
		# 3.从地理位置中获取必要的城市和国家参数，然后验证对应的model是否创建
		# 4.最后将city_region和country_code写入session中
		ip = get('https://api.ipify.org').text
		ip_location = g.city(ip)
		# check city and country
		city_region = ip_location['region']
		country_code = ip_location['country_code']

		# 创建city和country对象
		try:
			country = Country.objects.get(code=country_code)
		except ObjectDoesNotExist:
			country = Country.objects.create(code=country_code, name = ip_location['country_name'])

		try:
			city = City.objects.get(region = city_region)
		except ObjectDoesNotExist:
			city = City.objects.create(region=city_region, name=ip_location['city'],belong_to_country=country)
			
		# 保存session	
		request.session['address'] = city_region+'_'+country_code

		session_data = {
			'city_region':city_region,
			'country_code':country_code
		}
	return session_data

