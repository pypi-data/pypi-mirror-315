import random
import os
from playsound import playsound

def play_random_sound():
    # Liste der verfügbaren MP3-Dateien
    sounds = ["knall1.mp3", "knall2.mp3", "knall3.mp3"]
    # Zufällige MP3 auswählen
    selected_sound = random.choice(sounds)
    sound_path = os.path.join(os.path.dirname(__file__), selected_sound)

    if os.path.exists(sound_path):
        playsound(sound_path)
    else:
        print(f"Fehler: Datei {selected_sound} nicht gefunden.")

def display_ascii_art():
    # Pfad zur ASCII-Datei
    ascii_path = os.path.join(os.path.dirname(__file__), "ascii.bumms")

    if os.path.exists(ascii_path):
        with open(ascii_path, "r", encoding="utf-8") as file:
            ascii_art = file.read()
            print(ascii_art)
    else:
        print("Fehler: ASCII-Datei nicht gefunden.")

def display_random_text():
    # Pfad zur Textdatei
    text_path = os.path.join(os.path.dirname(__file__), "txt.bumms")

    if os.path.exists(text_path):
        with open(text_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            random_text = random.choice(lines).strip()
            print("\n\n" + random_text)
    else:
        print("Fehler: Textdatei nicht gefunden.")

def main():
    play_random_sound()
    display_ascii_art()
    display_random_text()
