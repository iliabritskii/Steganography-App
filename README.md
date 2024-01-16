This is a program for encrypting text information into bitmap images. 

There are a command line program and a GUI application.

Requirements:

For GUI version should be installed kivy and easygui python packages.

Encryption options:

• Encoding depth is the number of bits that are replaced in one byte of the image. Each character from your message is converted to a 12-digit binary number. Then the program writes the code of this character into images in parts, replacing the low-order bits (those on the right) in the byte with part of the character code (1, 2, 3 or 4 bits depending on the selected encoding depth). Thus, recording one character can take 12, 6, 4 or 3 bytes of the image. The lower the encoding depth, the more difficult it is to distinguish the original picture from the picture with the message.

When choosing encoding depth 1 or 2, it is almost impossible to distinguish a picture from the original with the naked eye. When choosing an encoding depth of 4, a large message length, and using a picture with a light background, you may notice some differences. However, the lower the encoding depth, the fewer characters your message can contain. To select this parameter, you must use the drop-down list.

Example: Let's take the Russian letter "a". Its number in the Unicode table is 1072. Let's convert it to the binary system and get 010000110000. Let's assume that we have chosen a coding depth of 4. Then we select the first 4 digits and get 0100. Next, the program will read one byte from the image. Let's assume that it is equal to 11111111. Let's replace the 4 right-hand bits with part of the character code. We will receive a new byte 11110100. This byte will be written to the new image. These actions will be repeated until the program encrypts all parts of the symbol code. Then this algorithm will be repeated with another symbol.

• The offset of the encoding entry is the number of image bytes that will be skipped (simply overwritten into a new image) at the beginning of the image. This parameter allows you to increase the reliability of encryption, as it makes it much more difficult to crack the cipher through brute force. The offset of the encoding entry is a positive integer!

Example: Let's assume that the selected encoding record offset value is 46. This means that the program will skip (simply rewrite into a new one) the first 54 bytes of the image (they are the keepers of service information, for example, the file name), then skip another 46 bytes. Thus, writing the first character into images will start from byte 101.

• The interval between encoded characters is the number of bytes that will be skipped (simply rewritten into a new image) after writing one character. This parameter allows you to increase the reliability of encryption, as it makes it much more difficult to crack the cipher through brute force. The spacing between encoded characters is a positive integer!

Example: Let's assume that the selected interval value is 4. This means that after writing a character to images (this may take 12, 6, 4 or 3 bytes (see the item "selecting encoding depth")) it will be skipped (simply rewritten into a new image) 4 bytes, and then a new character will begin to be written.

