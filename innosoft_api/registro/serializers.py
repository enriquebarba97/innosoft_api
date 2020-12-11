from rest_framework import serializers 
from registro.models import User 
from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model= Group
		fields = ('id','name',)
class ListUserSerializer(serializers.ModelSerializer):
	class Meta: 
		model = User 
		fields = ('id','uvus','email','first_name','last_name','groups')
	def to_representation(self, instance):
		self.fields['groups'] =  GroupSerializer(many=True)
		return super(ListUserSerializer, self).to_representation(instance)

class UserCreateSerializer(serializers.ModelSerializer):
	class Meta: 
		model = User 
		fields = ('id','uvus','email','first_name','last_name','password','groups')
		
		
	def create(self,data):
		user= User.objects.create(uvus=data['uvus'],email=data['email'],
		first_name=data['first_name'],last_name=data['last_name'])
		user.set_password(data['password'])
		user.is_staff = True
		user.save()
		for group in data['groups']:
			user.groups.add(group)
		return user
class UpdateUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id','uvus','email','first_name','last_name','groups')
