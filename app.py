from build import tkinter as tk

from PIL import ImageTk, Image
from build.tkinter import ttk
from ship_classes import *

current_engine = CurrentEngine(90, 13600, 2.8, 3.2, 6, 4.3, 3.8, 1.9, 22, 1.3, 7.4 )

current_generator = CurrentGenerator(50, 481, 84.3, [230,230,235,235,225,230], 230.8, [35,35,35,35,35,35], [89,91,89,89,89,90], 3.3, 2.2, 1.1, 1.8, 74, 71)
diesel = Diesel('6L23/30H', 225, 300, 801, 720, 18.5, 7.2, 133.5, [1,4,2,6,3,5], 30, 14.3, 13, 'Система постоянного давления с внутренним охлаждением', 30, 7, 'UG8D,  24 v')
generator = Generator('HYNDAY HFC6 506-14E', 750, 450, 1202.81, 60, 96, 0.8)

current_boiler = CurrentBoiler(50, 16, 933, 60, 260, 7.8, 47)


captain = CrewMember('Тихонович Александр Генадьевич', 'Капитан', 'Несение ходовой вахты', 'Мостик', r'crew\Тихон.jpg')
starpom = CrewMember('Медведев Степан Александрович', 'Старший помошник капитана', 'Оформление грузовых документов', 'Личная каюта', r'crew\Стёпа.jpg')
second_chief = CrewMember('Осипов Максим Алексеевич', 'Второй помошник капитана', 'Ведение журанала регистраций с мусором', 'Личная каюта',r'crew\Макс.jpg')
starmech = CrewMember('Савицкий Никита Романович', 'Старший механик', 'Руководство машинной командой', 'Машинное помещение', r'crew\Моисей.jpg')
second_mech = CrewMember('Копцев Михаил Александрович', 'Второй механик', 'Составление ремонтных ведомостей', 'Личная каюта', r'crew\Михас.jpg')
third_mech = CrewMember('Брюнеткин Сергей Николаевич', 'Третий механик', 'Проведение технического обследования', 'Машинное помещение', r'crew\Серый.jpg')
electro_mech = CrewMember('Пекут Альберт Владиславович', 'Электромеханик', 'Проведение технических занятий по судовому электрооборудованию с членами экипажа', 'Столовая', r'crew\Альберт.jpg')
botsman = CrewMember('Щеколдин Кирилл Сергеевич', 'Боцман', 'Руководство работами по техническому обслуживанию корпуса', 'Палуба', r'crew\Кирилл.jpg')

crew_list = [captain, starpom, second_chief, starmech,second_mech,third_mech,electro_mech,botsman]
tank1=Cargo(16914.8,'Сырая нефть', 15700,15700*800  )
tank2=Cargo(21982.4,'Сырая нефть', 18356, 18356*800)
tank3=Cargo(21982.4,'Сырая нефть', 18575, 18575*800)
tank4=Cargo(21982.4,'Сырая нефть', 18350, 18350*800)
tank5=Cargo(21982.4,'Сырая нефть', 18350, 18350*800)
tank6=Cargo(19923.6,'Сырая нефть', 0, 0)
tank_list = [tank1,tank2,tank3,tank4,tank5,tank6]
ship1 = Ship('STENA CONTENDER', 'Либерия',
    '11642', 'ABS +1(E),Танкер для нефти ESP,ледовый класс IC',
    '2-х корпусной',  'HSD – MAN/B&W 5S70MC-C',
    [15.1,16],
    'Daewoo Shipbuilding & marine Engineering Co., Юж. Корея',
    '02.12.2003', 133280.1, 114545.9,
    124768.6, 249.9, 44.0, 49.87, 21.0)
engine1 = Engine('5S70MC-C', 5, 700,
                 2800, 21100, 91, 18990,
                 87.9, 150, 'пресной водой',
                 'сжатым воздухом',
                 'маслом',
                 'пресной водой',
                 [1,4,3,2,5], 36,
                 126, 42700)
current_info_1 = CurrentInfo('LAIZHOU (Port) Country: China', 'YEOSU (Port) Country: Korea', '2021-04-09 07:35 LT (UTC +8)',
                             '2021-04-12 09:01 LT (UTC +9)', '(UTC +9)', 'NCHINA - Yellow Sea', 36.19767, 123.8756,
                             'Underway using Engine', 10.6, 166, 11, [ 'SE', 142], 11)
window = tk.Tk()

window.geometry('1360x768')
main_frame = tk.Frame(window)
main_frame.pack(fill=tk.BOTH, expand=1)
my_canvas = tk.Canvas(main_frame)
my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))
second_frame = tk.Frame(my_canvas)
my_canvas.create_window((0,0), window=second_frame, anchor="nw")
flag_engine = False
flag_generator = False
flag_boiler = False
def open_engine_room():
    engine_window = tk.Toplevel(window)
    engine_window.title('Информаци о машинном отделении')
    engine_window.geometry('1000x800')
    engine_current_info = tk.Label(engine_window, text='Текущие показатели главного двигателя', width=50, )
    engine_current_info.grid(column=0, row=0)
    engine_string = tk.StringVar()
    engine_string.set(current_engine)
    engine_current = tk.Label(engine_window, textvariable =engine_string, justify='left', borderwidth=1, relief="solid")
    engine_current.grid(column=0, row=1, )

    generator_current_info = tk.Label(engine_window, text='Текущие показатели дизельного генератора', width=50, )
    generator_current_info.grid(column=1, row=0)
    generator_string = tk.StringVar()
    generator_string.set(current_generator)
    generator_current = tk.Label(engine_window, textvariable=generator_string, justify='left', borderwidth=1, relief="solid")
    generator_current.grid(column=1, row=1, )

    boiler_current_info = tk.Label(engine_window, text='Текущие показатели парового котла', width=50, )
    boiler_current_info.grid(column=0, row=3)
    boiler_string = tk.StringVar()
    boiler_string.set(current_boiler)
    boiler_current = tk.Label(engine_window, textvariable=boiler_string, justify='left', borderwidth=1,
                                 relief="solid")
    boiler_current.grid(column=0, row=4, )

    def reload_engine():
        if flag_engine:
            current_engine.reload()
            engine_string.set(current_engine)
            engine_window.after(1000, reload_engine)
    def trigger_engine():
        global flag_engine
        flag_engine = not flag_engine
        engine_window.after(1000, reload_engine)

    def reload_generator():
        if flag_generator:
            current_generator.reload()
            generator_string.set(current_generator)
            engine_window.after(1000, reload_generator)
    def trigger_generator():
        global flag_generator
        flag_generator = not flag_generator
        engine_window.after(1000, reload_generator)

    def reload_boiler():
        if flag_boiler:
            current_boiler.reload()
            boiler_string.set(current_boiler)
            engine_window.after(1000, reload_boiler)
    def trigger_boiler():
        global flag_boiler
        flag_boiler = not flag_boiler
        engine_window.after(1000, reload_boiler)

    start_engine = tk.Button(engine_window, text='Start', command=trigger_engine )
    start_engine.grid(column=0, row=2, )

    start_generator = tk.Button(engine_window, text='Start', command=trigger_generator)
    start_generator.grid(column=1, row=2)

    start_boiler = tk.Button(engine_window, text='Start', command=trigger_boiler)
    start_boiler.grid(column=0, row=5)

def open_tanks():
    tank_window = tk.Toplevel(window)
    tank_window.title('Информация об экипаже')
    tank_window.geometry('1000x300')
    main_frame = tk.Frame(tank_window)
    main_frame.pack(fill=tk.BOTH, expand=1)
    my_canvas = tk.Canvas(main_frame)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    tank_frame = tk.Frame(my_canvas)
    my_canvas.create_window((0, 0), window=tank_frame, anchor="nw")
    for i in range(len(tank_list)):
        tk.Label(tank_frame, text=tank_list[i], justify='left', borderwidth=1, relief="solid", width=20).grid(column=i, row=0, padx = 5)


def open_crew():
    crew_window = tk.Toplevel(window)
    crew_window.title('Информация об экипаже')
    crew_window.geometry('200x700')
    main_frame = tk.Frame(crew_window)
    main_frame.pack(fill=tk.BOTH, expand=1)
    my_canvas = tk.Canvas(main_frame)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    crew_frame = tk.Frame(my_canvas)
    my_canvas.create_window((0, 0), window=crew_frame, anchor="nw")
    for i in range(len(crew_list)):
        tk.Label(crew_frame, text=crew_list[i], justify='left', borderwidth=1, relief="solid", width=100).grid(column = 0, row = i)
        image = Image.open(crew_list[i].picture_url)
        image1 = image.resize((100, 75), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image1)
        tk.Label(crew_frame, image=test).image = test
        tk.Label(crew_frame, image=test).grid(column = 1, row = i)
image1 = Image.open(r"1331041587_chertezh-tankera.jpg")
image1 = image1.resize((950, 250), Image.ANTIALIAS)
test = ImageTk.PhotoImage(image1)
label1 = tk.Label(second_frame,image=test)
label1.image = test
label1.grid(column = 1, row =1)


button_crew = tk.Button(second_frame, text = 'Информация об экипаже', command = open_crew, )
button_crew.grid(column = 1, row =0, sticky = 'w')


button_tanks = tk.Button(second_frame, text = 'Информация об грузе', command = open_tanks, )
button_tanks.grid(column = 1, row =2)

engine_room = tk.Button(second_frame, text = 'Машинное отделение', command = open_engine_room, )
engine_room.grid(column = 1, row =2, sticky = 'w', padx = 100)

lab_main_info = tk.Label(second_frame, text= 'Основная информация о судне:', width = 50, )
lab_main_info.grid(column =0, row = 0)
lab_ship_info = tk.Label(second_frame, text= ship1, justify = 'left', borderwidth=1, relief="solid")
lab_ship_info.grid(column = 0, row =1,)


lab_engine_info = tk.Label(second_frame, text= 'Основная информация о двигателе:')
lab_engine_info.grid(column = 0, row =2)
lab_engine = tk.Label(second_frame, text= engine1, justify = 'left', borderwidth=2, relief="groove")
lab_engine.grid(column = 0, row =3)

lab_current_info = tk.Label(second_frame, text= 'Текущая информация о судне:')
lab_current_info.grid(column = 0, row =4)
lab_current = tk.Label(second_frame, text= current_info_1, justify = 'left', borderwidth=2, relief="groove")
lab_current.grid(column = 0, row =5)


lab_dieselgenerator_info = tk.Label(second_frame, text= 'Основная информация о дизеле:', )
lab_dieselgenerator_info.grid(column = 1, row =4, sticky = 'w')
lab_diesel = tk.Label(second_frame, text= diesel, justify = 'left', borderwidth=2, relief="groove")
lab_diesel.grid(column = 1, row =5, sticky = 'w')

lab_generator_info = tk.Label(second_frame, text= 'Основная информация о генераторе:', )
lab_generator_info.grid(column = 1, row =6, sticky = 'w')
lab_generator = tk.Label(second_frame, text= generator, justify = 'left', borderwidth=2, relief="groove")
lab_generator.grid(column = 1, row =7, sticky = 'w')

window.mainloop()
