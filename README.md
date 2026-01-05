# Pygame AI Gridworld Agent

This project implements an **intelligent agent in a grid-based environment** using **Pygame**.
The agent navigates a 2D grid world, perceives its surroundings, and selects actions to achieve
its objectives while respecting the environment constraints.

## Context
Academic project developed for the course **Artificial Intelligence**.

## Features
- Grid-world environment represented as a matrix
- Pygame-based graphical interface
- Intelligent agent with discrete actions (movement / interaction)
- Clear separation between environment logic and agent behaviour

## Tech Stack
- Python
- Pygame
- AI concepts: state representation, actions, environment interaction

## Project Structure
- `run.py` — main game loop and execution
- `Matrix.py` — grid representation and environment logic
- `iron.py` — agent behaviour and decision-making
- `textures/` — sprites and visual assets

## How to Run
```bash
pip install pygame
python run.py
