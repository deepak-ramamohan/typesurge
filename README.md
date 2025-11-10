# TypeMania

This repository contains a collection of typing games built with the Python arcade library.

## Getting Started

First, you'll need to clone the repository to your local machine. You can do this by running the following command in your terminal:

```bash
git clone https://github.com/deepak-ramamohan/typing-game.git
```

Once you have cloned the repository, you'll need to set up a Python environment. Below are instructions for both `conda` and `venv`.

### Using Conda

If you are using Anaconda or Miniconda, you can create a new environment with the following commands:

```bash
# Create a new conda environment with Python 3.12
conda create --name typemania python=3.12

# Activate the environment
conda activate typemania

# Install the required dependencies
pip install -r requirements.txt
```

### Using venv

If you are using a standard Python installation, you can use `venv` to create a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows
venv\\Scripts\\activate
# On macOS and Linux
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt
```

## Running the Game

Once you have set up the environment and installed the dependencies, you can run the game with the following command:

```bash
python main.py
```

## Game Modes

### Space Shooter

A fast-paced arcade game where you must type words to shoot down enemy meteors. The difficulty ramps up as your score gets higher.

### AI Trainer

A training mode that helps you improve your typing skills. It tracks your words-per-minute (WPM) and accuracy. This mode intelligently selects words that you have previously mistyped to help you practice and improve on your weaknesses.
