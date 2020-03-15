from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from miscellaneous import *
from json import *
import os.path
from modeling import *


fig_count = -1


class TheD(Frame, metaclass=Singleton):
    # class for the main frame

    def __init__(self, parent):
        # initialization of the main frame
        # frame's variables goes here

        Frame.__init__(self, parent)
        self.parent = parent

        self.field_height_entry_value = StringVar()  # value for CA's field height
        self.field_width_entry_value = StringVar()  # value for CA's field width
        self.field_step_amount = StringVar()  # value for amount of steps
        self.spreaders_percentage = IntVar()  # value for idea's spreaders percentage
        self.opposers_percentage = IntVar()  # value for idea's opposers percentage
        # variables for sliders
        self.s1 = NONE
        self.s2 = NONE
        self.s3 = NONE
        self.s4 = NONE
        self.s5 = NONE
        self.s6 = NONE
        self.s7 = NONE
        self.s8 = NONE

        self.f = None  # pointer to the current settings' file

        self.init_ui()  # initialization of main frame's UI

    def init_ui(self):
        # initialization of main frame's UI
        # frame's UI's elements goes here

        self.parent.title("ProjectD")  # setting window's title
        # custom function for closing window
        self.parent.protocol("WM_DELETE_WINDOW", self.close_window)
        # creating menu for file manipulation
        menu_bar = Menu(self.parent)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Новый файл", command=self.create_file)
        file_menu.add_command(label="Открыть", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_command(label="Сохранить как...", command=self.save_file_as)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        self.parent.config(menu=menu_bar)

        row = 0  # row number

        # setting's frame (left)
        settings_frame = Frame(self, height=200, width=150)
        settings_frame.grid(row=0, column=0, sticky='n')

        # settings
        # field's size
        # label
        Label(settings_frame, text="Размер сетки: ").grid(row=row, sticky=W)
        row += 1
        # frame for size entries
        size_entries_frame = Frame(settings_frame)
        reg_field = size_entries_frame.register(is_correct3)  # register for validating field entries
        size_entries_frame.grid(row=row, sticky=W)
        Entry(size_entries_frame,  width=5, textvariable=self.field_height_entry_value,
              validate='key', validatecommand=(reg_field, '%P'))\
            .grid(row=0, column=0, sticky=W)
        Label(size_entries_frame, text="x", height=1).grid(row=0, column=1)
        Entry(size_entries_frame,  width=5, textvariable=self.field_width_entry_value,
              validate='key', validatecommand=(reg_field, '%P'))\
            .grid(row=0, column=2, sticky=E)

        row += 1
        col = 0

        # faction's sizes (%)
        Label(settings_frame, text="Процентные сооотношения групп людей: ").grid(row=row, sticky=W)
        row += 1
        # faction sizes frame
        faction_sizes_frame = Frame(settings_frame)
        faction_sizes_frame.grid(row=row, sticky=W)
        Label(faction_sizes_frame, text="Распространителей идеи, %: ").grid(row=0, column=0, sticky=W)
        Scale(faction_sizes_frame, from_=1, to=20, resolution=1, variable=self.spreaders_percentage,
              orient=HORIZONTAL, tickinterval=5).grid(row=0, column=1)

        Label(faction_sizes_frame, text="Защитников, %: ").grid(row=1, column=0, sticky=W)
        Scale(faction_sizes_frame, from_=1, to=20, resolution=1, variable=self.opposers_percentage,
              orient=HORIZONTAL, tickinterval=5).grid(row=1, column=1)
        row += 1

        # step amount entry
        # label
        Label(settings_frame, text="Количество шагов: ").grid(row=row, sticky=W)
        row += 1
        reg_steps = size_entries_frame.register(is_correct2)  # register for validating step entry
        Entry(settings_frame, width=5, textvariable=self.field_step_amount,
              validate='key', validatecommand=(reg_steps, '%P')) \
            .grid(row=row, column=0, sticky=W)
        row += 1

        # model button frame
        models_frame = Frame(settings_frame)
        models_frame.grid(row=row, sticky=W)
        Button(models_frame , text="Моделировать", command=self.create_model)\
            .grid(row=0, column=0, sticky=W)
        Button(models_frame, text="Загрузить модель", command=self.load_model).\
            grid(row=1, column=0, sticky=W)
        row += 1

        # model's frame
        faction_settings_frame = Frame(self, height=200, width=200)
        faction_settings_frame.grid(row=0, column=1)

        row = 0

        # Spreaders' frame
        # label
        Label(faction_settings_frame, text="Распространители деструктивной идеи (красные): ", height=2).grid(row=row, sticky=W)
        row += 1
        # spreaders entry frame
        spreaders_frame = Frame(faction_settings_frame)
        spreaders_frame.grid(row=row, sticky=W)
        # influence entry
        Label(spreaders_frame, text="Степень влияния: ").grid(row=0, column=0, sticky=W, padx=20)
        self.s1 = Scale(spreaders_frame, from_=0, to=9, resolution=1, orient=HORIZONTAL, tickinterval=3)
        self.s1.grid(row=0, column=1, sticky=W)
        row += 1
        # resistance entry
        Label(spreaders_frame, text="Степень невосприятия: ").grid(row=1, column=0, sticky=W, padx=20)
        self.s2 = Scale(spreaders_frame, from_=0, to=9, resolution=1, orient=HORIZONTAL, tickinterval=3)
        self.s2.grid(row=1, column=1, sticky=W)
        # self.s2.set(self.spreaders_resistance)
        row += 1

        # opposers' frame
        # label
        Label(faction_settings_frame, text="Противоборцы деструктивной идеи (синие): ", height=2).grid(row=row, sticky=W)
        row += 1
        # opposers entry frame
        opposers_frame = Frame(faction_settings_frame)
        opposers_frame.grid(row=row, sticky=W)
        # influence entry
        Label(opposers_frame, text="Степень влияния: ").grid(row=0, column=0, sticky=W, padx=20)
        self.s3 = Scale(opposers_frame, from_=0, to=9, resolution=1,
                        orient=HORIZONTAL, tickinterval=3)
        self.s3.grid(row=0, column=1, sticky=W)
        row += 1
        # resistance entry
        Label(opposers_frame, text="Степень невосприятия: ").grid(row=1, column=0, sticky=W, padx=20)
        self.s4 = Scale(opposers_frame, from_=0, to=9, resolution=1,
                        orient=HORIZONTAL, tickinterval=3)
        self.s4.grid(row=1, column=1, sticky=W)
        # self.s4.set(self.opposers_resistance)
        row += 1

        # Infected's frame
        # label
        Label(faction_settings_frame, text="Заражённые деструктивной идеей (фиолетовые): ", height=2).grid(row=row, sticky=W)
        row += 1
        # infected's entry frame
        infected_frame = Frame(faction_settings_frame)
        infected_frame.grid(row=row, sticky=W)
        # influence entry
        Label(infected_frame, text="Степень влияния: ").grid(row=0, column=0, sticky=W, padx=20)
        self.s5 = Scale(infected_frame, from_=0, to=9, resolution=1,
                        orient=HORIZONTAL, tickinterval=3)
        self.s5.grid(row=0, column=1, sticky=W)
        row += 1
        # resistance entry
        Label(infected_frame, text="Степень невосприятия: ").grid(row=1, column=0, sticky=W, padx=20)
        self.s6 = Scale(infected_frame, from_=0, to=9, resolution=1,
                        orient=HORIZONTAL, tickinterval=3)
        self.s6.grid(row=1, column=1, sticky=W)
        # self.s6.set(self.infected_resistance)
        row += 1

        # Normal's frame
        # label
        Label(faction_settings_frame, text="Обычные люди (зелёные): ", height=2).grid(row=row, sticky=W)
        row += 1
        # normal's entry frame
        normal_frame = Frame(faction_settings_frame)
        normal_frame.grid(row=row, sticky=W)
        # influence entry
        Label(normal_frame, text="Степень влияния: ").grid(row=0, column=0, sticky=W, padx=20)
        self.s7 = Scale(normal_frame, from_=0, to=9, resolution=1,
                        orient=HORIZONTAL, tickinterval=3)
        self.s7.grid(row=0, column=1, sticky=W)
        row += 1
        # resistance entry
        Label(normal_frame, text="Степень невосприятия: ").grid(row=1, column=0, sticky=W, padx=20)
        self.s8 = Scale(normal_frame, from_=0, to=9, resolution=1,
                        orient=HORIZONTAL, tickinterval=3)
        self.s8.grid(row=1, column=1, sticky=W)
        row += 1

    def create_model(self):
        #  getting model settings from form and calculating model with these parameters

        # checking if dimensions are entered
        if self.field_height_entry_value.get() == '' or self.field_width_entry_value.get() == '':
            messagebox.showerror("Размерность", "Введите размерность поля!")
            return
        # checking if fields are not 0
        if int(self.field_height_entry_value.get()) == 0 or int(self.field_width_entry_value.get()) == 0:
            messagebox.showerror("Недопустимая размерность", "Размерность поля не может быть нулевой!")
            return
        # checking if step amount is entered
        if self.field_step_amount.get() == '':
            messagebox.showerror("Количество шагов", "Введите количество шагов!")
            return
        # checking is step count is above 0
        if int(self.field_step_amount.get()) == 0:
            messagebox.showerror("Некорректное количество шагов", "Число шагов должно быть больше 0!")
            return

        update_model_settings(self.get_settings())
        cellular_automaton = init_custom(int(self.field_height_entry_value.get()),
                                         int(self.field_width_entry_value.get()),
                                         s_prob=self.spreaders_percentage.get() / 100,
                                         o_prob=self.opposers_percentage.get() / 100)

        cellular_automaton, demographics = evolve(cellular_automaton, timesteps=int(self.field_step_amount.get()),
                                                  neighbourhood='Moore', apply_rule=destructive_distribution_rule)

        # saving calculated model
        result = messagebox.askquestion("Сохранение модели", "Сохранить модель в файл?", icon='question')
        if result == 'yes':
            model_file = filedialog.asksaveasfile(initialdir=os.path.dirname(os.path.abspath(__file__)),
                                                  mode='wb',
                                                  filetypes=[('Файлы моделей', '*.model'), ("Все файлы", "*.*")],
                                                  initialfile="Новый файл модели", defaultextension=".model")

            np.savez(model_file, ca=cellular_automaton, dem=demographics)
            model_file.close()
            messagebox.showinfo("Сохранение файла", "Файл успешно сохранён.", icon='info')

        name = 'Несохранённая конфигурация'
        # if there is file from which configuration was loaded, then make it's name plot's title
        if self.f is not None:
            name, _ = os.path.basename(self.f.name).split('.')
        global fig_count
        fig_count += 2
        plot_animate(cellular_automaton, fig_count, title=name, dem=demographics)

    def load_model(self):
        # loading and animated model from file
        model_file = filedialog.askopenfile(initialdir=os.path.dirname(os.path.abspath(__file__)),
                                            mode='rb',
                                            filetypes=[('Файлы моделей', '*.model'), ("Все файлы", "*.*")])
        try:
            model = np.load(model_file)
        except:
            messagebox.showerror("Некорректный файл модели",
                                 "Выбранный файл не является файлом модели либо содержит ошибки!")
            return

        if (type(model['ca']) == np.ndarray) and (type(model['dem'] == np.ndarray)):
            name, _ = os.path.basename(model_file.name).split('.')
            global fig_count
            fig_count += 2
            plot_animate(model['ca'], fig_count, name, model['dem'])

        else:
            messagebox.showerror("Некорректный файл модели",
                                 "Выбранный файл не является файлом модели либо содержит ошибки!")
        model_file.close()

    def handle_unsaved_file(self):
        # handling unsaved file by offering to save it

        result = messagebox.askquestion("Несохранённый файл", "Сохранить файл?", icon='question')
        if result == 'yes':
            if self.f is None:
                self.save_file_as()
            else:
                self.save_file()
                messagebox.showinfo("Сохранение файла", "Файл успешно сохранён.", icon='info')

    def create_file(self):
        # creating new settings' file, clearing window's parameters' values

        self.handle_unsaved_file()

        # resetting file pointer
        self.f = None
        # setting all parameters to 0
        self.field_height_entry_value.set(0)
        self.field_width_entry_value.set(0)
        self.spreaders_percentage.set(0)
        self.opposers_percentage.set(0)
        self.s1.set(0)
        self.s2.set(0)
        self.s3.set(0)
        self.s4.set(0)
        self.s5.set(0)
        self.s6.set(0)
        self.s7.set(0)
        self.s8.set(0)

    def open_file(self):
        # opening settings' file

        self.handle_unsaved_file()

        self.f = filedialog.askopenfile(initialdir=os.path.dirname(os.path.abspath(__file__)),
                                        mode='rt',
                                        filetypes=[('Файлы конфигурации', '*.json'), ("Все файлы", "*.*")])
        if self.f is None:  # askopenfile return `None` if dialog closed with "cancel"
            return
        # trying to load settings from file and putting them into form
        try:
            self.set_settings(load(self.f))
        except JSONDecodeError:  # catching incorrect configuration file
            messagebox.showerror("Ошибка", "Выбранный файл не является подходящим файлом конфигурации!")
        self.f.close()

    def save_file(self):
        # saving existing file

        # if there is no current settings' file, invoke save_file_as() function
        if self.f is None:
            self.save_file_as()
        else:
            self.f = open(self.f.name, mode='w')  # getting name from file pointer, opening file by his name
            dump(self.get_settings(), self.f)
            self.f.close()

    def save_file_as(self):
        # saving file as new file

        self.f = filedialog.asksaveasfile(initialdir=os.path.dirname(os.path.abspath(__file__)),
                                          mode='w',
                                          filetypes=[('Файлы конфигурации', '*.json'), ("Все файлы", "*.*")],
                                          initialfile="Новый файл конфигурации", defaultextension=".json")

        if self.f is None:  # asksaveasfile return `None` if dialog closed with "cancel"
            return
        dump(self.get_settings(), self.f)
        self.f.close()

    def get_settings(self):
        # method for extracting parameters from form

        # handling empty entries
        if self.field_height_entry_value.get() is '':
            field_height = 0
        else:
            field_height = int(self.field_height_entry_value.get())

        if self.field_width_entry_value.get() is '':
            field_width = 0
        else:
            field_width = int(self.field_width_entry_value.get())

        # extracting values from corresponding sliders
        settings = {'field_height': field_height,
                    'field_width': field_width,
                    'spreaders_percentage': self.spreaders_percentage.get(),
                    'opposers_percentage': self.opposers_percentage.get(),
                    'spreaders_influence': self.s1.get(), 'spreaders_resistance': self.s2.get(),
                    'opposers_influence': self.s3.get(), 'opposers_resistance': self.s4.get(),
                    'infected_influence': self.s5.get(), 'infected_resistance': self.s6.get(),
                    'normal_influence': self.s7.get(), 'normal_resistance': self.s8.get()}

        return settings

    def set_settings(self, settings):
        # method for verifying parameters and putting them into form

        self.field_height_entry_value.set(check_input(settings['field_height'], 0, 150))
        self.field_width_entry_value.set(check_input(settings['field_width'], 0, 150))
        self.spreaders_percentage.set(check_input(settings['spreaders_percentage'], 1, 20))
        self.opposers_percentage.set(check_input(settings['opposers_percentage'], 1, 20))

        self.s1.set(check_input(settings['spreaders_influence'], 0, 9))
        self.s2.set(check_input(settings['spreaders_resistance'], 0, 9))
        self.s3.set(check_input(settings['opposers_influence'], 0, 9))
        self.s4.set(check_input(settings['opposers_resistance'], 0, 9))
        self.s5.set(check_input(settings['infected_influence'], 0, 9))
        self.s6.set(check_input(settings['infected_resistance'], 0, 9))
        self.s7.set(check_input(settings['normal_influence'], 0, 9))
        self.s8.set(check_input(settings['normal_resistance'], 0, 9))

    def close_window(self):

        self.handle_unsaved_file()
        # method for closing window
        self.parent.destroy()


def check_input(value, left_boundary, right_boundary):
    # checking if value is integer and whether it is in set boundaries

    if not isinstance(value, int):
        return 0
    elif value < left_boundary:
        return left_boundary
    elif value > right_boundary:
        return right_boundary
    return value


def is_correct2(value):
    # function for checking correctness of steps' inputs
    # it should be integers-only, no longer than 2 digits

    if value.isdigit():
        if len(value) < 3:
            if value is 0:
                return False
            return True
        else:
            return False
    elif value == "":
        return True
    else:
        return False


def is_correct3(value):
    # function for checking correctness of dimensions' inputs
    # it should be integers-only, no longer than 3 digits

    if value.isdigit():
        if len(value) < 4:
            if int(value) > 150:
                return False
            return True
        else:
            return False
    elif value == "":
        return True
    else:
        return False
