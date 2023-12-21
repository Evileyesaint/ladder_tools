import requests,time,schedule
from bs4 import BeautifulSoup


domain_list = ['https://suying100.xyz',
                'https://suying300.com',
                'https://suying400.com',
               'https://suying400.net',
                'https://suying400.xyz',
                'https://suying500.com',
                'https://suying500.net',
                'https://suying500.xyz',
                'https://suying200.org',
                'https://suying600.com',
                'https://suying600.net',]

class robot():
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

    def get_user(self):
        get_use_url = self.main_domain+'/user'
        state = self.session.get(get_use_url,headers=self.main_header)
        soup = BeautifulSoup(state.text,'lxml')
        state_index = soup.find_all('div','card-wrap')
        duration = state_index[0].get_text().replace('\n','').replace(' ','')  ##会员时长 duration
        traffic = state_index[1].get_text().replace('\n','').replace('                      ','\n').replace(' ','').replace(':','')  ##流量 traffic
        # online_device = state_index[2].get_text().replace('\n','')[:11].replace(' ','')  ##在线设备 online_device
        # last_use = state_index[2].get_text().replace('\n','')[12:]  ##最后使用在线时间 last_use
        return traffic,duration
    
    def checkin(self):
        checkin_url = self.main_domain+'/user/checkin'
        state = self.session.post(url=checkin_url,headers=self.main_header).json()
        return state['ret'],state['msg'] ##第一个是状态 1是签到成功 0是已经签到 

    def format_fix(self,index):  #格式修复 去除回车以后的内容
        new_str = ''
        for i in index:
            if i == '\n':
                return new_str
            new_str+=i
        return new_str


    def dispose(self):   #处理 包含返回签到和个人信息
        now_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+': '
        user_info = self.get_user()
        check_info = self.checkin()
        if check_info[0] == 0:
            print(now_time+'当天已经签到完成 ')
        else:
            print(now_time+'签到完成  '+ str(check_info[1])+', '+ self.format_fix(user_info[0])+', '+user_info[1])

    def main(self):
        try:
            for i in domain_list:  #遍历新的域名表
                self.reload_main_domain(i)
                if self.login():
                    self.dispose()
                    return
        except:
            print('Error!')
    
def main():
    main = robot()
    main.main()

main()
schedule.every().day.at("12:05").do(main) #创建任务

while True:
    schedule.run_pending()
    time.sleep(10)




