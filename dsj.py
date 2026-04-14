from tkinter.font import names
import pymysql
import requests
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import json
import time
from bs4 import BeautifulSoup
import  pymysql
from urllib.parse import urlparse, parse_qs
from  xiangqing import select,update
def agent_info():
    headers = {
        'Cookie': 'QC005=7fe37cf66427a912b4d69a1060c84ef1; T00404=2e8d9c3adbc9d455bb4d2fd5cf7da7df; QC173=0; QC234=019a0d34fdab179077a03652e7d4081b; QC006=yqx2cdjx6or8kg6leunonq9i; QC235=d551d089d215459b89fd60ed1130b835; TQC030=1; PD005=7tvcwbzwwzb9plvnujojpuc2hca9qcx8; QP0038=500; QP0035=4; QP0042={"v":3,"cpu":32,"avc":{"de":2,"wv":1,"pr":1},"hvc":{"de":2,"wv":0,"pr":1},"av1":{"de":2,"wv":1,"pr":1},"av110":{"de":2,"wv":0,"pr":0}}; P00004=.1756780493.1c2777ee04; QP0041=%5B%5B%224239145695513300%22%2C243%2C1756780812879%5D%5D; __dfp=a07eeae2bdd1194b6789d0f3448e33987091648793fa1b1e9e90195e8e747e6d65@1758074837275@1756778838275; QP007=1200; QC007=DIRECT; QP0037=0; IMS=IggQABj_y-HFBiorCiBhODM5MTM4OTc0ZTY0MjMwODgxMzMwNDJiOGIxOWZlNBAAIgAo8QEwBTAAMAAwAHIkCiBhODM5MTM4OTc0ZTY0MjMwODgxMzMwNDJiOGIxOWZlNBAAggEEIgIQBooBJAoiCiBhODM5MTM4OTc0ZTY0MjMwODgxMzMwNDJiOGIxOWZlNA; QC008=1756778837.1756778837.1756863251.2; QC191=; nu=0; curDeviceState=width%3D1699%3BconduitId%3D%3Bscale%3D150%3Bbrightness%3Ddark%3BisLowPerformPC%3D0%3Bos%3Dbrowser%3Bosv%3D10.0.19044; P00001=38Tj2Mm3Bp80PznaXu7m1r4LPm338IrucNUT1x3CwKjdBAEykf016rJ1Sf6qtLiub58oL9c; P00007=38Tj2Mm3Bp80PznaXu7m1r4LPm338IrucNUT1x3CwKjdBAEykf016rJ1Sf6qtLiub58oL9c; P00003=4495999183698432; P00010=4495999183698432; P01010=1756915200; P00PRU=4495999183698432; P00002=%7B%22uid%22%3A%224495999183698432%22%2C%22pru%22%3A4495999183698432%2C%22user_name%22%3A%22150****3476%22%2C%22nickname%22%3A%22%5Cu7528%5Cu6237%40ff91662413a00%22%2C%22pnickname%22%3A%22%5Cu7528%5Cu6237%40ff91662413a00%22%2C%22type%22%3A11%2C%22email%22%3Anull%7D; vipTypes=0; QC170=0; QY_PUSHMSG_ID=7fe37cf66427a912b4d69a1060c84ef1; QC010=169397494',
        'Host': 'www.iqiyi.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'
    }
    return headers
def get_list_url(url):
    ##print('正在请求：', url)
    headers = agent_info()
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    ##print('抓取电视剧详情链接')

    TV_urls = []
    items = soup.find_all(attrs={'class': 'rvi__list'})
    for item in items:
        a_tags = item.find_all('a')  # 获取当前rvi__list下所有a标签
        for a in a_tags:
            href = a.get('href')
            if not href.startswith('https'):
                href = 'https:' + href
            TV_urls.append(href)
    ##print(TV_urls)

    TV_names=[]
    items = soup.find_all(attrs={'class': 'rvi__con'})
    for item in items:
        names=item.find_all(attrs={'class': 'rvi__tit1'})
        for name in names:
            name=name.get('title')
            TV_names.append(name)
    ##print(TV_names)

    TV_years = []
    items = soup.find_all(attrs={'class': 'rvi__con'})
    for item in items:
        years = item.find_all(attrs={'class': 'rvi__type1'})
        for year in years:
            text = year.get_text(strip=True)
            # 按“/”分割文本，取第二个部分（年份）
            year_text = text.split('/')[1].strip()
            TV_years.append(year_text)
    ##print(TV_years)

    TV_actors = []
    items = soup.find_all(attrs={'class': 'rvi__con'})
    for item in items:
        actors = item.find_all(attrs={'class': 'rvi__type1'})
        for actor in actors:
            text = actor.get_text(strip=True)
            # 按“/”分割文本，取第二个部分（年份）
            actor_text = text.split('/')[3].strip()
            TV_actors.append(actor_text)
    ##print(TV_actors)

    TV_pops=[]
    pops = soup.find_all(attrs={'class': 'rvi__index'})
    for pop in pops:
        pop = pop.span.text
        TV_pops.append(pop)
    ##print(TV_pops)

    TV_ranks = []
    ranks = soup.find_all(attrs={'class': 'rvi__img__box'})
    for rank in ranks:
        rank = rank.i.span.text
        TV_ranks.append(rank)
    ##print(TV_ranks)


    TV_aids=[]
    items= soup.find_all(attrs={'class': 'rvi__list'})
    for item in items:
        aids=item.find_all('a')
        for aid in aids:
            aid = aid.get('data-pb-v2')[4:]
            TV_aids.append(aid)
    ##print(TV_aids)

    TV_types = []
    items = soup.find_all(attrs={'class': 'rvi__con'})
    for item in items:
        years = item.find_all(attrs={'class': 'rvi__type1'})
        for year in years:
            text = year.get_text(strip=True)
            # 按“/”分割文本，取第二个部分（年份）
            year_text = text.split('/')[2].strip()
            TV_types.append(year_text)
    ##print(TV_types)

    if len(TV_ranks) == len(TV_names) == len(TV_actors) == len(TV_types) == len(TV_urls) == len(TV_pops) == len( TV_years) == len(TV_aids):

        for i in range(len(TV_ranks)):
            print(f"排名: {TV_ranks[i]}")
            print(f"电影名称: {TV_names[i]}")
            print(f"主演: {TV_actors[i]}")
            print(f"电影类型: {TV_types[i]}")
            print(f"热度: {TV_pops[i]}")
            print(f"年份: {TV_years[i]}")
            print(f"标识: {TV_aids[i]}")
            print(f"链接: {TV_urls[i]}")
            print("-" * 140)
    else:
        print("警告：电影名称和主演数量不匹配")
    for i in range(25):
        sql = (
            'insert into`tv`(`name`, `year`, `actor`, `popularity`, `rank`, `url`) values("{}", "{}", "{}", " {}","{}","{}")'
            .format(TV_names[i], TV_years[i], TV_actors[i], TV_pops[i], TV_ranks[i], TV_urls[i]))
        sql4 = ('select aid from hash where aid="{}"'.format(TV_aids[i]))
        res = select(sql4)
        if not res:
            update(sql)

    for i in range(25):
        sql2 = ('insert into hash(aid) values("{}")'.format(TV_aids[i]))
        sql4 = ('select aid from hash where aid="{}"'.format(TV_aids[i]))
        res = select(sql4)
        if not res:
            update(sql2)

    for i in range(len(TV_aids)):
        aid = TV_aids[i]
        type_group = TV_types[i]
        sql5 = ('select aid from type where aid="{}"'.format(TV_aids[i]))
        record = select(sql5)
        if not record:
            single_types = type_group.split(' ')
            for single_type in single_types:
                sql3 = ('insert into type(aid,type) values("{}","{}")'.format(aid, single_type))
                update(sql3)





if __name__ == '__main__':

    get_list_url("https://www.iqiyi.com/ranks1/-1/-6")





