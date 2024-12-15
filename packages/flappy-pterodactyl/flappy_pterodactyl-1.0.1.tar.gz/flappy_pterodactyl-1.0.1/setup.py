from setuptools import setup, find_packages

setup(
    name="flappy-pterodactyl",  # Package name on PyPI
    version="1.0.1",            # Semantic versioning
    description="A Flappy Pterodactyl game using AR and face tracking",
    long_description=open("flappy/README.md").read(),
    long_description_content_type="text/markdown",
    author="Abhijit Bhattacharjee",
    author_email="abhijit@example.com",
    url="https://github.com/abhijitbhattacharjee/flappy",  # Update with the actual repo URL
    license="MIT",
    packages=find_packages(),  # Automatically find all packages
    include_package_data=True, # Include non-code files specified in MANIFEST.in
    install_requires=[
        "pygame",
        "mediapipe",
        "pyglet",
        "screeninfo",
        "opencv-python",
        "openpyxl",
        "pandas",
        "pillow",
        "pyaudio",
        "playsound",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "flappy=flappy.Flappy:main",  # Update with your main entry point
        ],
    },
)