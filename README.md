# MazeBuilderFork
A mazebuilder GUI, but with a few additional QOL-tweaks. This version features a fully-functional undo system, alongside rotating blocks.

## How to Use
- Make sure python version is fully updated
- Run the WallGui.py program using `python WallGui.py`
- Set your canvas size
- Click on the screen to place a wall
- Customise the wall using the width and height sliders
- Click GENERATE CODE to generate a txt file "wall_code.txt" of code you can copy and paste into your main.c
- The txt file will be in the directory next to the WallGUI.py file

The contents of the txt file will kinda look like 
```C
insertAndSetFirstWall(&head, 0, 625, 375, 10, 100);
insertAndSetFirstWall(&head, 1, 535, 465, 100, 10);
// and so on...
```

### Selecting & Deleting
- Select any of the instances listed on the right. It'll highlight the corresponding wall on the screen so you know what walls you are about to delete. 
- After selecting an instance and the corresponding wall is highlighted, click the 'Delete selected' button.

### Rotating
- The block that you are currently holding can be rotated with `r`. This will swap its width and height. Useful for quickly building walls.

### Undo 
- Ctrl + Z will undo the last action, if it was to delete a block, it will restore the deleted block. If it was to place a block, it will then delete the block.
- Re-doing (using Ctrl + y) will be added soon.

### Loading
- If you want to load your own walls to the editor, use the UPLOAD DATA BUTTON. This takes a txt file containing examples like:
```C
insertAndSetFirstWall(&head, 0, 625, 375, 10, 100);
insertAndSetFirstWall(&head, 1, 535, 465, 100, 10);
insertAndSetFirstWall(&head, 2, 445, 465, 100, 10);
// etc...
```
## TROUBLESHOOTING

#### Uploaded maze is not fitting 
- Make sure to set your canvas width and height first 

#### Blocks arent being placed down 
- Try keeping the GUI windowed and not FULLSCREEN. 

#### Uploaded file is not being read; 
- the txt file must be in the exact format as the output file. Containing only lines of
```C
insertAndSetFirstWall(&head, 0, 625, 375, 10, 100);
insertAndSetFirstWall(&head, 1, 535, 465, 100, 10);
```

### Blocks are hard to match up or align
- Adjust the snap scale to 5, 10 or 15

## Contributors
Original code written by Elvis Nguyen with assistance from chatGPT 4


Modified by Isa


[Mudit-B](https://github.com/Mudit-B) - Provided Added Ctrl + Z, Clipboard functionality and fixed various issues

