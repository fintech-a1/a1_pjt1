#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
import os

url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101'
FILE_NAME = 'stock.csv'
SCROLL_PAUSE_TIME = 0.5
flag = True

driver = webdriver.Chrome()

####################### crawling 위한 리스트 정의 #####################
code=[]    # 종목코드
name=[]    # 종목이름
market=[]    # 시장구분
sub=[]    # 소속부
end_price=[]    # 전일종가
rise_fall=[]    # 등락
rise_fall_rate=[]    #대비
start_price=[]    # 시가
high_price=[]    # 고가 
low_price=[]    #저가
trade_volume=[]    # 거래량
trade_balance=[]    # 거래액
market_cap=[]    # 시가총액
stock_listed=[]    # 주식 발행수
scroll_accum=0


#####################  List를 통해 Memory에 저장  #####################################

def load_to_memory (stock_data):
    
    global code;global name;global market;global sub; global end_price; global rise_fall; global rise_fall_rate; global start_price; global high_price; global low_price
    global trade_volume; global trade_balance; global market_cap; global stock_listed
    
    for stock in stock_data :
        code.append(stock.select('td')[0].text)   #종목코드
        name.append(stock.select('td')[1].text)    #종목명
        market.append(stock.select('td')[2].text)    #시장명
#         sub.apppend(stock.select('td')[3].text)    #소속부
        end_price.append(stock.select('td')[4].text)    #종가
        rise_fall.append(stock.select('td')[5].text)    #대비
        rise_fall_rate.append(stock.select('td')[6].text)    #등락률
        start_price.append(stock.select('td')[7].text)    #시가
        high_price.append(stock.select('td')[8].text)    #고가
        low_price.append(stock.select('td')[9].text)    #저가
        trade_volume.append(stock.select('td')[10].text)    #거래량
        trade_balance.append(stock.select('td')[11].text)    #거래대금
        market_cap.append(stock.select('td')[12].text)    #시가총액
        stock_listed.append(stock.select('td')[13].text)    #상장주식수
        
#####################  csv 파일로 저장   ##################################### 

def write_disk(flag, *param) :
    global FILE_NAME
    
    if flag :
        f = open(FILE_NAME,'w')
    else :
        f = open(FILE_NAME,'a')
        
    for i in param :
        f.write('{};'.format(i))
    f.write('\n')
    f.close
        
#####################  csv 파일에 쓸 준비  #####################################
        
def write_to_file(*param) :
    
    if len(param)==1 :
        global code;global name;global market;global sub; global end_price; global rise_fall; global rise_fall_rate; global start_price; global high_price; global low_price
        global trade_volume; global trade_balance; global market_cap; global stock_listed

        for i in range(param[0]) :
            write_disk(False,code[i],name[i],market[i],end_price[i],rise_fall[i],rise_fall_rate[i],start_price[i],                       high_price[i],low_price[i], trade_volume[i],trade_balance[i],market_cap[i],stock_listed[i])
    else :
        write_disk(True,'종목코드','종목명','시장구분','전일종가','등락폭','등락대비','시작가','고가','저가','거래량','거래액','시가총액','주식발행량')

        
#####################  변수들 flushing  #####################################        
        
def cleaning_memory() :
    global code;global name;global market;global sub; global end_price; global rise_fall; global rise_fall_rate; global start_price; global high_price; global low_price;
    global trade_volume; global trade_balance; global market_cap; global stock_listed
    
    code.clear();name.clear();market.clear();sub.clear();end_price.clear();rise_fall.clear();rise_fall_rate.clear();start_price.clear();high_price.clear();low_price.clear()
    trade_volume.clear();trade_balance.clear();market_cap.clear();stock_listed.clear()


#####################  main 시작  #####################################

driver.get(url)
date = input("검색하실 날짜를 yyyymmdd 형식으로 입력해주세요")

elem = driver.find_element_by_xpath('//*[@id="trdDd"]')

for _ in range(8) :
    elem.send_keys(Keys.BACKSPACE)
elem.send_keys(date)

driver.find_element_by_xpath('//*[@id="jsSearchButton"]').click()
time.sleep(2)


# ==========================스크롤 내리기=======================================================

gridlist=driver.find_element_by_class_name('CI-FREEZE-SCROLLER')

while True :
    if flag :
        driver.execute_script("arguments[0].scrollBy(0,1596)",gridlist) #처음엔 114/2 만큼 grid scroll
        scroll_accum+=1596
        write_to_file('first','time')
        flag = False
    else :
        driver.execute_script("arguments[0].scrollBy(0,3192)",gridlist)  # 두번째 114만큼
        scroll_accum+=3192
    
    if scroll_accum >=  driver.execute_script("return arguments[0].scrollHeight",gridlist) :    # scroll down 상태의 창 높이 저장 :
        break
        
    time.sleep(1)
# ========================== html parsing =======================================================    
    html = driver.page_source
    page_data = BeautifulSoup(html,'html.parser')
    stock_data = page_data.select('tbody.CI-GRID-BODY-TABLE-TBODY>tr')
    
    load_to_memory(stock_data)    # parsing data 에서 list로 변환
    write_to_file(len(stock_data))    # list를 csv 파일로 저장
    cleaning_memory()    # list 들을 초기화




# In[ ]:




