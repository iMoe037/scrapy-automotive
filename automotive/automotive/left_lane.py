# Functions for Left Lane News

# Only Global var for now
makes = {}

# Convert make or model name case for links
def string_link(make_model):
	if make_model == None:
		return None
	else:
		make_model = make_model.strip()
		make_model = make_model.replace(' ', '-')
		make_model = make_model.lower()
		return make_model

# Adds to make and models global var used so we don't have to recrawl leftnews
def add_make_models(make, model_list):
	if model_list == None:
		return None

	if make in makes:
		print('%s shouldn\'t exist in makes yet')
	else:
		make = string_link(make)
		makes[make] = {}
		for model in model_list:
			name = model.css('a::attr(title)').extract_first()

			if name == None:
				return None
			else:
				name = string_link(name)
				makes[make][name] = model.css('a::attr(href)').extract_first()

# Get Models from variable
def get_models(make):
	make = string_link(make)
	if make in makes:
		return makes[make]

	return False

# Gets the make model link
def get_link(make, model):
	make = string_link(make)
	model = string_link(model)

	if make in makes:
		if model in makes[make]:
			return makes[make][model]

	return None

