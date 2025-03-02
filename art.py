"""
Todo:

- Save into a folder you like/don't like.
-- set up the code with a prompt; loop round; y/n to define taste
-- do this until there is a healthy set of paintings in the folder

- Show some simple statistics describing the painting
-- Load the descriptors from the pickled data
-- all the params; numerical description
-- colours; use a colour histogram of some sort

- Change the parameters using scikit-learn
- Implement a simple recommender system script
- Try it out with different source images, stop when something looks cool enough.
"""

from datetime import datetime
from aggdraw import Draw, Symbol, Pen, Brush
import sklearn as sk
from PIL import Image
import numpy as np
import random
import pandas as pd
from random import random, choice
import pickle

MAXIMUM_STROKE_SIZE = 500
MAXIMUM_CURVE_PARTS = 20
MAXIMUM_START_POINT = 400
MAXIMUM_PEN_WIDTH = 10
N_MARKS = 100
PEN_BIAS = 0.4
MIN_OPACITY = 150


def add_a_mark_to_the_canvas(canvas, symbol_params, pen, start_point):
    """Add a symbol to the canvas using a brush or pen."""
    # Turn the parameters into a command.
    print(symbol_params)
    symbol = Symbol(symbol_params)
    # Apply the symbol to the canvas.
    canvas.symbol(start_point, symbol, pen)
    canvas.flush()


def gen_sentence_of_strokes(letters, sizes, movements):
    sentence = []
    for l, s, m in zip(letters, sizes, movements):
        sentence.append(f"{l}{s} {m}")
    sentence = " ".join(sentence)
    return sentence


def get_mark_maker():
    # Randomly select a brush or pen.
    use_pen = random() > PEN_BIAS
    # Generate a random colour.
    r_colour = lambda : int(random()*255)
    color = (r_colour(), r_colour(), r_colour())
    # Generate a random opacity.
    opacity = int(MIN_OPACITY + random()*(255-MIN_OPACITY))
    # Generate a random width.
    width = int(random()*MAXIMUM_PEN_WIDTH)
    # Create a mark maker
    if use_pen:
        mark_spec = (color, width, opacity)
        return Pen(*mark_spec), mark_spec
    else:
        mark_spec = (color, opacity, None)
        return Brush(*mark_spec[:2]), mark_spec


def gen_random_marks():
    # Generate the symbols that will decorate the canvas (random pen and brushstrokes).
    gen_stroke_size = lambda : random()*MAXIMUM_STROKE_SIZE

    # Create all the brushstroke paths; randomly.
    start_points = []
    marks = []
    stroke_lengths = (np.random.random(N_MARKS)*MAXIMUM_STROKE_SIZE).astype(int)
    for length in stroke_lengths:
        start_point = ((random()*MAXIMUM_START_POINT,
                        random()*MAXIMUM_START_POINT))
        valid_letters = "MLHVCSQTZ"
        letters = [choice(valid_letters) for x in range(length)]
        sizes = [gen_stroke_size() for x in range(length)]
        movements = [gen_stroke_size() for x in range(length)]
        mark = gen_sentence_of_strokes(letters, sizes, movements)
        start_points.append(start_point)
        marks.append(mark)
    
    return start_points, marks 


def gen_random_mark_makers():
    # Create all the pens and brushes randomly, and record the variables we used for them.
    mark_makers = []
    mark_specs = []
    for _ in range(N_MARKS):
        mm, ms = get_mark_maker()
        mark_makers.append(mm)
        mark_specs.append(ms)
    print(mark_makers)
    return mark_makers, mark_specs


def load_and_recreate_an_image(filename):
    # Recreate the image and check it looks the same.
    # Load description.
    df2 = pickle.load(open(filename.replace('.png', '.pickle'), 'rb'))
    # Set up a blank canvas.

    image = Image.fromarray(np.zeros((800, 600, 3)), mode="RGB")
    canvas = Draw(image)

    # Re-create the markmaker for the mark, then apply saved params.
    start_points = df2['start_points'].values
    marks = df2['marks'].values
    mark_specs = df2['mark_specs'].values

    for start_point, mark, mark_spec in zip(start_points, marks, mark_specs):
        # Re-create a pen or a brush.
        if mark_spec[2]:
            mark_maker = Pen(*mark_spec)
        else:
            mark_maker = Brush(*mark_spec[:2])
        # Re-create the symbol
        add_a_mark_to_the_canvas(canvas, mark, mark_maker, start_point)



if __name__ == "__main__":

    # Keep asking the user about paintings until they quit.
    while True:

        # Set up a canvas to paint on.
        image = Image.fromarray(np.zeros((800, 600, 3)), mode="RGB")
        canvas = Draw(image)

        # Add Symbols with Pens and Brushes; paint that picture!
        start_points, marks = gen_random_marks()
        mark_makers, mark_specs = gen_random_mark_makers()
        for start_point, mark, mark_maker in zip(start_points, marks, mark_makers):
            add_a_mark_to_the_canvas(canvas, mark, mark_maker, start_point)
        
        # Prompt the user, save into a the like or dislike folder based on critique.
        image.show()
        response = input("Do you like it? (y/n)")
        save_dir = {'y':'like', 'n':'dislike'}[response]

        # Save the image.
        now = datetime.now()
        filename = f"data/{save_dir}/art_{now.strftime('%Y_%m_%d_%H_%M_%S')}"
        image.save(filename + ".png")
        image.close()

        # Save instructions for how to re-create the image in a DataFrame.
        df = pd.DataFrame()
        df['start_points'] = start_points
        df['marks'] = marks
        df['mark_specs'] = mark_specs

        # Save it.
        df.to_pickle(filename + '.pickle')