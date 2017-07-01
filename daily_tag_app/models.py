from django.db import models
from django.core.urlresolvers import reverse
from datetime import date, datetime, time
from uuslug import slugify
# Create your models here.

# headtag
class HeadTag(models.Model):
	title = models.CharField(max_length=200,blank=True,null=True)
	desc = models.TextField(blank=True,null=True)
	slug = models.SlugField(blank=True,null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)
	belong_to_city = models.ForeignKey('City', related_name='headtags',blank=True,null=True)
	ip = models.GenericIPAddressField(protocol='IPv4',blank=True,null=True)
	detail_url = models.URLField(max_length=200,blank=True,null=True)
	page_view_count = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('daily_tag_app:detail',args=[self.id, self.slug])

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(HeadTag,self).save(*args, **kwargs)
		# 保存完后再调用赋值
		self.detail_url = self.get_absolute_url()

	class Meta:
		ordering = ('-created_date',)

# city
class City(models.Model):
	name = models.CharField(max_length=50,blank=True,null=True)
	region = models.CharField(max_length=20,blank=True, null=True)
	belong_to_country = models.ForeignKey('Country', related_name='cities')

	def __str__(self):
		return self.name


# country
class Country(models.Model):
	name = models.CharField(max_length=50, blank=True,null=True)
	code = models.CharField(max_length=20,blank=True, null=True)
	def __str__(self):
		return self.name

# view_record
class ViewRecord(models.Model):
	view_count = models.IntegerField()
	head_tag = models.OneToOneField('HeadTag', related_name='view_count')

	def __str__(self):
		return '{} view count {}'.format(self.head_tag.title,self.view_count)





