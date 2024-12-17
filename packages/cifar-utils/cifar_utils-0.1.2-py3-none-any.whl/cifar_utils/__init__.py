def get_classes():
    """
    Returns a list of 100 class names from the CIFAR-100 dataset.

    The list is in the same order as the labels in the CIFAR-100 dataset.
    """
    class_names = [
        'apple', 'aquarium_fish', 'baby', 'bear', 'beaver', 'bed', 'bee', 'beetle', 'bicycle', 'bottle',
        'bowl', 'boy', 'bridge', 'bus', 'butterfly', 'camel', 'can', 'castle', 'caterpillar', 'cattle',
        'chair', 'chimpanzee', 'clock', 'cloud', 'cockroach', 'couch', 'crab', 'crocodile', 'cup', 'dinosaur',
        'dolphin', 'elephant', 'flatfish', 'forest', 'fox', 'girl', 'hamster', 'house', 'kangaroo', 'keyboard',
        'lamp', 'lawn_mower', 'leopard', 'lion', 'lizard', 'man', 'maple_tree', 'motorcycle', 'mouse', 'mushroom',
        'oak_tree', 'orange', 'orchid', 'otter', 'palm_tree', 'pear', 'pickup_truck', 'pine_tree', 'plain', 'plate',
        'poppy', 'rabbit', 'ray', 'road', 'rocket', 'rose', 'sea', 'seal', 'shark', 'shrew', 'skyscraper',
        'snake', 'spider', 'squirrel', 'streetcar', 'sunflower', 'sweet_pepper', 'table', 'tank', 'telephone',
        'television', 'tiger', 'tractor', 'train', 'trout', 'tulip', 'turtle', 'wardrobe', 'whale', 'wolf',
        'woman', 'worm'
    ]
    
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
    
    return super_classes
