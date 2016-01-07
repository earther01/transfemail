from django.db import models
from django.contrib import admin

# Create your models here.
class Mail(models.Model):
	id = models.AutoField(primary_key=True)
	subject = models.CharField(max_length = 254)
	fromperson = models.CharField(max_length = 150)
	content = models.TextField(null=True)
	mailid = models.CharField(null=True,max_length=100)
	timestamp = models.DateTimeField()
	updatetime = models.DateTimeField()
	views = models.IntegerField(default=0)
	attach_num = models.IntegerField(default=0)
	comment_num = models.IntegerField(default=0)
	fromperson_re = models.CharField(max_length = 150)

	def __str__(self):
    		return self.subject 

	class Meta:
		ordering = ('-timestamp',)

class AttachFile(models.Model):
	attachfile = models.CharField(null=True,max_length = 254)
	filename = models.CharField(max_length = 254)
	filesize = models.IntegerField(default=0)
	mail = models.ForeignKey(Mail)

class Comments(models.Model):
	#id = models.AutoField(primary_key=True)
	comments = models.ForeignKey(Mail)
	pid = models.IntegerField(default=-1)
	user_ip = models.CharField(null=True,max_length = 150)
	user_location = models.CharField(null=True,max_length = 254)
	user_content = models.TextField()
	timestamp = models.DateTimeField()
	floor = models.IntegerField(default=0)

	class Meta:
		ordering = ('timestamp',)

class MailAdmin(admin.ModelAdmin):
	list_display = ('id','subject','timestamp','mailid','updatetime','content','views','comment_num')

class AttachAdmin(admin.ModelAdmin):
	list_display = ('id','mail_id','filename','filesize','attachfile')

class CommentsAdmin(admin.ModelAdmin):
	list_display = ('id','pid','user_ip','user_location','user_content','timestamp')

	


admin.site.register(Mail,MailAdmin)
admin.site.register(AttachFile,AttachAdmin)
admin.site.register(Comments,CommentsAdmin)