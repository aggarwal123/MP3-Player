from tkinter import *
from pygame import mixer
from tkinter import filedialog
import time
import os
from mutagen.mp3 import MP3
import tkinter.ttk as ttk



mixer.init()
root = Tk()
root.title("MP3 PLAYER")
# IMAGE ALONG WITH TITLE
image_icon = PhotoImage(file = "Images/icon.png")
root.iconphoto(False, image_icon)
# root.configure(background =  "#000000")
# WINDOW GEOMETRY
root.geometry("500x350")
root.minsize(width=500, height=350)
# root.resizable(False, False)



###############################   LENGTH OF THE SONG   ###############################
def Play_Time():
    if stopped:
        return
    current_time = mixer.music.get_pos() / 1000       # THIS WILL BE IN MILLI SECONDS. TO MAKE IT IN SECONDS WE DIVIDE IT BY 1000
    # PUTTING A TEMP LABEL TO GET DATA
    # slider_label.config(text=f"Slider: {int(my_slider.get())}  and Song Position: {int(current_time)}")
    
    # current = playlist.curselection()  # WILL GET A INDEX OF SONG IN TUPLE
    song = playlist.get(ACTIVE)
    song_path = None

    for directory in directories:
        file_path = os.path.join(directory, song) + ".mp3"
        if os.path.exists(file_path):
            song_path = file_path
            break  # STOP SEARCHING ONCE SONG PATH IS FOUND
    song_mut = MP3(song_path)
    global song_length
    song_length = song_mut.info.length
    # CONVERTING SONG_LENGTH
    converted_song_length = time.strftime("%M:%S", time.gmtime(song_length)) 
    
    current_time+=1
    
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f"Time Elapsed: {converted_song_length}  \nSong Length: {converted_song_length}  ")
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        # SLIDER HASNT MOVED
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
    else:
        # SLIDER HAS MOVED
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        
        converted_current_time = time.strftime("%M:%S", time.gmtime(int(my_slider.get())))
        # UPDATING STATUS BAR
        status_bar.config(text=f"Time Elapsed: {converted_current_time}  \nSong Length: {converted_song_length}  ")
        # MOVING THE TIME
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)
    
    # UPDATING SLIDER
    # my_slider.config(value=int(current_time))
    

    # UPDATING TIME
    status_bar.after(1000, Play_Time)



#############################   ADD SONG FUNCTION   ####################################
def Add_One_Song():
    global directories
    file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        directory = os.path.dirname(file_path) + "/"
        if directory not in directories:
            directories.append(directory)
        song_name = os.path.basename(file_path)
        song_name = os.path.splitext(song_name)[0]
        playlist.insert(END, song_name)
    print(directories)



############################   ADDING MULTIPLE SONGS   ############################
def Add_Multiple_Song():
    global directories
    file_paths = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
    
    for file_path in file_paths:
        directory = os.path.dirname(file_path) + "/"
        if directory not in directories:
            directories.append(directory)
        
        song_name = os.path.basename(file_path)
        song_name = os.path.splitext(song_name)[0]
        playlist.insert(END, song_name)
    print(directories)



############################   ADDING A FOLDER OF SONGS   ############################
def Add_Folder():
    global directories
    folder_path = filedialog.askdirectory()

    if folder_path:
        if folder_path not in directories:
            directories.append(folder_path)

        folder_name = os.path.basename(folder_path)

        for root_dir, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".mp3"):
                    song_name = os.path.splitext(file)[0]
                    playlist.insert(END, song_name)



###############################   PLAYING A SONG   ################################
def Play_Music():
    global stopped
    stopped = False
    song = playlist.get(ACTIVE)
    song_path = None
    
    # Search for the song in the specified directories
    for directory in directories:
        file_path = os.path.join(directory, song) + ".mp3"
        if os.path.exists(file_path):
            song_path = file_path
            break  # Stop searching once the song is found
    
    if song_path:
        mixer.music.load(song_path)
        mixer.music.play(loops=0)
    
    # CALLING Play_Time FUNCTION TO GET THE SONG LENGTH
    Play_Time()
    
    # UPDATING SLIDER
    # slider_position = int(song_length)
    # my_slider.config(to=slider_position, value=0)



#############################   STOPPING MUSIC   #############################
global stopped
stopped = False
def Stop_Music():
    # RESET SLIDER AND STATUS BAR
    status_bar.config(text=" ")
    my_slider.config(value=0)
    # STOP SONG FOR PLAYING
    mixer.music.stop()
    playlist.selection_clear(ACTIVE)
    # CLEAR STATUS BAR
    status_bar.config(text=" ")
    # SET STOP VARIABLE TO TRUE
    global stopped
    stopped = True


##############################   CREATE GLOBAL PAUSE VARIABLE   #############################
global paused
paused = False

##############################   PAUSE AND RESUME   #############################
def Pause_Music(is_paused):
    global paused
    paused = is_paused
    if paused:
        # UNPAUSE
        mixer.music.unpause()
        paused = False
    else:
        # PAUSE
        mixer.music.pause()
        paused = True
    

##############################   NEXT BUTTON   #############################
def Next_Song():
    # RESET SLIDER AND STATUS BAR
    status_bar.config(text=" ")
    my_slider.config(value=0)
    next = playlist.curselection()  # WILL GET A INDEX OF SONG IN TUPLE
    next = next[0] + 1
    song = playlist.get(next)
    song_path = None

    for directory in directories:
        file_path = os.path.join(directory, song) + ".mp3"
        if os.path.exists(file_path):
            song_path = file_path
            break  # STOP SEARCHING ONCE SONG PATH IS FOUND
    if song_path:
        mixer.music.load(song_path)
        mixer.music.play(loops=0)
    
    # MOVING THE ACTIVE BAR SELECTION
    playlist.selection_clear(0,END)   # CLEARING THE BAR
    playlist.activate(next)  # ACTIVATING THE SONG BAR
    playlist.selection_set(next, last=None)
    
    
##################################   PREVIOUS SONG   #################################
def Previous_Song():
    # RESET SLIDER AND STATUS BAR
    status_bar.config(text=" ")
    my_slider.config(value=0)
    prev = playlist.curselection()  # WILL GET A INDEX OF SONG IN TUPLE
    prev = prev[0] - 1
    song = playlist.get(prev)
    song_path = None

    for directory in directories:
        file_path = os.path.join(directory, song) + ".mp3"
        if os.path.exists(file_path):
            song_path = file_path
            break  # STOP SEARCHING ONCE SONG PATH IS FOUND
    if song_path:
        mixer.music.load(song_path)
        mixer.music.play(loops=0)
    
    # MOVING THE ACTIVE BAR SELECTION
    playlist.selection_clear(0,END)   # CLEARING THE BAR
    playlist.activate(prev)  # ACTIVATING THE SONG BAR
    playlist.selection_set(prev, last=None)


##############################   REMOVE A SONG   #############################
def Remove_Song():
    Stop_Music()
    playlist.delete(ANCHOR)
    mixer.music.stop()


##############################   REMOVE ALL SONGS   #############################
def Remove_All_Songs():
    Stop_Music()
    playlist.delete(0, END)
    mixer.music.stop()


###############################   SLIDER FUNCTION   ###############################
def Slide(x):
    # # slider_label.config(text=f"{int(my_slider.get())}  of  {int(song_length)}")
    song = playlist.get(ACTIVE)
    song_path = None
    
    # Search for the song in the specified directories
    for directory in directories:
        file_path = os.path.join(directory, song) + ".mp3"
        if os.path.exists(file_path):
            song_path = file_path
            break  # Stop searching once the song is found
    
    if song_path:
        mixer.music.load(song_path)
        mixer.music.play(loops=0, start=int(my_slider.get()))


##################################   VOLUME FUNCTION   ##############################
def Volume(x):
    mixer.music.set_volume(volume_slider.get())
    
    # CHANGE VOLUME IMAGE
    current_volume = mixer.music.get_volume()
    current_volume *= 100
    if int(current_volume) < 1:
        volume_meter.config(image=vol0)
    elif int(current_volume)>0 and int(current_volume)<40:
        volume_meter.config(image=vol1)
    elif int(current_volume)>=40 and int(current_volume)<85:
        volume_meter.config(image=vol2)
    elif int(current_volume)>=85:
        volume_meter.config(image=vol3)











#############################   CREATING A MASTER FRAME   #############################
# WE WILL PUT PLAYLIST AND BUTTONS IN MASTER FRAME
master_frame = Frame(root)
master_frame.pack(pady=20)


##############################   CREATING PLAYER CONTROL FRAME   #############################

control_frame = Frame(master_frame)
control_frame.grid(row=1, column=0, pady=25)


##############################   CREATING PLAYER VOLUME FRAME   #############################

volume_frame = LabelFrame(master_frame, text="VOLUME")
volume_frame.grid(row=0, column=1, padx=20)


##############################   CREATING LIST OF SONGS   #############################

playlist = Listbox(master_frame, bg="lightblue", fg="black", width=60,
                     selectbackground="gray", selectforeground="black")
playlist.grid(row=0, column=0)


##############################   DEFINING CONTROL AND VOLUME BUTTONS   #############################

back_button_image = PhotoImage(file = "Images/back.png")
next_button_image = PhotoImage(file = "Images/next.png")
play_button_image = PhotoImage(file = "Images/play.png")
pause_button_image = PhotoImage(file = "Images/pause.png")
stop_button_image = PhotoImage(file = "Images/stop.png")

global vol0
global vol1
global vol2
global vol3
vol0 = PhotoImage(file = "Images/sound1.png")
vol1 = PhotoImage(file = "Images/sound2.png")
vol2 = PhotoImage(file = "Images/sound3.png")
vol3 = PhotoImage(file = "Images/sound4.png")


##############################   CREATING PLAYER VOLUME FRAME   #############################

volume_meter = Label(master_frame, image=vol3)
volume_meter.grid(row=1, column=1, padx=20)


##############################   CREATING PLAYER CONTROL BUTTONS   #############################

back_button = Button(control_frame, image=back_button_image, borderwidth=0,
                     command=Previous_Song).grid(row=0, column=0, padx=10)

pause_button = Button(control_frame, image=pause_button_image, borderwidth=0,
                      command=lambda: Pause_Music(paused)).grid(row=0, column=1, padx=10)

play_button = Button(control_frame, image=play_button_image, borderwidth=0,
                     command=Play_Music).grid(row=0, column=2, padx=10)

stop_button = Button(control_frame, image=stop_button_image, borderwidth=0,
                     command=Stop_Music).grid(row=0, column=3, padx=10)

next_button = Button(control_frame, image=next_button_image, borderwidth=0,
                     command=Next_Song).grid(row=0, column=4, padx=10)


##############################   INITIALIZING THE DIRECTORY ARRAY   #############################
directories = []


##################################   CREATING MENU   ###################################
my_menu = Menu(root)
root.config(menu=my_menu)


#################################   ADD SONG MENU   ##################################
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song to Playlist", command=Add_One_Song)
add_song_menu.add_command(label="Add Multiple Song to Playlist", command=Add_Multiple_Song)
add_song_menu.add_command(label="Add Folder to Playlist", command=Add_Folder)

##############################   DELETING OR REMOVAL OF SONGS   #############################
delete_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=delete_song_menu)
delete_song_menu.add_command(label="Remove the Selected Song", command=Remove_Song)
delete_song_menu.add_command(label="Remove All Songs", command=Remove_All_Songs)


##############################   STATUS BAR   #############################
status_bar = Label(root, text=" ", bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipadx=2)


##############################   MUSIC POSITION SLIDER   #############################
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=Slide, length=360)
my_slider.grid(row=2, column=0)


##############################   VOLUME SLIDER   #############################
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=Volume, length=125)
volume_slider.pack(pady=10)



root.mainloop()