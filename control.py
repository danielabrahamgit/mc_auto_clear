from operator import ge
from re import T
from tkinter.constants import W
from image_utils import *
import time
import pyautogui

TICKS_PER_DEG = 8
MINING_ANGLE = 33
WALKING_SPEED = 4.317

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

			if abs(err1) <= 2 and abs(err2) <= 2:
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
		target_h -= 2
	elif turn_type == 'left':
		target_h += 2

	set_angles(target_h, v, win, pos_dict, xc, yc)

def move_feedback(n, win, pos_dict, mining=False):
	# Get start values
	pair = get_values(['x', 'z'], pos_dict)
	while pair[0] is None or pair[1] is None:
		pair = get_values(['x', 'z'], pos_dict)
	start_x, start_z = pair

	# Get start angles for direction purposes
	both = get_values(['angle'], pos_dict)[0]
	while both is None:
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
			target = start_z + n
		else:
			z_dir = -1
			target = start_z - n
		pos = start_z
	else:
		if vert < 0:
			x_dir = 1
			target = start_x + n
		else:
			x_dir = -1
			target = start_x - n
		pos = start_x
	target = round(target * 2) / 2.0
	
	hitting = False
	t_sec = 1
	prev_pos = pos
	# Feedback controller
	while pos is None or abs(pos - target) > 0.2:
		if pos is not None:
			t_sec = abs(pos - target) / WALKING_SPEED
			prev_pos = pos
		else:
			pos = prev_pos
		if not hitting and mining:
				pyautogui.mouseDown(button='left')
				hitting = True
		if x_dir != 0 and pos is not None:
			if x_dir * (pos - target) < 0:
				move_forward(t_sec=t_sec, win=win)
			else:
				move_backward(t_sec=t_sec, win=win)
			pos = get_values(['x'], pos_dict)[0]
		elif z_dir != 0:
			if z_dir * (pos - target) < 0:
				move_forward(t_sec=t_sec, win=win)
			else:
				move_backward(t_sec=t_sec, win=win)
			pos = get_values(['z'], pos_dict)[0]
	
		if hitting and pos is not None and abs(pos - target) <= 0.2:
			pyautogui.mouseUp(button='left')
				
def move_forward(t_sec, win):
	win.type_keys('{w down}')
	time.sleep(t_sec)
	win.type_keys('{w up}')

def move_backward(t_sec, win):
	win.type_keys('{s down}')
	time.sleep(t_sec)
	win.type_keys('{s up}')

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

def break_one_col(win, pos_dict):
	n_changes = 0
	# Get target block
	old = get_values(['target'], pos_dict)[0]
	while old is None:
		old = get_values(['target'], pos_dict)[0]
	
	# left click untill two changes
	pyautogui.mouseDown(button='left')

	# One change
	trip = get_values(['target'], pos_dict)[0]
	while trip == old:
		trip = get_values(['target'], pos_dict)[0]
	old = trip

	# Second change
	trip = get_values(['target'], pos_dict)[0]
	while trip == old:
		trip = get_values(['target'], pos_dict)[0]
	
	pyautogui.mouseUp(button='left')
