# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from bru import views

urlpatterns=patterns('',
	url(r'^$', views.newestlist),
	url(r'^newest/$', views.newestlist),
	url(r'^bytag/(?P<page>\d+)/$', views.taglesspage),
	url(r'^uploadform/$', views.uploadform, name="bru_uploadform"),
	url(r'^uploadimage/$', views.uploadimage, name="bru_uploadimage"),
	url(r'^viewimage/(?P<image>\w+)/$', views.viewimage, name="bru_viewimage"),
	url(r'^addtag/(?P<image>\d+)/$', views.addtag, name="bru_addtag"),
	url(r'^removetag/(?P<image>\d+)/(?P<tag>\w+)/$', views.removetag, name="bru_removetag"),
	url(r'^sidebarsearch/$', views.sidebarsearch, name='bru_sidebarsearch'),
	url(r'^bytag/(?P<tags>[\-a-zA-Z0-9\ ]*)/(?P<page>\d+)/$', views.bytag, name="bru_bytag"),
	url(r'^edittag/(?P<tagname>\w+)/$', views.edittag, name="bru_edittag"),
#	url(r'^loginpage/$', views.loginpage, name="loginpage"),
#	url(r'^logoutpage/$', views.logoutpage, name="logoutpage"),
#	url(r'^registerpage/$', views.registerpage, name="registerpage"),
	url(r'^addcomment/(?P<pic>\d+)/$', views.addcomment, name="bru_addcomment"),
#	url(r'^bytag/(?P<page>\d+)/(?P<tags>[a-zA-Z0-9\ ]*)/$', views.bytag, name="bru_bytag_pagefirst"),


	url(r'ajax_tags/(?P<pic>\d+)/$', views.ajax_tags, name="bru_ajax_tags"),
	url(r'ajax_comments/(?P<pic>\d+)/$', views.ajax_comments, name="bru_ajax_comments"),
	url(r'ajax_bytag/(?P<tags>[a-zA-Z0-9\ ]*)/(?P<page>\d+)/$', views.ajax_bytag, name="bru_ajax_bytag"),
	url(r'ajax_bytag/(?P<page>\d+)/$', views.ajax_bytag_tagless),
	url(r'ajax_tag/(?P<tagname>\w+)/$', views.ajax_tag, name="bru_ajax_tag"),
)
