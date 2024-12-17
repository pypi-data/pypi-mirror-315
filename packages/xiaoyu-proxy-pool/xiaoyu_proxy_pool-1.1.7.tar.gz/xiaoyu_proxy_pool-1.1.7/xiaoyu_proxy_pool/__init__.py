from loguru import logger
import requests
class Porp_text_file:
    # 这里是配置本地环境的代理逻辑 负责逻辑处理!
    def get_ip(ip_address,port):
        return 'http://'+ip_address+':'+port
    # 这是关于http的
    def get_ips(ip_address,port):
        return 'https://'+ip_address+':'+port
    def proxy_url(proxy_url,ip_address_url):
        # 指定的配置好的代理池
        logger.info('使用指定的代理池')
        proxies={
            'http':proxy_url,
            'https':proxy_url
        }
        response=requests.get(ip_address_url,proxies=proxies)
        return response.text
    def proxy_file(proxy_file):
        # 读取代理池文件
        logger.info('读取代理池文件')
        try:
            with open(proxy_file,'r') as f:
                lines=f.readlines()
            return lines
        except:
            print('ERROR IS NOT FILE FOUND !!!找不到指定文件!')