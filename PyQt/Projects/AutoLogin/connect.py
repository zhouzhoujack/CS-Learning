# -*- coding: UTF-8 -*-
# 联网脚本

import codecs
import http.client as requests
import urllib as urlparse
import argparse
import datetime
import sys

class Options(object):
    """
    一些登录默认参数的设置
    """
    def __init__(self, id, pwd):
        parser = argparse.ArgumentParser(description="Matching network")
        parser.add_argument('--host','-R', type=str, default='172.16.200.13')
        parser.add_argument('--port','-P', type=int, default=80)
        parser.add_argument('--username','-u', type=str,default=id )
        parser.add_argument('--password','-p',type=str ,default=pwd )
        self.parser = parser
    def parse(self):
        return self.parser.parse_args()

class NetManager():
    def __init__(self, options):
        self.options = options
        self.events = {
          "01": u"帐号或密码不对,请重新输入",
          "01-error0": u"认证服务器不允许Web方式登录",
          "01-error1": u"用户帐号不允许Web方式登录",
          "02": u"账号正在使用中,请您与网管联系",
          "03": u"帐号只能在指定地址使用",
          "04": u"帐号费用超支或时长流量超过限制",
          "05": u"帐号暂停使用",
          "06": u"系统繁忙,请稍后重试",
          "11": u"帐号只能在指定地址使用",
          "13": u"未检测到设备登录,设备可能已经处于离线状态",
          "14": u"注销成功",
          "15": u"登录成功",
          "00": u"脚本信息捕获占位符,不影响使用",
          "99": u"未知错误"
        }

    def auth_reachable(self):
        '''
        检测是否能进入登录网址
        '''
        conn = None
        c = False
        try:
            conn = requests.HTTPConnection(self.options.host,self.options.port,timeout=5)
            conn.request('GET','/')
        except Exception as e:
            raise e
        else:
            r = conn.getresponse()
            c = True if r.status < 300 else False
        finally:
            conn and conn.close()
            return c

    def inet_reachable(self):
        '''
        检测是否已经联网
        '''
        conn = None
        c = False
        try:
            conn = requests.HTTPConnection("www.baidu.com", 80, timeout=5)
            conn.request('GET','/')
        except Exception as e:
            raise e
        else:
            r = conn.getresponse()
            if r.status < 300:
                try:
                    body = codecs.decode(r.read(),"utf_8")
                    c = u"百度" in body
                except Exception as e:
                    c = False
            else:
                c = False
        finally:
            conn and conn.close()
            return c

    def login(self):
        conn = None
        event = "00"
        try:
            payload = urlparse.parse.urlencode({
                'DDDDD': self.options.username,
                'upass': self.options.password,
                '0MKKey': 123
            })
            headers = {
                "Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/html"
            }
            conn = requests.HTTPConnection(self.options.host, self.options.port, timeout=5)
            conn.request('POST', '/', payload, headers)
        except Exception as e:
            raise e
        else:
            ## show response info
            r = conn.getresponse()
            body = codecs.decode(r.read(), "gb2312")
            if "You have successfully logged into our system." in body:
                event = "15"
            elif u"在完成工作后，请别忘记注销。" in body:
                event = "15"
            else:
                idx = body.find("Msg=")
                event = body[idx + 4:idx + 6]
                if "01" == event:
                    idx = body.find("msga=")
                    if "'" == body[idx + 6:idx + 7]:
                        pass
                    else:
                        msga = body[idx + 6:idx + 12]
                        key = event + "-" + msga
                        if not key in self.events.keys():
                            event = "99"
                        else:
                            event = key
                else:
                    pass
        finally:
            conn and conn.close()
            return event

    def logout(self):
        """
        注销登录
        """
        try:
            conn = requests.HTTPConnection('172.16.200.13', self.options.port, timeout=5)
            conn.request('GET','/F.htm')
        except Exception as e:
            raise e

def current_time():
    """
    返回当前时间
    """
    return datetime.datetime.now().strftime('%F %T')

def disconnect_from_network(window, id, pwd):
    option = Options(id, pwd).parse()
    net = NetManager(option)
    net.logout()
    window.status_textEdit.append(current_time() + '  ' +"已注销登录")
    return True

def connect_to_network(window,id, pwd):
    option = Options(id, pwd).parse()
    net = NetManager(option)
    if net.auth_reachable():
        if net.inet_reachable():
            window.status_textEdit.append(current_time() + '  ' + "客户端已接入互联网")
        else:
            window.status_textEdit.append(current_time()+ '  ' + "设备尚未接入互联网,开始登录...")
            assert option.username and option.password
            event = net.login()
            if event == "15":
                if net.inet_reachable():
                    # window.status_textEdit.append("登录成功")
                    return True
            else:
                window.status_textEdit.append(net.events[event])
                return False
    else:
        window.status_textEdit.append(current_time() + '  '+ "登陆入口 "+ option.host + " 不可访问")
        return False

def net_reachable():
    '''
    检测是否已经联网
    '''
    conn = None
    c = False
    try:
        conn = requests.HTTPConnection("www.baidu.com", 80, timeout=5)
        conn.request('GET','/')
    except Exception as e:
        raise e
    else:
        r = conn.getresponse()
        if r.status < 300:
            try:
                body = codecs.decode(r.read(),"utf_8")
                c = u"百度" in body
            except Exception as e:
                c = False
        else:
            c = False
    finally:
        conn and conn.close()
        return c
