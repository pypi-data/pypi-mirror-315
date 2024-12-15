# Skytree
2D game framework for Python
_Version 0.2.1_

Skytree is a flexible, easy-to-use game framework that leverages Pygame for creating side-scrolling platformers and other kinds of 2D games.

![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey)

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License, which allows you to share and adapt the material for non-commercial purposes as long as you provide appropriate attribution and share any adaptations under the same license.  
For more information, see [CC BY-NC-SA 4.0 License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Features
Skytree uses Pygame to render 2D graphics, play audio and read user inputs. At the moment, only keyboard inputs are supported.
The engine abstracts the game loop from the user, provides a standard structure for active game objects and a way to manage game resources.
Objects are generally constructed by combining basic features (e.g., Drawable, Updateable) via multiclassing and can be connected or disconnected
ultimately to a game manager singleton object in order to make them active or inactive.
Drawable objects provide methods to manipulate their draw order and alignment, and there is a frame-by-frame animation system.
Skytree features a collision detection-response system with support for different shaped hitboxes.
User inputs are translated to string commands that can be interpreted by the game objects.
There is a system of classes dedicated to modeling game entities and spaces, with a focus on sidescrolling platformers.

## Installation

### Install via pip

The easiest way to install Skytree is through pip:

```
pip install skytree
```

### Dependencies

Skytree requires `pygame` version 2.6. When you install via pip, this will be handled automatically.

## Basic example

Setting up a controllable character in a blank space:

```Python
#######################################
# FIRST STEP: SET UP THE GAME MANAGER #
#######################################

# Import any Pygame constant you want to use.
from pygame.locals import K_a, K_w, K_d, K_s, K_LEFT, K_UP, K_RIGHT, K_DOWN, K_ESCAPE, K_RETURN, KEYUP, KEYDOWN

# Import configuration file, game manager and any event controller you need.
from skytree import config
from skytree.game import Game
from skytree.key_commands import KeyboardReader

# Set configurations (see skytree.config for details).
# In this particular example, we'll stay with default resolution (256 x 240),
# but we'll scale the window by x2.
config.WINDOW_MAGNIFY = 2
# In this example, we'll use Skytree resources; you can set up your own resource folder paths with:
#     config.[FILE | IMG | FONT | MUSIC | SOUND]_PATH = [desired_path]
# Or just:
#     config.set_all_paths([desired_path])

# Define key bindings for keyboard controller.
# We'll use arrows / WASD for movement, plus ESC / ENTER for pausing
# (a default pause state will be created automatically).
keyboard_reader = KeyboardReader({
    **{key: "left" for key in (K_a, K_LEFT)},
    **{key: "up" for key in (K_w, K_UP)},
    **{key: "right" for key in (K_d, K_RIGHT)},
    **{key: "down" for key in (K_s, K_DOWN)},
    K_ESCAPE: "esc",
    K_RETURN: "enter"
    })

# Instantiate the game manager.
game = Game()
    
# Bind event controllers to the game manager.
for event in (KEYUP, KEYDOWN):
    game.set_event_controller(event, keyboard_reader)

#######################################
# SECOND STEP: SET UP EVERYTHING ELSE #
#######################################

# Import whatever else you need.
# We'll import a simple board and an omnidirectional moving player-controlled sprite.
# We'll also need to define a TileSet.
from skytree.tileset import TileSet
from skytree.boards import Board
from skytree.sprites import TopDownPlayer

# You could actually do the whole next part with an one-liner, but let's break it down for clarity:

# Constructing the player tileset:
#     canvas: a valid image path in the resource folder.
#         --you could also just input dimensions (width, height) to generate a blank surface and draw on it later using Pygame functions.
#     tile_dim: you need to tell the TileSet the dimensions of each tile in the image.
player_tileset = TileSet(canvas = "player.png", tile_dim=(16, 24))

# Animation dictionary for the player
# Each entry has the name of an animation as a key pointing to a collection of values.
# Each of those values consists on a tile index for the tile set, and an amount of frames for that image to be drawn.
# Animation names are hard-coded in the objects that use them (see sprites module documentation for reference)
player_anims = td_player_anims = {
        "idle_right": ((0,20), (1,1)),
        "walk_right": ((2,1), (0,1), (3,1), (0,1)),
        "idle_left": ((7,20), (8,1)),
        "walk_left": ((9,1), (7,1), (10,1), (7,1)),
        "idle_up": ((25,float("inf")),),
        "walk_up": ((26,1), (25,1), (27,1), (25,1)),
        "idle_down": ((21,20), (22,1)),
        "walk_down": ((23,1), (21,1), (24,1), (21,1)),
        "idle_right_up": ((32,float("inf")),),
        "walk_right_up": ((33,1), (32,1), (34,1), (32,1)),
        "idle_right_down": ((28,20), (29,1)),
        "walk_right_down": ((30,1), (28,1), (31,1), (28,1)),
        "idle_left_up": ((39,float("inf")),),
        "walk_left_up": ((40,1), (39,1), (41,1), (39,1)),
        "idle_left_down": ((35,20), (36,1)),
        "walk_left_down": ((37,1), (35,1), (38,1), (35,1))
        }

# Among other ways of controlling object position, you can set it on instantiation.
# Any data set on instantiation will be persistent (meaning that if the object is
#     ever reset, it will recover its initial state by default).
player_starting_pos = (120, 108)

# Using these variables to create the player-controlled sprite.
topdown_player = TopDownPlayer(tileset=player_tileset, pos=player_starting_pos, anims=player_anims)

# Setting up the board.
#     name: by giving a board a name, it will automatically become available as a game state on instantiation.
#     border_policies: what happens by default when a sprite collides with the frame borders.
#         We'll set this one for screen wrap because that's fun.
#     music: self-explanatory. Try also skytree_groove.org or skytree_bounce.org if you want!
#     entities: a collection of entities to be added to the level on instantiation (just one for this example).
#     first_state: setting this as True will connect the board to the game mannager on instantiation.
# You'll notice a blue background. This is a default; you can change it by assigning
#     config.BOARD_BGCOLOR = ([0-255], [0-255], [0-255]) before instantiating the board.
Board(name="simple", border_policies="wrap", music="skytree_bask.ogg", entities=(topdown_player,), first_state=True)

#############################
# THIRD STEP: RUN THE GAME! #
#############################

game.run()
```
