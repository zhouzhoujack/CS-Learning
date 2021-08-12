# -*- coding:utf-8 -*-
# 天气脚本
import json
import urllib as urlparse
import http.client
import requests
from lxml import etree

target_url = 'https://www.ip.cn/'
municipality = ['北京市','上海市','重庆市','天津市']

class weather(object):

    def download_page(self, url):
        """
        获取网页源代码
        """
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}
            html = requests.get(url,headers=headers).content
            return html
        except Exception as e:
            raise e

    def get_city_name(self,html):
        """
        对网页内容进行解析并分析得到需要的数据
        """
        try:
            index = 0
            selector = etree.HTML(html)     # 将源码转换为能被XPath匹配的格式
            location = selector.xpath("/html/body/div/div[5]/div/p[2]/code")[0].text
            location = location.split(" ")[0]
            if location in municipality:
                city = location[:-1]        # 直辖市的话不取'市'，不然天气结果会不准
            else:
                for i, char in enumerate(location):
                    if char == "区" or char == "省":
                        index = i + 1
                        break
                city = location[index:-1]       # 取'省'后面一直到'市'中间的城市名称用作天气搜索
            return city
        except Exception as e:
            raise e

    def get_city_code(self, city='合肥'):
        """
        输入一个城市，返回在中国天气网上城市所对应的code
        """
        try:
            parameter = urlparse.parse.urlencode({'cityname': city})
            conn = http.client.HTTPConnection('toy1.weather.com.cn', 80, timeout=5)
            conn.request('GET', '/search?' + parameter)
            r = conn.getresponse()
            data = r.read().decode()[1:-1]
            json_data = json.loads(data)
            code = json_data[0]['ref'].split('~')[0]        # 返回城市编码
            return code
        except Exception as e:
            raise e

    def get_city_weather(self, city_code):
        """
        通过城市编码找到天气信息
        """
        try:
            url = 'http://www.weather.com.cn/weather1d/' + city_code + '.shtml'
            headers = { "Referer": url }
            conn = http.client.HTTPConnection('d1.weather.com.cn', 80, timeout=5)
            conn.request('GET', '/sk_2d/' + city_code + '.html', headers=headers)
            r = conn.getresponse()
            data = r.read().decode()[13:]
            weather_info = json.loads(data)
            return weather_info
        except Exception as e:
            raise e

    def return_city_weather(self):
        """
        返回城市天气信息
        """
        try:
            city = self.get_city_name(self.download_page(target_url))
            city_code = self.get_city_code(city)
            city_wether = self.get_city_weather(city_code)
        except:
            return None
        return city_wether
