# -*- coding: utf-8 -*-
import scrapy
from ..items import TherapistsItem
from w3lib.html import remove_tags

class TherapistsProfilesSpider(scrapy.Spider):
    name = "therapists_profiles"
    allowed_domains = ["therapists.psychologytoday.com"]
    start_urls = (
        'https://therapists.psychologytoday.com/',
    )

    def parse(self, response):
        stats_urls = response.xpath('//*[@id="searchStatesCities"]/div/div[3]/div/ul/li/a/@href').extract()
        for url in stats_urls[:1]:
            yield scrapy.Request(response.urljoin(url), self.parse_state)

    def parse_state(self, response):
        therapists_prof_urls = response.xpath('//*[@id="results-page"]/div[4]/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/a/@href').extract()
        next_page = response.xpath('//*[@id="results-page"]/div[5]/div/div[2]/div/a[1]/@href').extract()

        for url in therapists_prof_urls[:1]:
            yield scrapy.Request(response.urljoin(url), self.parse_therapists_prof)

        # for url in next_page[:1]:
        #     yield scrapy.Request(response.urljoin(url), self.parse_state)

    def parse_therapists_prof(self, response):
        item = TherapistsItem()
        item["Profile_Link"] = response.url
        item["Website"] = response.xpath('//*[@id="profileContainer"]/div[2]/div[1]/div/a[2]/@href').extract()
        item["Image"] = response.xpath('//*[@id="profilePhoto"]/img/@src').extract_first()
        item["name"] = response.xpath('//*[@id="profileContainer"]/div[2]/div[2]/div[1]/div[1]/h1/text()').extract_first().strip()
    	item["title"]  = ' '.join(remove_tags(response.xpath('//*[@id="profileContainer"]/div[2]/div[2]/div[1]/div[1]/div/h2').extract_first()).split())
        try:
            item["verified"] = remove_tags(response.xpath('//*[@id="profileContainer"]/div[2]/div[3]/div/div/div/div/div').extract_first()).strip()
        except:
            item["verified"] = ""
        location = filter(None, map(unicode.strip, remove_tags(response.xpath('//*[@id="profile-content"]/div/div[2]/div[1]/div/div/div[1]').extract_first()).split('\n')))
        item["Business_Name"] = location[0]
        item["Address"] = location[1]
        item["Suite"] = location[2]
        item["City"] = location[3]
        item["State"] = location[4]
        item["zip_code"] = location[5]
        item["phone_number"] = location[6]
        item["specialties"] =  response.xpath('//*[@id="profile-content"]/div/div[2]/div[2]/div[1]/div/ul/li/text()').extract()#list
        qualifications = filter(None, map(unicode.strip, remove_tags(response.xpath('//*[@id="profile-content"]/div/div[1]/div[4]/ul').extract_first()).split('\n')))
        for index in range(len(qualifications)):
            if ":" in qualifications[index]:
                if "Years in Practice:" == qualifications[index]:
                    item["Years_in_Practice"] = qualifications[index + 1]
                elif "School:" == qualifications[index]:
                    item["School"] = qualifications[index + 1]
                elif "Year Graduated:" == qualifications[index]:
                    item["Graduated"] = qualifications[index + 1]
                elif "License No. and State:" == qualifications[index]:
                    item["License_No_and_State"] = qualifications[index + 1]

        item["Avg_Cost_per_session"] = response.xpath('//*[@id="profile-content"]/div/div[1]/div[5]/ul/li[1]/text()').extract()[1].strip()
        item["Sliding_Scale"] = response.xpath('//*[@id="profile-content"]/div/div[1]/div[5]/ul/li[2]/text()').extract()[1].strip()
        item["Payment_Methods1"] = response.xpath('//*[@id="profile-content"]/div/div[1]/div[5]/ul/li[3]/text()').extract()[1].strip().replace('  ', '')
        try:
            item["Accepted_Insurance_Plans"] = ' '.join(remove_tags(response.xpath('//*[@id="profile-content"]/div/div[1]/div[5]/div[1]').extract_first()).split())
        except:
            pass
        item["Issues"] =  filter(None, map(unicode.strip, remove_tags(response.xpath('//*[@id="profile-content"]/div/div[2]/div[2]/div[2]').extract_first()).split('\n')))#list

        focus = filter(None, map(unicode.strip, remove_tags(response.xpath('//*[@id="profile-content"]/div/div[2]/div[3]').extract_first()).split('\n')))
        if "Religious Orientation:" in focus:
            item["Religious_Orientation"] = focus[focus.index("Religious Orientation:") + 1]
        if "Age" in focus:
            item["Age"] =  focus[focus.index("Age") + 1:]

        item["Treatment_Orientation"] = filter(None, map(unicode.strip, remove_tags(response.xpath('//*[@id="profile-content"]/div/div[2]/div[4]/div[1]').extract_first()).split('\n')))#list
        item["Modality"] =  filter(None, map(unicode.strip, remove_tags(response.xpath('//*[@id="profile-content"]/div/div[2]/div[4]/div[2]').extract_first()).split('\n')))

        yield item
