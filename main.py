#-*- coding: utf-8 -*-
import argparse
import sys
import pypng.code.png as png
import subprocess

def xor(a, b):
    ''' (String, String) -> String '''
    if (a == '1' and b == '0') or (a == '0' and b == '1'):
        return '1'
    return '0'

def text_to_ASCII(text):
    ''' (String) -> String '''
    ascii_array = [bin(ord(char))[2:].zfill(8) for char in text]  # Get binary ASCII for each character.
    ascii_string = ''.join(ascii_array)
    ascii_string.join('00000000')  # Ending of the message (\0 in binary ASCII).
    return ascii_string

def ASCII_to_text(ascii):
    ''' (String) -> String '''
    ascii_array = [ascii[index:index+8] for index in range(0, len(ascii), 8)]  # Separate each ASCII characters.
    text_array = [chr(int(char, 2)) for char in ascii_array]  # Get their integer value and decode them.
    text_string = ''.join(text_array)
    return text_string

def read_txt(filename):
    ''' (String) -> String '''
    file = open(filename, 'r')
    text = file.read()
    file.close()
    return text

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

    # Check if the two image filenames are identical.
    if image_dest == image_orig and write:
        user_confirmation = ''
        while True:
            user_confirmation = input('Positionnal arguments image_orig and image_dest are equal. The original image will be overwritten. It is needed to decrypt the message afterward.\nWould you like to continue ? [yes] or [no] ')
            if user_confirmation == 'no':
                exit()
            if user_confirmation == 'yes':
                break
