import requests #获取网页内容使用
from lxml import etree #解析网页内容使用
import pandas as pd #写入csv并保存使用


# 获取网页文本信息
def article_info_get(url):
    # 发送请求 获取网页内容
    response = requests.get(url)
    response.encoding = response.apparent_encoding#调整编码防止中文乱码
    # print(response.text)


    #解析html文本
    html = etree.HTML(response.text)

    #读取文本文件进行解析（可省略）
    # result = etree.tostring(html, encoding='utf-8')
    # print(result.decode('utf8'))

    # 分析html使用xpath语句获取文章标题
    titles = html.xpath("//li/p/a/text()")
    # 获取文章标题
    authors = html.xpath("//li/span/text()")

    return titles,authors



# 获取需要爬取数据的网页
def url_get():
    url_list = []#创建网址总集列表作为返回值
    for y in ['2021','2022',2023]: #近两年的期刊年份
        if y == 2023:
            for n in range(1,4):#查询网页得知2023年份只更新到第三期
                url ="https://jjyglpl.sdufe.edu.cn/qkml1/n"+str(y)+"nd"+str(n)+"q.htm"
                url_list.append(url)
        else:
            for n in range(1,7):#获取21-22年份全年六期的网址
                url = "https://jjyglpl.sdufe.edu.cn/qkml1/jjyglpl"+str(y)+"nd"+str(n)+"q.htm"
                url_list.append(url)
    return(url_list)


url = url_get()
titles=[]#创建列表保存题目
authors=[]#创建空列表保存作者
for i in url: #遍历所有的网址获取文章标题和作者
    titles = titles + article_info_get(i)[0]
    authors = authors + article_info_get(i)[1]

#写入csv并保存为文件
dataframe = pd.DataFrame({"标题":titles,"作者":authors})
dataframe.to_csv(r'.\经济与管理评论作者及题目.csv',index = False,sep=",",encoding='utf-8',mode='w')