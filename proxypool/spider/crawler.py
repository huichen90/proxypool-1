import json
import re
from lxml import etree
from proxypool.spider.utils import get_page
from pyquery import PyQuery as pq
from proxypool.log.save_log import add_spider_log
from proxypool.common.setting import *


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            add_spider_log('成功获取到代理-%s' % proxy, LOG_INFO)
            proxies.append(proxy)
        return proxies
        
    # def crawl_daxiang(self):
    #     url = 'http://vtp.daxiangdaili.com/ip/?tid=559363191592228&num=50&filter=on'
    #     html = get_page(url)
    #     if html:
    #         urls = html.split('\n')
    #         for url in urls:
    #             yield url
          
    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            add_spider_log('Crawling%s'%url,LOG_INFO)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_ip181(self):
        start_url = 'http://www.ip181.com/'
        html = get_page(start_url)
        # ip_address = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
        ip_list = json.loads(html)['RESULT']

        for ip in ip_list:
            result = ip.get('ip') + ':' + ip.get('port')
            yield result.replace(' ', '')

    def crawl_ip3366(self):
        for page in range(1, 4):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = get_page(start_url)
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address+':'+ port
                yield result.replace(' ', '')


#    def crawl_kxdaili(self):
 #       for i in range(1, 11):
  #          start_url = 'http://www.kxdaili.com/dailiip/1/{}.html#ip'.format(i)
   #         html = get_page(start_url)
    #        ip_address = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
    #        # \s* 匹配空格，起到换行作用
    #        re_ip_address = ip_address.findall(html)
    #        for address, port in re_ip_address:
     #           result = address + ':' + port
    #            yield result.replace(' ', '')
#

    # def crawl_premproxy(self):
    #     for i in ['China-01','China-02','China-03','China-04','Taiwan-01']:
    #         start_url = 'https://premproxy.com/proxy-by-country/{}.htm'.format(i)
    #         html = get_page(start_url)
    #         if html:
    #             ip_address = re.compile('<td data-label="IP:port ">(.*?)</td>')
    #             re_ip_address = ip_address.findall(html)
    #             for address_port in re_ip_address:
    #                 yield address_port.replace(' ','')

    # def crawl_xroxy(self):
    #     for i in ['CN','TW']:
    #         start_url = 'http://www.xroxy.com/proxylist.php?country={}'.format(i)
    #         html = get_page(start_url)
    #         if html:
    #             ip_address1 = re.compile("title='View this Proxy details'>\s*(.*).*")
    #             re_ip_address1 = ip_address1.findall(html)
    #             ip_address2 = re.compile("title='Select proxies with port number .*'>(.*)</a>")
    #             re_ip_address2 = ip_address2.findall(html)
    #             for address,port in zip(re_ip_address1,re_ip_address2):
    #                 address_port = address+':'+port
    #                 yield address_port.replace(' ','')
    #
    def crawl_kuaidaili(self):
        for i in range(1, 4):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>') 
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address,port in zip(re_ip_address, re_port):
                    address_port = address+':'+port
                    yield address_port.replace(' ','')

    def crawl_xicidaili(self):
        try:
            for i in range(1, 3):
                start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
                headers = {
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
                    'Host':'www.xicidaili.com',
                    'Referer':'http://www.xicidaili.com/nn/3',
                    'Upgrade-Insecure-Requests':'1',
                }
                html = get_page(start_url, options=headers)
                selector = etree.HTML(html)
                ip_list = selector.xpath('//table[@id="ip_list"]//tr')
                for ips in ip_list[1:]:
                    ip = ips.xpath('./td[2]/text()')[0]
                    port = ips.xpath('./td[3]/text()')[0]
                    address_port = ip + ':' + port
                    yield address_port.replace(' ', '')
        except Exception as e:
            pass
    
    def crawl_ip3366(self):
        for i in range(1, 5):
            start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
            html = get_page(start_url)
            if html:
                selector = etree.HTML(html)
                ip_list = selector.xpath('//tbody/tr')
                for ips in ip_list[1:]:
                    ip = ips.xpath('./td[1]/text()')[0]
                    port = ips.xpath('./td[2]/text()')[0]
                    address_port = ip + ':' + port
                    yield address_port.replace(' ', '')
    
    def crawl_iphai(self):
        start_url = 'http://www.iphai.com/'
        html = get_page(start_url)
        if html:
            selector = etree.HTML(html)
            ip_list = selector.xpath('//tr')
            for ips in ip_list[1:]:
                ip = ips.xpath('./td[1]/text()')[0]
                port = ips.xpath('./td[2]/text()')[0]
                address_port = ip + ':' + port
                yield address_port.replace(' ', '').replace('\r\n', '')

    def crawl_89ip(self):
        for i in range(1, 5):
            start_url = 'http://www.89ip.cn/index_{}.html'.format(i)
            html = get_page(start_url)
            if html:
                selector = etree.HTML(html)
                ip_list = selector.xpath('//tbody/tr')
                for ips in ip_list:
                    ip = ips.xpath('./td[1]/text()')[0]
                    port = ips.xpath('./td[2]/text()')[0]
                    address_port = ip + ':' + port
                    yield address_port.replace(' ', '').replace('\n', '').replace('\t', '')

    def crawl_data5u(self):
        start_url = 'http://www.data5u.com/free/gngn/index.shtml'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
            'Host': 'www.data5u.com',
            'Referer': 'http://www.data5u.com/free/index.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        }
        html = get_page(start_url, options=headers)
        if html:
            selector = etree.HTML(html)
            ip_list = selector.xpath('//div[@class="wlist"]//ul[@class="l2"]')
            for ips in ip_list:
                ip = ips.xpath('./span[1]/li/text()')[0]
                port = ips.xpath('./span[2]/li/text()')[0]
                address_port = ip + ':' + port
                yield address_port.replace(' ', '')


