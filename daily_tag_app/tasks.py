from celery.task.schedules import crontab  
from celery.decorators import periodic_task  
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from .models import HeadTag

# 定时任务 每隔2分钟 更新一次阅读数
@periodic_task(run_every=2*60,name='update_tag_view_recored')
def update_tag_view_record():
	# 首先从缓存里读取数据
	tag_view_cache_list = cache.keys('htpv_*')
	# 循环数据，逐条更新进数据库
	for item in tag_view_cache_list:
		item_view_record_value = cache.get(item)
		item = item.split('_')
		item_id = item[1]
		try:
			head_tag = HeadTag.objects.get(id=item_id)
		except ObjectDoesNotExist:
			pass

		head_tag.page_view_count = item_view_record_value

		# save
		head_tag.save()









