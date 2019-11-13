import RPi.GPIO as GPIO
import time
from pygame import mixer

up = 37
down = 35
left = 33
right = 31
center = 29

GPIO.setmode(GPIO.BOARD)
GPIO.setup(up, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(down, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(left, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(right, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(center, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	

mixer.init() # pygame mixer setup
playlist = ["playlist/song1.mp3", "playlist/song2.mp3", "playlist/song3.mp3"]
index = 0

first_song_played = False # this is the intial setup
pause_state = False # toggle between pause and unpause
volume = 0.5 #volume is between 0 and 1

while True:
	time.sleep(0.2) # set a delay between commands
	if GPIO.input(left) == GPIO.HIGH:
		print("LEFT")
		index = (index-1)%3 #go back 1 song
		mixer.music.load(playlist[index])
		mixer.music.play()
		print(index)
	elif GPIO.input(center) == GPIO.HIGH:
		print("CENTER")
		if first_song_played == False:
			mixer.music.load(playlist[index])
			mixer.music.play()
			first_song_played = True
		elif first_song_played == True:
			if pause_state == False:
				mixer.music.pause()
				pause_state = True
				print("paused")
			elif pause_state == True:
				mixer.music.unpause()
				pause_state = False
				print("unpaused")
	elif GPIO.input(up) == GPIO.HIGH:
		print("UP")
		new_volume = volume + 0.2 
		if new_volume > 1: # check that the new volume is within bounds
			pass
		else:
			volume = new_volume
			mixer.music.set_volume(volume)
		print("Volume set to: ", volume)
	elif GPIO.input(right) == GPIO.HIGH:
		print("RIGHT")
		index = (index+1)%3 #go forward 1 song
		mixer.music.load(playlist[index])
		mixer.music.play()
		print(index)
	elif GPIO.input(down) == GPIO.HIGH:
		print("DOWN")
		new_volume = volume - 0.2 
		if new_volume < 0: # check that the new volume is within bounds
			pass
		else:
			volume = new_volume
			mixer.music.set_volume(volume)
		print("Volume set to: ", volume)
