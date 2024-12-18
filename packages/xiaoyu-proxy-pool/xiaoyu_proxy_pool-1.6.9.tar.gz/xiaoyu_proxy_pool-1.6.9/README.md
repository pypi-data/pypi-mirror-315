`软件名称`
    小鱼工具包
`软件说明`
This is an automation toolkit development environment to use, the software integrates multi-threading, global variables, global agents and other tools, for high efficiency automated office, for automated script office provides a certain help behavior.
Used to do scripting global variable proxy test tool, the tool can add ports and specified local production environment for local automation and multi-threaded batch interface testing
This software is a toolkit series, provides a huge API interface, you can package the interface code, has a certain help for automated testing or for the development of JS and the like also have a little help, thank you for your support
`中文参考文档`:
这是一个自动化工具包的开发环境使用,软件集成了多线程,全局变量,全局代理等一些列的工具,进行高效率自动化办公,
为自动化脚本办公提供了一定的帮助行为。该工具可以添加端口和指定的本地生产环境，用于本地自动化和多线程批量接口测试,
同时可以为高效率的办公提供了一定程度的帮助!
本软件是一个工具包系列,提供了庞大的API接口,对自动化测试有一定的帮助或者对开发JS之类的也有稍微帮助,谢谢各位的支持

`功能使用说明`:
`自动化代理功能区域`
    1.头部生成: Proxy_header  随机生成一个头部
    调用示例:
        print(Porp_text_file.Proxy_header())
        随机生成一个Header头部
        返回为:{'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)', 'X-Forward-for': '181.175.174.204'}
    2.多代理模式: Proxy_header_list 代理IP 需要传入一个IP列表,以及代理的url网站
        调用示例:Porp_text_file.Proxy_header_list([127.0.0.1:8080”],"代理的URL网站")
        返回响应的结果文本()
    3.全局处理接口模式:
        弃用原先的代码,处理新的接口处理URL模式
        Porp_text_file.get_ip(ip_address,port,newCode) 一共三个参数,第一参数填写你poatman中经常全局变量中的ip地址,第二个是端口号,newcode 0或者1 0hhtps 1http
        返回示例:https://192.168.1.1:8080 本地接口测试
    4.uat(InterFaceName,newCode) 参数: InterFaceName:接口名称,newCode:0或者1,0为https,1为http
        关于线上接口测试,例如说,https://api//text?name=test&age=18
    """
        Porp_text_file.get_html_with_proxy(['https://www.xxx.com','',''],[{"http": "http://192.168.1.1:8080"}])
        param urls: 要爬取的网页URL列表
        :proxies_list: 代理服务器信息列表，格式如 [{"http": "http://proxy_ip:proxy_port", "https": "https://proxy_ip:proxy_port"},...]
        :return: 一个字典，键为URL，值为对应网页的HTML内容（如果请求成功）或者None（如果请求失败）
        """
`处理文件区域`
    5._path(file_path) 检查文件并创建新文件的
    调用示例:Porp_text_file._path("./test.txt")
    `校验文件是否存在`



`关于本工具说明:`
    工具可能比较复杂,您可以自己测试,希望能够帮到您!目的是为了懒人项目的自动化办公
        


`历史版本`:
`1.6.9` 修复了版本无法无法识别问题,增加了部分功能日志,删除部分文件无用工具,本版本作为临时的测试API版本,后期有需要会进行整改
`1.6.7` 更新了1.1.7,修复了大部分漏洞,修复了部分bug,增加了很多功能工具,具体看功能日志
`1.1.7` 更新部分API接口功能,暂时没有更新多线程,后期将更新多线程功能
`1.0` 初始测试版本
