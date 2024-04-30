import os
import pygame
import tkinter as tk
from tkinter import filedialog

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("300x150")

        self.song_list = []
        self.current_song_index = 0

        self.initialize_player()
        
    def initialize_player(self):
        # Initialize Pygame mixer
        pygame.mixer.init()

        # Create GUI elements
        self.play_button = tk.Button(self.root, text="Play", command=self.play_music)
        self.play_button.pack()

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_music)
        self.pause_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_music)
        self.stop_button.pack()

        self.select_folder_button = tk.Button(self.root, text="Select Folder", command=self.select_folder)
        self.select_folder_button.pack()

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.song_list = [os.path.join(folder_selected, file) for file in os.listdir(folder_selected) if file.endswith(".mp3")]
            if self.song_list:
                self.current_song_index = 0
                self.play_music()

    def play_music(self):
        if self.song_list:
            pygame.mixer.music.load(self.song_list[self.current_song_index])
            pygame.mixer.music.play()

    def pause_music(self):
        pygame.mixer.music.pause()

    def stop_music(self):
        pygame.mixer.music.stop()

# Create Tkinter window
root = tk.Tk()
app = MusicPlayer(root)
root.mainloop()
