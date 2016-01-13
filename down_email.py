#encoding=utf-8
import poplib
import email
import sqlite3
import time
import os
import random
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

newMail = 0
#spam = 0
outRang = True
searchMail = 10

logSpamMail = 0
logReceiveMail = 0
logMailSubject = []

white_list=[]


if __name__ == '__main__':
        M = poplib.POP3('pop.163.com')
        M.user('sample@163.com')  
        M.pass_('1234567')
        # M = poplib.POP3('pop.yeah.net')
        # M.user('sample@yeah.net')
        # M.pass_('1234')
        #打印有多少封信  
        numMessages = len(M.list()[1])  
        #print 'num of messages', numMessages  
        #ret=M.list()
        #print ret
        for j in range(numMessages-searchMail,numMessages):
                m_num = M.retr(j+1)
                msg_num = email.message_from_string('\n'.join(m_num[1]))
                #allHeaders = email.Header.decode_header(msg)
                if not os.path.exists('already.inbox'):
                    os.system("touch already.inbox")
                if file("already.inbox",'rb').read()==msg_num['Message-Id']:
                    newMail=j+1
                    if newMail==numMessages:
                        outRang = False
                        print('No new Mail')
                    else:
                        outRang = False
                        print("Will receive %d Mail"% (numMessages-newMail))
                    break;
        if outRang:
            newMail = numMessages-searchMail
            print "Too Many New Mails, only receive "+str(searchMail)
            #只打印inbox中没有的的邮件
            for i in range(newMail,numMessages):
                    m = M.retr(i+1)
                    msg = email.message_from_string('\n'.join(m[1]))
                    #allHeaders = email.Header.decode_header(msg)
                    msg_re=re.sub(r'^.*<|>$',"",msg['from'])
                    if not (msg_re in white_list):
                        logSpamMail = logSpamMail + 1
                        continue
                    conn = sqlite3.connect('emailsql')
                    c = conn.cursor()
                    contentList = []
                    for part in msg.walk(): #遍历所有payload
                            contenttype = part.get_content_type()
                            if contenttype == 'text/plain':
                                    #保存正文
                                    data = part.get_payload(decode=True)
                                    charset = part.get_content_charset('iso-8859-1')
                                    #print('Content : '+ data.decode(charset).encode('utf-8'))
                                    #p.content = data.decode(charset).encode('utf-8')
                                    contentList.append(data.decode(charset))
                                    #c.execute('update blog_mail set content=%s where subject=%s' %Content)
                                   
                                    #file('mail%d.txt' % (i+1), 'w').write(data.decode(charset).encode('utf-8'))
                    #print ('1234'+Content+'5678')
                    Content = contentList[0]
                    if Content:
                        if Content == '\n':
                            Content = ""
                    if msg['Message-Id']:
                        file("already.inbox",'wb').write(msg['Message-Id'])
                    else:
                        file("already.inbox",'wb').write(str(random.uniform(1, 10)))
                    #print msg['Message-Id']
                    
                    aimHeaderStrs = {'from':'', 'subject':'','Message-Id':'','Date':''}
                    for aimKey in aimHeaderStrs.keys():
                            aimHeaderList = email.Header.decode_header(msg[aimKey])
                            for tmpTuple in aimHeaderList:
                                    if tmpTuple[1] == None:
                                            aimHeaderStrs[aimKey] += tmpTuple[0]
                                    else:
                                            aimHeaderStrs[aimKey] += tmpTuple[0].decode(tmpTuple[1]) #转成unicode
                    #for aimKey in aimHeaderStrs.keys():
                            #print aimKey,':',aimHeaderStrs[aimKey].encode('utf-8') #转成utf-8显示
                    '''p = Mail(updatetime =  time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()))
                    p.fromperson = aimHeaderStrs['from']
                    p.subject = aimHeaderStrs['subject']
                    p.mailid = aimHeaderStrs['Message-Id']
                    p.timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", aimHeaderStrs['Date'])'''
                    temp_time = aimHeaderStrs['Date'].split(' +')
                    #print temp_time
                    #temp_time = temp_time[:24]
                    #print temp_time
                    struct_time = time.strptime(temp_time[0],"%a, %d %b %Y %H:%M:%S")
                    final_time = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)
                    Content = Content.lstrip('\n').lstrip()
                    views = 0
                    comments = 0
                    attachnum = 0
                    fromperson_tr = aimHeaderStrs['from']
                    subject = aimHeaderStrs['subject'].replace("Fw:","").replace("转发:","").lstrip()
                    print "================================================="
                    print "\n================================================="
                    print "mail: "+subject
                    logMailSubject.append(subject)
                    fromperson_re = re.sub(r'<.*$',"",fromperson_tr)
                    if fromperson_re == "":
                        fromperson_re = re.sub(r'^.*<|>$',"",fromperson_tr)
                    else:
                        fromperson_re = fromperson_re.replace(" ","")
                    #print fromperson_re
                    #print Content
                    logReceiveMail = logReceiveMail + 1
                    args =(subject,aimHeaderStrs['Message-Id'],final_time,aimHeaderStrs['from'],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),Content,views,attachnum,comments,fromperson_re)
                    sql ="insert into blog_mail(subject,mailid,timestamp,fromperson,updatetime,content,views,attach_num,comment_num,fromperson_re) values(?,?,?,?,?,?,?,?,?,?)"
                    #print final_time
                    #print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    c.execute(sql,args)
                    conn.commit()
                    #c.execute("insert into blog_mail(subject,mailid,timestamp,fromperson,updatetime) values(aimHeaderStrs['subject'],aimHeaderStrs['Message-Id'],time.strftime("%Y-%m-%d %H:%M:%S", aimHeaderStrs['Date']),aimHeaderStrs['from'],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())")
                    #c.execute(insert into ceshi (user,note)  values('mPfiJRIH9T','mPfiJRIH9T')
                    attachmailid = 0
                    for part in msg.walk():
                            filename = part.get_filename()
                            if filename: #and contenttype=='application/octet-stream':
                                    #保存附件
                                    data = part.get_payload(decode=True)
                                    charset = part.get_content_charset('ios-8859-1')
                                    if filename:
                                         h = email.Header.Header(filename)
                                         dh = email.Header.decode_header(h)
                                         fname = dh[0][0]
                                         encodeStr = dh[0][1]
                                         if encodeStr != None:
                                             if charset == None:
                                                 fname = fname.decode(encodeStr, 'gbk')
                                             else:
                                                 fname = fname.decode(encodeStr, charset)
                                         data = part.get_payload(decode=True)
                                         filesize = len(data)
                                         #print filesize
                                    subject = re.sub(r'((?=[\x21-\x7e]+)[^A-Za-z0-9])|\s',"_",subject)
                                    att_dir ='./attachment'
                                    att_dir = os.path.join(att_dir,time.strftime("%Y_%m_%d")+"_"+subject)
                                    if not os.path.isdir(att_dir):
                                        os.mkdir(att_dir)
                                    file("%s/%s" % (att_dir,fname),'wb').write(data)
                                    print('attachment : ' + fname)
                                    attachnum = attachnum + 1
                                    filepath = "../../attachment/"+time.strftime("%Y_%m_%d")+"_"+subject+"/"+fname
                                    filename = fname
                                    queryid =  (aimHeaderStrs['Message-Id'],)
                                    c.execute("select id from blog_mail where mailid=?",queryid)
                                    cur_mailid = c.fetchone()
                                    attachmailid = cur_mailid[0]
                                    #print cur_mailid
                                    c.execute("insert into blog_attachfile(mail_id,filename,attachfile,filesize) values(?,?,?,?)",(cur_mailid[0],filename,filepath,filesize))
                                    conn.commit()
                    c.execute("update blog_mail set attach_num=? where id=?",(attachnum,attachmailid))
                    conn.commit()
            print "Done!"
            print "received "+str(logReceiveMail)+" mails!"
            if logReceiveMail > 0:
                logTotal = logReceiveMail+logSpamMail
                logData='''============================================
receive time: '''+time.strftime("%Y_%m_%d %H:%M:%S")+'''
receive mail number: '''+str(logReceiveMail)+'''
mail subject list: 
'''+'\n'.join(logMailSubject)+'''
spam mail number: '''+str(logSpamMail)+'''
total: '''+str(logTotal)+'''
============================================'''
                #logData = logData.encode('utf-8')
                file("./log/%s" % ("log-"+time.strftime("%Y_%m_%d-%H_%M_%S")+"-"+str(logReceiveMail)),'wb').write(logData)
                print "log save done!" 
        # else:
        #     print "Too Many New Emails!!"
                               
