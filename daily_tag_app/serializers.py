from .models import HeadTag, City, Country
from rest_framework import serializers

class HeadTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadTag
       	fields = '__all__'
       	read_only_fields = ('slug','created_data','ip','active','belong_to_city','detail_url')
    