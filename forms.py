from django import forms
from django.forms import ModelForm, Textarea
from bru.models import PicTag, Comment
from django.core.validators import RegexValidator

class UploadImageForm(forms.Form):
	origin=forms.CharField(required=False)
	imagefile=forms.FileField()

class AddTagForm(forms.Form):
	text=forms.CharField(validators=[RegexValidator(r'^[a-zA-Z0-9]*$')])

class SidebarSearch(forms.Form):
	text=forms.CharField(validators=[RegexValidator(r'^[\-a-zA-Z0-9\ ]*$')])

class EditTagForm(forms.ModelForm):
	class Meta:
		model=PicTag
		fields=['description', 'url', 'color']

class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields=['text']
		widgets={
		    'text': Textarea(attrs={'rows':10, 'cols':80}),
		}
