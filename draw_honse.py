"""
This script draws a parameterized horse (honse) using the PIL (Pillow) library.
It can create horses with various body shapes, leg lengths, mane styles, and more.
"""

from PIL import Image, ImageDraw
import numpy as np
import random
import os

def draw_honse(draw, center_x, center_y, params=None, size_factor=1.0):
    """
    Draw a parameterized horse at the specified position with given parameters.
    
    Args:
        draw: ImageDraw object to draw on
        center_x: x-coordinate of the horse's center
        center_y: y-coordinate of the horse's center
        params: dictionary of parameters to customize the horse appearance
        size_factor: scaling factor for the horse (1.0 is original size)
    
    Returns:
        A dictionary of the parameters used (for reference)
    """
    # Default parameters
    default_params = {
        # Body parameters
        "body_length": 1.0,        # Relative body length (1.0 is default)
        "body_height": 1.0,        # Relative body height
        "neck_length": 1.0,        # Relative neck length
        "neck_thickness": 1.0,     # Relative neck thickness
        "head_size": 1.0,          # Relative head size
        "leg_length": 1.0,         # Relative leg length
        "leg_thickness": 1.0,      # Relative leg thickness
        "tail_length": 1.0,        # Relative tail length
        "tail_thickness": 1.0,     # Relative tail thickness
        "mane_length": 1.0,        # Relative mane length
        "mane_density": 1.0,       # Relative mane density (number of strands)
        
        # Color parameters (RGB values)
        "body_color": (139, 69, 19),    # Brown
        "mane_color": (51, 25, 0),      # Dark brown
        "eye_color": (0, 0, 0),         # Black
        
        # Pose parameters
        "head_angle": 0,           # Head angle in degrees (0 is straight)
        "neck_angle": 0,           # Neck angle in degrees
        "tail_angle": 45,          # Tail angle in degrees
        "leg_pose": "standing",    # "standing", "walking", "running", "rearing"
        
        # Style parameters
        "mane_style": "flowing",   # "flowing", "short", "mohawk", "braided"
        "tail_style": "flowing",   # "flowing", "short", "braided"
        "eye_style": "normal",     # "normal", "cartoon", "realistic"
    }
    
    # Use provided parameters or defaults
    if params is None:
        params = {}
    
    # Merge provided parameters with defaults
    for key in default_params:
        if key not in params:
            params[key] = default_params[key]
    
    # Base dimensions
    base_body_length = 200 * params["body_length"] * size_factor
    base_body_height = 80 * params["body_height"] * size_factor
    base_neck_length = 100 * params["neck_length"] * size_factor
    base_neck_thickness = 40 * params["neck_thickness"] * size_factor
    base_head_size = 60 * params["head_size"] * size_factor
    base_leg_length = 120 * params["leg_length"] * size_factor
    base_leg_thickness = 15 * params["leg_thickness"] * size_factor
    
    # Body position
    body_left = center_x - base_body_length/2
    body_top = center_y - base_body_height/2
    body_right = body_left + base_body_length
    body_bottom = body_top + base_body_height
    
    # Draw body (oval)
    draw.ellipse([body_left, body_top, body_right, body_bottom], fill=params["body_color"])
    
    # Calculate neck start position (on the body)
    neck_start_x = body_left + base_body_length * 0.8
    neck_start_y = body_top + base_body_height * 0.3
    
    # Calculate neck angle in radians
    neck_rad = np.radians(params["neck_angle"])
    
    # Calculate neck end position
    neck_end_x = neck_start_x + np.sin(neck_rad) * base_neck_length
    neck_end_y = neck_start_y - np.cos(neck_rad) * base_neck_length
    
    # Draw neck - thicker and blockier
    # We'll use a polygon to represent the neck
    neck_width = base_neck_thickness * 0.8  # Increased width for thicker neck
    neck_angle_perp = neck_rad + np.pi/2  # Perpendicular to neck angle
    
    # Calculate the four corners of the neck polygon
    nx1 = neck_start_x + np.cos(neck_angle_perp) * neck_width
    ny1 = neck_start_y + np.sin(neck_angle_perp) * neck_width
    nx2 = neck_start_x - np.cos(neck_angle_perp) * neck_width
    ny2 = neck_start_y - np.sin(neck_angle_perp) * neck_width
    nx3 = neck_end_x - np.cos(neck_angle_perp) * (neck_width * 0.9)  # Less narrowing at the top
    ny3 = neck_end_y - np.sin(neck_angle_perp) * (neck_width * 0.9)
    nx4 = neck_end_x + np.cos(neck_angle_perp) * (neck_width * 0.9)
    ny4 = neck_end_y + np.sin(neck_angle_perp) * (neck_width * 0.9)
    
    # Draw the neck
    draw.polygon([(nx1, ny1), (nx2, ny2), (nx3, ny3), (nx4, ny4)], fill=params["body_color"])
    
    # Calculate head angle in radians (relative to neck)
    head_rad = neck_rad + np.radians(params["head_angle"])
    
    # Head position (at the end of the neck)
    head_center_x = neck_end_x + np.sin(head_rad) * (base_head_size * 0.3)
    head_center_y = neck_end_y - np.cos(head_rad) * (base_head_size * 0.3)
    
    # Draw head with longer nose
    # Main head part (oval)
    head_width = base_head_size
    head_height = base_head_size * 0.7
    head_left = head_center_x - head_width/2
    head_top = head_center_y - head_height/2
    head_right = head_center_x + head_width/2
    head_bottom = head_center_y + head_height/2
    
    # Draw the main head oval
    draw.ellipse([head_left, head_top, head_right, head_bottom], fill=params["body_color"])
    
    # Add elongated nose/muzzle
    nose_length = base_head_size * 0.9  # Longer nose
    nose_width = base_head_size * 0.4
    nose_angle = head_rad  # Same angle as head
    
    # Calculate nose end point
    nose_end_x = head_center_x + np.cos(nose_angle) * nose_length
    nose_end_y = head_center_y + np.sin(nose_angle) * nose_length
    
    # Draw nose as elongated oval
    nose_left = nose_end_x - nose_width/2
    nose_top = nose_end_y - nose_width/3
    nose_right = nose_end_x + nose_width/2
    nose_bottom = nose_end_y + nose_width/3
    
    # Create points for a polygon connecting head to nose
    nose_points = [
        (head_center_x + head_width/4, head_center_y),
        (head_center_x - head_width/4, head_center_y),
        (nose_end_x - nose_width/3, nose_end_y),
        (nose_end_x + nose_width/3, nose_end_y)
    ]
    
    # Draw the nose extension
    draw.polygon(nose_points, fill=params["body_color"])
    draw.ellipse([nose_left, nose_top, nose_right, nose_bottom], fill=params["body_color"])
    
    # Draw eye - moved back on the head
    eye_size = base_head_size * 0.15
    eye_x = head_center_x + base_head_size * 0.15  # Moved back
    eye_y = head_center_y - base_head_size * 0.15
    
    if params["eye_style"] == "normal":
        draw.ellipse([eye_x - eye_size/2, eye_y - eye_size/2, 
                      eye_x + eye_size/2, eye_y + eye_size/2], 
                     fill=params["eye_color"])
    elif params["eye_style"] == "cartoon":
        # Larger eye with white background
        draw.ellipse([eye_x - eye_size, eye_y - eye_size, 
                      eye_x + eye_size, eye_y + eye_size], 
                     fill=(255, 255, 255))
        draw.ellipse([eye_x - eye_size/2, eye_y - eye_size/2, 
                      eye_x + eye_size/2, eye_y + eye_size/2], 
                     fill=params["eye_color"])
    elif params["eye_style"] == "realistic":
        # More detailed eye
        draw.ellipse([eye_x - eye_size, eye_y - eye_size, 
                      eye_x + eye_size, eye_y + eye_size], 
                     fill=(255, 255, 255))
        draw.ellipse([eye_x - eye_size*0.7, eye_y - eye_size*0.7, 
                      eye_x + eye_size*0.7, eye_y + eye_size*0.7], 
                     fill=(139, 69, 19))  # Brown iris
        draw.ellipse([eye_x - eye_size*0.3, eye_y - eye_size*0.3, 
                      eye_x + eye_size*0.3, eye_y + eye_size*0.3], 
                     fill=params["eye_color"])  # Pupil
    
    # Draw nostrils at the end of the nose
    nostril_size = base_head_size * 0.08
    nostril_spacing = nostril_size * 2
    
    # Position nostrils at the end of the nose
    draw.ellipse([nose_end_x - nostril_spacing/2 - nostril_size/2, nose_end_y - nostril_size/2, 
                  nose_end_x - nostril_spacing/2 + nostril_size/2, nose_end_y + nostril_size/2], 
                 fill=(30, 30, 30))
    draw.ellipse([nose_end_x + nostril_spacing/2 - nostril_size/2, nose_end_y - nostril_size/2, 
                  nose_end_x + nostril_spacing/2 + nostril_size/2, nose_end_y + nostril_size/2], 
                 fill=(30, 30, 30))
    
    # Add a mouth line
    mouth_length = nose_width * 0.6
    mouth_y = nose_end_y + nose_width/4
    draw.line([
        (nose_end_x - mouth_length/2, mouth_y),
        (nose_end_x + mouth_length/2, mouth_y)
    ], fill=(30, 30, 30), width=max(1, int(size_factor * 2)))
    
    # Draw ears
    ear_size = base_head_size * 0.25
    ear_left_x = head_center_x - base_head_size * 0.2
    ear_left_y = head_center_y - base_head_size * 0.3
    ear_right_x = head_center_x + base_head_size * 0.2
    ear_right_y = head_center_y - base_head_size * 0.3
    
    # Left ear
    draw.polygon([
        (ear_left_x, ear_left_y),
        (ear_left_x - ear_size, ear_left_y - ear_size*1.5),
        (ear_left_x + ear_size, ear_left_y - ear_size*1.5)
    ], fill=params["body_color"])
    
    # Right ear
    draw.polygon([
        (ear_right_x, ear_right_y),
        (ear_right_x - ear_size, ear_right_y - ear_size*1.5),
        (ear_right_x + ear_size, ear_right_y - ear_size*1.5)
    ], fill=params["body_color"])
    
    # Draw mane
    mane_length = base_neck_length * params["mane_length"] * 0.5
    mane_density = int(10 * params["mane_density"])
    
    if params["mane_style"] == "flowing":
        # Flowing mane with individual strands
        for i in range(mane_density):
            # Position along the neck
            t = i / (mane_density - 1)
            mane_x = neck_start_x + t * (neck_end_x - neck_start_x)
            mane_y = neck_start_y + t * (neck_end_y - neck_start_y)
            
            # Length varies along the neck
            strand_length = mane_length * (1 - 0.5 * abs(2*t - 1))  # Longest in the middle
            
            # Direction perpendicular to neck, slightly random
            angle = neck_angle_perp + np.radians(random.uniform(-20, 20))
            
            # End point of the strand
            strand_end_x = mane_x + np.cos(angle) * strand_length
            strand_end_y = mane_y + np.sin(angle) * strand_length
            
            # Draw the strand
            draw.line([(mane_x, mane_y), (strand_end_x, strand_end_y)], 
                      fill=params["mane_color"], 
                      width=max(1, int(2 * size_factor)))
    
    elif params["mane_style"] == "short":
        # Short mane as a simple shape
        mane_points = []
        for i in range(mane_density):
            t = i / (mane_density - 1)
            mane_x = neck_start_x + t * (neck_end_x - neck_start_x)
            mane_y = neck_start_y + t * (neck_end_y - neck_start_y)
            
            # Short spikes
            strand_length = mane_length * 0.3
            angle = neck_angle_perp + np.radians(random.uniform(-10, 10))
            
            mane_points.append((mane_x, mane_y))
            mane_points.append((
                mane_x + np.cos(angle) * strand_length,
                mane_y + np.sin(angle) * strand_length
            ))
        
        if mane_points:
            draw.polygon(mane_points, fill=params["mane_color"])
    
    elif params["mane_style"] == "mohawk":
        # Mohawk style - straight up
        for i in range(mane_density):
            t = i / (mane_density - 1)
            mane_x = neck_start_x + t * (neck_end_x - neck_start_x)
            mane_y = neck_start_y + t * (neck_end_y - neck_start_y)
            
            # Straight up with varying length
            strand_length = mane_length * (0.7 + 0.3 * np.sin(t * np.pi))
            angle = neck_rad - np.pi/2  # Straight up relative to neck
            
            strand_end_x = mane_x + np.cos(angle) * strand_length
            strand_end_y = mane_y + np.sin(angle) * strand_length
            
            # Draw thicker strands
            draw.line([(mane_x, mane_y), (strand_end_x, strand_end_y)], 
                      fill=params["mane_color"], 
                      width=max(2, int(3 * size_factor)))
    
    elif params["mane_style"] == "braided":
        # Braided mane - zigzag pattern
        braid_points = []
        zigzag_width = mane_length * 0.2
        
        for i in range(mane_density * 2):
            t = i / (mane_density * 2 - 1)
            mane_x = neck_start_x + t * (neck_end_x - neck_start_x)
            mane_y = neck_start_y + t * (neck_end_y - neck_start_y)
            
            # Zigzag pattern
            side = 1 if i % 2 == 0 else -1
            angle = neck_angle_perp
            
            braid_points.append((
                mane_x + np.cos(angle) * zigzag_width * side,
                mane_y + np.sin(angle) * zigzag_width * side
            ))
        
        if braid_points:
            # Draw the braid as a thick line
            for i in range(len(braid_points) - 1):
                draw.line([braid_points[i], braid_points[i+1]], 
                          fill=params["mane_color"], 
                          width=max(3, int(5 * size_factor)))
    
    # Draw legs based on pose
    leg_positions = [
        (body_left + base_body_length * 0.2, body_bottom),  # Front left
        (body_left + base_body_length * 0.3, body_bottom),  # Front right
        (body_left + base_body_length * 0.7, body_bottom),  # Back left
        (body_left + base_body_length * 0.8, body_bottom),  # Back right
    ]
    
    leg_angles = []
    if params["leg_pose"] == "standing":
        # Standing - all legs straight down
        leg_angles = [0, 0, 0, 0]
    elif params["leg_pose"] == "walking":
        # Walking - alternating legs forward/backward
        leg_angles = [15, -15, -15, 15]
    elif params["leg_pose"] == "running":
        # Running - front legs forward, back legs backward
        leg_angles = [30, 30, -30, -30]
    elif params["leg_pose"] == "rearing":
        # Rearing - front legs up, back legs straight
        leg_angles = [-60, -60, 0, 0]
        # Adjust front leg positions for rearing
        leg_positions[0] = (leg_positions[0][0], leg_positions[0][1] - base_body_height * 0.3)
        leg_positions[1] = (leg_positions[1][0], leg_positions[1][1] - base_body_height * 0.3)
    
    # Draw each leg
    for i, (leg_x, leg_y) in enumerate(leg_positions):
        leg_angle_rad = np.radians(leg_angles[i])
        
        # Calculate leg end point
        leg_end_x = leg_x + np.sin(leg_angle_rad) * base_leg_length
        leg_end_y = leg_y + np.cos(leg_angle_rad) * base_leg_length
        
        # Draw the leg
        draw.line([(leg_x, leg_y), (leg_end_x, leg_end_y)], 
                  fill=params["body_color"], 
                  width=max(1, int(base_leg_thickness)))
        
        # Draw hoof
        hoof_size = base_leg_thickness * 0.8
        draw.ellipse([
            leg_end_x - hoof_size, leg_end_y - hoof_size/2,
            leg_end_x + hoof_size, leg_end_y + hoof_size/2
        ], fill=(30, 30, 30))  # Dark hooves
    
    # Draw tail
    tail_start_x = body_left + base_body_length * 0.1
    tail_start_y = body_top + base_body_height * 0.4
    
    tail_length = base_body_length * 0.6 * params["tail_length"]
    tail_angle_rad = np.radians(params["tail_angle"])
    
    if params["tail_style"] == "flowing":
        # Flowing tail with multiple strands
        tail_strands = int(7 * params["tail_thickness"])
        for i in range(tail_strands):
            # Vary the angle slightly for each strand
            strand_angle = tail_angle_rad + np.radians(random.uniform(-20, 20))
            strand_length = tail_length * (0.7 + 0.3 * random.random())
            
            # End point of the strand
            strand_end_x = tail_start_x - np.cos(strand_angle) * strand_length
            strand_end_y = tail_start_y + np.sin(strand_angle) * strand_length
            
            # Draw the strand with varying thickness
            draw.line([(tail_start_x, tail_start_y), (strand_end_x, strand_end_y)], 
                      fill=params["mane_color"], 
                      width=max(1, int(2 * size_factor * params["tail_thickness"])))
    
    elif params["tail_style"] == "short":
        # Short tail as a simple triangle
        tail_end_x = tail_start_x - np.cos(tail_angle_rad) * tail_length * 0.4
        tail_end_y = tail_start_y + np.sin(tail_angle_rad) * tail_length * 0.4
        
        # Width at the end
        tail_width = base_body_height * 0.2 * params["tail_thickness"]
        perp_angle = tail_angle_rad + np.pi/2
        
        tail_points = [
            (tail_start_x, tail_start_y),
            (tail_end_x + np.cos(perp_angle) * tail_width, 
             tail_end_y + np.sin(perp_angle) * tail_width),
            (tail_end_x - np.cos(perp_angle) * tail_width, 
             tail_end_y - np.sin(perp_angle) * tail_width)
        ]
        
        draw.polygon(tail_points, fill=params["mane_color"])
    
    elif params["tail_style"] == "braided":
        # Braided tail - similar to braided mane but longer
        braid_points = []
        zigzag_width = tail_length * 0.1
        zigzag_steps = 10
        
        for i in range(zigzag_steps):
            t = i / (zigzag_steps - 1)
            tail_x = tail_start_x - np.cos(tail_angle_rad) * tail_length * t
            tail_y = tail_start_y + np.sin(tail_angle_rad) * tail_length * t
            
            # Zigzag pattern
            side = 1 if i % 2 == 0 else -1
            perp_angle = tail_angle_rad + np.pi/2
            
            braid_points.append((
                tail_x + np.cos(perp_angle) * zigzag_width * side,
                tail_y + np.sin(perp_angle) * zigzag_width * side
            ))
        
        if braid_points:
            # Draw the braid as a thick line
            for i in range(len(braid_points) - 1):
                draw.line([braid_points[i], braid_points[i+1]], 
                          fill=params["mane_color"], 
                          width=max(3, int(5 * size_factor * params["tail_thickness"])))
    
    # Return the parameters used
    return params

def generate_random_honse_params():
    """Generate random parameters for a honse."""
    return {
        # Body parameters - vary within reasonable ranges
        "body_length": random.uniform(0.8, 1.2),
        "body_height": random.uniform(0.8, 1.2),
        "neck_length": random.uniform(0.7, 1.3),
        "neck_thickness": random.uniform(1.0, 1.5),  # Thicker necks
        "head_size": random.uniform(0.8, 1.2),
        "leg_length": random.uniform(0.8, 1.2),
        "leg_thickness": random.uniform(0.8, 1.2),
        "tail_length": random.uniform(0.7, 1.3),
        "tail_thickness": random.uniform(0.8, 1.2),
        "mane_length": random.uniform(0.7, 1.3),
        "mane_density": random.uniform(0.7, 1.3),
        
        # Color parameters - keep within brown/chestnut range for realism
        "body_color": (
            random.randint(100, 160),  # R - brown range
            random.randint(50, 90),    # G - brown range
            random.randint(10, 30)     # B - brown range
        ),
        "mane_color": (
            random.randint(30, 70),    # R - darker brown
            random.randint(15, 40),    # G - darker brown
            random.randint(0, 15)      # B - darker brown
        ),
        "eye_color": (0, 0, 0),  # Black eyes
        
        # Pose parameters
        "head_angle": random.uniform(-20, 20),
        "neck_angle": random.uniform(-10, 30),
        "tail_angle": random.uniform(30, 60),
        "leg_pose": random.choice(["standing", "walking", "running", "rearing"]),
        
        # Style parameters
        "mane_style": random.choice(["flowing", "short", "mohawk", "braided"]),
        "tail_style": random.choice(["flowing", "short", "braided"]),
        "eye_style": random.choice(["normal", "cartoon", "realistic"]),
    }

def draw_single_honse(params=None, filename="honse.png"):
    """Draw a single honse with the given parameters."""
    # Set up a canvas with a light blue sky background
    width, height = 800, 600
    image = Image.new('RGB', (width, height), color=(135, 206, 235))  # Sky blue
    draw = ImageDraw.Draw(image)
    
    # Draw some grass
    draw.rectangle([(0, height*0.7), (width, height)], fill=(34, 139, 34))  # Forest green
    
    # Generate random parameters if none provided
    if params is None:
        params = generate_random_honse_params()
    
    # Draw the honse
    used_params = draw_honse(draw, width/2, height*0.7, params, 1.0)
    
    # Show the image
    image.show()
    
    # Save the image
    image.save(filename)
    print(f"Honse drawing saved as '{filename}'")
    
    return used_params

def draw_multiple_honses(num_honses=5, filename="honse_herd.png"):
    """Draw multiple honses with different parameters."""
    # Set up a larger canvas
    width, height = 1200, 800
    image = Image.new('RGB', (width, height), color=(135, 206, 235))  # Sky blue
    draw = ImageDraw.Draw(image)
    
    # Draw sky with gradient
    for y in range(height):
        # Create a gradient from light blue to darker blue
        t = y / height
        r = int(135 * (1 - t) + 100 * t)
        g = int(206 * (1 - t) + 150 * t)
        b = int(235 * (1 - t) + 200 * t)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Draw hills in the background
    for i in range(3):
        hill_height = random.uniform(0.2, 0.4)
        hill_width = random.uniform(0.5, 1.5)
        hill_x = random.uniform(-0.3, 0.7) * width
        
        # Draw a hill as a green arc
        hill_color = (
            random.randint(30, 100),
            random.randint(100, 160),
            random.randint(30, 80)
        )
        
        # Create hill points
        hill_points = []
        for x in range(int(width * 1.5)):
            # Parabolic curve for the hill
            dx = (x - hill_x) / (width * hill_width)
            y = height * (0.7 - hill_height * (1 - dx*dx))
            if 0 <= x < width and y < height:
                hill_points.append((x, y))
        
        # Add bottom corners to complete the polygon
        if hill_points:
            hill_points.append((width, height))
            hill_points.append((0, height))
            draw.polygon(hill_points, fill=hill_color)
    
    # Draw grass in the foreground
    draw.rectangle([(0, height*0.7), (width, height)], fill=(34, 139, 34))  # Forest green
    
    # Draw some random grass tufts
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(int(height*0.7), height)
        grass_height = random.randint(5, 15)
        grass_color = (
            random.randint(30, 100),
            random.randint(120, 180),
            random.randint(30, 80)
        )
        draw.line([(x, y), (x, y-grass_height)], fill=grass_color, width=2)
    
    # Draw multiple honses
    honses_params = []
    for i in range(num_honses):
        # Random position, with larger honses in the foreground
        size = random.uniform(0.3, 1.0)
        y_pos = height * (0.7 - 0.1 * (1 - size))  # Larger honses lower in the scene
        x_pos = random.uniform(width * 0.1, width * 0.9)
        
        # Generate random parameters
        params = generate_random_honse_params()
        
        # Draw the honse
        used_params = draw_honse(draw, x_pos, y_pos, params, size)
        honses_params.append(used_params)
    
    # Show the image
    image.show()
    
    # Save the image
    image.save(filename)
    print(f"Honse herd drawing saved as '{filename}'")
    
    return honses_params

if __name__ == "__main__":
    # Uncomment one of these lines to choose what to draw
    # draw_single_honse()  # Draw a single honse with random parameters
    draw_multiple_honses(7)  # Draw multiple honses (adjust number as desired)
