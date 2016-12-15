import scrapy
import automotive.helper_functions as func
import automotive.left_lane as ln
import automotive.both as websites
from automotive.items import AutomotiveItem
from automotive.urls import urls

class Automotive(scrapy.Spider):
	name = "automotive"
	start_urls = urls

# Car and Driver Make and Models
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
				yield websites.get_url(car, more_data_link, self.get_car_data)

# Car and driver specific car page
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

		left_lane_models = 'http://www.leftlanenews.com/new-car-buying/' + websites.space_to_dash(car['make']) + '/'
		yield websites.get_url(car, left_lane_models, self.left_lane_makes)

# Left lane Make and Models
	def left_lane_makes(self, response):
		car = response.meta['car']
		models = response.css('ul.car_list > li')
		ln_car_link = ln.find_model(car['model'], models)
		if ln_car_link == None:
			yield car
		else:
			yield websites.get_url(car, ln_car_link, self.ln_model)

# Left Lane Specfic car page
	def ln_model(self, response):
		car = response.meta['car']
		links = {}
		links['images'] = response.css('div.large_image > div.left > a::attr(href)').extract_first()
		links['specs'] = response.css('li#overview-tab + li > a::attr(href)').extract_first()
		car['links'] = links 
		if links['images'] == None:
			yield car
		else:
			yield websites.get_url(car, links['images'], self.ln_images)

		
# Left Lane Specific Car Images
	def ln_images(self, response):
		car = response.meta['car']
# Handle Count
		if response.meta.get('count'):
			count = response.meta['count']
		else:
			count = 0

		if count > 4:
			if car['links']['specs'] == None:
				yield car
			else:
				yield websites.get_url(car, car['links']['specs'],self.ln_specs)
		else:
			car['images'] = ln.get_image(response)
			next_image = response.css('div.image-button > a + a::attr(href)').extract_first()
			yield websites.get_url(car, next_image, self.ln_images, count)

# Get Leftlane Specs
	def ln_specs(self, response):
		car = response.meta['car']
		style = websites.strip_str(scrapy.Selector(response=response).xpath('//*[@id="Body Style"]/text()').extract_first())
		car['ln_type'] = style
		return car







