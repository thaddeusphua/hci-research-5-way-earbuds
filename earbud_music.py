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

# pygame mixer sound setup
mixer.init() # pygame mixer setup
playlist = ["playlist/song1.mp3", "playlist/song2.mp3", "playlist/song3.mp3"]
index = 0

# action song sounds
pause_sound = mixer.Sound("action_sounds/pause.oga")
pause_sound.set_volume(1)
vol_sound = mixer.Sound("action_sounds/volume_change.oga")
vol_sound.set_volume(1)
song_change_sound = mixer.Sound("action_sounds/song_change.oga")
song_change_sound.set_volume(1)

first_song_played = False # this is the intial setup
pause_state = False # toggle between pause and unpause
volume = 0.39 #volume is between 0 and 1


while True:
	if GPIO.input(up) == GPIO.HIGH:
		vol_sound.play()
		new_volume = volume + 0.3
		if new_volume > 1: # check that the new volume is within bounds
			pass
		else:
			volume = new_volume
			mixer.music.set_volume(volume)
		print("UP; Volume: {:.2f}".format(volume))
	elif GPIO.input(down) == GPIO.HIGH:
		vol_sound.play()
		new_volume = volume - 0.3
		if new_volume < 0: # check that the new volume is within bounds
			pass
		else:
			volume = new_volume
			mixer.music.set_volume(volume)
		print("DOWN; Volume: {:.2f}".format(volume))
	elif GPIO.input(left) == GPIO.HIGH:
		song_change_sound.play()
		index = (index-1)%3 #go back 1 song
		mixer.music.load(playlist[index])
		mixer.music.play()
		print("LEFT; ", playlist[index])
	elif GPIO.input(right) == GPIO.HIGH:
		song_change_sound.play()
		index = (index+1)%3 #go forward 1 song
		mixer.music.load(playlist[index])
		mixer.music.play()
		print("RIGHT; ", playlist[index])
	elif GPIO.input(center) == GPIO.HIGH:
		pause_sound.play()
		if first_song_played == False:
			mixer.music.load(playlist[index])
			mixer.music.play()
			first_song_played = True
			print("CENTER; play")
		elif first_song_played == True:
			if pause_state == False:
				mixer.music.pause()
				pause_state = True
				print("CENTER; paused")
			elif pause_state == True:
				mixer.music.unpause()
				pause_state = False
				print("CENTER; unpaused")
	# set delay after all events
	time.sleep(0.4)
