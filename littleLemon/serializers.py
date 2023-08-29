from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
import bleach


class UserSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        attrs['username'] = bleach.clean(attrs['username'])
        attrs['email'] = bleach.clean(attrs['email'])
        attrs['password'] = bleach.clean(attrs['password'])
        return super().validate(attrs)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ['id', 'title', 'slug']

    def validate(self, attrs):
        cleaned_title = bleach.clean(attrs.get('title'))
        cleaned_slug = bleach.clean(attrs.get('slug'))

        existing_title = models.Category.objects.filter(title=cleaned_title).exclude(
            pk=self.instance.pk if self.instance else None).first()

        if existing_title:
            raise serializers.ValidationError("This title is already in use.")

        existing_slug = models.Category.objects.filter(slug=cleaned_slug).exclude(
            pk=self.instance.pk if self.instance else None).first()

        if existing_slug:
            raise serializers.ValidationError("This slug is already in use.")

        attrs['title'] = cleaned_title
        attrs['slug'] = cleaned_slug
        return attrs


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']

    def validate(self, attrs):
        if 'title' in attrs:
            attrs['title'] = bleach.clean(attrs['title'])
        return super().validate(attrs)
