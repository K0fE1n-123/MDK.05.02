from itertools import tee
import tkinter as tk
from tkinter import CENTER, messagebox, Toplevel, Label, Button, Entry
from tkinter.ttk import Treeview
import sqlite3

# Подключение к базе данных (или создание, если ее нет)
conn = sqlite3.connect('flights.db')
cursor = conn.cursor()

# Создание таблицы в базе данных, если она еще не создана
cursor.execute('''
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY,
    flight_number TEXT,
    destination TEXT,
    available_seats INTEGER,
    sold_seats INTEGER
)
''')
conn.commit()

# Функция для отображения таблицы с данными о рейсах
def view_table():
    new_window = Toplevel(window)
    new_window.title('Таблица рейсов')
    new_window.geometry('600x400')

    # Создание таблицы
    columns = ('id', 'Расстояние', 'Место_назначения', 'Доступные_места', 'Проданные_места')
    tree = Treeview(new_window, columns=columns, show='headings')
    tree.pack(side='left', fill='both', expand=True)

    # Заголовки столбцов
    for col in columns:
        tree.heading(col, text=col)

    # Получение данных из базы данных и заполнение таблицы
    cursor.execute('SELECT * FROM flights')
    rows = cursor.fetchall()
    for row in rows:
        tree.insert('', 'end', values=row)

# Функция для регистрации пользователя (здесь просто заглушка)
def register_user():
    messagebox.showinfo('Регистрация', 'Функция регистрации пользователя')

# Функция для открытия нового окна
def open_new_window(user_type):
    new_window = Toplevel(window)
    new_window.title('Новый лист')
    new_window.geometry('600x300')
    if user_type == 'admin':
        Label(new_window, text='Добро пожаловать, Администратор!', font=('Arial', 15)).pack(pady=20)
        # Добавление кнопок для администратора
        Button(new_window, text='Создание рейса', command=lambda: view_table(user_type)).pack(pady=10)
        Button(new_window, text='Свободные места', command=register_user).pack(pady=10)
        Button(new_window, text='Проданные места', command=lambda: view_table(user_type)).pack(pady=10)
        Button(new_window, text='Проверка брони', command=lambda: view_table(user_type)).pack(pady=10)
        
    else:
        Label(new_window, text='Вы успешно вошли!', font=('Arial', 15)).pack(pady=20)
        Button(new_window, text='Свободные места', command=view_table).pack(pady=10)
        Button(new_window, text='Проверка брони', command=view_table).pack(pady=10)

# Функция, вызываемая при нажатии кнопки 'Войти'
def clicked():
    # Предполагаемые данные пользователя и пароля
    correct_username = 'user'
    correct_password = '123'
    admin_username = 'admin'
    admin_password = '123'

    # Получение введенных пользователем данных
    username = username_entry.get()
    password = password_entry.get()

    # Проверка имени пользователя и пароля
    if username == correct_username and password == correct_password:
        messagebox.showinfo('Успех', 'Авторизация прошла успешно!')
        view_table('user')  # Открытие нового окна для пользователя
    elif username == admin_username and password == admin_password:
        messagebox.showinfo('Успех', 'Авторизация Администратора прошла успешно!')
        view_table('admin')  # Открытие нового окна для администратора
    else:
        messagebox.showerror('Ошибка', 'Неверное имя пользователя или пароль')

# Создание основного окна
window = tk.Tk()
window.title('Авторизация')
window.geometry('600x300')
window.resizable(False, False)

# Настройки шрифтов и отступов
font_header = ('Arial', 15)
font_entry = ('Arial', 12)
label_font = ('Arial', 11)
base_padding = {'padx': 10, 'pady': 8}
header_padding = {'padx': 10, 'pady': 12}

# Создание и расположение виджетов
main_label = Label(window, text='Авторизация', font=font_header, justify=CENTER, **header_padding)
main_label.pack()

username_label = Label(window, text='Имя пользователя', font=label_font , **base_padding)
username_label.pack()

username_entry = Entry(window, bg='#fff', fg='#444', font=font_entry)
username_entry.pack()

password_label = Label(window, text='Пароль', font=label_font , **base_padding)
password_label.pack()

password_entry = Entry(window, bg='#fff', fg='#444', font=font_entry, show='*')  # Скрытие ввода пароля
password_entry.pack()

send_btn = Button(window, text='Войти', command=clicked)
send_btn.pack(**base_padding)
# Добавление данных в таблицу flights
def add_flight_data():
    # Значения для добавления
    flight_data = ('1000km', 'Moscow-Sochi', 12, 24)
    
    # SQL-запрос для вставки данных
    cursor.execute(
        '''
        INSERT INTO flights (flight_number, destination, available_seats, sold_seats)
        VALUES (?, ?, ?, ?)
        ''', 
        flight_data
    )
    
    # Сохранение изменений в базе данных
    conn.commit()
# Вызов функции для добавления данных
add_flight_data()
# Функция для обновления данных о рейсе
def update_flight_data(id, flight_number, destination, available_seats, sold_seats):
    cursor.execute('''
    UPDATE flights SET
    flight_number = ?,
    destination = ?,
    available_seats = ?,
    sold_seats = ?
    WHERE id = ?
    ''', (flight_number, destination, available_seats, sold_seats, id))
    conn.commit()


# Функция для редактирования выбранной записи
def edit_selected_flight(tree):
    selected_item = tree.selection()[0]  # Получение выбранной записи
    flight = tree.item(selected_item)['values']
    edit_window = Toplevel(window)
    edit_window.title('Редактирование рейса')
    edit_window.geometry('300x200')

    # Поля для редактирования
    flight_number_entry = Entry(edit_window)
    flight_number_entry.insert(0, flight[1])
    flight_number_entry.pack()

    destination_entry = Entry(edit_window)
    destination_entry.insert(0, flight[2])
    destination_entry.pack()

    available_seats_entry = Entry(edit_window)
    available_seats_entry.insert(0, flight[3])
    available_seats_entry.pack()

    sold_seats_entry = Entry(edit_window)
    sold_seats_entry.insert(0, flight[4])
    sold_seats_entry.pack()

    # Кнопка для сохранения изменений
    save_btn = Button(edit_window, text='Сохранить изменения', command=lambda: update_flight_data(
        flight[0],
        flight_number_entry.get(),
        destination_entry.get(),
        available_seats_entry.get(),
        sold_seats_entry.get()
    ))
    save_btn.pack()
# Функция для подсчета свободных мест
def count_available_seats():
    cursor.execute('SELECT SUM(available_seats) FROM flights')
    total_available_seats = cursor.fetchone()[0]
    messagebox.showinfo('Свободные места', f'Общее количество свободных мест: {total_available_seats}')

# Функция для отображения таблицы с данными о рейсах
 # Функция для удаления выбранного рейса
def delete_selected_flight(tree):
    selected_item = tree.selection()[0]  # Получение выбранной записи
    flight_id = tree.item(selected_item)['values'][0]
    cursor.execute('DELETE FROM flights WHERE id = ?', (flight_id,))
    conn.commit()
    tree.delete(selected_item)  # Удаление записи из таблицы
# Функция для создания нового рейса
def create_flight():
    create_window = Toplevel(window)
    create_window.title('Создание рейса')
    create_window.geometry('300x200')

    # Поля для ввода данных нового рейса
    flight_number_entry = Entry(create_window)
    flight_number_entry.pack()

    destination_entry = Entry(create_window)
    destination_entry.pack()

    available_seats_entry = Entry(create_window)
    available_seats_entry.pack()

    sold_seats_entry = Entry(create_window)
    sold_seats_entry.pack()

    # Кнопка для добавления нового рейса в базу данных
    add_btn = Button(create_window, text='Добавить рейс', command=lambda: add_flight_data(
        flight_number_entry.get(),
        destination_entry.get(),
        available_seats_entry.get(),
        sold_seats_entry.get()
    ))
    add_btn.pack()

# Измененная функция для добавления данных в таблицу flights
def add_flight_data(flight_number, destination, available_seats, sold_seats):
    # Значения для добавления
    flight_data = (flight_number, destination, available_seats, sold_seats)
    
    # SQL-запрос для вставки данных
    cursor.execute(
        '''
        INSERT INTO flights (flight_number, destination, available_seats, sold_seats)
        VALUES (?, ?, ?, ?)
        ''', 
        flight_data
    )
    
    # Сохранение изменений в базе данных
    conn.commit()

# Функция для сортировки данных в таблице
def sortby(tree, col, descending):
    """Сортировка дерева содержимого по столбцу и направлению."""
    # Получаем список элементов в виде (идентификатор, значения)
    data = [(tree.set(child, col), child) for child in tree.get_children('')]

    # Если данные числовые, преобразуем их
    data = change_numeric(data)
    # Сортируем данные
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)

    # Меняем направление сортировки
    tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))

# Функция для преобразования строковых данных в числовые, если это необходимо
def change_numeric(data):
    new_data = []
    for item, val in data:
        try:
            new_data.append((float(item), val))
        except ValueError:
            new_data.append((item, val))
    return new_data

# Измененная функция view_table для добавления сортировки
def view_table(user_type):
    new_window = Toplevel(window)
    new_window.title('Таблица рейсов')
    new_window.geometry('1200x400')

    columns = ('id', 'flight_number', 'destination', 'available_seats', 'sold_seats')
    tree = Treeview(new_window, columns=columns, show='headings')
    tree.pack(side='left', fill='both', expand=True)

    for col in columns:
        tree.heading(col, text=col, command=lambda _col=col: sortby(tree, _col, False))

    cursor.execute('SELECT * FROM flights')
    rows = cursor.fetchall()
    for row in rows:
        tree.insert('', 'end', values=row)

    # Кнопки для администратора
    if user_type == 'admin':
        # Кнопка для редактирования выбранного рейса
        edit_btn = Button(new_window, text='Редактировать выбранный рейс', command=lambda: edit_selected_flight(tree))
        edit_btn.pack(pady=10)

        # Кнопка для удаления выбранного рейса
        delete_btn = Button(new_window, text='Удалить выбранный рейс', command=lambda: delete_selected_flight(tree))
        delete_btn.pack(pady=10)

        # Кнопка для создания нового рейса
        create_btn = Button(new_window, text='Создать новый рейс', command=create_flight)
        create_btn.pack(pady=10)

    # Кнопка для подсчета свободных мест (доступна всем пользователям)
    count_seats_btn = Button(new_window, text='Подсчитать свободные места', command=count_available_seats)
    count_seats_btn.pack(pady=10)

# Функция для создания нового рейса
def create_flight():
    create_window = Toplevel(window)
    create_window.title('Создание рейса')
    create_window.geometry('300x200')

    # Поля для ввода данных нового рейса
    flight_number_entry = Entry(create_window)
    flight_number_entry.pack()

    destination_entry = Entry(create_window)
    destination_entry.pack()

    available_seats_entry = Entry(create_window)
    available_seats_entry.pack()

    sold_seats_entry = Entry(create_window)
    sold_seats_entry.pack()

    # Кнопка для добавления нового рейса в базу данных
    add_btn = Button(create_window, text='Добавить рейс', command=lambda: add_flight_data(
        flight_number_entry.get(),
        destination_entry.get(),
        available_seats_entry.get(),
        sold_seats_entry.get()
    ))
    add_btn.pack()


window.mainloop()
