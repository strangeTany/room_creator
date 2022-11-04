import argparse
import os
from psd_tools import PSDImage

parser = argparse.ArgumentParser()
parser.add_argument('filepath', type=str, help='Absolute path to the folder with psd file')
parser.add_argument('filename', type=str, help='Name of the psd file without extension')
parser.add_argument('-d', '--decoration', action='store_true')
args = parser.parse_args()

PATH = args.filepath
FILENAME = args.filename
is_decoration = args.decoration


def decoration_export():
    shadow = input('Input shadow suffix: ')
    copy = input('Input copy suffix: ')
    stage = len(input('Input stage prefix: '))
    for group in psd:
        os.makedirs(os.path.join(PATH, f'{FILENAME}_export', group.name))
        for layer in group:
            resize_value = 2
            if copy in layer.name.lower():
                continue
            if shadow in layer.name:
                resize_value = 4
            print(layer.name)
            image = layer.composite()
            (width, height) = (image.width // resize_value, image.height // resize_value)
            img = image.resize((width, height))
            file_path = os.path.join(PATH, f'{FILENAME}_export', group.name, f'{layer.name[stage+1:]}.png')
            img.save(file_path)


def room_export():
    return


if __name__ == '__main__':
    psd = PSDImage.open(os.path.join(PATH, FILENAME+'.psd'))
    while os.path.exists(os.path.join(PATH, f'{FILENAME}_export')):
        input(f'Please delete folder {FILENAME}_export and press enter')
    os.makedirs(os.path.join(PATH, f'{FILENAME}_export'))
    if is_decoration:
        decoration_export()

