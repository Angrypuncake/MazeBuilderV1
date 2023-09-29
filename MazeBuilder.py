import tkinter as tk
import math
from tkinter import filedialog

# optional for copy code to clipboard
#import pyperclip

wall_list = []

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
snap_scale_var = tk.IntVar(value=10)  # Default value is 10
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

width_scale = tk.Scale(root, from_=1, to=200, orient="horizontal", label="Width", variable=width_var)
width_scale.pack()

width_spinbox = tk.Spinbox(root, from_=1, to=200, textvariable=width_var)
width_spinbox.pack()

height_scale = tk.Scale(root, from_=1, to=200, orient="horizontal", label="Height", variable=height_var)
height_scale.pack()

height_spinbox = tk.Spinbox(root, from_=1, to=200, textvariable=height_var)
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
                canvas.delete(canvas_id)
                del canvas_ids[index]  # Remove the canvas ID from the list
                del wall_list[index]
                del canvas_to_wall_mapping[canvas_id]
                
                # Update the instance IDs in the listbox after deletion
                instance_listbox.delete(index)
                instance_counter -= 1
                update_listbox()  # Update the listbox to reflect the changes
        else:
            print("Index out of range: ", index)  # Debugging line

def delete_last_instance(event):
    # Basic code for Ctrl + Z functioning based on above code
    global instance_counter
    # Check if there are any instances to delete
    if canvas_ids: 
        # Get the index of the last instance
        index = len(canvas_ids) - 1
        # Get the last instance
        canvas_id = canvas_ids[index]
        # Copy paste of the above code
        wall_data = canvas_to_wall_mapping.get(canvas_id)
        if wall_data:
            canvas.delete(canvas_id)
            del canvas_ids[index]  # Remove the canvas ID from the list
            del wall_list[index]
            del canvas_to_wall_mapping[canvas_id]

            # Update the instance IDs in the listbox after deletion
            instance_listbox.delete(index)
            instance_counter -= 1
            update_listbox()  # Update the listbox to reflect the changes

root.bind('<Control-z>', delete_last_instance)

def update_listbox():
    instance_listbox.delete(0, tk.END)
    for i, wall_data in enumerate(wall_list):
        instance_info = f"Instance {i}: X={wall_data['x']}, Y={wall_data['y']}, Width={wall_data['width']}, Height={wall_data['height']}, Angle={wall_data['angle']}"
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
        'angle': angle
    }
    wall_list.append(wall_data)


    # Store the mapping of canvas ID to wall data
    canvas_to_wall_mapping[rect] = wall_data
    
    # Update the listbox with instance information
    instance_info = f"Instance {instance_id}: X={x}, Y={y}, Width={width}, Height={height}, Angle={angle}"
    instance_listbox.insert(tk.END, instance_info)  # Insert the instance information as a new item
    instance_counter += 1
    
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


    
def delete_all_instances():
    global instance_counter
    instance_listbox.delete(0, tk.END)  # Delete all items from the listbox
    for canvas_id in canvas_ids:  # Loop through all stored canvas IDs
        canvas.delete(canvas_id)  # Delete each instance from the canvas
    canvas_ids.clear()  # Clear the list of canvas IDs
    wall_list.clear()  # Clear the wall list
    instance_counter = 0 

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

    instance_id = instance_counter  # Start instance_id at 0
    
    wall_data = {
        'x': x,
        'y': y,
        'width': width,
        'height': height,
        'angle': angle
    }
    wall_list.append(wall_data)

    # Store the mapping of canvas ID to wall data
    canvas_to_wall_mapping[rect] = wall_data
    
    # Update the listbox with instance information
    instance_info = f"Instance {instance_id}: X={x}, Y={y}, Width={width}, Height={height}, Angle={angle}"
    instance_listbox.insert(tk.END, instance_info)  # Insert the instance information as a new item
    instance_counter += 1

    # Highlight the selected instance
    canvas.itemconfig(rect, outline="red", width=2)  # Highlight with a red outline
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
