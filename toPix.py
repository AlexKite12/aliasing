#!/usr/bin/env python
import numpy as np
import sys, random, argparse
import math

from PIL import Image, ImageSequence
from images2gif import writeGif

def getImage(data):
    """
    Get image from numpy array

    Parameters
    ----------
    data : numpy.ndarray
        converted image to numpy array

    Returns
    -------
    image : PIL.Image.image
    """
    return Image.fromarray(data)

def generateArray():
    pass

def getArray(image):
    """
    Get numpy array from image

    Parameters
    ----------
    image : PIL.Image.image

    Returns
    -------
    data : numpy.ndarray
        converted image to numpy array
    """
    return np.array(image)

def remaster(data, length = 8):
    for i in range(length, data.shape[0], length):
        for j in range(data.shape[1]):
            data[i - length : i, j] = data[i - length, j]
    for i in range(data.shape[0]):
        for j in range(length, data.shape[1], length):
            data[i, j - length : j] = data[i, j - length]
    return data

def covertImageToPixel(imageFile):
    image = Image.open(imageFile).convert('RGBA')
    data = getArray(image)
    data = remaster(data)
    new_image = getImage(data)
    new_image.show()
    return new_image

def covertAnimationToPixel(animation):
    frames_list = []
    animation = Image.open(animation)
    duration = animation.info['duration']
    for frame in get_frames(animation):
        data = getArray(frame)
        data = remaster(data)
        new_image = getImage(data)
        frames_list.append(new_image)
    return get_animation(frames_list, duration)

def get_frames(animation):
    frames_list = [frame.copy() for frame in ImageSequence.Iterator(animation)]
    for frame in frames_list:
        yield frame

def get_animation(frames_list, duration=0.1):
    writeGif('animation.gif', frames_list, duration=duration)

def main():
    parser = argparse.ArgumentParser(description='Convert image to pixel')
    parser.add_argument('--file', '-f', dest='imageFile')
    parser.add_argument('--gif', dest='gifFile')

    args = parser.parse_args()
    imageFile = args.imageFile
    if imageFile is not None:
        covertImageToPixel(imageFile)

    gifFile = args.gifFile
    if gifFile is not None:
        covertAnimationToPixel(gifFile)

if __name__ == '__main__':
    main()
