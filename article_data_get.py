import requests #获取网页代码使用
from lxml import etree #解析网页代码和利用xpath语法获取数据使用
import pandas as pd #写入csv文件使用
#获取文章数据的标题及关键词
def articles_info_get(url):
    response = requests.get(url)#获取网页源码
    response.encoding = response.apparent_encoding#防止网页源码里面的中文乱码
    # print(response.text)
    html = etree.HTML(response.text)#解析网页源代码
#解析网页源代码获取文章的标题及关键字
    keywords = html.xpath('//td[@height="25" and @class="J_zhaiyao"]/a[@class="txt_zhaiyao1"and @href="#"]/text()')
    titles = html.xpath('//span[@class="J_biaoti"]/text()')
    keywords = ','.join(map(str, keywords))#更改分隔符为‘，’
    return titles,[keywords]



#获取各个文章链接
def article_url_get(url_1):
    response = requests.get(url_1)#获取网页源码
    response.encoding = response.apparent_encoding#防止网页源码里面的中文乱码
    # print(response.text)
    html = etree.HTML(response.text)#解析网页源代码
   #获取网页中全部文章的链接
    url_0_list=html.xpath('//a[@target="_blank" and @class="txt_biaoti"]/@href')
    return url_0_list


#遍历获取所有目录网页的url
def ctalogue_url_get():
    url_catalogue_list=[]#创建空列表 最后作为返回值
    #观察网页特点找到其共性
    for i in range(1552,1560):#期刊目录网页从2022年6月到2023年1月的排序为顺序 依次从1552加1到1659
        u="https://manu44.magtech.com.cn/Jwk_infotech_wk3/CN/volumn/volumn_"+str(i)+".shtml"
        url_catalogue_list.append(u)
    for j in [1567,1568,1569]:#从2023年2月到4月依次为1567加1到1569
        p = "https://manu44.magtech.com.cn/Jwk_infotech_wk3/CN/volumn/volumn_" + str(j) + ".shtml"
        url_catalogue_list.append(p)
    # print(url_catalogue_list)
    return url_catalogue_list


#获取目录中所有文章的url
def all_article_url():
    url_catalogue_list = ctalogue_url_get()#创建列表对象村放所有目录网页url
    article_url_list=[]#创建空列表存放文章url作为返回值
    for url_catalogue in url_catalogue_list:#遍历所有网页url 调用前面获取文章url的方法依次获取每页的文章url
        article_url_list = article_url_list + article_url_get(url_catalogue)

    # print(article_url_list)
    return article_url_list

titles=[]#创建空列表存放文章标题
keywords=[]#创建空列表存放关键词
for i in all_article_url():#遍历所有文章url
    titles = titles+articles_info_get(i)[0] #调用文章标题和关键的方法获取标题及关键词，并依次存放入之前的空列表
    keywords = keywords +articles_info_get(i)[1]
# print(keywords)

#保存到csv文件中
dataframe = pd.DataFrame({"标题":titles,"关键词":keywords})
dataframe.to_csv(r'.\论文题目及关键词.csv',index = False,sep=",",encoding='utf-8',mode='w')