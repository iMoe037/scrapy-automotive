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

# Check if leftlane version of car exists
		models = ln.get_models(car['make'])
		if(models):
			to_model = ln.get_link(car['make'], car['model'])
			if to_model  == None:
				yield
			else:
				yield websites.get_url(car, to_model, self.left_lane_model)
		else:
			left_lane_models = 'http://www.leftlanenews.com/new-car-buying/' + car['make'].lower() + '/'
			yield websites.get_url(car, left_lane_models, self.left_lane_makes)

# Left lane Make and Models
	def left_lane_makes(self, response):
		car = response.meta['car']
		models = response.css('ul.car_list > li')
		ln.add_make_models(car['make'], models)
		to_model = ln.get_link(car['make'], car['model'])
		if to_model  == None:
			yield
		else:
			yield websites.get_url(car, to_model, self.left_lane_model)
		

# Left Lane Specific car page
	def left_lane_model(self,response):
		car = response.meta['car']
		img_link = response.css('div.large_image > div.left > a::attr(href)').extract_first()
		yield websites.get_url(car, img_link, self.left_lane_images)

# Left Lane Images
	def left_lane_images(self, response):
		car = response.meta['car']
		if response.meta.get('count'):
			count = response.meta['count']
			if count > 3:
				print('Done')
				return car

		car = response.meta['car']
		if not car.get('images'):
			car['images'] = []
		image = response.css('img.large::attr(src)').extract_first()
		if image != None:
			if response.meta.get('count'):
				count = response.meta['count']
			else:
				count = 0
			image = 'http:' + image
			car['images'].append(image)
			next_image = response.css('div.image-button > a + a::attr(href)').extract_first()
			return websites.get_url(car,next_image, self.left_lane_images, count)






