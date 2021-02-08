from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()

root.title("MP3 Player")
root.geometry("500x400")

# Initialize pygame

pygame.mixer.init()


# Create function to deal with time
def play_time():
	# Grab current song time
	if stopped:
		return

	current_time = pygame.mixer.music.get_pos() / 1000
	# Convert song time to time format
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

	# Reconstruct song with directory structure
	song = playlist_box.get(ACTIVE)
	song = f'E:/Python/MP3 Player/audio/{song}.mp3'

	# Find currrent song length
	song_mut = MP3(song)
	global song_len
	song_len = song_mut.info.length
	# convert to time formate
	converted_song_len = time.strftime('%M:%S', time.gmtime(song_len))

	# Check to see if song is over
	if int(song_slider.get()) == int(song_len):
		stop()


	elif paused:
		# Check to see if paused, if so -
		pass
	else:
		# Move slider along 1 second at a time
		next_time = int(song_slider.get()) + 1
		# Output new time value to slider
		song_slider.config(to=song_len, value=next_time)

		# convert slider position to time format
		converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

		# output slider

		status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_len}  ')


	# Add current time to status bar
	if current_time >= 1:
		status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_len}  ')

	# create loop to check the time every second
	my_label.after(1000, play_time)

# A fun which adds a single song

def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),))
    # Strip out directory structure and .mp3

    song = song.replace("E:/Python/MP3 Player/audio/", "")
    song = song.replace(".mp3", "")

    # Add to end of playlist

    playlist_box.insert(END, song)


# A fun which adds multiple songs

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),))

    # Loop through song list and replace directory structure and mp3 from list

    for song in songs:
        # Strip out directory structure and .mp3

        song = song.replace("E:/Python/MP3 Player/audio/", "")
        song = song.replace(".mp3", "")

        # Add to end of playlist

        playlist_box.insert(END, song)

# Function for Delete a song from playlist

def delete_song():
	# Delete highlighted song in the playlist
	playlist_box.delete(ANCHOR)

# Function for Deleting all songs in playlist

def delete_songs():
	# Delete all songs in playlist

	playlist_box.delete(0, END)

# Create a play function

def play():

	# Set stopped to false
	global stopped
	stopped = False
	# Reconstruct song with directory structure
	song = playlist_box.get(ACTIVE)
	song = f'E:/Python/MP3 Player/audio/{song}.mp3'

	# Load song with pygame mixer
	pygame.mixer.music.load(song)

	# Play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	# Get song time
	play_time()


# Create stopped variable
global stopped
stopped = False

# create a stop function
def stop():
	# Stop the song
	pygame.mixer.music.stop()

	#clear playlist bar
	playlist_box.selection_clear(ACTIVE)

	status_bar.config(text='')
	# Reset slider position and status bar
	song_slider.config(value=0)
	# Set stop variable to true
	global stopped
	stopped = True

#Create pause variable
global paused
paused = False

# Create pause function
def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		# Unpause
		pygame.mixer.music.unpause()
		paused = False
	else:
		#Pause
		pygame.mixer.music.pause()
		paused = True


# Create a function to play next song

def next_song():
	# Reset slider position and status bar
	status_bar.config(text='')
	song_slider.config(value=0)
	# Get current song number
	next_one = playlist_box.curselection()
	# add 1 to to the current song no. from tuple
	next_one = next_one[0] + 1

	# Grab the song title from the playlist
	song = playlist_box.get(next_one)
	song = f'E:/Python/MP3 Player/audio/{song}.mp3'
	# Load song with pygame mixer
	pygame.mixer.music.load(song)

	# Play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	# Clear active bar in playlist
	playlist_box.selection_clear(0, END)

	# Move active bar to next song
	playlist_box.activate(next_one)

	# Set active bar to next song
	playlist_box.selection_set(next_one, last=None)

# create function to play previous song
def previous_song():
	# Reset slider position and status bar
	status_bar.config(text='')
	song_slider.config(value=0)
	# Get current song number
	next_one = playlist_box.curselection()
	# subtract 1 to to the current song no. from tuple
	next_one = next_one[0] - 1

	# Grab the song title from the playlist
	song = playlist_box.get(next_one)
	song = f'E:/Python/MP3 Player/audio/{song}.mp3'
	# Load song with pygame mixer
	pygame.mixer.music.load(song)

	# Play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	# Clear active bar in playlist
	playlist_box.selection_clear(0, END)

	# Move active bar to next song
	playlist_box.activate(next_one)

	# Set active bar to next song
	playlist_box.selection_set(next_one, last=None)
# Create Volume funtion
def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())

# Create a slide function
def slide(x):
	# Reconstruct song with directory structure
	song = playlist_box.get(ACTIVE)
	song = f'E:/Python/MP3 Player/audio/{song}.mp3'

	# Load song with pygame mixer
	pygame.mixer.music.load(song)

	# Play song with pygame mixer
	pygame.mixer.music.play(loops=0, start=song_slider.get())



# create main frame
main_frame = Frame(root)
main_frame.pack(pady=20)

# Create volume slider frame
volume_frame = LabelFrame(main_frame, text='Volume')
volume_frame.grid(row=0, column=1, padx=20)

# Create volume slider
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, length=130, command=volume)
volume_slider.pack(pady=10)

# Create song slider
song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=360, command=slide)
song_slider.grid(row=2, column=0, pady=20)



# create playlist box
playlist_box = Listbox(main_frame, bg="black", fg="green", width=60, selectbackground="green", selectforeground="black")
playlist_box.grid(row=0, column=0)

# Define button images for control
back_btn_img = PhotoImage(file='images/back50.png')
forward_btn_img = PhotoImage(file='images/forward50.png')
play_btn_img = PhotoImage(file='images/play50.png')
pause_btn_img = PhotoImage(file='images/pause50.png')
stop_btn_img = PhotoImage(file='images/stop50.png')

# craete button frame
control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)

# create play/stop etc buttons
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command = stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

# Create Main Menu

my_menu = Menu(root)
root.config(menu=my_menu)

# Create add song menu dropdows
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add song to playlist", command=add_song)
add_song_menu.add_command(label="Add songs to playlist", command=add_many_songs)

# Create delete songs menu dropdowns
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song", command=delete_song)
remove_song_menu.add_command(label="Delete all songs", command=delete_songs)


# Create status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Temporary Label

my_label = Label(root, text='')
my_label.pack(pady=10)

root.mainloop()
