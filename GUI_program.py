from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
import sys
import easygui                                      #Для окна выбора файла



class MainApp(App):

    def build(self):                                        #Стартовое окно с двумя кнопками

        floatlayout = FloatLayout()                    #Сюда будем добалять символы

        button_encrypt = Button(text="Зашифровать",                         #Кнопка зашифровать
                                size_hint=(0.48, 0.45),
                                pos_hint={'center_x': 0.25, 'center_y': 0.5},                    #Расположение на экране
                                background_color=(0/255, 191/255, 255/255, 1))
        button_encrypt.bind(on_press=app.encrypt_window)                       #При нажатии
        floatlayout.add_widget(button_encrypt)

        button_decrypt = Button(text="Расшифровать",                    #Кнопка расшифровать
                                size_hint=(0.48, 0.45),
                                pos_hint={'center_x': 0.75, 'center_y': 0.5},
                                background_color=(0/255, 191/255, 255/255, 1))
        button_decrypt.bind(on_press=app.decrypt_window)
        floatlayout.add_widget(button_decrypt)

        button_help = Button(text="Справка",                    #Кнопка справки
                             size_hint=(0.3, 0.17),
                             pos_hint={'center_x': 0.5, 'center_y': 0.11},
                             background_color=(0/255, 191/255, 255/255, 1))
        button_help.bind(on_press=app.help)
        floatlayout.add_widget(button_help)

        Window.clearcolor = (0/255, 191/255, 255/255, 1)       #Используется RGB со значениями делеными на 255

        return floatlayout



    def encrypt_window(self, instance):                             #Окно для шифрования

        grid_layout = GridLayout(cols=2, rows=7, padding=5)                 #Создаем гридлайаут для расположения элементов на экране

        select_depth_label = Label(text="Выберите глубину кодирования",
                                   size_hint=(0.5, 0.5))
        grid_layout.add_widget(select_depth_label)

        dropdown = DropDown()                                       #Выпадающий список для выбора глубины кодировки
        for depth in "1234":                                        #Кнопки с выбором глубины кодирования
            button_depth = Button(text=depth, size_hint=(1, None), height=50, background_color=(0/255, 191/255, 255/255, 1))           #Выпадающая кнопка со значением

            button_depth.bind(on_press=lambda button_depth: dropdown.select(button_depth.text))

            dropdown.add_widget(button_depth)
        dropdown.bind(on_select=lambda instance, x: setattr(self.default_depth_button, 'text', x))       #Для переноса выбранного значения на кнопку

        self.default_depth_button = Button(text='...', size_hint=(None, None), background_color=(0/255, 191/255, 255/255, 1))          #Кнопка, со значением по умолчанию
        self.default_depth_button.bind(on_press=dropdown.open)                       #Данная кнопка открывает выпадающий список
        grid_layout.add_widget(self.default_depth_button)

        select_offset_label = Label(text="Укажите смещение записи кодировки",
                                    size_hint=(0.5, 0.5))
        grid_layout.add_widget(select_offset_label)

        self.select_offset = TextInput(text="0", size_hint=(0.5, 0.5))         #Поле ввода для значения смещения
        grid_layout.add_widget(self.select_offset)

        select_interval_label = Label(text="Укажите интервал между закодированными символами",
                                      size_hint=(0.5, 0.5))
        grid_layout.add_widget(select_interval_label)

        self.select_interval = TextInput(text="0",  size_hint=(0.5, 0.5))         #Поле ввода для значения интервала
        grid_layout.add_widget(self.select_interval)

        select_way_to_image_label = Label(text="Выбор изображения",
                                          size_hint=(0.5, 0.5))
        grid_layout.add_widget(select_way_to_image_label)

        select_way_to_image = Button(text="Выбрать фаил",                              #Кнопка для открытия окна с выбором файла
                                          size_hint=(0.5, 0.5),
                                          background_color=(0/255, 191/255, 255/255, 1))
        select_way_to_image.bind(on_press=app.select_start_image)
        grid_layout.add_widget(select_way_to_image)

        select_way_to_message_label = Label(text="Нажмите на кнопку и введите сообщение",
                                            size_hint=(0.5, 0.5))
        grid_layout.add_widget(select_way_to_message_label)

        write_message_button = Button(text="Записать сообщение",           #Кнопка для открытия окна для записи сообщения
                                      size_hint=(0.5, 0.5),
                                      background_color=(0/255, 191/255, 255/255, 1))
        write_message_button.bind(on_press=app.enter_message_window)
        grid_layout.add_widget(write_message_button)

        select_place_for_encrypted_image_label = Label(text="Выбор место для сохранения нового файла",
                                                       size_hint=(0.5, 0.5))
        grid_layout.add_widget(select_place_for_encrypted_image_label)

        select_place_for_encrypted_image_button = Button(text="Выбрать место",       #Кнопка для выбора места для сохранения файла с зашифрованной информацией
                                                        size_hint=(0.5, 0.5),
                                                        background_color=(0/255, 191/255, 255/255, 1))
        select_place_for_encrypted_image_button.bind(on_press=app.select_place_for_save_encrypted_image)
        grid_layout.add_widget(select_place_for_encrypted_image_button)

        popup = Popup(title="Зашифровать сообщение",              #Заголовок для окна
                      content=grid_layout,
                      background_color=(30/255, 144/255, 255/255, 1))                            #Добавляем элементы на экран
        popup.open()                                                #Вызываем окно

        encrypt_button = Button(text="Зашифровать", background_color=(0/255, 191/255, 255/255, 1))             #Кнопка для старта
        encrypt_button.bind(on_press=app.encrypt)                        #При нажатии запускается функция, забирающая введенные значения
        grid_layout.add_widget(encrypt_button)

        closeButton = Button(text="На главный экран",           #Кнопка возврата на главный экран
                             size_hint=(0.5, 0.5),
                             background_color=(0/255, 191/255, 255/255, 1))
        closeButton.bind(on_press=popup.dismiss)
        grid_layout.add_widget(closeButton)



    def decrypt_window(self, instance):                                 #Окно для расшифровки

        grid_layout = GridLayout(cols=2, rows=4, padding=5)                 #Создаем гридлайаут для расположения элементов на экране

        select_offset_label = Label(text="Укажите смещение записи кодировки",
                                    size_hint=(0.5, 0.5))
        grid_layout.add_widget(select_offset_label)

        self.select_offset = TextInput(text="0", size_hint=(0.5, 0.5))         #Поле ввода для значения смещения
        grid_layout.add_widget(self.select_offset)

        select_interval_label = Label(text="Укажите интервал между \nзакодированными символами",
                                      size_hint=(0.5, 0.5))
        grid_layout.add_widget(select_interval_label)

        self.select_interval = TextInput(text="0", size_hint=(0.5, 0.5))         #Поле ввода для значения интервала
        grid_layout.add_widget(self.select_interval)

        select_way_to_image_label = Label(text="Выбор изображения",
                                          size_hint=(0.5, 0.5))
        grid_layout.add_widget(select_way_to_image_label)

        select_way_to_image = Button(text="Выбрать фаил",                              #Кнопка для открытия окна с выбором картинки
                                          size_hint=(0.5, 0.5),
                                          background_color=(0/255, 191/255, 255/255, 1))
        select_way_to_image.bind(on_press=app.select_encrypted_image)
        grid_layout.add_widget(select_way_to_image)

        popup = Popup(title="Расшифровать сообщение",              #Заголовок для окна
                      content=grid_layout,
                      background_color=(30/255, 144/255, 255/255, 1))                            #Добавляем элементы на экран
        popup.open()                                                #Вызываем окно

        decrypt_button = Button(text="Расшифровать",
                                size_hint=(0.75, 0.5),
                                background_color=(0/255, 191/255, 255/255, 1))                #Кнопка для начала расшифровки
        decrypt_button.bind(on_press=app.decrypt)
        grid_layout.add_widget(decrypt_button)

        closeButton = Button(text="На главный экран",           #Кнопка возврата на главный экран
                             size_hint=(0.5, 0.5),
                             background_color=(0/255, 191/255, 255/255, 1))
        closeButton.bind(on_press=popup.dismiss)                  #Кнопка возврата наглавный экран
        grid_layout.add_widget(closeButton)



    def select_start_image(self, instance):                 #Окно выбора картинки для записи

        self.way_to_start_image = easygui.fileopenbox(title="Выбор изображения", default="*.bmp")



    def enter_message_window(self, instance):                  #Окно ввода сообщения

        boxlayout = BoxLayout(orientation="vertical",         #Сверху сообщение, снизу кнопка возврата
                              padding=5,                     #Оконтовка по краю
                              spacing=10)                        #Расстояние между элиментами

        self.text_message_label = TextInput(text="")           #Записываем сообщение в поле
        boxlayout.add_widget(self.text_message_label)

        popup = Popup(title="Введите сообщение",              #Заголовок для окна
                      content=boxlayout,
                      background_color=(30/255, 144/255, 255/255, 1))
        popup.open()

        close_button = Button(text="Назад",
                              size_hint=(1, 0.33),
                              background_color=(0/255, 191/255, 255/255, 1))
        close_button.bind(on_press=popup.dismiss)
        boxlayout.add_widget(close_button)



    def select_place_for_save_encrypted_image(self, instance):               #Окно выбора места для сохранения картинки с зашифрованной информацией

        self.place_for_encrypted_image = easygui.filesavebox(title='Выберите место сохранения файла', default='encrypted_image.bmp')



    def succes_encrypt_window(self):                    #Окно при успешной расшифровке

        boxlayout = BoxLayout(orientation="vertical",         #Сверху сообщение, снизу кнопка возврата
                              padding=5,                     #Оконтовка по краю
                              spacing=10)                        #Расстояние между элиментами

        global default_depth_button                 #Забираем значение глубины кодирования
        depth = self.default_depth_button.text

        global select_offset                        #Забираем значение смещения от начала байтов, с закодированной информацией
        step = self.select_offset.text

        global select_interval                      #Забираем значение интервала между зашифрованными и записанными символами
        interval = self.select_interval.text

        global text_message_label                           #Забираем длину сообщения
        message_len = str(len(self.text_message_label.text))

        text=f"Выбранная гулубина кодировки: {depth} \nВыбранный отступ для записи: {step} \nВыбранный интервал: {interval} \nДлина сообщения: {message_len}"

        information_label = Label(text=text)           #Записываем сообщение в поле
        boxlayout.add_widget(information_label)

        popup = Popup(title="Сообщение успешно засшифровано",              #Заголовок для окна
                      content=boxlayout,
                      background_color=(30/255, 144/255, 255/255, 1))
        popup.open()

        close_button = Button(text="Назад",
                              size_hint=(1, 0.33),
                              background_color=(0/255, 191/255, 255/255, 1))
        close_button.bind(on_press=popup.dismiss)
        boxlayout.add_widget(close_button)



    def select_encrypted_image(self, instance):                     #Окно выбора картинки с сообщением

        self.way_to_encrypted_image = easygui.fileopenbox(title="Выбор изображения", default="*.bmp")



    def succes_decrypt_window(self):                  #Окно при успешном шифровании

        boxlayout = BoxLayout(orientation="vertical",         #Сверху сообщение, снизу кнопка возврата
                              padding=5,                     #Оконтовка по краю
                              spacing=10)                        #Расстояние между элиментами

        global decrypted_text                       #Забираем расшифрованное сообщение
        text = self.decrypted_text
        text_label = TextInput(text=text)           #Записываем сообщение в поле
        boxlayout.add_widget(text_label)

        popup = Popup(title="Сообщение успешно расшифровано",              #Заголовок для окна
                      content=boxlayout,
                      background_color=(30/255, 144/255, 255/255, 1))
        popup.open()

        close_button = Button(text="Назад",
                              size_hint=(1, 0.33),
                              background_color=(0/255, 191/255, 255/255, 1))
        close_button.bind(on_press=popup.dismiss)
        boxlayout.add_widget(close_button)



    def help(self, instance):                               #Окно со справкой

        boxlayout = BoxLayout(orientation="vertical",         #Сверху текст, снизу кнопка возврата
                              padding=5,                     #Оконтовка по краю
                              spacing=10)                        #Расстояние между элиментами

        text = '## Главный экран: \n\n    # Кнопка "Зашифровать": \n          Если вы хотите зашифровать сообщение в изображение нажмите на эту кнопку.' \
               '\n\n    # Кнопка "Расшифровать": \n          Если вы хотите расшифровать сообщение из изображения нажмите на эту кнопку.' \
               '\n\n    # Кнопка "Справка": \n          Данная кнопка открывает окно со справкой. Нажмите на неё, если у вас есть вопросы о работе программы.' \
               '\n\n## Окно "Зашифровать сообщение": \n\n    # Выбор глубины кодирования:' \
               '\n          Глубина кодирования - это количество битов, которые заменяются в одном байте изображения. ' \
               'Каждый символ из вашего сообщения приводится к виду 12-ти значного двоичного числа. ' \
               'Затем программа по частям записывает код данного символа в изображения, заменяя младшие биты (те, что стоят справа) в байте на часть кода символа (1, 2, 3 или 4 бита в зависимости от выбранной глубины кодирования). ' \
               'Таким образом, на запись одного символа может затрачиваться 12, 6, 4 или 3 байта изображения. Чем меньше глубина кодирования, тем сложнее отличить исходную картинку от картинки с сообщением.' \
               '\n          При выборе глубины кодирования 1 или 2 отличить картинку от оригинала невооруженным взглядом практически невозможно. При выборе глубины кодирования 4, большой длине сообщения и использование картинки со светлым фоном можно заметить некоторые отличия. ' \
               'Однако чем меньше глубина кодирования, тем меньше символов может быть в вашем сообщение. Для выбора данного параметра необходимо воспользоваться выпадающим списком.' \
               '\n          Пример: Возмём русскую букву "а". Её номер в таблице Unicode - 1072. Переведём в двоичную систему и получим 010000110000. Предположим, что мы выбрали глубину кодирования 4. Тогда выделим первые 4 цифры и получим 0100. ' \
               'Далее программа прочитает один байт из изображения. Допустим, что он равен 11111111. Заменим 4 правых бита на часть кода символа. Получим новый байт 11110100. Данный байт и будет записан в новое изображение. ' \
               'Данные дейтвия будут повторяться, пока программа не зашифрует все части кода сивола. Затем данный алгоритм будет повторен с другим символом.' \
               '\n\n    # Выбор смещения записи кодировки:' \
               '\n          Смещение записи кодировки - это количество байтов изображения, которые будут пропущены (просто переписаны в новое изображение) в начале изображения. ' \
               'Данный параметр позволяет повысить надежность шифрования, так как он значительно усложняет взлом шифра путем полного перебора. Смещение записи кодировки - это положительное целое число!' \
               '\n          Пример: Предположим, что выбранное значение смещения записи кодировки равно 46. Это значит, что программа пропустит (просто перепишет в новое) первые 54 байта изображения (являются хранителями служебной информации, например, имени файла), ' \
               'а затем пропустит ещё 46 байт. Таким образом, запись первого символа в изображения начнется со 101 байта.' \
               '\n\n    # Выбор интервала между закодированными символами:' \
               '\n          Интревал между закодированными символами - это количество байт, которое будет пропущено (просто переписано в новое изображение) после записи одного символа. Данный параметр позволяет повысить надежность шифрования, так как он значительно усложняет взлом шифра путем полного перебора. ' \
               'Интервал между зашированными символа - это положительное целое число!' \
               '\n          Пример: Предположим, что выбранное значение интервала равно 4. Это значит, что после записи символа в изображения (на это может уйти 12, 6, 4 или 3 байта (смотри пункт "выбор глубины кодирования")) будет пропущено (просто переписано в новое изображение) 4 байта, а затем начнет записываться новый символ.' \
               '\n\n    # Выбор изображения:' \
               '\n          Для выбора изображения, в которое вы хотите зашифровать сообщение, необходимо нажать кнопку "Выбрать фаил". Будет создана копия выбранного изображения. Поддерживаются только изображения в формате Bitmap (.bmp).' \
               '\n\n    # Запись сообщения:' \
               '\n          Для записи сообщения необходимо нажать на кнопку "Записать сообщение" и ввести свое сообщение в поле ввода в открывшемся окне. После этого нужно нажать на кнопку "Назад" и вы вернетесь на экран "Зашифровать сообщение". ' \
               '\n\n    # Выбор места сохранения и имени для изображения с зашифрованной информацией:' \
               '\n          Для выбора места сохранения и имени нового изображения необходимо нажать кнопку "Выбрать место", в открывшемся окне перейти в нужную папку, ввести имя нового изображения (по умолчанию имя равно encrypted_image) и нажать кнопку "Сохранить".' \
               '\n\n    # Кнопка "Зашифровать":' \
               '\n          Данная кнопка запустит процесс шифрования. Если шифрование пройдет успешно, появиться окно с сообщением об успешном шифровании и вспомогательной информацией о выбранных параметрах. Нажав на кнопку "Назад" в данном окне, вы вернетесь на экран "Зашифровать сообщение".' \
               '\n\n    # Кнопка "На главный экран":' \
               '\n          Данная кнопка вернет вас на главный экран.' \
               '\n\n## Окно "Расшифровать сообщение":' \
               '\n\n    # Ввод смещения записи кодировки:' \
               '\n          В поле ввода необходимо ввести значение смещения записи кодировки, выбранное при шифровании. Смещение записи кодировки - положительное целое число! За что отвечает данный парметр можно посмтреть в подпункте "Выбор смещения записи кодировки" пункта "Окно "Зашифровать сообщение"".' \
               '\n\n    # Ввод интервала между закодированными символами:' \
               '\n          В поле ввода необходимо ввести значение интервала между закодированными символами, выбранное при шифровании. Интервал между закодированными символами - положительное целое число! За что отвечает данный парметр можно посмтреть в подпункте "Выбор интервала между закодированными символами" пункта "Окно "Зашифровать сообщение"".' \
               '\n\n    # Выбор изображения с закодированной в нем информацией:' \
               '\n          Для выбора изображения, из которого вы хотите расшифровать сообщение, необходимо нажать кнопку "Выбрать фаил". Поддерживаются только изображения в формате Bitmap (.bmp).' \
               '\n\n    # Кнопка "Расшифровать":' \
               '\n          Данная кнопка запустит процесс расшифровки. Если расшифровка пройдет успешно, появиться окно с расшифрованным сообщением. Нажав на кнопку "Назад" в данном окне, вы вернетесь на экран "Расшифровать сообщение".' \
               '\n\n    # Кнопка "На главный экран":' \
               '\n          Данная кнопка вернет вас на главный экран.'

        help_text = TextInput(text=text, focus=True)
        boxlayout.add_widget(help_text)

        popup = Popup(title="Справка",              #Заголовок для окна
                      content=boxlayout,
                      background_color=(30/255, 144/255, 255/255, 1))
        popup.open()

        close_button = Button(text="Назад",
                              size_hint=(1, 0.2),
                              background_color=(0/255, 191/255, 255/255, 1))
        close_button.bind(on_press=popup.dismiss)
        boxlayout.add_widget(close_button)



    def encrypt(self, instance):

        try:                        #Пробуем зашифровать
            check_value = ""                 #Параметр для проверки введенных значений

            global default_depth_button                 #Забираем значение глубины кодирования
            try:
                depth = int(self.default_depth_button.text)
            except:
                check_value = "stop"
                easygui.msgbox('Выберите глубину кодирования!', 'Не выбрано значение')   #Окно с ошибкой

            global select_offset                        #Забираем значение смещения от начала байтов, с закодированной информацией
            try:                                        #Проверка на корректность введенного значения
                step = int(self.select_offset.text)
                if step < 0:
                    check_value = "stop"
                    easygui.msgbox('Введено некорректное значение смещения. \nВведите положительное число!', 'Ошибка в значение')   #Окно с ошибкой
            except:
                check_value = "stop"
                easygui.msgbox('Введено некорректное значение смещения. \nВведите положительное число!', 'Ошибка в значение')

            global select_interval                      #Забираем значение интервала между зашифрованными и записанными символами
            try:                                            #Проверка на корректность введенного значения
                interval = int(self.select_interval.text)
                if interval < 0:
                    check_value = "stop"
                    easygui.msgbox('Введено некорректное значение интервала. \nВведите положительное число!', 'Ошибка в значение')  #Окно с ошибкой
            except:
                check_value = "stop"
                easygui.msgbox('Введено некорректное значение интервала. \nВведите положительное число!', 'Ошибка в значение')

            global text_message_label                           #Забираем сообщение
            message = self.text_message_label.text

            global way_to_start_image                               #Забираем путь до стартового изображения
            start_image_position = self.way_to_start_image
            warning_type_of_file = ""                                   #Проверка на формат файла
            for i in range(len(start_image_position) - 3):
                if start_image_position[i]+start_image_position[i+1]+start_image_position[i+2]+start_image_position[i+3] == ".bmp":
                    warning_type_of_file = "normal"
            if warning_type_of_file != "normal":
                easygui.msgbox('Выбран фаил формата отличного от .bmp \nВыберите .bmp фаил!', 'Неподдерживаемый формат файла')
                check_value = "stop"

            global place_for_encrypted_image                                    #Забираем путь для сохранения нового изображения
            encrypted_image_position = self.place_for_encrypted_image
            check_encrypted_image_position = ""                                                   #Проверка на формат и наличие точек в файле
            for i in range(len(encrypted_image_position)):
                if encrypted_image_position[i] == ".":
                    check_encrypted_image_position = "error"
            for i in range(len(encrypted_image_position) - 3):
                if encrypted_image_position[i] + encrypted_image_position[i+1] + encrypted_image_position[i+2] + encrypted_image_position[i+3] == ".bmp":
                    check_encrypted_image_position = "normal"
            if check_encrypted_image_position == "":
                encrypted_image_position += ".bmp"
            elif check_encrypted_image_position == "error":
                check_value = "stop"
                easygui.msgbox('Введено недопустимое имя файла! \nМожно сохранять только файлы .bmp формата. '
                                   '\nНе используйте точки в имени файла!', 'Недопустимое имя файла')                       #Окно с ошибкой

            if check_value != "stop":                       #При корректных значениях шифруем
                message_mask=0b111111111111                                #Создаем маски для шифрования
                image_mask=0b11111111
                message_mask <<= (12 - depth)        #Сдвиг влево для получения необходмиго вида маски, например, 11000000
                message_mask %= 4096                 #Для обрезки лишних символов слева
                image_mask >>= depth                    #Сдвиг вправа для удаления единиц
                image_mask <<= depth                    #Сдвиг влево для получения нолей справа

                message_len = len(message)            #Подсчет количества символов в сообщение
                image = open(start_image_position, "rb")
                size_image = len(image.read())                #Подсчет количества байтов в изображение

                check_len = ""                                  #Проверка на длину сообщения
                if size_image < (54 + step + 4 + len(str(message_len))*(12//depth) + (12//depth) + message_len*(12//depth + interval)):    #Проверка на длину закодированного сообщения в байтах
                    easygui.msgbox('Данное сообщение невозможно записать в выбранный фаил. \nСократите сообщение, выберите другой фаил или измените параметры шифрования.', 'Ошибка длины')
                    check_len = "stop"

                if check_len != "stop":
                    image = open(start_image_position, "rb")
                    encrypted_image = open(encrypted_image_position, "wb")

                    skip = image.read(54 + step)                                     #Первые 54 байта пропускаем + указанное смещение
                    encrypted_image.write(skip)                              #и записываем в новую картинку

                    copy_depth = ord(str(depth))                              #Создаем копию глубины кодировки для записи в картинку
                    encrypt_depth_mask = 0b11000000
                    special_image_mask = 0b11111100
                    for i in range(4):                                                  #Для кодирования глубины будет использована глубина 2
                        bits_of_depth = (copy_depth & encrypt_depth_mask)                         #Вписываем глубину кодировки в изображение для уменьшения количества
                        bits_of_depth >>= 6                                             #параметров, передаваемых отдельно

                        byte_of_image = image.read(1)
                        byte_of_image = int.from_bytes(byte_of_image, sys.byteorder)
                        bits_of_image = byte_of_image & special_image_mask

                        new_byte = bits_of_depth | bits_of_image
                        new_byte = new_byte.to_bytes(1, sys.byteorder)
                        encrypted_image.write(new_byte)

                        copy_depth <<= 2
                        copy_depth %=256

                    copy_message_len = str(message_len) + "*"             #Длина сообщения в формате строки и * для отделения от последующего сообщения
                    for i in range(len(copy_message_len)):              #Длина также записывается в изображение
                        symbol = ord(copy_message_len[i])

                        for j in range(12//depth):
                            bits_of_symbol = (symbol & message_mask)
                            bits_of_symbol >>= (12 - depth)                      #Оставляем нужное количество битов от символа

                            byte_of_image = image.read(1)
                            byte_of_image = int.from_bytes(byte_of_image, sys.byteorder)
                            bits_of_image = byte_of_image & image_mask                        #Очищаем такое же количество битов в байте изображения

                            new_byte = bits_of_symbol | bits_of_image                 #Создаем байт с частью информации о символе
                            new_byte = new_byte.to_bytes(1, sys.byteorder)         #Перевод в системный формат записи байтов
                            encrypted_image.write(new_byte)

                            symbol <<= depth                                    #Убираем уже записанные биты
                            symbol %= 4096                                       #Приведение к 8-ми значному виду

                    for i in range(message_len):
                        symbol = ord(message[i])

                        for j in range(12//depth):                            #Цикл для записи всех битов из символа
                            bits_of_symbol = (symbol & message_mask)
                            bits_of_symbol >>= (12 - depth)                      #Оставляем нужное количество битов от символа

                            byte_of_image = image.read(1)
                            byte_of_image = int.from_bytes(byte_of_image, sys.byteorder)
                            bits_of_image = byte_of_image & image_mask                        #Очищаем такое же количество битов в байте изображения

                            new_byte = bits_of_symbol | bits_of_image                 #Создаем байт с частью информации о символе
                            new_byte = new_byte.to_bytes(1, sys.byteorder)         #Перевод в системный формат записи байтов
                            encrypted_image.write(new_byte)

                            symbol <<= depth                                    #Убираем уже записанные биты
                            symbol %= 4096                                       #Приведение к 8-ми значному виду

                        encrypted_image.write(image.read(interval))

                    encrypted_image.write(image.read())             #Запись оставшихся байтов картинки

                    self.succes_encrypt_window()

        except:
            if check_value != "stop":                   #Чтобы избежать появления двух окон
                easygui.msgbox('Произошла какая-то неизвестная ошибка. \nПроверте заполнение всех полей.'
                               '\nВозможно в вашем сообщение есть неподдерживаемые символы или изображение было повреждено.', 'Ошибка')



    def decrypt(self, instance):

        try:                                #Пробуем расшифровать
            check_value = ""                        #Параметр для проверки значений на корректность

            global select_offset                            #Забираем значение смещения от начала для закодированных байтов
            try:                                        #Проверка введенного значения
                step = int(self.select_offset.text)
                if step < 0:
                    check_value = "stop"
                    easygui.msgbox('Введено некорректное значение смещения. \nВведите положительное число.', 'Ошибка в значение')   #Окно с ошибкой
            except:
                check_value = "stop"
                easygui.msgbox('Введено некорректное значение смещения. \nВведите положительное число.', 'Ошибка в значение')

            global select_interval                          #Забираем значение интервала между зашифрованными символами
            try:                                                    #Проверка введенного значения
                interval = int(self.select_interval.text)
                if interval < 0:
                    check_value = "stop"
                    easygui.msgbox('Введено некорректное значение интервала. \nВведите положительное число.', 'Ошибка в значение')  #Окно с ошибкой
            except:
                check_value = "stop"
                easygui.msgbox('Введено некорректное значение интервала. \nВведите положительное число.', 'Ошибка в значение')

            global way_to_encrypted_image                          #Забираем путь до картинки с информацией
            encrypted_image_position = self.way_to_encrypted_image

            warning_type_of_file = ""                                   #Проверка на формат файла
            for i in range(len(encrypted_image_position) - 3):
                if encrypted_image_position[i]+encrypted_image_position[i+1]+encrypted_image_position[i+2]+encrypted_image_position[i+3] == ".bmp":
                    warning_type_of_file = "normal"
            if warning_type_of_file != "normal":
                easygui.msgbox('Выбран фаил формата отличного от .bmp \nВыберите .bmp фаил!', 'Неподдерживаемый формат файла')
                check_value = "stop"

            if check_value != "stop":                   #При корректных значениях расшифровываем
                encrypted_image = open(encrypted_image_position, "rb")

                skip = encrypted_image.read(54 + step)                       #Пропускаем байты со служебной информацией + заданное смещение

                decrypted_depth_mask = 0b00000011
                depth = 0b00000000
                counter = 0                                              #Вспомогательный счетсчик для смещения
                for i in range(4):                                                                  #Считываем глубину кодировки из изображения
                    byte_of_encrypted_image = encrypted_image.read(1)                                         #Глубина кодировки для кодировки глубины всегда 2
                    byte_of_encrypted_image = int.from_bytes(byte_of_encrypted_image, sys.byteorder)
                    bits_of_depth = byte_of_encrypted_image & decrypted_depth_mask

                    if (6 - counter) > 0:                               # Нельзя делать смещение на 0 символов, поэтому проверка
                        bits_of_depth <<= (6-counter)
                        depth=depth | bits_of_depth

                        counter += 2                                    #Увеличение значения счетсчика, для дальнейшей записи битов кодированного символа

                    if (6 - counter) == 0:
                        depth=depth | bits_of_depth

                depth = int(chr(depth))                                    #Переводим из кодировки unicod  в цифру, а затем в числовой формат

                decrypcted_image_mask = 0b111111111111                    #Создаем маску для расшифровки
                decrypcted_image_mask >>= (12 - depth)

                symbol = ""
                message_len = ""
                while symbol != "*":                               #Будет выполняться пока не найдет специально поставленную * (отделяющую длину от сообщения)
                    symbol_of_message_len = 0b000000000000
                    counter = 0                                      #Счетчик, который будет помогать записи двоичного кода расшифрованного сивола

                    for i in range(12//depth):
                        byte_of_encrypted_image = encrypted_image.read(1)                                     #Читаем байт с шифрованной информацией
                        byte_of_encrypted_image = int.from_bytes(byte_of_encrypted_image, sys.byteorder)

                        bits_of_encrypted_image = byte_of_encrypted_image & decrypcted_image_mask      #Получение нужных для расшифровки битов из байтов картинки

                        if (12 - depth - counter) > 0:                       # Нельзя делать смещение на 0 символов, поэтому проверка
                            bits_of_encrypted_image <<= (12 - depth - counter)                   #Смещение для записи с начала (потом будет сдвигаться левее)
                            symbol_of_message_len = symbol_of_message_len | bits_of_encrypted_image               #Записываем биты кодированного символа

                            counter += depth                                           #Увеличение значения счетсчика, для дальнейшей записи битов кодированного символа

                        if (12 - depth - counter) == 0:
                            symbol_of_message_len = symbol_of_message_len | bits_of_encrypted_image

                    symbol_of_message_len = chr(symbol_of_message_len)                        #Переводим двоичный код в цифру

                    if symbol_of_message_len != "*":                                        #* не нужна в длине сообщения
                        message_len += symbol_of_message_len                                     #Заполняем длину сообщения

                    symbol = symbol_of_message_len                                            #Запоминаем расшифрованный символ для проверки на *

                message_len = int(message_len)                                    #Переводим длину сообщения в числовой формат для дальнейшей работы

                self.decrypted_text = ""                       #Создаем строку в которуюдобавим расшифрованные символы

                for i in range(message_len):
                    ord_of_symbol = 0b000000000000
                    counter = 0                                      #Счетчик, который будет помогать записи двоичного кода расшифрованного сивола
                    for j in range(12//depth):
                        byte_of_encrypted_image = encrypted_image.read(1)                                 #Читаем байт с шифрованной информацией
                        byte_of_encrypted_image = int.from_bytes(byte_of_encrypted_image, sys.byteorder)
                        bits_of_encrypted_image = byte_of_encrypted_image & decrypcted_image_mask     #Получение нужных для расшифровки битов из байтов картинки

                        if (12 - depth - counter) > 0:                       # Нельзя делать смещение на 0 символов, поэтому проверка
                            bits_of_encrypted_image <<= (12 - depth - counter)                   #Смещение для записи с начала (потом будет сдвигаться левее)
                            ord_of_symbol = ord_of_symbol | bits_of_encrypted_image               #Записываем биты кодированного символа

                            counter += depth                                           #Увеличение значения счетсчика, для дальнейшей записи битов кодированного символа

                        if (12 - depth - counter) == 0:
                            ord_of_symbol = ord_of_symbol | bits_of_encrypted_image

                    symbol = chr(ord_of_symbol)                           #Определие символа по таблице кодировок

                    self.decrypted_text += symbol                       #Добавляем символ в строку

                    encrypted_image.read(interval)                  #Пропуск интервала между символами

                self.succes_decrypt_window()                    #Вызываем окно успешной расшифровки

        except:                                   #Если не получается расшифровать
            if check_value != "stop":                   #Чтобы избежать появления двух окон
                easygui.msgbox('Произошла ошибка при расшифровке. \nПроверьте выбран ли фаил. '
                                '\nПроверте соответствие введеных значений выбранному файлу.', 'Ошибка')  #Окно с ошибкой



if __name__ == '__main__':
    app = MainApp()
    app.run()





