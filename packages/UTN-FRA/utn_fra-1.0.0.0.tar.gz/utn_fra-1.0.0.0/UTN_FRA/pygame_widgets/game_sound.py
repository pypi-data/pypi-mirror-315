import pygame.mixer as mixer

class GameSound:
    
    def __init__(self):
        mixer.init()

    def play_sound(self, sound_path: str, volume: float = 0.8):
        sound = mixer.Sound(sound_path)
        sound.set_volume(volume)
        sound.play()
    
    def play_music(self, music_path: str, volume: float = 0.5):
        mixer.music.load(music_path)
        mixer.music.set_volume(volume)
        mixer.music.play(-1, 0, 3000)
    
    def stop_music(self):
        mixer.music.fadeout(500)
        