#-*- coding: utf-8 -*-
import argparse
import sys
import pypng.code.png as png
import subprocess

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Encrypt (write) or Decrypt (read) text in an image.')
    parser.add_argument('-w', '--writing_mode', action='store_true', help='Switch to writing mode.')
    parser.add_argument('image_orig', type=str, help='Set the original image filename (the one without message).')
    parser.add_argument('image_dest', type=str, help='Set the image filename that contain the message (reading mode) or will (writing mode).')
    parser.add_argument('-f', '--filename', type=str, required=False, help='Set the filename of the message to encrypt, if writing mode.')
    parser.add_argument('-t', '--text', type=str, required=False, help='Write the quoted message to encrypt, if writing mode (please use simple quotes instead of double quotes or surround message with spaces)')
    args = parser.parse_args()

    write = args.writing_mode
    filename = args.filename
    text = args.text
    image_orig = args.image_orig
    image_dest = args.image_dest
