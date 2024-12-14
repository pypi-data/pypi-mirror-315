from setuptools import setup, find_packages

setup(
    name="pywordle-cli",
    version="0.1.0",
    description="A command line based wordle game",
    author="Ousmane Barry",
    author_email="abarr156@uottawa.ca",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["colorama", "setuptools"],
    python_requires='>=3.7',  
    entry_points={
        "console_scripts": [
            "wordle=wordle.wordle:main",
        ],
    },
    classifiers=[
      "Development Status :: 4 - Beta",
      "Environment :: Console",
      "Intended Audience :: End Users/Desktop",
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      "Topic :: Games/Entertainment :: Puzzle Games",
    ],
)
