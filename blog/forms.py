from django import forms 
from django.db import models

class CommForm(forms.Form):
	comments = forms.CharField(widget=forms.Textarea,label='')
	#pid = forms.IntegerField(widget=forms.HiddenInput())
	#mid = forms.IntegerField(widget=forms.HiddenInput())
	#user_ip = models.CharField(null=True,max_length = 150)
	#user_location = models.CharField(null=True,max_length = 254)
	#timestamp = models.DateTimeField()
	def clean_comments(self):
		comment = self.cleaned_data['comments']
		#num_words = len(comments.split())
		if not comment:
			raise forms.ValidationError("Not enough words!")
		return comment