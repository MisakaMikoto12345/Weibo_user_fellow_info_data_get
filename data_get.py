import requests#获取网页源码使用
import time#加入程序时间间隔
from lxml import etree#解析网页源代码用
import pandas as pd#将数据保存为csv格式用



#获取指定用户的关注界面的json
def fellow_json_get(uid,page):

    base_url = "https://weibo.com/ajax/friendships/friends?page="+str(page)+"&uid="+str(uid)#修改基本网址


    #下列请求头中的agent和cookie要更换成自己浏览器已经登陆微博界面的！！！！！一定注意否则无法 登陆的微博账号最好不要关注跟山东省地级市相关的账号
    headers= {
            'cookie':'UOR=passport.weibo.com,weibo.com,login.sina.com.cn; SINAGLOBAL=4270609297130.9385.1686138848583; ULV=1686138848586:1:1:1:4270609297130.9385.1686138848583:; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhGQw2m3PE_GLECAgfk7Jgy5JpX5KMhUgL.FoMfShep1hq71hM2dJLoI02LxK-LB.-LBK2LxK-L1-BL1hzLxKMLB.-L12-LxKML1K5LBoBLxKBLBonLBoqEeh5X; XSRF-TOKEN=re_9cdyFcAgu8mIDsNdglk4r; ALF=1688991421; SSOLoginState=1686399421; SCF=AnIKwRGJ_zSXfFdplm9SDg4HjV6B0yPedlrCSxdqqjLOg80wfWcOsfHLSjFeVMPTY7SUdcUJWm3bDJw0oWWxTn4.; SUB=_2A25JgBntDeRhGeFL71EQ-CjMwzuIHXVq9AwlrDV8PUNbmtANLUX8kW9NQgb-dh8bTC614ZAeUNT31IUKSgUA6Ya6; WBPSESS=GQu48jBGTr8TVKFVKK9oLy_rWvIVf_EFg7oEgy6UyCSC4_gBlKSLaXzBFHZvwd4XXfTkO2lIYb50oIF-bBlOxGNF4ucMa4KUxwTzlFYXrSDtyPXmgN2nGyjaEdmWl7yCnWf2mXakUmZ7mHbFTho3QQ==',
            'User_Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
          }


    # for url in url_list:
    response = requests.get(base_url,headers=headers)
    response.encoding = 'utf-8'#防止中文乱码2
    if response.status_code == 200:
        if "users" in response.json():#判断博主的关注是否公开展示，若公开则返回原json文档
            return response.json()["users"]
        if "users" not in response.json():#若不公开则返回“博主设置仅针对粉丝展示全部关注”
            return response.json()["msg"]



#获取不同地市的政务微博的用户id以及uid
def get1(name):
    base_url = "https://s.weibo.com/user?q="+name+"&auth=org_vip&page=1"#选取每个地市相关搜索界面网页网址作为爬取对象
    # 下列请求头中的agent和cookie要更换成自己浏览器已经登陆微博界面的！！！！！一定注意 否则无法获取网页源代码 登陆的微博账号最好不要关注跟山东省地级市相关的账号
    headers= {
            'cookie':'UOR=passport.weibo.com,weibo.com,login.sina.com.cn; SINAGLOBAL=4270609297130.9385.1686138848583; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhGQw2m3PE_GLECAgfk7Jgy5JpX5KMhUgL.FoMfShep1hq71hM2dJLoI02LxK-LB.-LBK2LxK-L1-BL1hzLxKMLB.-L12-LxKML1K5LBoBLxKBLBonLBoqEeh5X; WBPSESS=GQu48jBGTr8TVKFVKK9oLy_rWvIVf_EFg7oEgy6UyCTPMsbiRy0rGB9I64mTo4GXN7XDtWDZPlwHMYuFHbFVeis0dh-4D08K2CeLqtDrDn5xp3bPSUfgZFlQLfJW8OP98lAnHkIH-1izIm_IN-UVaQ==; _s_tentry=s.weibo.com; Apache=6766670027946.162.1686446479508; ULV=1686446479515:3:3:1:6766670027946.162.1686446479508:1686400529621; XSRF-TOKEN=DLxz7lFtqLFrtm8dqAB1Iw14; ALF=1689038489; SSOLoginState=1686446489; SCF=AnIKwRGJ_zSXfFdplm9SDg4HjV6B0yPedlrCSxdqqjLOBuxV1P_iiakf74L6NpRZc_J6GhFvTHIeqBqhkjaGrpk.; SUB=_2A25JgVHJDeRhGeFL71EQ-CjMwzuIHXVq98QBrDV8PUNbmtANLXnEkW9NQgb-dmjhbBTK55mT9u5VL7wNWdgfgPNH',
            'User_Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
          }


    # for url in url_list:
    response = requests.get(base_url,headers=headers)#获取网页代码
    response.encoding = response.apparent_encoding#防止网页源码中的中文乱码

    html = etree.HTML(response.text)#解析网页源码
    # print(response.text)
    customer_id=html.xpath('//div[@class="info"]//a[@class="name"]/text()')#获取网页代码中用户名字符
    uid_list=html.xpath('//div[@class="btn"]/button[@action-type="userFollow"]/@uid')#获取网页代码中用户uid
    # print(customer_id)
    return customer_id,uid_list#返回用户名及用户uid
    # print(uid_list)


#获取用户id对应uid的字典
def get_info_dict(name2):
    customer_id=[]
    uid_list=[]
    customer_id = get1(name2)[0]#将获取的用户名保存在此列表中
    uid_list = get1(name2)[1]#将获取的用户uid保存在此列表中

    # print(customer_id)
    # print(uid_list)
    infor_dict={}
    infor_dict=dict(zip(customer_id,uid_list))#把用户名列表和对应的用户uid用键值对表示

    # print (infor_dict)
    re_customer_id=[]#初始化重置后的用户id
    for j in customer_id:#筛选出用户id长度等于4的id 保存在列表中
        if len(j) == 4:
            re_customer_id.append(j)
    # print(re_customer_id)

    re_uid_list=[]#初始化筛选后用户对应的uid

    for l in re_customer_id:#依次找到字典中用户对应的uid
        re_uid_list.append(infor_dict[l])
    # print(re_uid_list)
    re_infor_dict={}
    re_infor_dict=dict(zip(re_customer_id,re_uid_list))#再将筛选后的用户名和其对应的uid用键值对表示

    return re_infor_dict#返回用户名与uid的键值对







#获取关注列表的用户名
def user_id_get(uid2):
    fellow_json_list=[]#初始化关注网页json源代码所包含的列表
    info_userid_list=[]#初始化用于存放关注用户名的列表
    if isinstance(fellow_json_get(uid2,1),list):#判断返回的网页源代码格式是否是列表 如果是则取其前6页合并为一个总列表
        for p in range (1,7):
            time.sleep(3)#增加时间间隔防止被网页禁止访问导致返回空数据
            print(uid2,p)#确认获取进度哪个用户的第几页
            fellow_json_list = fellow_json_list + fellow_json_get(uid2,p)#将所有列表保存在该列表中
        print(fellow_json_list)#确认总网页源码不为空 防止报错和帮助检查错误

        for info_cutsomer_2 in fellow_json_list:#遍历全部的列表元素，因为列表元素均为字典，因此每一个元素的包含的name键与值可以直接获取
            info_userid_list.append(info_cutsomer_2["name"])
        return info_userid_list
    else:#如果返回的网页源码不为列表，而是溢出网页处json源码键值对下msg键的值则返回一下列表
        return ["仅限关注可见"]




name_list=["济南","青岛","淄博","枣庄","东营","烟台","潍坊","济宁","泰安","威海","日照","临沂","德州","聊城","滨州","菏泽"]#山东省16地级市构成的列表，用于替换get1(name)方法中的name，获取不同地市的搜索结果
user_name_list=[]#初始化保存用户名的列表
total_uid_list=[]#初始化保存用户uid的列表
diff_dict={}#初始化保存需要被爬取关注列表用户的用户名和uid的键值对
for city_name in name_list:#遍历山东省所有地级市
    time.sleep(3)#增加时间间隔防止被禁止访问
    diff_dict=get_info_dict(city_name)#保存需要被爬取关注列表用户的用户名和uid的键值对
    print(list(diff_dict.keys()))#输出当前要被爬取关注列表用户的所有用户名的列表
    print(list(diff_dict.values()))#输出当前要被爬取关注列表用户的所有uid的列表
    user_name_list = user_name_list + list(diff_dict.keys())#保存十二地市全部的要被爬取关注列表的用户名
    total_uid_list = total_uid_list +list(diff_dict.values())#保存十二地市全部的要被爬取关注列表的uid

print(user_name_list)#输出十二地市所有要被爬取的用户的用户名
print(total_uid_list)#输出十二地市全部的要被爬取关注列表的uid



toal_fellow_list=[]#初始化保存所有用户的关注列表的用户名

for user_id_2 in total_uid_list:#遍历所有需要被爬取关注列表用户的uid
    toal_fellow_list.append(user_id_get(user_id_2))#获取到数据后依次放入列表
print(toal_fellow_list)#检查


#将用户名和对应用户关注的用户的名称保存到csv输出
dataframe = pd.DataFrame({"用户名":user_name_list,"关注":toal_fellow_list})
dataframe.to_csv(r'.\山东省各地市十二地市部分政务相关微博的关注列表.csv',index = False,sep=",",encoding='utf-8',mode='w')