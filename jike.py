# -*-coding:utf8-*-
#用于读取网页数据
import urllib

import re

import os
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 总页面
rootUrl = "http://www.jikexueyuan.com/path/python/"
sText = ""


# 读取网页，并将其保存到指定的文件中（默认为content.txt）
def req_url(hurl, txt_name='content.txt'):
    f = open(txt_name, 'w')
    if not hurl.startswith('http'):
        hurl = 'http:' + hurl
    html = requests.get(hurl)
    html_text = html.text
    f.write(html_text)
    f.close()
    return html_text


#读取保存网页内容的文件
def read_html_file(txt_name='content.txt'):
    f = open(txt_name, 'r')
    html_text = f.read()
    f.close()
    return html_text


stageIdx = 0
stage = []


# 获取指定子段落下，该段落包含的信息
# < div class ="pathstage-txt" >
#   < h2 > 3.Python定向爬虫入门 < / h2 >
#   < p > 本阶段主要介绍了使用Python语言编...< / p >
#   < span > (共3课程，124分钟，88229人已经学习) < / span >
# < / div >
def read_stage(each):
    title_text = each.xpath('div[@class="pathstage-txt"]/h2/text()')[0]
    desc_text = each.xpath('div[@class="pathstage-txt"]/p/text()')[0]
    desc_text =each.xpath('div[@class="pathstage-txt"]/span/text()')[0]+ desc_text
    # 将以上得到的信息保存到stage数组结构中
    stage.append({"Title": title_text, "desc": desc_text, "lessons": []})


# 读取并分析网页内容（保存于sText变量中）
def read_text(sel):
    content_field = sel.xpath('//div[@class="pathstage mar-t30"]')
    for each in content_field:
        read_stage(each)
        lessonUL = each.xpath('.//ul[@class="cf"]/li')
        for eachL in lessonUL:
            lessID = eachL.xpath(".//@id")[0]
            lessUrl = eachL.xpath('.//div[@class="lessonimg-box"]/a/@href')[0]
            imageUrl = eachL.xpath('.//img[@class="lessonimg"]/@src')[0]
            imgName = ".\img\\" + (lessID) + imageUrl[-4:1000]
            save_img(imageUrl, imgName)
            lessName = eachL.xpath('.//h2[@class="lesson-info-h2"]/a/text()')[0]
            lessDesc = eachL.xpath('.//div[@class="lesson-infor"]/p/text()')[0]
            lessDesc=lessDesc.replace('\n','').replace('\t','')
            stage[stage.__len__() - 1]["lessons"].append(
                {"name":lessName,
                 "desc":lessDesc,
                 "ID":lessID,
                 "imgName":imgName,
                 "href": lessUrl})

            reply_info = each.xpath('div')
        # title_field = each.xpath('h2/text()')[0]
        stage[stage.__len__() - 1]["lessCount"]=len(stage[stage.__len__() - 1]["lessons"])
        # print(stage[stage.__len__()-1]["Title"])
        # print(stage[stage.__len__()-1]["desc"])


def save_img(image_url, file_name):
    u = urllib.urlopen(image_url)
    data = u.read()
    f = open(file_name, 'wb')
    f.write(data)
    f.close()


def readimg(sel, b_save=False):
    imgUrl = sel.xpath('//img')
    iTmp = 1
    for each in imgUrl:
        TitleText = each.xpath('@src')[0]
        print(str(iTmp) + TitleText)
        if(b_save):
            if (str(TitleText).endswith('.jgp')):
                save_img(TitleText, ".\jike%d.jpg" % iTmp)
            if (str(TitleText).endswith('.png')):
                save_img(TitleText, "..\down\jike%d.png" % iTmp)
        iTmp = iTmp + 1


def read_lesson():
    for each_stage in stage:
        for each_lesson in each_stage["lessons"]:
            print (each_lesson["href"])


def save_lesson(url, txt_name):
    url_text = req_url(url, txt_name)
    return url_text


bWrite = False  # True # False  #True
if bWrite:
    sText = req_url(rootUrl, "root.txt")
else:
    sText = read_html_file("root.txt")
selector = etree.HTML(sText)
# readimg(selector)
read_text(selector)
read_lesson()
# sText = save_lesson(stage[0]["lessons"][0]["href"], "lesson/201.txt")
sText = ""
