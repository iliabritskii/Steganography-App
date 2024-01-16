import sys

print("Welcome to the Encrypt/Decrypt programm!")

def start():

    while True:
        select_mode=int(input("Select mode: 1-encrypt, 2-decrypt, 3-exit  \n"))
        if select_mode==1:
            encrypt()
        elif select_mode==2:
            decrypct()
        elif select_mode==3:
            break
        else:
            print("Mode error")


def encrypt():

    depth=int(input("Select depth of encrypt: 1,2,3,4  \n"))       #Выбор количества младших битов в байте, которые будут
    check_depth="1234"                                                        #меняться в байтах изображения
    if str(depth) not in check_depth or depth>=10:
        print("Depth error")
        return 0

    step=int(input("Enter the offset of message (bytes): \n"))      #Смещение от начала "цветовых байтов" (пропуск какого-то количества после 54 служебных)
    if step<0:                                                      #Только положительное число для правильной работы
        print("Error. Only > 0")
        return 0

    interval=int(input("Enter the interval between encrypted symbols (bytes): \n"))     #Выбор интервала между закодированными символами
    if interval<0:                                                                     #Интервал после конца кодировки каждого символа, т.е. после
        print("Error. Only > 0")                                                            # 1, 2, 4, или 8 байт в картинке
        return 0

    message=input("Enter the message:\n")

    start_image_position=input("Enter the full position of image: \n")
    check_image=""
    for i in range(len(start_image_position)-3):
        if start_image_position[i]+start_image_position[i+1]+start_image_position[i+2]+start_image_position[i+3]==".bmp":
            check_image="normal"
    if check_image != "normal":
        print("Image format error. Only .bmp !")

    name=input("Enter the name for encrypted image. Don`t enter the format of image, only name!\n")

    message_len=len(message)         #Подсчет количества символов в сообщение
    image=open(start_image_position, "rb")
    size_image=len(image.read())                #Подсчет количества байтов в изображение

    if size_image < (54 + step + 4 + len(str(message_len))*(12//depth) + (12//depth) + message_len*(12//depth + interval)):    #Проверка на длину закодированного сообщения в байтах
        print("Very long message")
        return 0

    image=open(start_image_position, "rb")
    encrypted_image=open(name+".bmp", "wb")

    skip=image.read(54 + step)                                     #Первые 54 байта пропускаем + указанное смещение
    encrypted_image.write(skip)                              #и записываем в новую картинку

    copy_depth=ord(str(depth))                              #Создаем копию глубины кодировки для записи в картинку
    encrypt_depth_mask=0b11000000
    special_image_mask=0b11111100
    for i in range(4):                                                  #Для кодирования глубины будет использована глубина 2
        bits_of_depth=(copy_depth & encrypt_depth_mask)                         #Вписываем глубину кодировки в изображение для уменьшения количества
        bits_of_depth >>= 6                                             #параметров, передаваемых отдельно

        byte_of_image=image.read(1)
        byte_of_image=int.from_bytes(byte_of_image, sys.byteorder)
        bits_of_image=byte_of_image & special_image_mask

        new_byte=bits_of_depth | bits_of_image
        new_byte=new_byte.to_bytes(1, sys.byteorder)
        encrypted_image.write(new_byte)

        copy_depth <<= 2
        copy_depth %=256

    message_mask, image_mask = encrypt_masks(depth)             #Импротируем маски

    copy_message_len=str(message_len) + "*"             #Длина сообщения в формате строки и * для отделения от последующего сообщения
    for i in range(len(copy_message_len)):              #Длина также записывается в изображение
        symbol=ord(copy_message_len[i])

        for j in range(12//depth):
            bits_of_symbol=(symbol & message_mask)
            bits_of_symbol >>= (12 - depth)                      #Оставляем нужное количество битов от символа

            byte_of_image=image.read(1)
            byte_of_image=int.from_bytes(byte_of_image, sys.byteorder)
            bits_of_image=byte_of_image & image_mask                        #Очищаем такое же количество битов в байте изображения

            new_byte=bits_of_symbol | bits_of_image                 #Создаем байт с частью информации о символе
            new_byte=new_byte.to_bytes(1, sys.byteorder)         #Перевод в системный формат записи байтов
            encrypted_image.write(new_byte)

            symbol <<= depth                                    #Убираем уже записанные биты
            symbol %= 4096                                       #Приведение к 8-ми значному виду

    for i in range(message_len):
        symbol=ord(message[i])

        for j in range(12//depth):                            #Цикл для записи всех битов из символа
            bits_of_symbol=(symbol & message_mask)
            bits_of_symbol >>= (12 - depth)                      #Оставляем нужное количество битов от символа

            byte_of_image=image.read(1)
            byte_of_image=int.from_bytes(byte_of_image, sys.byteorder)
            bits_of_image=byte_of_image & image_mask                        #Очищаем такое же количество битов в байте изображения

            new_byte=bits_of_symbol | bits_of_image                 #Создаем байт с частью информации о символе
            new_byte=new_byte.to_bytes(1, sys.byteorder)         #Перевод в системный формат записи байтов
            encrypted_image.write(new_byte)

            symbol <<= depth                                    #Убираем уже записанные биты
            symbol %= 4096                                       #Приведение к 8-ми значному виду

        encrypted_image.write(image.read(interval))

    encrypted_image.write(image.read())             #Запись оставшихся байтов картинки

    print("*Message successfully encrypted*")
    print("Selected encrypting depth:", depth)
    print("Lenght of message:", message_len)
    print("Selected offset of message (bytes):", step)
    print("Selected interval between encrypted symbols (bytes):", interval)


def decrypct():

    step=int(input("Enter the offset of message: \n"))
    if step<0:                                                      #Только положительное число для правильной работы
        print("Error. Only > 0")
        return 0

    interval=int(input("Enter the interval between encrypted symbols: \n"))
    if interval<0:
        print("Error. Only > 0")
        return 0

    encrypted_image_position=input("Enter the full position of image with message: \n")
    check_image=""
    for i in range(len(encrypted_image_position)-3):
        if encrypted_image_position[i]+encrypted_image_position[i+1]+encrypted_image_position[i+2]+encrypted_image_position[i+3]==".bmp":
            check_image="normal"
    if check_image != "normal":
        print("Image format error. Only .bmp !")

    encrypted_image=open(encrypted_image_position, "rb")
    message=""

    skip=encrypted_image.read(54 + step)                       #Пропускаем байты со служебной информацией + заданное смещение

    decrypted_depth_mask=0b00000011
    depth=0b00000000
    counter=0                                              #Вспомогательный счетсчик для смещения
    for i in range(4):                                                                  #Считываем глубину кодировки из изображения
        byte_of_encrypted_image=encrypted_image.read(1)                                         #Глубина кодировки для кодировки глубины всегда 2
        byte_of_encrypted_image=int.from_bytes(byte_of_encrypted_image, sys.byteorder)
        bits_of_depth=byte_of_encrypted_image & decrypted_depth_mask

        if (6 - counter) > 0:                               # Нельзя делать смещение на 0 символов, поэтому проверка
            bits_of_depth <<= (6-counter)
            depth=depth | bits_of_depth

            counter += 2                                    #Увеличение значения счетсчика, для дальнейшей записи битов кодированного символа

        if (6 - counter) == 0:
            depth=depth | bits_of_depth

    depth=int(chr(depth))                                    #Переводим из кодировки unicod  в цифру, а затем в числовой формат

    decrypted_image_mask = decrypt_mask(depth)                  #Импортируем маску

    symbol=""
    message_len=""
    while symbol != "*":                               #Будет выполняться пока не найдет специально поставленную * (отделяющую длину от сообщения)
        symbol_of_message_len=0b000000000000
        counter=0                                      #Счетчик, который будет помогать записи двоичного кода расшифрованного сивола

        for i in range(12//depth):
            byte_of_encrypted_image=encrypted_image.read(1)                                     #Читаем байт с шифрованной информацией
            byte_of_encrypted_image=int.from_bytes(byte_of_encrypted_image, sys.byteorder)

            bits_of_encrypted_image=byte_of_encrypted_image & decrypted_image_mask      #Получение нужных для расшифровки битов из байтов картинки

            if (12 - depth - counter) > 0:                       # Нельзя делать смещение на 0 символов, поэтому проверка
                bits_of_encrypted_image <<= (12 - depth - counter)                   #Смещение для записи с начала (потом будет сдвигаться левее)
                symbol_of_message_len=symbol_of_message_len | bits_of_encrypted_image               #Записываем биты кодированного символа

                counter += depth                                           #Увеличение значения счетсчика, для дальнейшей записи битов кодированного символа

            if (12 -depth - counter) == 0:
                symbol_of_message_len=symbol_of_message_len | bits_of_encrypted_image

        symbol_of_message_len=chr(symbol_of_message_len)                        #Переводим двоичный код в цифру

        if symbol_of_message_len != "*":                                        #* не нужна в длине сообщения
            message_len +=symbol_of_message_len                                     #Заполняем длину сообщения

        symbol=symbol_of_message_len                                            #Запоминаем расшифрованный символ для проверки на *

    message_len=int(message_len)                                    #Переводим длину сообщения в числовой формат для дальнейшей работы

    for i in range(message_len):
        ord_of_symbol=0b000000000000
        counter=0                                      #Счетчик, который будет помогать записи двоичного кода расшифрованного сивола
        for j in range(12//depth):
            byte_of_encrypted_image=encrypted_image.read(1)                                 #Читаем байт с шифрованной информацией
            byte_of_encrypted_image=int.from_bytes(byte_of_encrypted_image, sys.byteorder)

            bits_of_encrypted_image=byte_of_encrypted_image & decrypted_image_mask      #Получение нужных для расшифровки битов из байтов картинки

            if (12 - depth - counter) > 0:                       # Нельзя делать смещение на 0 символов, поэтому проверка
                bits_of_encrypted_image <<= (12 - depth - counter)                   #Смещение для записи с начала (потом будет сдвигаться левее)
                ord_of_symbol=ord_of_symbol | bits_of_encrypted_image               #Записываем биты кодированного символа

                counter += depth                                           #Увеличение значения счетсчика, для дальнейшей записи битов кодированного символа

            if (12 - depth - counter) == 0:
                ord_of_symbol=ord_of_symbol | bits_of_encrypted_image

        symbol=chr(ord_of_symbol)                           #Определие символа по таблице кодировок
        message += symbol

        encrypted_image.read(interval)                  #Пропуск интервала между символами

    print(message)


def encrypt_masks(depth):

    message_mask=0b111111111111
    image_mask=0b11111111

    message_mask <<= (12 - depth)        #Сдвиг влево для получения необходмиго вида маски, например, 11000000
    message_mask %= 4096                 #Для обрезки лишних символов слева
    image_mask >>= depth                    #Сдвиг вправа для удаления единиц
    image_mask <<= depth                    #Сдвиг влево для получения нолей справа

    return message_mask, image_mask


def decrypt_mask(depth):

    decrypcted_image_mask=0b11111111
    decrypcted_image_mask >>= (8 - depth)

    return decrypcted_image_mask

start()



