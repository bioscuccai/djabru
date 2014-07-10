# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

COLOR_CHOICES=(("blue","blue"), ("yellow","yellow"), ("red","red"), ("green","green"), ("cyan","cyan"),("purple","purple"),("gray","gray"))

class PicTag(models.Model):
	text=models.CharField(max_length=256, unique=True)
	description=models.CharField(max_length=2048, blank=True)
	url=models.CharField(max_length=512, blank=True)
	color=models.CharField(max_length=24, blank=False, default="blue", choices=COLOR_CHOICES)
	def __unicode__(self):
		return self.text

class Picture(models.Model):
	tags=models.ManyToManyField(PicTag)
	added=models.DateTimeField(auto_now=True)
	filename=models.CharField(max_length=256)
	origin=models.URLField(max_length=256, blank=True)
	filetype=models.CharField(max_length=10)
	user=models.ForeignKey(User)

	def __unicode__(self):
		return str(self.pk)+" / "+self.filename
	class Meta:
		ordering=["-added"]

class Comment(models.Model):
	picture=models.ForeignKey(Picture)
	user=models.ForeignKey(User)
	text=models.TextField(max_length=2048)
	added=models.DateTimeField(auto_now=True)
	class Meta:
		ordering=["added"]
