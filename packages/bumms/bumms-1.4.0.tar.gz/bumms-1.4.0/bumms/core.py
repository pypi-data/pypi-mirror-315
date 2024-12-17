import random
import os
import pygame
import subprocess

def play_random_sound():
    sounds = ["knall1.mp3", "knall2.mp3", "knall3.mp3"]
    selected_sound = random.choice(sounds)
    sound_path = os.path.join(os.path.dirname(__file__), selected_sound)

    if os.path.exists(sound_path):
        pygame.mixer.init()
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    else:
        print(f"Fehler: Datei {selected_sound} nicht gefunden.")

def display_ascii_art():
    ascii_path = os.path.join(os.path.dirname(__file__), "ascii.bumms")
    if os.path.exists(ascii_path):
        with open(ascii_path, "r", encoding="utf-8") as file:
            print(file.read())
    else:
        print("Fehler: ASCII-Datei nicht gefunden.")

def display_random_text():
    text_path = os.path.join(os.path.dirname(__file__), "txt.bumms")
    if os.path.exists(text_path):
        with open(text_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            print("\n\n" + random.choice(lines).strip())
    else:
        print("Fehler: Textdatei nicht gefunden.")

def play_video_in_ascii():
    video_path = os.path.join(os.path.dirname(__file__), "video.mp4")
    if os.path.exists(video_path):
        print("Starte Video im ASCII-Format mit Ton...")
        subprocess.run(["video-to-ascii", "-f", video_path])
    else:
        print(f"Fehler: Datei {video_path} nicht gefunden.")

def bumms_hd():
    play_video_in_ascii()

def main():
    play_random_sound()
    display_ascii_art()
    display_random_text()

if __name__ == "__main__":
    bumms_hd()  # Um bumms_hd als Standardausführung zu testen
    # main()  # Alternativ die Standardausführung
