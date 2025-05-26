from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="ChaTerminal",
    version="0.0.1",
    author="Gofaone Tlalang",
    author_email="gofaonetlalang@gmail.com",
    description="A terminal-based encrypted chat system for LAN and remote connections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gofaone315/ChaTerminal",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "chat=ChaTerminal.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Communications :: Chat",
        "Topic :: Security :: Cryptography"
    ],
    python_requires=">=3.6",
    install_requires=[
        "colorama",
        "pyfiglet"
    ],
)
