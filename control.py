from operator import ge
from image_utils import *
import time
import pyautogui

TICKS_PER_DEG = 8
# Optimal mining angle (vertical)
MINING_ANGLE = 35

def set_angles(h, v, win, pos_dict, xc=968, yc=539):
	kp1 = TICKS_PER_DEG
	kp2 = TICKS_PER_DEG

	for _ in range(10):
		both = get_values(['angle'], pos_dict)[0]
		if both is not None:
			if h == None:
				h = both[0]
			if v == None:
				v = both[1] 
			err1 = both[0] - h
			err2 = both[1] - v

			if err1 > 180:
				err1 -= 360
			elif err1 < -180:
				err1 += 360

			if err2 > 180:
				err2 -= 360
			elif err2 < -180:
				err2 += 360

			if abs(err1) <= 3 and abs(err2) <= 3:
				break 

			resp1 = kp1 * err1
			resp2 = kp2 * err2

			win.move_mouse_input((xc - int(resp1), yc), absolute=False)
			win.move_mouse_input((xc, yc - int(resp2)), absolute=False)

def set_mining_angle(win, pos_dict, xc=968, yc=539):
	both = get_values(['angle'], pos_dict)[0]
	while both is None:
		both = get_values(['angle'], pos_dict)[0]
	
	set_angles(both[0], MINING_ANGLE, win, pos_dict, xc, yc)


def turn(turn_type, win, pos_dict, xc=968, yc=539):
	angle = 0
	if turn_type == 'right':
		angle = 90
	elif turn_type == 'left':
		angle = -90
	elif turn_type == '180':
		angle = 180

	# First find current direction
	both = get_values(['angle'], pos_dict)[0]
	while both is None:
		both = get_values(['angle'], pos_dict)[0]
	h = both[0]
	v = both[1]
	target_h = h + angle
	if target_h > 180:
		target_h -= 360
	elif target_h < -180:
		target_h += 360
	if   -45 <= target_h and target_h <= 45:
		target_h = 0
	elif  45 <= target_h and target_h <= 135:
		target_h = 90
	elif 135 <= target_h and target_h <= 180:
		target_h = 180
	elif -180 <= target_h and target_h <= -135:
		target_h = -180
	elif -135 <= target_h and target_h <= -45:
		target_h = -90
	
	if turn_type == 'right':
		target_h -= 5
	elif turn_type == 'left':
		target_h += 5

	set_angles(target_h, v, win, pos_dict, xc, yc)

def move_feadback(n, win, pos_dict):
	# Get start values
	start_x, start_z = get_values(['x', 'z'], pos_dict)

	# Get start angles for direction purposes
	both = get_values(['angle'], pos_dict)[0]
	h, _ = both

	# Determine which direction we want to go in
	x_dir = 0
	z_dir = 0
	rads = np.pi * h / 180.0
	horiz, vert = np.cos(rads), np.sin(rads)
	if abs(horiz) > abs(vert):
		if horiz > 0:
			z_dir = 1
		else:
			z_dir = -1
		start = start_z
	else:
		if vert > 0:
			x_dir = 1
		else:
			x_dir = -1
		start = start_x
	pos = start
	
	# Main loop
	while int(abs(pos - start)) != n:
		if x_dir != 0:
			pos = get_values(['x'], pos_dict)[0]
			if x_dir * (pos - start) < n:
				win.type_keys('{w down}')
				win.type_keys('{w up}')
			else:
				win.type_keys('{s down}')
				win.type_keys('{s up}')
		elif z_dir != 0:
			pos = get_values(['z'], pos_dict)[0]
			if z_dir * (pos - start) < n:
				win.type_keys('{w down}')
				win.type_keys('{w up}')
			else:
				win.type_keys('{s down}')
				win.type_keys('{s up}')
		print(start, pos)

	win.type_keys('{w up}')
	win.type_keys('{s up}')
		
	

def move(num_blocks, win):
	win.type_keys('{w down}')
	time.sleep(num_blocks)
	win.type_keys('{w up}')

def set_torch(toolbar, win, pos_dict, xc=968, yc=539):
	# First, search for torch if it exists
	orig_ind = toolbar[-1]
	torch_ind = 0
	for i, tool in enumerate(toolbar[:-1]):
		if tool == 'torch':
			torch_ind = i + 1
	if torch_ind == 0:
		print('No torch in toolbar')
		return False

	# Find current state
	both = get_values(['angle'], pos_dict)[0]
	while both is None:
		both = get_values(['angle'], pos_dict)[0]

	# Next we need to look at the floor and then right click
	set_angles(None, 90, win, pos_dict, xc, yc)

	# Activate toolbar
	win.type_keys(f'{{{torch_ind} down}}')
	win.type_keys(f'{{{torch_ind} up}}')

	# Right click torch
	pyautogui.mouseDown(button='right')
	pyautogui.mouseUp(button='right')

	# Go back to old position 
	set_angles(None, both[1], win, pos_dict, xc, yc)

	# Keep orgininal toolbar item
	win.type_keys(f'{{{orig_ind} down}}')
	win.type_keys(f'{{{orig_ind} up}}')



	
