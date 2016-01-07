from html.parser import HTMLParser

class IpParser(HTMLParser):

    def __init__(self):
        #定义要搜寻的标签
        self.handledtags = ['td']  #提出标签，理论上可以提取所有标签的内容
        self.processing = None
        self.found_td = 0
        self.outt = ""
        HTMLParser.__init__(self)  #继承父类的构造函数

    def handle_starttag(self,tag,attrs):
        #判断是否在要搜寻的标签内
        if tag in self.handledtags:
            self.found_td = self.found_td + 1
            if self.found_td==3:
                self.data = ''
                self.processing = tag

    def handle_data(self,data):
        if self.processing:
            self.data += data

    def handle_endtag(self,tag):

        if tag == self.processing:
            if self.found_td==3:   
                outt=str(self.data)
                self.outt = outt
                #print(self.outt)
                self.processing = None
                #return self.outt

    #下面两个函数都是对html实体做的转码，没有深究
    # def handle_entityref(self,name): 
    #     if entitydefs.has_key(name): 
    #         self.handle_data(entitydefs[name]) 
    #     else: 
    #         self.handle_data('&'+name+';') 
            
    # def handle_charref(self,name): 
    #     try: 
    #         charnum=int(name) 
    #     except ValueError: 
    #         return 
    #     if charnum<1 or charnum>255: 
    #         return 
    #     self.handle_data(chr(charnum)) 
    


