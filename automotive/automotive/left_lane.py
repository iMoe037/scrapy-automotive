# Functions for Left Lane News
import automotive.both as websites

# Convert make or model name case for links
def string_link(make_model):
	if make_model == None:
		return None
	else:
		make_model = make_model.strip()
		make_model = make_model.replace(' ', '-')
		make_model = make_model.lower()
		return make_model

def find_model(model_name, model_list):
	if model_list == None:
		return None

	cd_model = rem_words(model_name)
	for model in model_list:
		ln_model = model.css('a::attr(title)').extract_first()
		ln_model = websites.strip_str(ln_model)
		ln_model = rem_words(ln_model)

		if ln_model != None and ln_model == cd_model: 
			return model.css('a::attr(href)').extract_first()

	return None

# Get Models from variable
def get_models(make):
	make = string_link(make)
	if make in makes:
		return makes[make]

	return False

# Gets the make model link
def get_link(make, model, link):
	make = string_link(make)
	model = string_link(model)

	if make in makes:
		if model in makes[make]:
			if link == 'model_link':
				return makes[make][model]['model_link']
			elif link == 'image':
				return makes[make][model]['images']
			elif link == 'spec':
				return makes[make][model]['spec']

	return None

# Stores image and spec link
def store_link(make, model, link_type, link):
	make = string_link(make)
	model = string_link(model)

	if make in makes:
		if model in makes[make]:
			makes[make][model][link_type] = link

# Get car images
def get_image(response):

	car = response.meta['car']
	if not car.get('images'):
		car['images'] = []
	image = response.css('img.large::attr(src)').extract_first()
	if image != None:
		image = 'http:' + image
		car['images'].append(image)
		return car['images']
	else:
		return None

# Removes some words from leftlane car names
def rem_words(name):
	if isinstance(name, str):
		name = name.lower()
		name = name.replace('sedan', '')
		return name.strip()
	else:
		return None

