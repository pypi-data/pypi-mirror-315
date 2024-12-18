import random
import requests
import time
import os
class Porp_text_file:
    def Proxy_header():
        ua_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59",
        ]
        user_agent = random.choice(ua_list)
        num = range(1, 255)
        ip_num1 = random.choice(num)
        ip_num2 = random.choice(num)
        ip_num3 = random.choice(num)
        ip_num4 = random.choice(num)
        headers = {
            'User-Agent': user_agent,  # 随机生成一个ua
            'X-Forward-for': "%d.%d.%d.%d" % (ip_num1, ip_num2, ip_num3, ip_num4) # 购买的代理IP
        }
        return headers
    def Proxy_头部():
        ua_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59",
        ]
        user_agent = random.choice(ua_list)
        return user_agent
    def Proxy_header_list(res_txt_IP,url):
        # 这里需要传一个数组列表
        while True:
            try:
                time.sleep(3)
                proxy= {'http': random.choice(res_txt_IP), 'https': random.choice(res_txt_IP)}
                req=requests.get(url,proxies=proxy)
                return req.text
            except:
                print('代理IP失效!请确定IP是否在线!')
    def get_ip(ip_address,port,newCode):
       if newCode==0:
           return 'https://'+ip_address+':'+port
       else:
           return 'http://'+ip_address+':'+port
    def uat(InterFaceName,newCode):
        if newCode==0:
            return 'https://'+InterFaceName
        else:
            return 'http://'+InterFaceName
    def _path(file_path):
        if os.path.exists(file_path):
            print('文件存在!')
        else:
            os.mkdir(file_path)
    
    def get_html_with_proxy(urls, proxies_list):
        
        results = {}
        for url in urls:
            for proxy in proxies_list:
                try:
                    response = requests.get(url, proxies=proxy, timeout=5)  # 设置超时时间为5秒，可按需调整
                    if response.status_code == 200:
                        results[url] = response.text
                        print(response.text)
                        break  # 如果成功获取，就换下一个URL，不再尝试其他代理
                    else:
                        continue
                except requests.RequestException as e:
                    print(f"请求 {url} 出现异常，代理 {proxy} 不可用，异常信息: {e}")
                    continue
            else:
                results[url] = None  # 如果所有代理都试过了还没成功获取，对应URL的值设为None
        return results
    