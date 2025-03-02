"""
Flask app for generating and displaying honses (horses).
This app allows users to generate random honses or customize parameters.
"""

from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image, ImageDraw
import io
import base64
import random
import os
import json
from draw_honse import draw_honse, generate_random_honse_params

app = Flask(__name__)

# Ensure the static directory exists
os.makedirs('static', exist_ok=True)
os.makedirs('static/images', exist_ok=True)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/generate_random', methods=['POST'])
def generate_random():
    """Generate a random honse and return the image."""
    # Create a new image
    width, height = 800, 600
    image = Image.new('RGB', (width, height), color=(135, 206, 235))  # Sky blue
    draw = ImageDraw.Draw(image)
    
    # Draw grass
    draw.rectangle([(0, height*0.7), (width, height)], fill=(34, 139, 34))
    
    # Generate random parameters
    params = generate_random_honse_params()
    
    # Draw the honse
    used_params = draw_honse(draw, width/2, height*0.7, params, 1.0)
    
    # Save to a BytesIO object
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    
    # Convert to base64 for embedding in HTML
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    
    # Save parameters for later reference
    honse_id = random.randint(10000, 99999)
    with open(f'static/images/honse_{honse_id}.json', 'w') as f:
        json.dump(used_params, f)
    
    # Save the image
    image.save(f'static/images/honse_{honse_id}.png')
    
    return jsonify({
        'image': f'data:image/png;base64,{img_base64}',
        'honse_id': honse_id,
        'params': used_params
    })

@app.route('/customize_honse', methods=['POST'])
def customize_honse():
    """Generate a honse with custom parameters."""
    # Get parameters from the request
    data = request.json
    params = data.get('params', {})
    
    # Create a new image
    width, height = 800, 600
    image = Image.new('RGB', (width, height), color=(135, 206, 235))
    draw = ImageDraw.Draw(image)
    
    # Draw grass
    draw.rectangle([(0, height*0.7), (width, height)], fill=(34, 139, 34))
    
    # Convert string parameters to appropriate types
    for key in params:
        if key in ['body_length', 'body_height', 'neck_length', 'neck_thickness',
                  'head_size', 'leg_length', 'leg_thickness', 'tail_length',
                  'tail_thickness', 'mane_length', 'mane_density']:
            params[key] = float(params[key])
        elif key in ['head_angle', 'neck_angle', 'tail_angle']:
            params[key] = float(params[key])
        elif key == 'body_color' or key == 'mane_color' or key == 'eye_color':
            if isinstance(params[key], str):
                # Convert from hex or parse tuple string
                if params[key].startswith('#'):
                    # Hex color
                    h = params[key].lstrip('#')
                    params[key] = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                elif params[key].startswith('(') and params[key].endswith(')'):
                    # Tuple string
                    params[key] = eval(params[key])
    
    # Draw the honse
    used_params = draw_honse(draw, width/2, height*0.7, params, 1.0)
    
    # Save to a BytesIO object
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    
    # Convert to base64 for embedding in HTML
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    
    # Save parameters and image
    honse_id = random.randint(10000, 99999)
    with open(f'static/images/honse_{honse_id}.json', 'w') as f:
        json.dump(used_params, f)
    
    image.save(f'static/images/honse_{honse_id}.png')
    
    return jsonify({
        'image': f'data:image/png;base64,{img_base64}',
        'honse_id': honse_id,
        'params': used_params
    })

@app.route('/generate_herd', methods=['POST'])
def generate_herd():
    """Generate a herd of honses."""
    # Get the number of honses to generate
    data = request.json
    num_honses = data.get('num_honses', 5)
    num_honses = min(max(1, num_honses), 10)  # Limit between 1 and 10
    
    # Create a new image
    width, height = 1200, 800
    image = Image.new('RGB', (width, height), color=(135, 206, 235))
    draw = ImageDraw.Draw(image)
    
    # Draw sky with gradient
    for y in range(height):
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
        
        hill_color = (
            random.randint(30, 100),
            random.randint(100, 160),
            random.randint(30, 80)
        )
        
        hill_points = []
        for x in range(int(width * 1.5)):
            dx = (x - hill_x) / (width * hill_width)
            y = height * (0.7 - hill_height * (1 - dx*dx))
            if 0 <= x < width and y < height:
                hill_points.append((x, y))
        
        if hill_points:
            hill_points.append((width, height))
            hill_points.append((0, height))
            draw.polygon(hill_points, fill=hill_color)
    
    # Draw grass
    draw.rectangle([(0, height*0.7), (width, height)], fill=(34, 139, 34))
    
    # Draw grass tufts
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
        size = random.uniform(0.3, 1.0)
        y_pos = height * (0.7 - 0.1 * (1 - size))
        x_pos = random.uniform(width * 0.1, width * 0.9)
        
        params = generate_random_honse_params()
        used_params = draw_honse(draw, x_pos, y_pos, params, size)
        honses_params.append(used_params)
    
    # Save to a BytesIO object
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    
    # Convert to base64
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    
    # Save the image
    herd_id = random.randint(10000, 99999)
    image.save(f'static/images/herd_{herd_id}.png')
    
    return jsonify({
        'image': f'data:image/png;base64,{img_base64}',
        'herd_id': herd_id
    })

@app.route('/download/<filename>')
def download_image(filename):
    """Download a saved image."""
    return send_file(f'static/images/{filename}', as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)