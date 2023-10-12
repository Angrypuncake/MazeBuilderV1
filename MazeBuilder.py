import tkinter as tk
import math
from tkinter import filedialog
from enum import Enum

# optional for copy code to clipboard
#import pyperclip

wall_list = []

class Commands(Enum):
    DELETE = 1
    PLACE = 2
    DELETE_ALL = 3
    

def rotate_point(x, y, angle, origin_x, origin_y):
    angle_rad = math.radians(angle)
    dx = x - origin_x
    dy = y - origin_y
    new_x = origin_x + dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
    new_y = origin_y + dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
    return new_x, new_y

def calculate_rotated_corners(x, y, width, height, angle):
    # Calculate the center of the rectangle
    cx, cy = x + width / 2, y + height / 2

    # Calculate all four corners of the rectangle
    corners = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]

    # Rotate each corner point
    rotated_corners = [rotate_point(px, py, angle, cx, cy) for px, py in corners]

    # Flatten the list of rotated corners
    flat_corners = [coord for point in rotated_corners for coord in point]
    
    return flat_corners

def on_drag(event):
    snap_scale = snap_scale_var.get()
    x, y = event.x - event.x % snap_scale, event.y - event.y % snap_scale
    canvas.coords(tk.CURRENT, x, y, x + width_var.get(), y + height_var.get())


def on_move(event):
    snap_scale = snap_scale_var.get()
    x, y = event.x - event.x % snap_scale, event.y - event.y % snap_scale
    new_width = width_scale.get()
    new_height = height_scale.get()
    angle = angle_var.get()

    # Calculate the center of the rectangle
    cx, cy = x + new_width / 2, y + new_height / 2

    # Calculate all four corners of the rectangle
    corners = [(x, y), (x + new_width, y), (x + new_width, y + new_height), (x, y + new_height)]

    # Rotate each corner point
    rotated_corners = [rotate_point(px, py, angle, cx, cy) for px, py in corners]

    # Flatten the list of rotated corners
    flat_corners = [coord for point in rotated_corners for coord in point]

    # Update the preview polygon
    canvas.coords("preview", *flat_corners)
    canvas.tag_raise("preview")
    canvas.update()

def generate_code():
    print("Generate Code Called")  # Debugging line
    with open("wall_code.txt", "w") as f:
        for index, wall in enumerate(wall_list):
            f.write(f"insertAndSetFirstWall(&head, {index}, {wall['x']}, {wall['y']}, {wall['width']}, {wall['height']});\n")
            
root = tk.Tk()
root.title("Wall Placement GUI")
angle_var = tk.IntVar()
snap_scale_var = tk.IntVar(value=10)  # Default value is 50
instance_counter = 0
canvas_to_wall_mapping = {}

canvas_frame = tk.Frame(root)
canvas_frame.pack(side="left", fill="both", expand=True)

listbox_frame = tk.Frame(root)
listbox_frame.pack(side="right", fill="both")

canvas = tk.Canvas(canvas_frame, bg="white", height=640, width=480)
canvas.pack()

# Create a Listbox for instances
instance_listbox = tk.Listbox(root)
instance_listbox = tk.Listbox(root, width=30)  # Adjust the width as needed
instance_listbox.pack(side="right", fill="both")


canvas.create_polygon(1, 1, 1, 1, 1, 1, 1, 1, outline="blue", tags="preview")

canvas.bind("<Motion>", on_move)

width_var = tk.IntVar(value=50)
height_var = tk.IntVar(value=50)


# CHECKBOX FOR MAZE_MIDDLE FUNCTION
list_for_checkbox_lines = []
def show_maze_middle_checkbox_function():
    # get the current canvas width and height
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # calculate the middle points of the canvas
    mid_x = canvas_width / 2
    mid_y = canvas_height / 2

    # get the current value of the checkbox
    value = checkbox_var.get()

    # if the value is "Checked":
    #           create two thin black polygons in the 
    #           middle of the canvas using create_polygon method
    # Else:
    #           delete lines
    if value == "Checked":
        # size of line is 1
        horizontal_id = canvas.create_polygon(
            0, mid_y - 0.5,
            0, mid_y + 0.5,
            canvas_width, mid_y + 0.5,
            canvas_width, mid_y - 0.5,
            fill="black",
        )
        vertical_id = canvas.create_polygon(
            mid_x - 0.5, 0,
            mid_x + 0.5, 0,
            mid_x + 0.5, canvas_height,
            mid_x - 0.5, canvas_height,
            fill="black",
        )
        list_for_checkbox_lines.append(horizontal_id)
        list_for_checkbox_lines.append(vertical_id)
    else:
        # delete lines
        for line in list_for_checkbox_lines:
            canvas.delete(line)
checkbox_var = tk.StringVar()
show_maze_middle_checkbox = tk.Checkbutton(
    root, 
    text="Show Maze Middle",
    command=show_maze_middle_checkbox_function,
    variable=checkbox_var, onvalue="Checked", offvalue="Unchecked")
show_maze_middle_checkbox.pack()


width_scale = tk.Scale(root, from_=1, to=500, orient="horizontal", label="Width", variable=width_var)
width_scale.pack()

width_spinbox = tk.Spinbox(root, from_=1, to=500, textvariable=width_var)
width_spinbox.pack()

height_scale = tk.Scale(root, from_=1, to=500, orient="horizontal", label="Height", variable=height_var)
height_scale.pack()

height_spinbox = tk.Spinbox(root, from_=1, to=500, textvariable=height_var)
height_spinbox.pack()

#rotation_scale = tk.Scale(root, from_=0, to=360, orient="horizontal", label="Rotation", variable=angle_var)
#rotation_scale.pack()

# Create sliders for canvas width and height
canvas_width_var = tk.IntVar(value=640)
canvas_height_var = tk.IntVar(value=480)

canvas_width_scale = tk.Scale(root, from_=1, to=2000, orient="horizontal", label="Canvas Width", variable=canvas_width_var)
canvas_width_scale.pack()

canvas_height_scale = tk.Scale(root, from_=1, to=2000, orient="horizontal", label="Canvas Height", variable=canvas_height_var)
canvas_height_scale.pack()

def validate_canvas_size_input(P):
    try:
        # Try to convert the input to an integer
        value = int(P)
        # Check if the value is within the desired range (100 to 2000)
        if 100 <= value <= 2000:
            return True
        else:
            return False
    except ValueError:
        # If the input is not a valid integer, accept it for editing
        return True


canvas_width_spinbox = tk.Spinbox(root, from_=1, to=2000, textvariable=canvas_width_var)
canvas_width_spinbox.pack()
canvas_height_spinbox = tk.Spinbox(root, from_=1, to=2000, textvariable=canvas_height_var)
canvas_height_spinbox.pack()

# Function to update canvas size
def update_canvas_size(*args):
    try:
        canvas_width = int(canvas_width_var.get())
        canvas_height = int(canvas_height_var.get())
        # Ensure canvas size is within the desired range
        canvas_width = min(2000, max(1, canvas_width))
        canvas_height = min(2000, max(1, canvas_height))
    except ValueError:  # Handle the case where get() returns an empty string or invalid value
        canvas_width = 500  # Default value
        canvas_height = 500  # Default value

    canvas.config(width=canvas_width, height=canvas_height)

def set_canvas_size():
    try:
        canvas_width = int(canvas_width_var.get())
        canvas_height = int(canvas_height_var.get())
    except ValueError:
        # Handle the case where get() returns an empty string or invalid value
        canvas_width = 500  # Default value
        canvas_height = 500  # Default value

    canvas.config(width=canvas_width, height=canvas_height)

# Set the canvas size originally to 640, 480
set_canvas_size()

set_canvas_size_button = tk.Button(root, text="Set Canvas Size", command=set_canvas_size)
set_canvas_size_button.pack()

generate_button = tk.Button(root, text="Generate Code", command=generate_code)
generate_button.pack()

snap_scale = tk.Scale(root, from_=1, to=100, orient="horizontal", label="Snap Scale", variable=snap_scale_var)
snap_scale.pack()

deleted_zone = [] # past deleted walls, used to restore when deleted (Stored as tuple of canvas_id and wall data)
commands_list: list[Commands] = [] # past commands, used when doing Ctrl+Z
undoed_commands: list[Commands] = [] # commands that have been undone, used when doing Ctrl+Y

canvas_ids = []
def delete_instance():
    global instance_counter
    selected = instance_listbox.curselection()
    if selected:
        index = selected[0]
        if index < len(canvas_ids):  # Check if the index is within the canvas_ids list
            canvas_id = canvas_ids[index]
            wall_data = canvas_to_wall_mapping.get(canvas_id)
            if wall_data:
                deleted_zone.append(wall_data)
                canvas.delete(canvas_id)
                canvas_ids.pop(index)  # Remove the canvas ID from the list
                wall_list.pop(index)  # Remove the wall data.
                del canvas_to_wall_mapping[canvas_id]

                # Update the instance IDs in the listbox after deletion
                instance_listbox.delete(index)
                instance_counter -= 1
                commands_list.append(Commands.DELETE)
                update_listbox()  # Update the listbox to reflect the changes
        else:
            print("Index out of range: ", index)  # Debugging line


def undo_last_command(event):
    # Basic code for Ctrl + Z functioning based on above code
    global instance_counter
    global commands_list
    # Check if there are any commands to undo
    if commands_list: 
        # Get the last command
        last_command = commands_list.pop(-1)
        if (last_command == Commands.PLACE and canvas_ids): # If the last action was to place something, and then check if there's anything on the canvas to delete.
            canvas_id = canvas_ids[-1] # Grab the last block.
            # Copy paste of the above code
            wall_data = canvas_to_wall_mapping.get(canvas_id)
            if wall_data:
                # Store the block in the deleted zone for restoration if needed.
                undoed_commands.append(last_command)
                deleted_zone.append(wall_data)
                
                canvas.delete(canvas_id)
                del canvas_ids[-1]  # Remove the canvas ID from the list
                del wall_list[-1]
                del canvas_to_wall_mapping[canvas_id]

                # Update the instance IDs in the listbox after deletion
                instance_listbox.delete(-1)
                instance_counter -= 1
                update_listbox()  # Update the listbox to reflect the changes
        elif (last_command == Commands.DELETE and deleted_zone): # If the last action was to delete something, check if there's anything in the deleted zone to restore.
            deleted_wall = deleted_zone.pop(-1) # Grab the last deleted wall.
            # Add it back into the canvas
            angle = angle_var.get()
            flat_corners = calculate_rotated_corners(deleted_wall['x'], deleted_wall['y'], deleted_wall['width'], deleted_wall['height'], angle)
            rect = canvas.create_polygon(*flat_corners, fill="blue", tags="draggable")
            
            canvas_ids.append(rect)
            wall_list.append(deleted_wall)
            canvas_to_wall_mapping[rect] = deleted_wall
            instance_data = f"Instance {instance_counter}: X={deleted_wall['x']}, Y={deleted_wall['y']}, Width={deleted_wall['width']}, Height={deleted_wall['height']}"
            instance_listbox.insert(tk.END, instance_data)
            instance_counter += 1
            print(f"Re-added canvas ID {rect} to canvas_ids")
            undoed_commands.append(last_command)
            update_listbox() # Update the listbox to reflect the change.
        elif (last_command == Commands.DELETE_ALL and deleted_zone): # If the last action was to clear the board, check if there's anything inside the deleted zone.
            deleted_walls = deleted_zone.pop(-1) # Grab the last walls deleted.
            for deleted_wall in deleted_walls:
                angle = angle_var.get()
                flat_corners = calculate_rotated_corners(deleted_wall['x'], deleted_wall['y'], deleted_wall['width'], deleted_wall['height'], angle)
                rect = canvas.create_polygon(*flat_corners, fill="blue", tags="draggable")
                
                canvas_ids.append(rect)
                wall_list.append(deleted_wall)
                canvas_to_wall_mapping[rect] = deleted_wall
                instance_data = f"Instance {instance_counter}: X={deleted_wall['x']}, Y={deleted_wall['y']}, Width={deleted_wall['width']}, Height={deleted_wall['height']}"
                instance_listbox.insert(tk.END, instance_data)
                instance_counter += 1
                print(f"Re-added canvas ID {rect} to canvas_ids")
            undoed_commands.append(last_command)
            update_listbox() # update the listbox to reflect the change.
                
            

root.bind('<Control-z>', undo_last_command)

def update_listbox():
    instance_listbox.delete(0, tk.END)
    for i, wall_data in enumerate(wall_list):
        instance_info = f"Instance {i}: X={wall_data['x']}, Y={wall_data['y']}, Width={wall_data['width']}, Height={wall_data['height']}"
        instance_listbox.insert(tk.END, instance_info)


delete_button = tk.Button(root, text="Delete Selected", command=delete_instance)
delete_button.pack()

def highlight_instance(event):
    selected_index = instance_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        if index < len(canvas_ids):  # Check if the index is within the canvas_ids list
            # Remove highlight from all instances
            remove_highlight()
            
            canvas_id = canvas_ids[index]
            canvas.itemconfig(canvas_id, outline="red", width=2)  # Highlight with a red outline
        else:
            print("Index out of range: ", index)  # Debugging line

def remove_highlight():
    for canvas_id in canvas_ids:
        canvas.itemconfig(canvas_id, outline="blue")  # Reset the outline to blue   

# Bind the function to canvas click event
def on_click_and_add_instance(event):
    global instance_counter 
    angle = angle_var.get()
    snap_scale = snap_scale_var.get()
    x, y = event.x - event.x % snap_scale, event.y - event.y % snap_scale
    width, height = width_var.get(), height_var.get()
    flat_corners = calculate_rotated_corners(x, y, width, height, angle)
    rect = canvas.create_polygon(*flat_corners, fill="blue", tags="draggable")
    canvas_ids.append(rect)  # Append the canvas ID for the new instance
    print(f"Added canvas ID {rect} to canvas_ids")

    instance_id = instance_counter  # Start instance_id at 0
    
    wall_data = {
        'x': x,
        'y': y,
        'width': width,
        'height': height,
    }
    wall_list.append(wall_data)


    # Store the mapping of canvas ID to wall data
    canvas_to_wall_mapping[rect] = wall_data
    
    # Update the listbox with instance information
    instance_info = f"Instance {instance_id}: X={x}, Y={y}, Width={width}, Height={height}"
    instance_listbox.insert(tk.END, instance_info)  # Insert the instance information as a new item
    instance_counter += 1
    commands_list.append(Commands.PLACE)
    
def parse_wall_data(line):
    # Remove leading and trailing whitespaces and remove the trailing semicolon
    line = line.strip().rstrip(";")

    # Split the line into components using comma as the delimiter
    components = line.split(',')

    if len(components) == 6:
        try:
            print(f"Components: {components}")
            print(f"Height Value: {components[5].strip()}")
            index = int(components[1].strip())  # Extract the index as an integer
            
            x = int(components[2].strip())      # Extract x as an integer
            
            y = int(components[3].strip())      # Extract y as an integer
            width = int(components[4].strip())  # Extract width as an integer
            height_value = components[5].strip().rstrip(")")
            height = int(''.join(filter(str.isdigit, height_value)))

            return {
                'index': index,
                'x': x,
                'y': y,
                'width': width,
                'height': height
            }
        except ValueError:
            # Handle any potential conversion errors here
            print(f"Error parsing line: {line}")
            return None
    else:
        print(f"Invalid line format: {line}")
        return None



def upload_and_generate_walls():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        create_instances_from_file(file_path)

def create_instances_from_file(file_path):
    global instance_counter
    with open(file_path, "r") as file:
        for line in file:
            wall_data = parse_wall_data(line)
            if wall_data:
                index = wall_data['index']
                x, y, width, height = wall_data['x'], wall_data['y'], wall_data['width'], wall_data['height']
                flat_corners = calculate_rotated_corners(x, y, width, height, angle_var.get())
                rect = canvas.create_polygon(*flat_corners, fill="blue", tags="draggable")
                canvas_ids.append(rect)  # Append the canvas ID for the new instance

                wall_list.append(wall_data)

                # Store the mapping of canvas ID to wall data
                canvas_to_wall_mapping[rect] = wall_data

                # Update the listbox with instance information
                instance_info = f"Instance {index}: X={x}, Y={y}, Width={width}, Height={height}"
                instance_listbox.insert(tk.END, instance_info)  # Insert the instance information as a new item
                # Update instance_counter based on the index of loaded instances
                instance_counter = max(instance_counter, index + 1)

    
def delete_all_instances():
    global instance_counter
    instance_listbox.delete(0, tk.END)  # Delete all items from the listbox
    deleted_zone.append(tuple(wall_list)) # Sends every wall to the deleted zone for restoration.
    for canvas_id in canvas_ids:  # Loop through all stored canvas IDs
        canvas.delete(canvas_id)  # Delete each instance from the canvas
    canvas_ids.clear()  # Clear the list of canvas IDs
    wall_list.clear()  # Clear the wall list
    instance_counter = 0
    global commands_list
    commands_list.append(Commands.DELETE_ALL) # Adds a DELETE_ALL to the commands list.

button_frame = tk.Frame(root)
button_frame.pack(side="bottom")

# Create the "Delete All Instances" button and place it in the button frame
delete_all_button = tk.Button(button_frame, text="Delete All Instances", command=delete_all_instances)
delete_all_button.pack(side="left")

def on_canvas_click(event):
    # Remove previous highlight and deselect listbox
    remove_highlight()
    instance_listbox.selection_clear(0, tk.END)
    
    # Add the code to create a new instance here (your existing on_click_and_add_instance code)
    global instance_counter 
    angle = angle_var.get()
    snap_scale = snap_scale_var.get()
    x, y = event.x - event.x % snap_scale, event.y - event.y % snap_scale
    width, height = width_var.get(), height_var.get()
    flat_corners = calculate_rotated_corners(x, y, width, height, angle)
    rect = canvas.create_polygon(*flat_corners, fill="blue", tags="draggable")
    canvas_ids.append(rect)  # Append the canvas ID for the new instance
    print(f"Added canvas ID {rect} to canvas_ids")

    instance_id = instance_counter  # Start instance_id at the current instance_counter value
    
    wall_data = {
        'x': x,
        'y': y,
        'width': width,
        'height': height,
    }
    wall_list.append(wall_data)

    # Store the mapping of canvas ID to wall data
    canvas_to_wall_mapping[rect] = wall_data
    
    # Update the listbox with instance information
    instance_info = f"Instance {instance_id}: X={x}, Y={y}, Width={width}, Height={height}"
    instance_listbox.insert(tk.END, instance_info)  # Insert the instance information as a new item
    
    instance_counter += 1  # Increment instance_counter for the next instance

    # Highlight the selected instance
    canvas.itemconfig(rect, outline="red", width=2)  # Highlight with a red outline
    commands_list.append(Commands.PLACE) # Add a place command to the command list.
    canvas.update()
    


canvas.bind("<Button-1>", on_canvas_click)
instance_listbox.bind('<<ListboxSelect>>', highlight_instance)
upload_button = tk.Button(root, text="Upload Wall Data", command=upload_and_generate_walls)
upload_button.pack()

# Copy code to clipboard
def copy_file_to_clipboard(event=None):
    generate_code()
    with open('wall_code.txt', 'r') as file:
        text = file.read()
    pyperclip.copy(text)
    pyperclip.paste()

button = tk.Button(root, text="Copy to Clipboard", command=copy_file_to_clipboard)
button.pack()
root.bind('<Control-c>', copy_file_to_clipboard)

root.mainloop()
