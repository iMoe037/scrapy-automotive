# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutomotiveItem(scrapy.Item):
	make = scrapy.Field()
	model = scrapy.Field()
	msrp = scrapy.Field()
	price = scrapy.Field()
	vehicle_type = scrapy.Field()
	vehicle_type_more = scrapy.Field()
	engine = scrapy.Field()
	displacement = scrapy.Field()
	transmission = scrapy.Field()
	dimensions = scrapy.Field()
	img_url = scrapy.Field()
	images = scrapy.Field()
	summary = scrapy.Field()
	overview = scrapy.Field()
	rating = scrapy.Field()
	city_epa = scrapy.Field()
	highway_epa = scrapy.Field()
	zero_sixty = scrapy.Field()
	hp = scrapy.Field()
	top_speed = scrapy.Field()
	ln_type = scrapy.Field()
	links = scrapy.Field()
	pass