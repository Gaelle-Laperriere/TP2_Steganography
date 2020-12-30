# TP2_Steganography
This project is about producing a self-contained tool in Python that can be used for covert messaging. The tool is able to “hide” ASCII text inside PNG files. This program only inserts text in the lowest-weight bits of each channel of the images.

## Technologies and frameworks used
All the scripts are written in <i>Python 3.7.4</i>.
The libraries used for this project are as follow:
- [Python 3.7.4](https://www.python.org)
- [Pypng 0.0.20](https://pypi.org/project/pypng/) to process png images

You can install Python through python's package manager or ``conda``. The Pypng library if given when pulling the git deposit: you mustn't install it. 

```
conda install python==3.7.4
```

## Execution
To run the software, you will have to pull all the deposit and activate your required environment. The program have two modes (reading and writing) specified through the ``-w`` switch. If the switch is not provided, reading mode will be assumed and the program will dump any text found in the PNG file to standard output.

The convention is as follow:
```
main.py [-h] [-w] [-f FILENAME] [-t TEXT] image_orig image_dest
```

You can use the option ``-h`` alone, for help or more information. 

### Writing mode
To encrypt a message in a PNG image, please use the command:

```
python main.py -w [-f filename] [-t "text"] image_orig.png image_dest.png
```

The ``image_orig.png`` will be the one used to generate the new image ``ìmage_dest.png``. This image will contain the encrypted message. It will be generated in your current directory as well. 

The text to be inserted in the PNG file should be specified by one of the three methods:
- if neither ``-f`` nor ``-t`` is specified, it will be read from standard input. You will be asked to write it in your console. 
- if ``-f filename`` is specified, it will be read from the file filename.
- If ``-t "text"`` is specified, it will be read from the command line.

Please be carefull with the text written in the command line. Use simple quotes if special characters are used, for more security. The same way, you can use double quotes by adding a space between them and the message (``" text "`` instead of ``"text"``). This problem is due to the Bash command line system, not the program nor the argparse module. If some specific characters are used without those securities, the command line might be badly interpreted by the system itself. 

Sanity checks are done before attempting to write. If the message is too long to fit in the image, the program will terminate with an error message. It is able to handle PNGs that have an alpha channel.

### Reading mode
To decrypt a message hidden in a PNG image, please use the command:

```
python main.py image_orig.png image_dest.png [| less]
```

Like the writing mode, you will need to give the original image filename, plus the one used for hidding the message. You can use a pipeline with ``less`` if you want to see the message being printed by parts. 
