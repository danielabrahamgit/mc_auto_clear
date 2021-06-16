from operator import pos
from re import A
import sys
import time
from tkinter.constants import E
import numpy as np
import pyautogui
import matplotlib.pyplot as plt
from box_reader import get_dict_from_file, detect_boxes
from image_utils import get_values
from control import break_one_col, move_feedback, set_mining_angle, turn, move_forward, move_backward, set_torch
from pywinauto import Application, Desktop
from pywinauto.keyboard import send_keys

# Direction for turn right or left
right = True

# Minecraft toolbar (9 items)
toolbar = [
	'pick',
	'pick',
	'pick',
	'pick',
	'pick',
	'pick',
	'pick',
	'torch',
	'food',
	1
]

# Defines the area to clear out
x_max, z_min = -1047.3, 486
x_min, z_max = -1057.3, 496


if ( __name__ == "__main__" ):
	assert len(sys.argv) <= 2
	

	# Find minecraft window name
	mc_win_name = ''
	for w in Desktop(backend="uia").windows():
		w_text = w.window_text()
		if 'Multiplayer' in w_text:
			mc_win_name = 'Minecraft 1.17 - Multiplayer'
			break
		elif 'Singleplayer' in w_text:
			mc_win_name = 'Minecraft 1.17 - Singleplayer'
			break

	# Link python to minecraft 
	minecraft_handle = Application().connect(title_re=mc_win_name, class_name="GLFW30")
	main_window = minecraft_handle.top_window()
	
	# Handle mouse stuff
	rect = main_window.rectangle()
	xc = rect.width()//2
	yc = rect.height()//2 + 11

	
	# OCR setup
	if len(sys.argv) == 2:
		detect_boxes()

	pos_dict = get_dict_from_file()

	# -------------------------- MINING BEGIN -------------------------- 
	set_mining_angle(main_window, pos_dict, xc, yc)
	steps_per_torch = 7
	straight = steps_per_torch * (60 // steps_per_torch)
	for turns in range(10):
		if turns % 4 == 0:
			for torch_steps in range(straight // steps_per_torch):
				move_feedback(steps_per_torch, main_window, pos_dict, mining=True)
				set_torch(toolbar, main_window, pos_dict, xc, yc)
				move_forward(0.3, main_window)
		else:
			move_feedback(straight, main_window, pos_dict, mining=True)
			move_forward(0.3, main_window)

			

		# Turn break two move in, turn again
		if right:
			turn('right', main_window, pos_dict, xc, yc)
			break_one_col(main_window, pos_dict)
			move_forward(0.5, main_window)
			turn('right', main_window, pos_dict, xc, yc)
			right = False
		else: 
			turn('left', main_window, pos_dict, xc, yc)
			break_one_col(main_window, pos_dict)
			move_forward(0.5, main_window)
			turn('left', main_window, pos_dict, xc, yc)
			right = True
	
# START = -1187, 418