import time,re,requests
from flask import Flask,request,render_template


class GetSublink():
    def __init__(self):
        self.session = requests.session()
        self.user_data = {
            'email': '',
            'passwd': '',
            'code': '', 
        }
        self.main_domain = ''
        self.main_header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'origin': self.main_domain,
        }
        self.domain_list = ['https://suying999.net',
                'https://suying810.net',
                'https://suying400.com',
               'https://suying400.net',
                'https://suying400.xyz',
                'https://suying500.com',
                'https://suying500.net',
                'https://suying500.xyz',
                'https://suying200.org',
                'https://suying600.com',
                'https://suying600.net',]


    def reload_main_domain(self,new_domain):
         self.main_domain = new_domain

    def login(self):
        try:
            login_url = self.main_domain+'/auth/login'
            state = self.session.post(login_url,headers=self.main_header,data=self.user_data,timeout=2)
            if state.json()['ret'] == 1:
                return True
            else:
                return False
        except:
            return False

    def Get_Sublink(self):
        #获取订阅链接
        get_use_url = self.main_domain+'/user'
        state = self.session.get(get_use_url,headers=self.main_header)
        try:
            subfun = re.search('(function importSublink.*?)appName',state.text,re.DOTALL).group(1)
            subfun = re.search(r'(http.*?)\?',subfun)
            print(subfun.group(1))
            return subfun.group(1)
        except:
            return False
    
    def main(self):
        for i in self.domain_list:  #遍历新的域名表
            self.reload_main_domain(i)
            if self.login():
                return self.Get_Sublink()
        return False  


app = Flask(__name__)

@app.route('/') 
def index():
    sublink = GetSublink().main()
    nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if sublink != False:
        return render_template('index.html',nowtime=nowtime,btnhidden='',msgboards=sublink[-16:],sublink=sublink)
    else:
        return render_template('index.html',nowtime=nowtime,btnhidden='hidden',msgboards='OOPS!\n请稍后再来\n亦或者联系管理员',sublink=sublink)
app.run(host='0.0.0.0',port=4299)
