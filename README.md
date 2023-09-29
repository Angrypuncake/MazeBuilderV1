# MazeBuilderV1
A mazebuilder algo because too lazy to make maze myself

#Despite being a relatively simple GUI, this is the first time I've developed a functional GUI so ChatGPT was a massive help in guiding me through using tkinter
#The code is not perfect, it is just a basic tool for you to creatively explore maze building because its a massive hassle to hardcode massive/complex mazes

"""
HOW TO USE
- Make sure python version is fully updated
- Run the WallGui.py program using any IDE like VSCODE
- Set your canvas size
- Click on the screen to place a wall
- Customise the wall using the width and height sliders
- Click GENERATE CODE to generate a txt file "wall_code.txt" of code you can copy and paste into your main.c
-The txt file will be in the directory next to the WallGUI.py file

the contents of the txt file will kinda look like 
insertAndSetFirstWall(&head, 0, 625, 375, 10, 100);
insertAndSetFirstWall(&head, 1, 535, 465, 100, 10);

SELECTING & DELETING
- To select a wall for deletion, click on the instance on the right instances list
- Then click delete selected 
- To clear the screen, press delete all instances.
- If you want to upload your own walls to the editor, use the UPLOAD DATA BUTTON. This takes a txt file containing examples like:

insertAndSetFirstWall(&head, 0, 625, 375, 10, 100);
insertAndSetFirstWall(&head, 1, 535, 465, 100, 10);
insertAndSetFirstWall(&head, 2, 445, 465, 100, 10);

TROUBLESHOOTING

Uploaded maze is not fitting 
- Make sure to set your canvas width and height first 

Blocks arent being placed down 
- Try keeping the GUI windowed and not FULLSCREEN. 

Uploaded file is not being read; 
the txt file must be in the exact format as the output file. Containing only lines of 
insertAndSetFirstWall(&head, 0, 625, 375, 10, 100);
insertAndSetFirstWall(&head, 1, 535, 465, 100, 10);

Blocks are hard to match up or align
- Adjust the snap scale to 5, 10 or 15

"""

#Code written by Elvis Nguyen with assistance from chatGPT 4

## Contributors
[Mudit-B](https://github.com/Mudit-B) - Provided Added Ctrl + Z, Clipboard functionality and fixed various issues

