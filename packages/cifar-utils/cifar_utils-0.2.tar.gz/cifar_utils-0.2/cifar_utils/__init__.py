def get_classes():
    """
    Returns a list of 100 class names from the CIFAR-100 dataset.

    The list is in the same order as the labels in the CIFAR-100 dataset.
    """
    class_names = [
        "apple", "aquarium_fish", "baby", "bear", "beaver", "bed", "bee", "beetle", 
        "bicycle", "bottle", "bowl", "boy", "bridge", "bus", "butterfly", "camel", 
        "can", "castle", "caterpillar", "cattle", "chair", "chimpanzee", "clock", 
        "cloud", "cockroach", "couch", "crab", "crocodile", "cup", "dinosaur", "dolphin", 
        "elephant", "flatfish", "forest", "fox", "girl", "hamster", "house", "kangaroo", 
        "keyboard", "lamp", "lawn_mower", "leopard", "lion", "lizard", "lobster", "man", 
        "maple_tree", "motorcycle", "mountain", "mouse", "mushroom", "oak_tree", "orange", 
        "orchid", "otter", "palm_tree", "pear", "pickup_truck", "pine_tree", "plain", "plate", 
        "poppy", "porcupine", "possum", "rabbit", "raccoon", "ray", "road", "rocket", "rose", 
        "sea", "seal", "shark", "shrew", "skunk", "skyscraper", "snail", "snake", "spider", 
        "squirrel", "streetcar", "sunflower", "sweet_pepper", "table", "tank", "telephone", 
        "television", "tiger", "tractor", "train", "trout", "tulip", "turtle", "wardrobe", 
        "whale", "willow_tree", "wolf", "woman", "worm"
    ]
    
    print(f"Total classes: {len(class_names)}")
    return class_names

def get_super_classes():
    """
    Returns a list of 20 superclasses from the CIFAR-100 dataset.

    Superclasses are broad categories that group the fine-grained classes together.
    """
    super_classes = [
        'aquatic mammals', 'fish', 'flowers', 'food containers', 'fruit and vegetables', 'household electrical devices',
        'household furniture', 'insects', 'large carnivores', 'large man-made outdoor things', 'large natural outdoor scenes',
        'large omnivores and herbivores', 'medium-sized mammals', 'non-insect invertebrates', 'people', 'reptiles',
        'small mammals', 'trees', 'vehicles 1', 'vehicles 2'
    ]
    
    print(f"Total super classes: {len(super_classes)}")
    return super_classes

import numpy as np
import tensorflow as tf
from collections import Counter

def image_data():
    """
    Displays a concise summary of CIFAR-100 dataset:
    - Image format (size, channels)
    - Number of superclasses
    """
    image_size = 32  # CIFAR-100 images are 32x32
    num_channels = 3  # RGB channels
    num_superclasses = 20  # CIFAR-100 has 20 superclasses

    # Displaying Image Format and Superclass Info
    print("CIFAR-100 Image Details:")
    print(f"- Image size: {image_size}x{image_size} pixels")
    print(f"- Number of channels: {num_channels} (RGB)")
    print(f"- Each image is represented as a 3D matrix: ({image_size}, {image_size}, {num_channels})")
    print(f"- Total number of superclasses: {num_superclasses}")
    images_per_superclass = 5 * 600
    print(f"- Each of the 20 superclasses has {images_per_superclass} images.")
    print()
    print("\nTo access the full class names or superclasses, use the following functions:")
    print("\n- Class Names: Get a list of 100 fine-grained class names using `get_classes()`.")
    print("- Superclasses: Get a list of 20 superclasses using `get_super_classes()`.\n")



