import re
import pytesseract
import numpy as np
from PIL import Image, ImageGrab

def extract_location(text):
	# Remove non numerics
	text = text.replace("[^0-9.]", "")

	# Replace comma with period
	text = text.replace(',', '.')

	# Attempt
	try:
		return float(text)
	except:
		return None

# Special function to extract the angle
def extract_angle(text):
	# Split by parenthesis
	splt = text.split('(')
	if len(splt) != 3:
		return None
	
	# Only want angle part
	angle_text = splt[-1]

	# Remove non numerics
	angle_text = angle_text.replace("[^0-9.]", "")
	angle_text = angle_text.replace(")", "")
	
	# Replace comma with period
	angle_text = angle_text.replace(',', '.')
	horiz, vert = angle_text.split('%')

	# Attempt
	try:
		horiz = float(horiz)
		vert  = float(vert)
		return horiz, vert
	except:
		return None
	
# Now we need to process the image 
def pixelwise_func(pixel): 
	r, g, b = pixel
	#Check if text
	if int(0.2989 * r + 0.5870 * g + 0.1140 * b) < 150:
		return 0
	else:
		#Else, return grayscale
		return int(0.2989 * r + 0.5870 * g + 0.1140 * b)

def process_image(img):
	#Update each pixel via the pixelwise_func
	cols, rows = img.size 
	new_cols, new_rows = cols * 2, rows * 4
	im_arr = np.array(img)
	new_img = np.zeros((new_rows, new_cols), dtype=np.uint8)
	for r in range(rows):
		for c in range(cols):
			new_img[r][c] = pixelwise_func(im_arr[r][c])
	
	new_img = np.roll(new_img, (new_rows//2 - rows//2), axis=0)
	new_img = np.roll(new_img, (new_cols//2 - cols//2), axis=1)

	return Image.fromarray(new_img)

def get_values(vals, val_dict, print_output=False):
	prnt_str = ''
	ret_lst = []
	for val in vals:
		# Get x1, y1, x2, y2
		pairs = val_dict[val]  
		# Grab the area of the screen
		image = screenGrab(pairs)
		image = process_image(image)
		# OCR the image
		text  = pytesseract.image_to_string(image, lang='mc')
		# IF the OCR found anything, print it
		text = text.strip()
		if len(text) > 0:
			if val == 'angle':
				ret = extract_angle(text)
				if ret == None:
					# Try again
					return get_values(vals, val_dict, print_output)
				else:
					h, v = ret
					prnt_str += f'Horizontal - {h}:\tVertical - {v}\n'
					ret_lst.append(ret)
			elif val == 'x' or val == 'y' or val == 'z':
				flt = extract_location(text)
				if flt is not None:
					prnt_str += f'{val}: {flt}'
					ret_lst.append(flt)
				else:
					# Try again
					return get_values(vals, val_dict, print_output)
		else:
			# Try again
			return get_values(vals, val_dict, print_output)
	
	if print_output:
		print(prnt_str)

	return ret_lst

def screenGrab(pairs):
	x1, y1 = pairs[0]
	x2, y2 = pairs[1]
	image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
	return image