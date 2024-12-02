# Algorithm Visualization Project

---

## Overview

This project provides a visual representation of pathfinding algorithms using the A* algorithm.  
Users can interact with a grid to set start points, end points, walls, and obstacles, and observe the algorithm's progress in finding an optimal path.  

The system also includes features to simulate the propagation of "smell intensity" from specific tiles, adding a heuristic twist to the pathfinding process.

---

## Features

- **Interactive Grid**:  
  Users can draw walls, set start and end points, and add "rotten" tiles.

- **Pathfinding Algorithms**:  
  - A* with diagonal movement.  
  - A* without diagonal movement.  

- **Dynamic Heuristics**:  
  Integration of "smell intensity" as an additional heuristic.

- **Reset Functionality**:  
  Clear the grid for a new simulation.

- **Visualization**:  
  Real-time visualization of the grid updates and algorithm progression.

---

## Structure

The project is organized into three main files:

### 1. `button.py`

Defines the **`Button`** class, which handles the graphical representation and functionality of buttons in the UI.

- **Key Methods**:
  - `__init__(x, y, image)`:  
    Initializes the button with its position and image.

  - `draw(win)`:  
    Renders the button onto the screen.

  - `isActivated()`:  
    Detects if the button is clicked.

---

### 2. `tile.py`

Defines the **`Tile`** class, which represents each square on the grid.

- **Attributes**:
  - `row`, `col`:  
    Tile's position in the grid.  

  - `width`:  
    Size of the tile.  

  - `color`:  
    Current color of the tile.  

  - `neighbors`:  
    Adjacent tiles.  

  - `smell_intensity`:  
    Represents the "smell" heuristic affecting pathfinding.  

- **Key Methods**:
  - `draw(win)`:  
    Draws the tile.

  - `setStart()`, `setEnd()`, `setWall()`, etc.:  
    Change the state of the tile.

  - `updateNeighbors(grid, allowDiagonal)`:  
    Updates the list of adjacent tiles based on the grid configuration.

  - `setRotten()`:  
    Marks a tile as "rotten" and initiates the smell intensity.

  - `propagateSmell(grid)`:  
    Simulates smell propagation using a BFS-like approach, modifying nearby tiles.

---

### 3. `main.py`

Entry point of the program and contains the logic for user interaction, rendering, and algorithm execution.

- **Key Functions**:
  - `create_grid(rows, width)`:  
    Generates a grid of `Tile` objects.

  - `update_grid_neighbors(grid, allow_diagonal)`:  
    Updates neighbors for all tiles in the grid.

  - `render_window(win, grid, ...)`:  
    Handles rendering of the grid, UI buttons, and text.

  - `a_star_pathfinding(draw, grid, start, end)`:  
    Implements the A* algorithm with additional heuristics like smell intensity.

  - `main(win, width)`:  
    Main game loop where user interactions and algorithm visualizations are handled.

---

## Usage Instructions

### Installation

1. Ensure Python is installed.  
2. Install the required libraries:  
   ```bash
   pip install pygame
