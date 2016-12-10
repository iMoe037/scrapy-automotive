import scrapy

def get_url(car, link, callback, count=None):
	request = scrapy.Request(link, callback=callback, dont_filter=True)
	request.meta['car'] = car
	if count != None:
		request.meta['count'] = count + 1
	return request