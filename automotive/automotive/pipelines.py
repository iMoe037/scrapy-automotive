# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AutomotivePipeline(object):
	def process_item(self, item, spider):
		for key in item:
			if item[key] == None:
				item[key] = 'N/A'
			elif key == 'rating':
				item[key] = self.convert_rating(item['rating'])
			elif isinstance(item[key], str):
				item[key] = item[key].strip()
		return item

	def convert_rating(self, rating):
		return float(''.join(filter(lambda x: x.isdigit(), rating))) * .05
