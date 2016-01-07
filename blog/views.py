from django.shortcuts import render , render_to_response
from blog.models import Mail,Comments
from blog.models import AttachFile
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django import forms
from .forms import CommForm
import time
from django.db.models import Q
import urllib.request
from getlocation import IpParser
from .JuncheePaginator import *

def index(request):
    limit = 4  # 每页显示的记录数	
    posts = Mail.objects.all()
    paginator = JuncheePaginator(posts, limit)  # 实例化一个分页对象
    page = request.GET.get('page')  # 获取页码
    try:
        posts = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        posts = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        posts = paginator.page(paginator.num_pages)  # 取最后一页的记录
    #print (posts.paginator.page_range_ext) 
    #print (posts.paginator.page_range) 
	#attach = AttachFile.objects.all()
    return render_to_response('blog/index.html',{'posts':posts})

def showemail(request,get_id):
	context_dict = {}
	pic_type = []
	limit = 1
	try:
		post = Mail.objects.get(id = get_id)
		post.views = post.views+1
		post.save()
		attachs = AttachFile.objects.filter(mail_id = get_id)
		comments = Comments.objects.filter(comments_id = get_id).filter(pid = -1)
		#replys = Comments.objects.filter(comments_id = get_id).exclude(pid = -1)
		paginator = JuncheePaginator(comments, limit)
		page = request.GET.get('page')
		try:
			comments = paginator.page(page)  # 获取某页对应的记录
		except PageNotAnInteger:  # 如果页码不是个整数
			comments = paginator.page(1)  # 取第一页的记录
		except EmptyPage:  # 如果页码太大，没有相应的记录
			comments= paginator.page(paginator.num_pages)  # 取最后一页的记录
		context_dict['post'] = post
		context_dict['attachs'] = attachs
		context_dict['comments'] = comments
		#context_dict['replys'] = replys
		#form = CommForm()
		#context_dict['form'] = form
		for attach_type in attachs:
			if attach_type.filename.split('.')[1] in 'JPGjpgBMPbmpJPEGjpegPNGpng' :
			 	pic_type.append(attach_type) 
		context_dict['pic_type'] = pic_type
	except Mail.DoesNoExist:
		pass
	return render_to_response('blog/showemail.html',context_dict)

def search(request):
    if 'search_mail' in request.GET:#GET是一个dict，使用文本框的name作为key
    #在这里需要做一个判断，是否存在提交数据，以免报错
        query = request.GET['search_mail']
        #使用lookup后缀，意思为书名不区分大小写，包含q就可以
        if query:
        	# if request.GET['search_sel'] == "subject":
        	# 	res_mail = Mail.objects.filter(subject__icontains=query)
        	# 	query_sel = "subject" 
        	# else :        
        	# 	res_mail = Mail.objects.filter(content__icontains=query)
        	# 	query_sel = "content" 
        	res_mail = Mail.objects.filter(Q(subject__icontains=query)|Q(content__icontains=query)) 
        	return render_to_response('blog/search_result.html', {'res_mail':res_mail, 'query':query})
        else: 
            return HttpResponseRedirect('/')
    else:
        message = 'You submitted an empty form.'
        #只是简单的返回一个response对象，因为没有使用模块，所以也不用渲染数据Context
        return HttpResponse(message)

def comment(request):
	if request.method == 'POST':
		#new_comm = CommForm(request.POST)
		comments = request.POST['newcomments']
		if not comments.strip() == "":
			pid = request.POST['pid']
			#pid = -1
			timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
			mid = request.POST['mid']
			# if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
			# 	ip =  request.META['HTTP_X_FORWARDED_FOR']
			# else:  
			# 	ip = request.META['REMOTE_ADDR']
			ip = getIPFromDJangoRequest(request)
			iplocation = getIPLocationFromsite(ip)
			t = Mail.objects.get(id = mid) 
			t.comment_num = t.comment_num + 1
			t.save()
			floor = t.comment_num
			p = Comments(pid=pid,timestamp=timestamp,user_ip=ip,user_content=comments,comments_id=mid,user_location=iplocation,floor=floor)
			p.save()
			return render_to_response('blog/savedone.html',{'mid':mid})
		else:
			mid = request.POST['mid']
			return render_to_response('blog/savefalse.html',{'mid':mid})
	else:
  		pass
  		#return render_to_response('blog/comments.html')

# def comment(request):
# 	if request.is_ajax():
# 		new_comm = request.POST['content']
# 		print (new_comm)
# 		if new_comm:
# 			comments = new_comm
# 			pid = request.POST['pid']
# 			#pid = -1
# 			timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# 			mid = request.POST['mid']
# 			# if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
# 			# 	ip =  request.META['HTTP_X_FORWARDED_FOR']
# 			# else:  
# 			# 	ip = request.META['REMOTE_ADDR']
# 			ip = getIPFromDJangoRequest(request)
# 			p = Comments(pid=pid,timestamp=timestamp,user_ip=ip,user_content=comments,comments_id=mid)
# 			p.save()
# 			t = Mail.objects.get(id = mid) 
# 			t.comment_num = t.comment_num + 1
# 			t.save()
# 			return HttpResponse(json.dumps({"content":new_comm}))
# 		else:
#   			pass 
# 	else:
#   		pass

def about(request):
	return render_to_response('blog/about.html')

def getIPFromDJangoRequest(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']
def getIPLocationFromsite(ip):
	if ip:
		queryip="http://ip.lockview.cn/ShowIP.aspx?ip="+ip
		page = urllib.request.urlopen(queryip).read().decode("utf8")
		parser = IpParser()
		parser.feed(page)
		parser.close()
		iplocation = parser.outt 
		#print (iplocation)
		return iplocation

# Create your views here.
