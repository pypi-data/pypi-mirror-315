from setuptools import setup, find_packages

setup(
    name="bumms",
    version="1.1.0",
    author="Justin Braun",
    description="Eine lustige Bibliothek mit Sounds, ASCII-Art und Texten.",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "playsound==1.2.2"
    ],
    entry_points={
        "console_scripts": [
            "bumms=bumms.__main__:main"
        ]
    },
    package_data={
        "bumms": ["knall1.mp3", "knall2.mp3", "knall3.mp3", "ascii.bumms", "txt.bumms"],
    }
)
