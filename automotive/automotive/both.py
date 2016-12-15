import scrapy

def get_url(car, link, callback, count=None):
	if not link:
		return None

	request = scrapy.Request(link, callback=callback, dont_filter=True)
	request.meta['car'] = car
	if count != None:
		request.meta['count'] = count + 1
	return request


# Removes excess spaces from string 
def strip_str(change):
	if isinstance(change, str):
		return change.strip()
	else:
		return None

# Replace spaces with dashes
def space_to_dash(change):
	if isinstance(change, str):
		change = change.strip()
		change = change.replace(' ', '-')
		change = change.lower()
		return change
	else:
		return None