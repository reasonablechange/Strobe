import os
import time

try:
    import requests
    from requests.structures import CaseInsensitiveDict
    from PIL import Image
    import numpy as np
except:
    try:
        os.system('pip3 install requests pillow numpy')
        import requests
        from requests.structures import CaseInsensitiveDict
    except:
        print('Не удается скачать один или несколько модулей, необходимых для корректной работы бота. '
              'Пожалуйста, проверьте соединение и перезапустите программу.')

version = 'v1.0.5 release'

import tkinter as tk
import tkinter.ttk as ttk
import threading
import sqlite3
from tkinter import Menu
import random

''' TODO:
1) Заменить цвет black на #252525 или #1B1C1E
2) Привязать механизм мигания к данным таблицы'''


class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.window.quit()

    def run(self):
        def check_database():
            conn = sqlite3.connect('main.db')
            c = conn.cursor()
            try:
                c.execute('SELECT * FROM Params')
            except sqlite3.OperationalError:
                c.execute('''CREATE TABLE Params
                             (ratio INTEGER, duration INTEGER, freq INTEGER, pic_left TEXT, pic_center TEXT, pic_right TEXT)''')
                if os.path.isfile('tree.png') and os.path.isfile('car.png') and os.path.isfile('apple.png'):
                    c.execute("INSERT INTO Params VALUES (?, ?, ?, ?, ?, ?)",
                              (12, 240, 10, 'tree.png', 'car.png', 'apple.png'))
            try:
                c.execute('SELECT * FROM Secondary_params')
            except sqlite3.OperationalError:
                c.execute('''CREATE TABLE Secondary_params
                             (pic_left TEXT, pic_center TEXT, pic_right TEXT)''')
                if os.path.isfile('tree.png') and os.path.isfile('car.png') and os.path.isfile('apple.png'):
                    c.execute("INSERT INTO Secondary_params VALUES (?, ?, ?)",
                              ('tree.png', 'car.png', 'apple.png'))

            try:
                c.execute('SELECT * FROM Screen_params')
            except sqlite3.OperationalError:
                c.execute('''CREATE TABLE Screen_params (screen_size TEXT)''')

            try:
                c.execute('SELECT * FROM Queue')
            except sqlite3.OperationalError:
                c.execute('''CREATE TABLE Queue (ratio INTEGER, duration INEGER)''')
                c.execute("INSERT INTO Queue VALUES (?, ?)", (12, 240))
                c.execute("INSERT INTO Queue VALUES (?, ?)", (12, 240))
                c.execute("INSERT INTO Queue VALUES (?, ?)", (12, 240))
                c.execute("INSERT INTO Queue VALUES (?, ?)", (12, 240))
                c.execute("INSERT INTO Queue VALUES (?, ?)", (12, 240))
                c.execute("INSERT INTO Queue VALUES (?, ?)", (12, 240))

            conn.commit()
            conn.close()

        def destroy_window():
            for widget in self.window.winfo_children():
                widget.destroy()

        def resize_image(input_file_path, output_file_path, new_width=None, new_height=None):
            with Image.open(input_file_path) as image:
                if not new_width and not new_height:
                    raise ValueError("Either 'new_width' or 'new_height' must be provided.")
                if not new_width:
                    new_width = round(new_height * image.width / image.height)
                if not new_height:
                    new_height = round(new_width * image.height / image.width)

                resized_image = image.resize((new_width, new_height))
                resized_image.save(output_file_path)

        def remove_thumbnails():
            for root, dirs, files in os.walk(".", topdown=False):
                for name in files:
                    if "thumbnail" in name:
                        os.remove(os.path.join(root, name))
                for name in dirs:
                    if "thumbnail" in name:
                        os.rmdir(os.path.join(root, name))  # добавлено удаление пустых папок, содержащих "thumbnail"

        def start():
            destroy_window()
            main_interface()

            database = sqlite3.connect('main.db')
            cursor = database.cursor()
            cursor.execute("SELECT * FROM Screen_params;")
            screen_size_db = cursor.fetchone()[0]
            cursor.execute("SELECT * FROM Params;")
            ratio, duration, freq, left, center, right = cursor.fetchone()

            # if screen_size_db.split('x')[0] != '1920' or screen_size_db.split('x')[1] != '1080':
            #     remove_thumbnails()
            #     resize_image(input_file_path=left,
            #                  output_file_path=f"{left.split['.'][0]}_thumbnail.png",
            #                  new_width=512 * (int(screen_size_db.split('x')[0]) / 1920))
            #     resize_image(input_file_path=center,
            #                  output_file_path=f"{center.split['.'][0]}_thumbnail.png",
            #                  new_width=512 * (int(screen_size_db.split('x')[0]) / 1920))
            #     resize_image(input_file_path=right,
            #                  output_file_path=f"{right.split['.'][0]}_thumbnail.png",
            #                  new_width=512 * (int(screen_size_db.split('x')[0]) / 1920))
            #     resize_image(input_file_path='black.png',
            #                  output_file_path=f"black_thumbnail.png",
            #                  new_width=512 * (int(screen_size_db.split('x')[0]) / 1920))
            #     tree = tk.PhotoImage(file=f"{left}_thumbnail.png")
            #     car = tk.PhotoImage(file=f"{center}_thumbnail.png")
            #     apple = tk.PhotoImage(file=f"{right}_thumbnail.png")
            #     black = tk.PhotoImage(file=f"black_thumbnail.png")
            #
            #     im = Image.open(f'{left}_thumbnail.png')
            #     tree_width, tree_height = im.size
            #
            #     im = Image.open(f'{center}_thumbnail.png')
            #     car_width, car_height = im.size
            #
            #     im = Image.open(f'{right}_thumbnail.png')
            #     apple_width, apple_height = im.size
            #
            # else:
            tree = tk.PhotoImage(file=left)
            car = tk.PhotoImage(file=center)
            apple = tk.PhotoImage(file=right)
            black = tk.PhotoImage(file="black.png")
            im = Image.open(left)
            tree_width, tree_height = im.size
            im = Image.open(center)
            car_width, car_height = im.size
            im = Image.open(right)
            apple_width, apple_height = im.size

            canvas_tree = tk.Canvas(self.window, height=tree_height + 10, width=tree_width + 10,
                                    background='black', bd=0, highlightthickness=0, relief='ridge')
            canvas_tree.create_image(5, 5, anchor='nw', image=tree)
            canvas_tree.place(x=(int(screen_size_db.split('x')[1]) / 3) - (tree_width / 2),
                              y=(int(screen_size_db.split('x')[0]) / 4) - (tree_height / 2))

            Artwork_car = tk.Label(self.window, image=car, height=car_height + 10, width=car_width + 10,
                                   background='black')
            Artwork_car.photo = car
            Artwork_car.place(x=(int(screen_size_db.split('x')[1]) / 3) + tree_width + 10 - (car_width / 2),
                              y=(int(screen_size_db.split('x')[0]) / 4) - (car_height / 2))

            canvas_apple = tk.Canvas(self.window, height=apple_height + 10, width=apple_width + 10,
                                     background='black', bd=0, highlightthickness=0, relief='ridge')
            canvas_apple.create_image(5, 5, anchor='nw', image=apple)
            canvas_apple.place(
                x=(int(screen_size_db.split('x')[1]) / 3) + tree_width + apple_width + 30 - (apple_width / 2),
                y=(int(screen_size_db.split('x')[0]) / 4) - (apple_height / 2))

            # def delete_tree():
            #     canvas_tree.delete('all')
            #     delete_tree_button.configure(text='Вернуть левую картинку', command=return_tree)
            #
            # def return_tree():
            #     canvas_tree.create_image(5, 5, anchor='nw', image=tree)
            #     delete_tree_button.configure(text="Удалить левую картинку", command=delete_tree)
            #
            # def delete_car():
            #     Artwork_car.configure(image=black)
            #     delete_car_button.configure(text='Вернуть среднюю картинку', command=return_car)
            #
            # def return_car():
            #     Artwork_car.configure(image=car)
            #     delete_car_button.configure(text="Удалить среднюю картинку", command=delete_car)
            #
            # def delete_apple():
            #     canvas_apple.delete('all')
            #     delete_apple_button.configure(text='Вернуть правую картинку', command=return_apple)
            #
            # def return_apple():
            #     canvas_apple.create_image(5, 5, anchor='nw', image=apple)
            #     delete_apple_button.configure(text="Удалить правую картинку", command=delete_apple)

            def show_and_hide_images(left_image, right_image, left_frequency, right_frequency, duration, ratio):
                def stop_flashing():
                    stopflag.append('stop')
                    # stop_button.configure(text='Старт', command=flash)
                    destroy_window()
                    main_interface()
                    start()

                stopflag = []
                stop_button = tk.Button(self.window, text="Стоп", command=stop_flashing)
                stop_button.place(x=(int(screen_size_db.split('x')[0]) / 2) + 11,
                                  y=(int(screen_size_db.split('x')[0]) / 4) + (car_height / 2) + 90)

                def show_image(ratio):
                    i = 0
                    while i < ratio:
                        left_image.pack(side='left',
                                        padx=(int(screen_size_db.split('x')[
                                                      0]) - tree_width - car_width - apple_width) / 4,
                                        pady=5)
                        self.window.update()
                        time.sleep(1 / left_frequency)
                        left_image.pack_forget()
                        self.window.update()
                        time.sleep(1 / left_frequency)
                        i += 1

                    right_image.pack(side='right',
                                     padx=(int(screen_size_db.split('x')[
                                                   0]) - tree_width - car_width - apple_width) / 4,
                                     pady=5)
                    self.window.update()
                    time.sleep(1 / left_frequency)
                    right_image.pack_forget()
                    self.window.update()
                    time.sleep(1 / left_frequency)

                end_time = time.time() + duration
                left_image.pack_forget()
                right_image.pack_forget()

                while time.time() <= end_time and stopflag == []:
                    if not stopflag:
                        show_image(ratio)
                    else:
                        break

            def flash():
                destroy_window()
                main_interface()

                tree_label = tk.Label(self.window, image=tree, bg='black', width=tree_width, height=tree_height)
                car_label = tk.Label(self.window, image=car, bg='black', width=car_width, height=car_height)
                apple_label = tk.Label(self.window, image=apple, bg='black', width=apple_width, height=apple_height)

                # tree_label.pack(side='left',
                #                 padx=(int(screen_size_db.split('x')[0])-tree_width-car_width-apple_width)/4, pady=5)
                # car_label.pack(side='left',
                #                padx=(int(screen_size_db.split('x')[0])-tree_width-car_width-apple_width)/4, pady=5)
                # apple_label.pack(side='left',
                #                  padx=(int(screen_size_db.split('x')[0])-tree_width-car_width-apple_width)/4, pady=5)

                self.window.update()
                # time.sleep(2)

                # tree_label.pack_forget()
                # apple_label.pack_forget()
                database = sqlite3.connect('main.db')
                cursor = database.cursor()
                cursor.execute("SELECT * FROM Queue;")
                queue = cursor.fetchall()
                database.close()
                for t in queue:
                    print(t)
                    left_show_count = t[1]
                    show_and_hide_images(tree_label, apple_label, freq, freq, t[0], t[1])


            # delete_tree_button = tk.Button(self.window, text="Удалить левую картинку", command=delete_tree)
            # delete_tree_button.place(x=(int(screen_size_db.split('x')[1]) / 3) - 66,
            #                          y=(int(screen_size_db.split('x')[0]) / 4) - (tree_height / 2) - 90)
            # delete_car_button = tk.Button(self.window, text="Удалить среднюю картинку", command=delete_car)
            # delete_car_button.place(x=(int(screen_size_db.split('x')[1]) / 3) * 2.5 - 66,
            #                         y=(int(screen_size_db.split('x')[0]) / 4) - (car_height / 2) - 90)
            # delete_apple_button = tk.Button(self.window, text="Удалить правую картинку", command=delete_apple)
            # delete_apple_button.place(x=(int(screen_size_db.split('x')[1]) / 3) * 4 - 66,
            #                           y=(int(screen_size_db.split('x')[0]) / 4) - (car_height / 2) - 90)
            start_button = tk.Button(self.window, text="Старт", command=flash)
            start_button.place(x=(int(screen_size_db.split('x')[1]) / 3) * 2.5 - 66,
                               y=(int(screen_size_db.split('x')[0]) / 4) + (car_height / 2) + 90)
            settings_button = tk.Button(self.window, text="Настройки", command=settings)
            settings_button.place(x=(int(screen_size_db.split('x')[1]) / 3) * 2.5 + 25,
                                  y=(int(screen_size_db.split('x')[0]) / 4) + (car_height / 2) + 90)

        def settings():
            def apply_settings():
                def change_color(image_name, red, green, blue):
                    if os.path.isfile(image_name) and red <= 255 and green <= 255 and blue <= 255:
                        im = Image.open(image_name)
                        data = np.array(im)

                        r1, g1, b1 = 255, 255, 255  # Original value
                        r2, g2, b2 = red, green, blue  # Value that we want to replace it with

                        red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
                        mask = (red == r1) & (green == g1) & (blue == b1)
                        data[:, :, :3][mask] = [r2, g2, b2]

                        im = Image.fromarray(data)
                        new_name = ''.join(random.choices('0123456789', k=12)) + '.png'
                        im.save(f'temporary/{new_name}')
                        return f'temporary/{new_name}'
                    else:
                        return image_name

                def delete_images(dir_path):
                    for file_name in os.listdir(dir_path):
                        # проверяем, является ли файл изображением (png, jpg, jpeg и т.д.)
                        if file_name.endswith('.png') or file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
                            # удаляем файл
                            os.remove(os.path.join(dir_path, file_name))
                            print(f"Файл {file_name} удален.")

                database = sqlite3.connect('main.db')
                cursor = database.cursor()
                cursor.execute("DELETE FROM Params;")
                cursor.execute("DELETE FROM Secondary_params;")
                database.commit()
                delete_images('temporary')

                if main_or_secondary.get() == 'основных картинок':
                    cursor.execute('INSERT INTO Params VALUES(?, ?, ?, ?, ?, ?)',
                                   (12, int(dur.get()), int(frequency_list.get()),
                                    change_color(left_image.get(), red=int(left_red.get()),
                                                 green=int(left_green.get()), blue=int(left_blue.get())),
                                    change_color(center_image.get(), red=int(center_red.get()),
                                                 green=int(center_green.get()), blue=int(center_blue.get())),
                                    change_color(right_image.get(), red=int(right_red.get()),
                                                 green=int(right_green.get()), blue=int(right_blue.get()))))
                else:
                    cursor.execute('INSERT INTO Secondary_params VALUES(?, ?, ?)',
                                   (change_color(left_image.get(), red=int(left_red.get()),
                                                 green=int(left_green.get()), blue=int(left_blue.get())),
                                    change_color(center_image.get(), red=int(center_red.get()),
                                                 green=int(center_green.get()), blue=int(center_blue.get())),
                                    change_color(right_image.get(), red=int(right_red.get()),
                                                 green=int(right_green.get()), blue=int(right_blue.get()))))
                database.commit()
                database.close()

                def generate_square(color_rgb, x, y, *args):
                    canvas = tk.Canvas(self.window, width=20, height=20,
                                       bg=f"#{color_rgb[0]:02x}{color_rgb[1]:02x}{color_rgb[2]:02x}")
                    canvas.pack()
                    canvas.place(x=x, y=y)

                generate_square(color_rgb=(int(left_red.get()),
                                           int(left_green.get()),
                                           int(left_blue.get())),
                                x=700, y=301)
                generate_square(color_rgb=(int(center_red.get()),
                                           int(center_green.get()),
                                           int(center_blue.get())),
                                x=700, y=361)
                generate_square(color_rgb=(int(right_red.get()),
                                           int(right_green.get()),
                                           int(right_blue.get())),
                                x=700, y=421)

            destroy_window()
            main_interface()
            database = sqlite3.connect('main.db')
            cursor = database.cursor()
            cursor.execute("SELECT * FROM Params;")
            ratio, duration, frequency, pic_left, pic_center, pic_right = cursor.fetchone()

            tk.Label(self.window, text='Настройки', bg='black', foreground='white').place(x=40, y=20)
            main_or_secondary = ttk.Combobox(values=['основных картинок'])
            main_or_secondary.set('основных картинок')
            # main_or_secondary.place(x=120, y=20)
            tk.Label(self.window, text='Картинки: ', bg='black', foreground='white').place(x=40, y=120)
            tk.Label(self.window, text='Положение на странице', bg='black', foreground='white').place(x=283, y=80)
            tk.Label(self.window, text='Слева', bg='black', foreground='white').place(x=200, y=120)
            tk.Label(self.window, text='По центру', bg='black', foreground='white').place(x=320, y=120)
            tk.Label(self.window, text='Справа', bg='black', foreground='white').place(x=465, y=120)
            tk.Label(self.window, text='Файл', bg='black', foreground='white').place(x=100, y=160)

            def get_png_files():
                png_files = []
                for filename in os.listdir('.'):
                    if filename.endswith('.png') and 'thumbnail' not in filename:
                        png_files.append(filename)
                return png_files

            left_image = ttk.Combobox(values=get_png_files(), width=10)
            if os.path.isfile('tree.png'):
                left_image.set('tree.png')
            center_image = ttk.Combobox(values=get_png_files(), width=10)
            if os.path.isfile('car.png'):
                center_image.set('car.png')
            right_image = ttk.Combobox(values=get_png_files(), width=10)
            if os.path.isfile('apple.png'):
                right_image.set('apple.png')

            left_image.place(x=180, y=160)
            center_image.place(x=313, y=160)
            right_image.place(x=450, y=160)

            apply_button = tk.Button(text='Применить настройки', command=apply_settings)
            apply_button.place(x=130, y=18)

            start_button = tk.Button(text='Старт', command=start)
            start_button.place(x=300, y=18)

            tk.Label(self.window, text='Частота мигания', bg='black', fg='white').place(x=40, y=220)
            frequency_list = ttk.Combobox(values=['20', '19', '18', '17', '16', '15', '14', '13', '12', '11', '10',
                                                  '9', '8', '7', '6', '5', '4', '3', '2', '1'], width=5)
            frequency_list.set(str(frequency))
            frequency_list.place(x=180, y=220)
            tk.Label(self.window, text='Гц', bg='black', fg='white').place(x=250, y=220)

            tk.Label(self.window, text='Цветокоррекция', bg='black', fg='white').place(x=40, y=300)
            tk.Label(self.window, text='Левой картинки', bg='black', fg='white').place(x=180, y=300)
            tk.Label(self.window, text='Средней картинки', bg='black', fg='white').place(x=180, y=360)
            tk.Label(self.window, text='Правой картинки', bg='black', fg='white').place(x=180, y=420)

            tk.Label(self.window, text='Красный', bg='black', fg='white').place(x=325, y=270)
            tk.Label(self.window, text='Зеленый', bg='black', fg='white').place(x=455, y=270)
            tk.Label(self.window, text='Синий', bg='black', fg='white').place(x=590, y=270)

            left_red = ttk.Scale(self.window, from_=0, to=255)
            left_green = ttk.Scale(self.window, from_=0, to=255)
            left_blue = ttk.Scale(self.window, from_=0, to=255)

            center_red = ttk.Scale(self.window, from_=0, to=255)
            center_green = ttk.Scale(self.window, from_=0, to=255)
            center_blue = ttk.Scale(self.window, from_=0, to=255)

            right_red = ttk.Scale(self.window, from_=0, to=255)
            right_green = ttk.Scale(self.window, from_=0, to=255)
            right_blue = ttk.Scale(self.window, from_=0, to=255)

            left_red.place(x=300, y=300)
            left_green.place(x=430, y=300)
            left_blue.place(x=560, y=300)

            center_red.place(x=300, y=360)
            center_green.place(x=430, y=360)
            center_blue.place(x=560, y=360)

            right_red.place(x=300, y=420)
            right_green.place(x=430, y=420)
            right_blue.place(x=560, y=420)

            # Создаем таблицу
            table = ttk.Treeview(self.window, columns=("Соотношение, n/1", "Длительность, с"), show="headings")

            database = sqlite3.connect('main.db')
            cursor = database.cursor()
            cursor.execute("SELECT * FROM Queue")
            play_data = cursor.fetchall()
            for i in play_data:
                table.insert("", tk.END, values=i)

            # Задаем размеры колонок
            table.column("Соотношение, n/1", width=120, anchor=tk.CENTER)
            table.column("Длительность, с", width=120, anchor=tk.CENTER)

            # Задаем заголовки столбцов
            table.heading("Соотношение, n/1", text="Соотношение, n/1")
            table.heading("Длительность, с", text="Длительность, с")

            # Размещаем таблицу на окне
            table.place(x=40, y=520)

            def add_data(duration, ratio):
                table.insert("", tk.END, values=(int(duration), int(ratio)))
                database = sqlite3.connect('main.db')
                cursor = database.cursor()
                cursor.execute("INSERT INTO Queue VALUES(?, ?);", (int(duration), int(ratio)))
                database.commit()
                database.close()
                play_data.append((int(duration), int(ratio)))

            def delete_data(event):
                for selected_item2 in table.selection():
                    item = table.item(selected_item2)
                    play_data.remove(tuple(item["values"]))
                    database = sqlite3.connect('main.db')
                    cursor = database.cursor()
                    cursor.execute("DELETE FROM Queue;")
                    for i in play_data:
                        cursor.execute("INSERT INTO Queue VALUES(?, ?);", (i[0], i[1]))
                    database.commit()
                    database.close()
                    row_id = table.focus()
                    table.delete(row_id)

            def clear_table():
                database = sqlite3.connect('main.db')
                cursor = database.cursor()
                cursor.execute("DELETE FROM Queue;")
                database.commit()
                database.close()
                table.delete(*table.get_children())

            table.bind("<<TreeviewSelect>>", delete_data)

            def set_dur(*args):
                dur.set(str(round(flash_duration.get())))

            def set_rat(*args):
                rat.set(str(round(image_ratio.get())))

            tk.Label(self.window, text='Параметры и порядок миганий', bg='black', fg='white').place(x=40, y=480)
            tk.Label(self.window, text='Соотношение', bg='black', fg='white').place(x=300, y=561)
            tk.Label(self.window, text='Длительность', bg='black', fg='white').place(x=300, y=521)

            dur = tk.StringVar()
            rat = tk.StringVar()
            dur.set('240')
            rat.set('12')
            flash_duration = ttk.Scale(self.window, from_=30, to=480, length=230,
                                       command=set_dur)
            image_ratio = ttk.Scale(self.window, from_=1, to=12, length=100,
                                    command=set_rat)

            flash_duration.place(x=430, y=520)
            image_ratio.place(x=430, y=560)

            tk.Label(self.window, textvariable=dur, background='black', foreground='white').place(x=670, y=520)
            tk.Label(self.window, text='c', background='black', foreground='white').place(x=695, y=520)
            tk.Label(self.window, textvariable=rat, background='black', foreground='white').place(x=540, y=561)
            tk.Label(self.window, text='/1', background='black', foreground='white').place(x=555, y=561)

            add_button = tk.Button(self.window, text='Добавить', command=lambda: add_data(dur.get(), rat.get()))
            add_button.place(x=309, y=600)
            clear_button = tk.Button(self.window, text='Очистить', command=clear_table)
            clear_button.place(x=309, y=640)

        def get_display_size():
            root = tk.Tk()
            root.update_idletasks()
            root.attributes('-fullscreen', True)
            root.state('iconic')
            height = root.winfo_screenheight()
            width = root.winfo_screenwidth()
            root.destroy()
            return f'{width}x{height}'

        def main_interface():
            menu = Menu(self.window)
            menu_button = Menu(menu, tearoff=0)

            menu_button.add_command(label='Старт', command=start)
            menu_button.add_command(label='Настройки', command=settings)

            menu.add_cascade(label='Меню', menu=menu_button)
            self.window.config(menu=menu)

        check_database()
        database = sqlite3.connect('main.db')
        cursor = database.cursor()
        cursor.execute("SELECT * FROM Screen_params;")
        screen_size_db = cursor.fetchone()
        if not screen_size_db:
            size = get_display_size()
            cursor.execute("INSERT INTO Screen_params VALUES(?)", (size,))
            database.commit()
        else:
            size = screen_size_db
        database.close()
        self.window = tk.Tk()
        self.window.title(f"{version}")
        self.window.geometry(size)
        self.window["bg"] = 'black'
        self.window.protocol("WM_DELETE_WINDOW", self.callback)
        self.window.focus_force()

        if not screen_size_db:
            settings()
        else:
            start()
        self.window.mainloop()


if __name__ == '__main__':
    app = App()
