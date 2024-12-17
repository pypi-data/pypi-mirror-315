from setuptools import setup, find_packages

setup(
    name="bumms",
    version="1.5.0",
    author="Justin Braun",
    description="Eine lustige Bibliothek mit Sounds, ASCII-Art und Texten.",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pygame",
        "video-to-ascii"
    ],
    entry_points={
        "console_scripts": [
            "bumms=bumms.__main__:main",        # Der Standardbefehl bumms
            "bumms-hd=bumms.__main__:bumms_hd"  # Der Befehl bumms-hd
        ]
    },
    package_data={
        "bumms": [
            "knall1.mp3", "knall2.mp3", "knall3.mp3",
            "ascii.bumms", "txt.bumms", "video.mp4"  # Video und andere Daten
        ],
    }
)
