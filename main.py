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

def write_message(text, pixels_b2, width, height, info, image_dest):
    ''' (String, array of bin, int, int, dictionary, String) -> NoneType '''
    if not(is_encryption_possible(text, width, height)):
        sys.exit('Error: This image is too small to contain your message.')
    ascii = text_to_ASCII(text)
    # Encrypt the binary ASCII message in the binary pixels using XOR.
    for index in range(len(ascii)):
        code = list(pixels_b2[index])
        code[7] = xor(code[7], ascii[index])
        pixels_b2[index] = ''.join(code)
    write_png(pixels_b2, width, height, info, image_dest)
    return

def read_message(pixels_b2_orig, pixels_b2_dest, width, height):
    ''' (array of bin, array of bin, int, int) -> NoneType '''
    ascii = ''
    # Decrypt the binary ASCII message using XOR, by comparing images.
    for index in range(len(pixels_b2_orig)):
        ascii += xor(pixels_b2_orig[index][7], pixels_b2_dest[index][7])
        # If we reached the end of the message (\0 in binary ASCII), end loop.
        if index % 7 == 0 and index > 1 and ascii.endswith('00000000'):
            break
    text = ASCII_to_text(ascii)
    print(text)
    #subprocess.Popen("strings 'aaa'", stdout=subprocess.PIPE)
    return

def is_encryption_possible(text, width, height):
    ''' (String, int, int) -> Boolean '''
    if len(text)*8 > width*height*4:
        return False
    return True

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

def read_png(filename):
    ''' (String) -> list of int, int, int, dictionary '''
    file = png.Reader(filename=filename)
    width, height, pixels, info = file.asRGBA8()  # .asRGBA8() prevents too many scenarios.
    pixels_b2 = get_pixels_b2(list(pixels), width, height)
    return pixels_b2, width, height, info

def write_png(pixels_b2, width, height, info, filename):
    ''' (matrix of int, int, int, dictionary, String) -> NoneType '''
    pixels_b10 = get_pixels_b10(pixels_b2, width, height)  # We always need pixel's values at base 10 to write the image.
    # Keep only the information usable by png.Writer.
    info_used = [
        'size',
        'greyscale',
        'alpha',
        'bitdepth',
        'transparent',
        'background',
        'gamma',
        'compression',
        'interlace',
        'planes',
        'colormap'
    ]
    info_keeped = {key: info[key] for key in info_used if key in info}
    # Write in file.
    writer = png.Writer(width, height, **info_keeped)
    file = open(filename, 'wb')
    writer.write(file, pixels_b10)
    file.close()
    return

def get_pixels_b2(pixels_list, width, height):
    ''' (list of int, int, int) -> array of bin '''
    pixels_b2 = []
    for i in range(0, height):
        for j in range(0, width*4):
            pixels_b2.append(bin(pixels_list[i][j])[2:].zfill(8))
    return pixels_b2

def get_pixels_b10(pixels_b2, width, height):
    ''' (array of bin, int, int) -> matrix of int '''
    pixels_b10 = []
    for i in range(0, height):
        row = []
        for j in range(0, width*4):
            row.append(int(pixels_b2[i*width*4+j], 2))
        pixels_b10.append(row.copy())
    return pixels_b10

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

    # Run the encryption / decryption
    pixels_b2_orig, width, height, info = read_png(image_orig)
    if write:
        if filename is not None:
            text = read_txt(filename)
        elif text is None:
            text = input('Please enter the message to encrypt: ')
        write_message(text, pixels_b2_orig, width, height, info, image_dest)
    else:
        pixels_b2_dest, width, height, info = read_png(image_dest)
        read_message(pixels_b2_orig, pixels_b2_dest, width, height)
