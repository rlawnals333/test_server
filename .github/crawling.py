#import

from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import requests
import os
import pandas as pd
import sqlite3
import json

class Market_data:
    def __init__(self,market_name,market_img,menu_price,menu_name,market_kind,market_tele,market_sign,market_score,market_location):
        self.market_name = market_name
        self.market_img = market_img
        self.menu_price = menu_price
        self.menu_name = menu_name
        self.market_kind = market_kind
        self.market_tele = market_tele
        self.market_sign = market_sign
        self.market_score = market_score
        self.market_location = market_location
        
    def show_market(self):
        print(f"식당 이름:{self.market_name}/ 가게 종류:{self.market_kind} / 전화번호 : {self.market_tele}  / 특이 사항:{self.market_sign} / 평점 : {self.market_score} / 위치 : {self.market_location}/ 메뉴 이름:{self.menu_name}  / 가격:{self.menu_price} "   , end =" ")
    
    def market_to_dict(self):
        return {"market_name":self.market_name, "kind":self.market_kind, "tel":self.market_tele, "sign" :self.market_sign, "score":self.market_score, "location":self.market_location, "menu_name":self.menu_name, "price" :self.menu_price ,"img_url":self.market_img}
        
#지도 접속
url = "https://map.naver.com"
#search => 투표결과 
search = "화곡동 김밥 맛집"
driver = wb.Chrome()
driver.get(url)
search_box = driver.find_element(By.CSS_SELECTOR, ".input_search")
search_box.send_keys(search)
search_box.send_keys(Keys.ENTER)
time.sleep(3)
#영업중 클릭
driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "#searchIframe"))
open_close = driver.find_element(By.CSS_SELECTOR, ".flicking-camera span+span a")
open_close.click()
time.sleep(3)
# 스토어 이름 엘리멘트들
market_names = driver.find_elements(By.CSS_SELECTOR, ".place_bluelink .TYaxT")
print(len(market_names))
print(market_names[0].text)
market_list = []
for market in market_names[:10]:  # Limit to first 5 stores\ #len(market_names)
    market_name = market.text # 식당이름 
    market.click()
    time.sleep(2)
    
    
    img_url_two = [] #2개 씩 
    price_two =[]
    menu_name_two = []

    
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "#entryIframe"))
    
    #가게 종류 
    try:
        kind = driver.find_element(By.CSS_SELECTOR, "#_title .lnJFt")
        menu_kind = kind.text
    except: #NoSuchElementException:
        menu_kind = "NULL"
    #장소
    try:
        location = driver.find_element(By.CSS_SELECTOR, ".vV_z_ .LDgIH")
        market_location = location.text
    except: #NoSuchElementException:
        market_location = "NULL"
    #전화번호
    try:    
        tele = driver.find_element(By.CSS_SELECTOR, ".vV_z_ .xlx7Q")
        market_tele = tele.text
    except: #NoSuchElementException:
        market_tele = "NULL"
    # 특이사항
    try:
        s = driver.find_element(By.CSS_SELECTOR, ".vV_z_ .xPvPE")
        market_sign = s.text
    except: #NoSuchElementException:
        market_sign = "NULL"
    # # 별점
    # try:
    #     sc = driver.find_element(By.CSS_SELECTOR, ".PXMot .place_blind")
    #     sc = driver.find_element(By.CSS_SELECTOR, ".PXMot")
    #     market_score = sc.text
    # except :#NoSuchElementException:
    #     market_score = "NULL"
    #     score_list = [item.replace("\n", ": ") if "NULL" not in item else item for item in market_score]
        # 별점
    try:
        sc = driver.find_element(By.CSS_SELECTOR, ".PXMot .place_blind")
        sc = driver.find_element(By.CSS_SELECTOR, ".PXMot")
        market_score = sc.text
    except : # NoSuchElementException:
        market_score = "NULL"
    market_score = market_score.replace("별점\n", "") if "NULL" not in market_score else market_score 
    
    
    try:#메뉴 클릭
        menu_elements = driver.find_elements(By.CLASS_NAME, "veBoZ")
        for element in menu_elements:
            if "메뉴" in element.text:
                element.click()
                break
                
        time.sleep(2)
        #이미지 엘리멘츠
        img_urls_1 = driver.find_elements(By.CLASS_NAME, "YBmM2") #1case
        img_urls_2 = driver.find_elements(By.CLASS_NAME, "img_box") #2case
        #가격 elements
        market_price_1 = driver.find_elements(By.CLASS_NAME, "price") #1case
        market_price_2 = driver.find_elements(By.CLASS_NAME, "GXS1X") #2case
        #메뉴 이름 elements
        menu_name_1 = driver.find_elements(By.CSS_SELECTOR, ".tit") #1case
        menu_name_2 = driver.find_elements(By.CSS_SELECTOR, ".lPzHi") #2case
        
        #이미지 넣기
        for img in img_urls_1[:2]:  # Limit to first 2 images
            if img:
                img_url_two.append(img.find_element(By.TAG_NAME, "img").get_attribute("src")) #1 case
        for img in img_urls_2[:2]: # Limit to first 2 images
            if img:
                img_url_two.append(img.find_element(By.TAG_NAME, "img").get_attribute("src")) #2 case
        if not img_url_two:
            img_url_two.append("NULL")
        #가격 넣기
        for price in market_price_1[:2]:  # Limit to first 2 images
            if price:
                price_two.append(price.find_element(By.TAG_NAME, "strong").text) #1 case
        for price in market_price_2[:2]: # Limit to first 2 images
            if price:
                price_two.append(price.find_element(By.TAG_NAME, "em").text) #2 case
        #메뉴이름 넣기
        for name in menu_name_1[:2]:  # Limit to first 2 images
            if name:
                menu_name_two.append(name.text) #1 case
                
        for name in menu_name_2[:2]: # Limit to first 2 images
            if name:
                menu_name_two.append(name.text) #2 case
        
        
        # menu_pic = driver.find_elements(By.CLASS_NAME, "YBmM2")
        # img_pic1 = menu_pic1[0].find_element(By.TAG_NAME, "img").get_attribute("src")
        # print(img_pic1)
    
    except Exception as e:
        print(f"Error downloading images for store : {e}")
    
    #데이터 전부 딕셔너리 타입으로 가공
    
    instance_market = Market_data(market_name,img_url_two,price_two,menu_name_two,menu_kind,market_tele,market_sign,market_score,market_location)
    instance_market.show_market()
    market_list.append(instance_market.market_to_dict()) #딕셔너리로 데이터 추가
        
    # img_url_list.append(img_url_two)
    # price_list.append(price_two)
    
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "#searchIframe"))
    #json 파일로 저장 
json_data3 = json.dumps(market_list,ensure_ascii=False)
with open("market.json","w") as writefile:
    json.dump(json_data3,writefile,indent = 4)
# #읽어오기
# with open("market.json","r") as file:
#     data = json.load(file)
# #데이터프레임으로 
# df = pd.read_json(data)
# df
