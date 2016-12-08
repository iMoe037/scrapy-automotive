import scrapy
import automotive.helper_functions as func
from automotive.items import AutomotiveItem
from automotive.urls import urls

class Automotive(scrapy.Spider):
	name = "automotive"
	start_urls = urls

	def parse(self, response):
		models = scrapy.Selector(response).xpath('//*[@id="make-list"]/li')
		for model in models:
			if(model.css("div.mobile-ad").extract_first() == None):
				car = AutomotiveItem()
				car['make'] = response.css("h1.make-name::text").extract_first()
				car['model'] = model.css("a > div.list-container > h3.list-title::text").extract_first()
				car['msrp'] = model.css("a > div.list-container > div::text").extract_first()
				car['overview'] = model.css("div.overviewContainer::text").extract_first()
				more_data_link = 'http://www.caranddriver.com/' + model.css("a::attr(href)").extract_first()
				request = scrapy.Request(more_data_link, callback=self.get_car_data)
				request.meta['car'] = car
				yield request

	def get_car_data(self, response):
		car = response.meta['car']
		car['img_url'] = func.image_link(response)
		car['summary'] = response.css('div.performance-data--overview::text').extract_first()
		car['price'] = func.convert_price(response.css('span.msrp-price::text').extract_first())
		car['rating'] = response.css('div.cad-rating-stars::attr(style)').extract_first()
		car['city_epa'] = func.get_epa('city', response.css('i.irg-epa-icon + span.data-value::text').extract_first())
		car['highway_epa'] = func.get_epa('highway', response.css('i.irg-epa-icon + span.data-value::text').extract_first())
		car['zero_sixty'] = response.css('i.irg-zero-sixty-icon + span.data-value::text').extract_first()
		car['hp'] = response.css('i.irg-hp-icon + span.data-value::text').extract_first()
		car['top_speed'] = response.css('i.irg-top-speed-icon + span.data-value::text').extract_first()
		car['vehicle_type'] = func.car_driver_type(response.css('h4.intro::text').extract_first())

		verdict_box = response.css('div#verdict_box > div > p')
		car['vehicle_type_more'] = func.format_paragraph('VEHICLE TYPE:', verdict_box)
		car['engine'] = func.format_paragraph('ENGINE TYPE:', verdict_box)
		car['displacement'] = func.parse_displacement(verdict_box)
		car['transmission'] = func.format_paragraph('TRANSMISSION:', verdict_box)
		car['dimensions'] = func.parse_dimensions(verdict_box)
		return car

