from pynput import mouse

SAVE_FILE = 'saved_boxes/box.txt'

val_to_position = {
	'x':[],
	'y':[],
	'z':[],
	'angle':[],
	'type':[]
}
key_list = list(val_to_position.keys())

inp_count = 0
inp_old = -1

def write_dict_to_file(dict):
	f = open(SAVE_FILE, 'w')
	f.write(str(dict))
	f.close()

def get_dict_from_file():
	f = open(SAVE_FILE, 'r')
	line = f.read()
	f.close()
	return eval(line)

def on_click(x, y, button, pressed):
	global inp_count, val_to_position
	point = (x, y)
	if button == mouse.Button.left:
		if pressed:
			val_to_position[key_list[inp_count]].append(point)
		else:
			val_to_position[key_list[inp_count]].append(point)
			inp_count += 1
			ask_input()
	elif button == mouse.Button.middle:
		
		return False

def ask_input():
	global inp_count
	if inp_count == len(key_list):
		print('All done, press middle mouse button')
	else:
		print("Enter box for " + key_list[inp_count])


def detect_boxes():
	listener = mouse.Listener(on_click=on_click)
	listener.start()
	ask_input()
	listener.join()
