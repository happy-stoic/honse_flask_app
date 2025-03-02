# Some quick exploratory data analysis

# Load in the likes and dislikes from the pickle files.
import os
import pickle
from pathlib import Path
from tkinter import W
from colorsys import hsv_to_rgb
from PIL import Image
import numpy as np



def load_list_of_paintings(painting_dir):
    painting_list = []
    for painting in painting_dir.glob('*.pickle'):
        with open(painting, 'rb') as fp:
            f = pickle.load(fp)
            painting_list.append(f)
    return painting_list


def make_a_colour_mark_image(painting_list, savename):
    """Make an image out of colours I liked."""
    # Make a list of every colour used.
    colours = []
    for p in painting_list:
        marks = p['mark_specs']
        for m in marks:
            colours.extend(m[0])
    # Find the biggest width of a square the image could fill.
    width = int(np.sqrt(len(colours)/3))
    print(width)
    # Make a square image with pixels as the mark colours.
    img = Image.frombytes('RGB', (width, width), bytes(colours))
    img.show()
    img.save(savename)


if __name__ == '__main__':

    # Load data for liked and disliked paintings.
    liked_dir = Path('./data/like')
    disliked_dir = Path('./data/dislike')
    liked_paintings = load_list_of_paintings(liked_dir)
    disliked_paintings = load_list_of_paintings(disliked_dir)
    print(f"loaded {len(liked_paintings)} I liked and {len(disliked_paintings)} I didn't.")

    make_a_colour_mark_image(liked_paintings, 'liked.png')
    make_a_colour_mark_image(disliked_paintings, 'disliked.png')