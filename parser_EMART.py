# Parser (CU, EMART24, GS25, Ministop, SevenEleven) 버전을 전부 합쳐서 model 에 일괄 올리는 작업을 할 예정임.
#TODO: Parser 를 최종 완성하고 나서 적은 양의 페이지만 불러오도롱 세팅해놓았던것을 전체 페이지를 로드하게 하고 최종 확인 해보기!!

from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedExceptionpython
from selenium.common.exceptions import StaleElementReferenceException
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bogo.settings')
import django
django.setup()

from conv.models import Product2

import platform

# Chrome 창을 띄우지 않고(headless 하게) driver 를 사용하기 위한 options 변수 선언 및 설정 그리고 driver 선언
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("--disable-gpu")
if "Darwin" in platform.system():
    driver = webdriver.Chrome('C:\chromedriver',options=options)
else:
    driver = webdriver.Chrome('C:\chromedriver',options=options)
driver.implicitly_wait(3)


def emart_parser():
    # Emart 페이지에 driver를 접속시킨다.
    driver.get('https://www.emart24.co.kr/product/eventProduct.asp')
    num = 1
    col = 0
    prod_list = []
    while 1:
        try:
            while num < 16:
                prod_input = []
                print("emart parsing")
                print(num)
                prod_input.append(driver.find_element_by_css_selector(
                    '#regForm > div.section > div.eventProduct > div.tabContArea > ul > li:nth-child(%s) > div > p.productDiv' % num).text)
                prod_input.append(driver.find_element_by_css_selector(
                    '#regForm > div.section > div.eventProduct > div.tabContArea > ul > li:nth-child(%s) > div > p.price' % num).text)
                try:
                    prod_input.append(driver.find_element_by_css_selector(
                        '#regForm > div.section > div.eventProduct > div.tabContArea > ul > li:nth-child(%s) > div > p.productImg' % num).find_element_by_tag_name(
                        'img').get_attribute('src'))
                except NoSuchElementException:
                    pass

                prod_input[1] = prod_input[1].replace(',', '')
                prod_input[1] = prod_input[1].replace(' 원', '')

                if '→' in prod_input[1]:
                    prod_input[1] = prod_input[1].replace('→ ', '')
                    prod_input[1] = prod_input[1].split(' ')[1]

                eventtype = driver.find_element_by_xpath(
                    '//*[@id="regForm"]/div[2]/div[3]/div[2]/ul/li[%s]/div/div/p/img' % num).get_attribute('alt')
                print(eventtype)
                if '2 + 1 뱃지' in eventtype:
                    eventtype = '2+1'
                elif 'SALE 뱃지' in eventtype:
                    eventtype = 'sale'
                elif 'X2 더블 뱃지' in eventtype:
                    eventtype = 'dum'
                elif '1 + 1 뱃지 이미지' in eventtype:
                    eventtype = '1+1'
                elif '3 + 1 뱃지' in eventtype:
                    eventtype = '3+1'
                else:
                    eventtype = 'error!'
                prod_input.append(eventtype)
                prod_list.append(prod_input)
                num += 1
                if num is 16:
                    col += 1
                    num = 1
                    driver.find_element_by_css_selector(
                        '#regForm > div.section > div.eventProduct > div.paging > a.next.bgNone').click()
        except NoSuchElementException:
            print("파싱종료")
            break
        except StaleElementReferenceException:
            time.sleep(0.5)
        except ElementClickInterceptedException:
            time.sleep(1)
    return prod_list

if __name__ == '__main__':
    parsed_data = emart_parser()
    for data in parsed_data:
        Product2(prodName=data[0], prodPrice=data[1], prodImg=data[2], prodEventType=data[3]).save()
                