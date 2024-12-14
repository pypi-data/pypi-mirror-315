import argparse
import os
import yaml

from pathlib import Path


def load_config(llm):
    path = Path(__file__).resolve()
    path = path.parent
    path = os.path.join(path, 'config.yaml')
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    return config[llm]


def restricted_float(x):
    x = float(x)
    if x <= 0.0 or x >= 1.0:
        raise argparse.ArgumentTypeError("%r not in range (0, 1)" % (x,))
    return x


def check_file(file_name):
    if not os.path.exists(file_name):
        with open(file_name, 'r') as file:
            file.write('')
