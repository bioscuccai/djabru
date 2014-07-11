# -*- coding: utf-8 -*-

import os.path
from PIL import Image
import imghdr

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from bru.models import PicTag, Picture, Comment
from bru.forms import UploadImageForm, AddTagForm, SidebarSearch, EditTagForm, CommentForm

PICS_PER_ROW=5
PICS_PER_PAGE=10
THUMB_W=200
THUMB_H=200

IMAGE_PATH=os.path.join(os.path.dirname(__file__), "static")
#IMAGE_PATH="/home/bioscuccai/brusite/static/"

def makethumb(fn):
	#i=Image.open(IMAGE_PATH+'upl/'+fn)
	i=Image.open(os.path.join(IMAGE_PATH,'upl',fn))
	(w,h)=i.size
	ratio=0.5
	if w>=h:
		ratio=float(THUMB_W)/float(w)
	else:
		ratio=float(THUMB_H)/float(h)
	i.thumbnail((int(w*ratio), int(h*ratio)), Image.ANTIALIAS)
	i.save(os.path.join(IMAGE_PATH,"thumb",fn))

# Create your views here.
def taglesspage(request, page):
	return redirect("bru_bytag", page=page, tags=" ")

def newestlist(request):
	return redirect("bru_bytag", page=1, tags=" ")

@login_required
def uploadform(request):
	form=UploadImageForm()
	return render(request, 'bru/upload.html', {'form':form})

@csrf_exempt
@login_required
def uploadimage(request):
	if request.method=='POST':
		form=UploadImageForm(request.POST, request.FILES)
		if form.is_valid():
			ext=os.path.splitext(request.FILES['imagefile'].name)[1]
			if ext != ".jpg" and ext != ".png":
				raise Http404
			pic=Picture(filename=request.FILES['imagefile'].name, origin=form.cleaned_data['origin'], filetype=ext, user=request.user)
			pic.save()
			filename=os.path.join(IMAGE_PATH,'upl',str(pic.pk)+ext)
			with open(filename, 'wb') as dest:
				for chunk in request.FILES['imagefile'].chunks():
					dest.write(chunk)
			if imghdr.what(filename)!= 'jpeg' and imghdr.what(filename)!='png':
				pic.delete()
				raise Http404
			makethumb(str(pic.pk)+ext)
			return redirect("bru_uploadform")
	raise Http404

def viewimage(request, image):
	tagform=AddTagForm()
	pic=Picture.objects.get(pk=image)
	taglist=pic.tags.all()
	form=CommentForm()
	comments=Comment.objects.filter(picture=pic)
	return render(request, 'bru/viewimage.html', {'pic':pic, 'tagform':tagform, 'tags':taglist, 'form':form, 'comments':comments})

@csrf_exempt
@login_required
def addtag(request, image):
	if request.method=='POST':
		form=AddTagForm(request.POST)
		if form.is_valid():
			pic=Picture.objects.get(pk=image)
			taglist=pic.tags.all()
			try:
				tag=PicTag.objects.get(text=form.cleaned_data['text'])
			except PicTag.DoesNotExist:
				tag=PicTag.objects.create(text=form.cleaned_data['text'])
			pic.tags.add(tag)
			return redirect("bru_viewimage",image=image)
	raise Http404

@csrf_exempt
@login_required
def removetag(request, image, tag):
	tagobj=PicTag.objects.get(text=tag)
	pic=Picture.objects.get(pk=image)
	pic.tags.remove(tagobj)
	return redirect("bru_viewimage", image)

@csrf_exempt
def sidebarsearch(request):
	if request.method=='POST':
		form=SidebarSearch(request.POST)
		if form.is_valid():
			return redirect("bru_bytag", tags=form.cleaned_data['text'], page=1)
	raise Http404

def bytag(request):
	return redirect("bru_bytag", tag=" ", page=1)

def getpagesandtags(tags):
	tagobs=[]
	notin=[]
	pictures=Picture.objects.all()
	if tags!="" and tags!=" ":
		tagarr=tags.split()
		for tagname in tagarr:
			toexclude=False
			if tagname.startswith("-"):
				if len(tagname)==1:
					continue
				tagname=tagname[1:len(tagname)]
				toexclude=True
			try:
				tag=PicTag.objects.get(text=tagname)
			except PicTag.DoesNotExist:
				continue
			if toexclude:
				notin.append(tag)
			else:
				tagobs.append(tag)
		if tagobs:
			pictures=pictures.filter(tags__in=tagobs)
	pictures=pictures.exclude(tags__in=notin)
	uniquepics=[]
	for p in pictures:
		if p not in uniquepics:
			uniquepics.append(p)
	pages=Paginator(uniquepics, PICS_PER_PAGE)
	return pages, tagobs

def bytag(request, tags, page):
	if tags==" ": tags=""
	pages, tagobs=getpagesandtags(tags)

	reltags=set()
	for p in pages.page(page).object_list:
		#related tagek
		for t in p.tags.all():
			if t != "":
				reltags.add(t)
	for t in reltags:
		t.links=Picture.objects.filter(tags__in=[t]).count()
	reltags_list=list(reltags)
	reltags_list.sort(key=lambda x:x.links, reverse=True)

	tagforms=[]
	for ctag in tagobs:
		if ctag is None: continue
		form=EditTagForm(instance=ctag)
		tagforms.append(form)

	return render(request, 'bru/viewpage.html',{'pictures':pages.page(page).object_list, 'pagerange':range(1,pages.num_pages+1),
	'currpage':page, 'currtags':tagobs,
	'tagstring':tags, 'tagforms':tagforms, 'reltags': reltags_list, 'th':THUMB_H, 'tw':THUMB_W, 'tw2':THUMB_W/2})

@csrf_exempt
@login_required
def edittag(request, tagname):
	tag=PicTag.objects.get(text=tagname)
	if request.method=="POST":
		form=EditTagForm(request.POST)
		if form.is_valid():
			tag.description=form.cleaned_data['description']
			tag.color=form.cleaned_data['color']
			tag.url=form.cleaned_data['url']
			tag.save()
			return redirect("bru_bytag", tags=tagname, page=1)
	form=EditTagForm(instance=tag)
	return render(request, 'bru/edittag.html', {'tag':tag, 'form':form})

@csrf_exempt
@login_required
def addcomment(request, pic):
	if request.method=="POST":
		form=CommentForm(request.POST)
		if form.is_valid():
			picobj=Picture.objects.get(pk=pic)
			comment=Comment(text=form.cleaned_data['text'], user=request.user, picture=picobj)
			comment.save()
	return redirect("bru_viewimage", image=pic)

#kephez tartozo tag-ek
def ajax_tags(request, pic):
	try:
		pic=Picture.objects.get(pk=pic)
	except Picture.DoesNotExist:
		raise Http404
	data=serializers.serialize("json", pic.tags.all())
	return HttpResponse(data, content_type="application/json")

def ajax_comments(request, pic):
	pic=Picture.objects.get(pk=pic)
	comments=Comment.objects.filter(picture=pic)
	users=set()
	for c in comments.all():
		users.add(c.user)
	comments_json=serializers.serialize("json", comments.all())
	users_json=serializers.serialize("json", users, fields=("username"))
	return HttpResponse("{\"comments\": "+comments_json+", \"users\": "+users_json+"}",  content_type="application/json")

def ajax_bytag(request, tags, page):
	pages, tags=getpagesandtags(tags)
	data=serializers.serialize("json", pages.page(page).object_list)
	return HttpResponse(data, content_type="application/json")

#a tag adatait keri le
def ajax_tag(request, tagname):
	try:
		tag=PicTag.objects.get(text=tagname)
	except PicTag.DoesNotExist:
		raise Http404
	data=serializers.serialize("json", [tag])
	return HttpResponse(data, content_type="application/json")

def ajax_bytag_tagless(request, page):
	return redirect("bru_ajax_bytag", tags=" ", page=page)
