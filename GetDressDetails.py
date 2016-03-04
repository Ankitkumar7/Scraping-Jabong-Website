# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 23:18:33 2016


"""

# -*- coding: utf-8 -*-


"""
Spyder Editor

Author: Ankit
Date: 1st March 2016 9:30 GMT
"""
from bs4 import BeautifulSoup
import requests
import random

class PageDetails:
    
    def __init__(self):
        self.soup = str()
        self.urls = 0     
        
    def get_urls(self,file_name):
        fh = open(file_name)
        self.urls = []
        for line in fh:
            line = line.strip()
            start = line.find("http")
            self.urls.append(line[start:])
        
    def get_soup(self, url):
        webpage = url
        try:
            response = requests.get(webpage)
            self.soup = BeautifulSoup(response.text,"html.parser")
        except Exception as badEggs:
            print("Some Really Bad Eggs of type:", type(badEggs),badEggs)
        
    def get_cloth_description(self):
        tags = self.soup.find_all("ul","prod-main-wrapper")
        tag = tags[0]
        children = []
        for child in tag:
            children.append(child)
        children.pop()
        self.description = {}
        
        for label in children:
            tags = []
            for tag in label:
                tags.append(tag)
            description_key = tags[0].contents[0]
            description_value = tags[1].contents[0]
            self.description[description_key] = description_value
        
    
    def get_other_details(self):
            self.details = dict()
            brand = self.soup.find("span","brand")
            brand_name = brand.string
            self.details['brand'] = brand_name
            price = self.soup.find("span","actual-price")
            price = price.string
            self.details["price"] = price
            title = self.soup.find("span","product-title")
            title = title.string
            self.details['title'] = title
            product_img_tags = self.soup.find_all("div","col-xs-12 col-sm-12 col-md-8 product-image")
            target_soup = BeautifulSoup(str(product_img_tags),"html.parser") 
            img_tags = target_soup.find_all("img")
            img_dict = dict()
            slide_num = 1
            for tag in img_tags:
                item = tag.attrs
                for key in item.keys():
                    if("data-src" not in str(key)):
                        del item[key]
                img_dict["slide-"+str(slide_num)] = item
                slide_num += 1
            self.details['img_urls'] = img_dict
            
    def get_page_info(self):
        self.get_cloth_description()
        self.get_other_details()
        info = self.description
        info['details'] = self.details
        return info
            
        
        
if __name__ == "__main__":
    pages_info = []
    for i in range(1000):
        obj = PageDetails()
        obj.get_urls("urls.txt")
        random_num = random.randint(1,len(obj.urls))
        obj.get_soup(obj.urls[random_num])
        info = obj.get_page_info()
        pages_info.append(info)
        print info['Types']
