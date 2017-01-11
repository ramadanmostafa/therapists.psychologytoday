# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TherapistsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Profile_Link = scrapy.Field()
    Website = scrapy.Field()
    Image = scrapy.Field()
    name = scrapy.Field()
	title  = scrapy.Field()
    Verified = scrapy.Field()
    Business_Name = scrapy.Field()
    Address = scrapy.Field()
    Suite = scrapy.Field()
    City = scrapy.Field()
    State = scrapy.Field()
    zip_code = scrapy.Field()
    phone_number = scrapy.Field()
    specialties = scrapy.Field()#list
    Years_in_Practice = scrapy.Field()
    School = scrapy.Field()
    Graduated = scrapy.Field()
    License_No_and_State = scrapy.Field()
    Avg_Cost_per_session = scrapy.Field()
    Sliding_Scale = scrapy.Field()
    Payment_Methods1 = scrapy.Field()
    Accepted_Insurance_Plans = scrapy.Field()
    Issues = scrapy.Field()#list
    Religious_Orientation = scrapy.Field()
    Age = scrapy.Field()#list
    Treatment_Orientation = scrapy.Field()#list
    Modality = scrapy.Field()#list
