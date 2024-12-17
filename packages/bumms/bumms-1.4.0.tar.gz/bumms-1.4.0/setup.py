from setuptools import setup, find_packages

setup(
    name="bumms",
    version="1.4.0",
    author="Justin Braun",
    description="Eine lustige Bibliothek mit Sounds, ASCII-Art und Texten.",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pygame",
        "video-to-ascii"  # Hinzufügen der Abhängigkeit für video-to-ascii
    ],
    entry_points={
        "console_scripts": [
            "bumms=bumms.__main__:main",        # Befehl für die Standardfunktion
            "bumms-hd=bumms.__main__:bumms_hd"  # Befehl für das HD-Video im ASCII-Format
        ]
    },
    package_data={
        "bumms": [
            "knall1.mp3", "knall2.mp3", "knall3.mp3",   # Sounddateien
            "ascii.bumms", "txt.bumms",                   # ASCII und Textdateien
            "video.mp4"                                   # Das Video für bumms-hd
        ],
    }
)
