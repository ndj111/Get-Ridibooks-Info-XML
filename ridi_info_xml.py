#-*- encoding: utf8 -*-
from selenium import webdriver

from pathlib import Path

import os, json, urllib.parse, requests, re
import urllib.request

import re
import xmltodict



print("\n============================================================================")
urlcode = input('책 코드를 입력하세요 : ')

urladdr = "https://ridibooks.com/books/" + urlcode




# makexml
xml = '''<?xml version="1.0"?>
<ComicInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Title>{title}</Title>
  <Series>{title}</Series>
  <Summary>{desc}</Summary>
  <Writer>{author}</Writer>
  <Publisher>{publisher}</Publisher>
  <Genre></Genre>
  <Tags></Tags>
  <LanguageISO>ko</LanguageISO>
  <Notes>완결</Notes>
  <CoverArtist></CoverArtist>
  <Penciller></Penciller>
  <Inker></Inker>
  <Colorist></Colorist>
  <Letterer></Letterer>
  <CoverArtist></CoverArtist>
  <Editor></Editor>
  <Characters></Characters>
  <Year>{year}</Year>
  <Month>{month}</Month>
  <Day>{day}</Day>
</ComicInfo>'''

def change_info(str):
    return str.replace('<', '"').replace('>', '"').replace('&', '&amp;').strip()






print("============================================================================\n")

# driver = webdriver.Firefox()

chromedriver = 'C:/chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(chromedriver, options=options)



try:
    driver.get(urladdr)

    driver.implicitly_wait(3)


    entity = {}


    entity['title'] = driver.find_element_by_css_selector("#page_detail > div.detail_wrap > div.detail_body_wrap > section > article.detail_header.trackable > div.header_info_wrap > div.info_title_wrap > h3").text

    entity['publisher'] = driver.find_element_by_css_selector("#page_detail > div.detail_wrap > div.detail_body_wrap > section > article.detail_header.trackable > div.header_info_wrap > div:nth-child(4) > p.metadata.file_info.publisher_info > a").text

    entity['code'] = driver.find_element_by_css_selector("#page_detail > div.detail_wrap > div.detail_body_wrap > section > article.detail_header.trackable > div.Header_Metadata_Block > ul:nth-child(1) > li.Header_Metadata_Item.book_info.isbn_info > ul > li").text

    entity['pubdate'] = driver.find_element_by_css_selector("#page_detail > div.detail_wrap > div.detail_body_wrap > section > article.detail_header.trackable > div.Header_Metadata_Block > ul:nth-child(1) > li.Header_Metadata_Item.book_info.published_date_info > ul > li").text

    entity['author'] = driver.find_element_by_css_selector("#page_detail > div.detail_wrap > div.detail_body_wrap > section > article.detail_header.trackable > div.header_info_wrap > div:nth-child(4) > p.metadata.metadata_writer > span > a").text

    entity['description'] = driver.find_element_by_css_selector(".detail_introduce_book > #introduce_book > p.introduce_paragraph").text



    set_xml = xml.format(
        title = change_info(entity['title']),
        desc = change_info(entity['description']),
        author = change_info(entity['author']),
        publisher = change_info(entity['publisher']),
        year = entity['pubdate'][0:4],
        month = entity['pubdate'][5:7] if len(entity['pubdate']) > 4 else '01',
        day = entity['pubdate'][8:10] if len(entity['pubdate']) > 6 else '01',
    )

    f = open(os.path.join(os.getcwd(), 'info.xml'), 'w', encoding='UTF-8')
    f.write(set_xml)
    f.close()


    print("title => "+entity['title']+"\n")
    print("author => "+entity['author']+"\n")
    print("code => "+entity['code']+"\n")
    print("pubdate => "+entity['pubdate']+"\n")
    print("publisher => "+entity['publisher']+"\n")
    print("description => "+entity['description'])


except Exception as ex :
    print(" *** 에러", ex)



driver.close()
print("\n============================================================================\n")



driver.quit()
os.system("pause")








                    



