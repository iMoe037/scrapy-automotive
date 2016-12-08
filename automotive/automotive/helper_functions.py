import string
# Functions for converting HTML data

# Gets the right paragraph for additonal car spec info from caranddriver.com
def get_paragraph(title, list_paragraphs):
	for paragraph in list_paragraphs:
		bold_text = paragraph.css("b::text").extract_first()

		if isinstance(bold_text, str):
			bold_text = bold_text.strip()
			if bold_text == title:
				return paragraph

	return None

# Formats the paragraph properly for Vehicle type, engine, and transmission
def format_paragraph(title, list_paragraphs):
	if list_paragraphs == None:
		return None

	paragraph = get_paragraph(title, list_paragraphs)

	if paragraph == None:
		return None

	return paragraph.css("::text").extract()[1]

# Creates an object for Dimensions
def parse_dimensions(list_paragraphs):
	if list_paragraphs == None:
		return None

	paragraph = get_paragraph('DIMENSIONS:', list_paragraphs)

	if paragraph == None:
		return None

	paragraph = paragraph.css("::text").extract()
	paragraph = paragraph[1:]

	obj = {}
	previous_key = ''

	for idx, key in enumerate(paragraph):
		if idx % 2 == 0:
			previous_key = key[0:len(key) - 1]
		else:
			obj[previous_key] = key

	return obj

# Joins Displacement Paragraph into a string
def parse_displacement(list_paragraphs):
	if list_paragraphs == None:
		return None

	paragraph = get_paragraph('Displacement:', list_paragraphs)

	if paragraph == None:
		return None

	paragraph = paragraph.css("::text").extract()

	displacement = []
	displacement.append(paragraph[1])
	paragraph = paragraph[2:]

	for i in range(0,len(paragraph),2):
		displacement.append(paragraph[i] + paragraph[i+1])

	return displacement

# Converts a string of highway and city gas mileage to seperate ints
def get_epa(area, city_highway_epa):
	if city_highway_epa == None:
		return None

	city_or_highway = city_highway_epa.split("/")
	return city_or_highway[0] if area == "city" else city_or_highway[1]

# Converts $ string into an int
def convert_price(price):
	if price == None:
		return None

	for char in string.punctuation:
		price = price.replace(char,"")

	return int(price)

# Checks if image is contained in link or not for main image extraction
def image_link(resp):
	within_link = resp.css("div.model-image > a > img::attr(src)").extract_first()
	without_link = resp.css("div.model-image > img::attr(src)").extract_first()
	if within_link == None and without_link == None:
		return None
	elif within_link != None:
		return within_link
	else:
		return without_link

# Removes 'Rank in ' from Car and driver vehicle type
def car_driver_type(car_type):
	if car_type == None:
		return None
	else:
		return car_type[8:]


