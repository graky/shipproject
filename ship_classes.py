import random
import pandas as pd
import requests
import json

HEADERS = {
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2MmJhZjZhNmRjM2UwYTAwMTA2ZGI1ZjEiLCJzdWIiOiI1ZTc1MDMyMWJiNWE0MzA3NTk5YmFlNWUiLCJncnAiOiI1ZTc1MDMyMGJiNWE0M2UyOTk5YmFlNTkiLCJvcmciOiI1ZTc1MDMyMGJiNWE0M2UyOTk5YmFlNTkiLCJsaWMiOnRydWUsInVzZyI6ImFwaSIsImZ1bGwiOmZhbHNlLCJyaWdodHMiOjEuNSwiaWF0IjoxNjU2NDIwMDA2LCJleHAiOjE2NjE4OTMyMDB9.WpYPc2_MLmF8VkNLAzkRhmY0LJrba96ynz8jA7HMxdE",
    "Content-Type": "application/json",
}

BOILER_MODEL_ID = "62bb0fe3dc3e0a00106db636"
GENERATOR_MODEL_ID = "62bb406edc3e0a00106db6fd"
ENGINE_MODEL_ID = "62bb4538dc3e0a00106db702"


def save_to_csv(filename, columns, add_to):
    try:
        data_frame = pd.read_csv(filename)
    except FileNotFoundError:
        data_frame = pd.DataFrame(columns=columns)

    data_frame = data_frame.append(add_to, ignore_index=True)
    data_frame.to_csv(filename, index=False)


def get_item(model_id, item_id=None):
    if item_id:
        object = requests.get(
            "http://dev.rightech.io/api/v1/objects/" + item_id, headers=HEADERS
        )
        object = json.loads(object.text)
        return object
    objects = requests.get("http://dev.rightech.io/api/v1/objects", headers=HEADERS)
    objects = json.loads(objects.text)
    objects = list(
        filter(lambda item: True if item["model"] == model_id else False, objects)
    )
    obj = random.choice(objects)
    state = obj["state"]
    state["_id"] = obj["_id"]
    return state


class CurrentBoiler:
    columns = [
        "Время",
        "Нагрузка котла",
        "Давление пара в котле",
        "Расход топлива",
        "Температура питательной воды",
        "Напор создаваемый питательным насосом",
        "Давление топлива перед форсунками",
        "Напор создаваемый циркуляционным насосом",
    ]

    def __init__(
        self,
        _id,
        boiler_load,
        steam_pressure,
        fuel,
        feed_water_temp,
        feed_pump_pressure,
        fuel_pressure,
        circulatory_pump_pressure,
        **kwargs,
    ):
        self._id = _id
        self.boiler_load = boiler_load
        self.steam_pressure = steam_pressure
        self.fuel = fuel
        self.feed_water_temp = feed_water_temp
        self.feed_pump_pressure = feed_pump_pressure
        self.fuel_pressure = fuel_pressure
        self.circulatory_pump_pressure = circulatory_pump_pressure

    def __repr__(self):
        return """Нагрузка котла – {0} %
        Давление пара в котле – {1} кг/см2
        Расход топлива – {2} кг/ч
        Температура питательной воды – {3} 0С
        Напор создаваемый питательным насосом – {4}м
        Давление топлива перед форсунками – {5} кг/см2
        Напор создаваемый циркуляционным насосом  – {6} м
        """.format(
            self.boiler_load,
            self.steam_pressure,
            self.fuel,
            self.feed_water_temp,
            self.feed_pump_pressure,
            self.fuel_pressure,
            self.circulatory_pump_pressure,
        )

    def repr_dict(self, time):
        dict_repr = {
            "Время": time,
            "Нагрузка котла": self.boiler_load,
            "Давление пара в котле": self.steam_pressure,
            "Расход топлива": self.fuel,
            "Температура питательной воды": self.feed_water_temp,
            "Напор создаваемый питательным насосом": self.feed_pump_pressure,
            "Давление топлива перед форсунками": self.fuel_pressure,
            "Напор создаваемый циркуляционным насосом": self.circulatory_pump_pressure,
        }
        return dict_repr

    def reload(self):
        new_data = get_item(BOILER_MODEL_ID, item_id=self._id)["state"]
        self.boiler_load = new_data["boiler_load"]
        self.fuel = new_data["fuel"]
        self.feed_pump_pressure = new_data["feed_pump_pressure"]
        self.fuel_pressure = new_data["fuel_pressure"]
        self.circulatory_pump_pressure = new_data["circulatory_pump_pressure"]


class Boiler:
    def __init__(
        self,
        steamcapacity,
        boiler_number,
        steam_pressure,
        temp_feed_water,
        temp_air,
        fuel_consumption,
        excess_air_ratio,
        oxygen_content,
        air_consumption,
        gas_flow,
        combustion_pressure,
        fuel,
        classification,
    ):
        self.steamcapacity = steamcapacity
        self.boiler_number = boiler_number
        self.steam_pressure = steam_pressure
        self.temp_feed_water = temp_feed_water
        self.temp_air = temp_air
        self.fuel_consumption = fuel_consumption
        self.excess_air_ratio = excess_air_ratio
        self.oxygen_content = oxygen_content
        self.air_consumption = air_consumption
        self.gas_flow = gas_flow
        self.combustion_pressure = combustion_pressure
        self.fuel = fuel
        self.classification = classification

    def __repr__(self):
        return """Паропроизводительность – {0} кг/ч
    Количество котлов на судне – {1} шт
    Давление пара – {2} кг/см2
    Температура питательной воды – {3} 0С
    Температура воздуха – {4}0С
    Расход топлива – {5} кг/ч
    Коэфицент избытка воздуха при 100% нагр,  – {6}
    Пар насыщенный
    Содержание кислорода – {7} %
    Расход воздуха – {8} кг/ч
    Проток газов – {9} кг/ч
    Давление сгорания топлива – {10} кг/см2
    Топливо – мазут с максимальной вязкостью {11} Сст/50 0С
    Классификация – {12}
    """.format(
            self.steamcapacity,
            self.boiler_number,
            self.steam_pressure,
            self.temp_feed_water,
            self.temp_air,
            self.fuel_consumption,
            self.excess_air_ratio,
            self.oxygen_content,
            self.air_consumption,
            self.gas_flow,
            self.combustion_pressure,
            self.fuel,
            self.classification,
        )


class CurrentGenerator:

    columns = [
        "Время",
        "Сила тока, вырабатываемая дизельгенератором",
        "Расход топлива",
        "Температура воздуха  в машинном отделении",
        "Температура уходящих газов tуг  по цилиндрам",
        "Средняя температура уходящих газов",
        "Давление  сжатия  в  цилиндрах",
        "Давление сгорания в цилиндре",
        "Давление охлаждающей воды за циркуляционным насосом системы охлаждения ДГ",
        "Давление охлаждающей воды на всасывании циркуляционного насоса",
        "Напор, создаваемый насосом",
        "Расход охлаждающей воды",
        "Температура охлаждающей воды на входе в охладитель",
        "Температура  охлаждающей  воды на выходе из водоохладителя",
    ]

    def __init__(
        self,
        _id,
        amperage,
        fuel,
        temp,
        exit_gas_temp,
        average_temp_exit,
        compression_pressure,
        combustion_pressure,
        cold_water_of,
        cold_water_exit,
        pressure,
        consump_water,
        temp_cold_water_in,
        temp_cold_water_out,
        **kwargs,
    ):
        self._id = _id
        self.amperage = amperage
        self.fuel = fuel
        self.temp = temp
        self.exit_gas_temp = exit_gas_temp
        self.average_temp_exit = average_temp_exit
        self.compression_pressure = compression_pressure
        self.combustion_pressure = combustion_pressure
        self.cold_water_of = cold_water_of
        self.cold_water_exit = cold_water_exit
        self.pressure = pressure
        self.consump_water = consump_water
        self.temp_cold_water_in = temp_cold_water_in
        self.temp_cold_water_out = temp_cold_water_out

    def __repr__(self):
        return """Сила тока, вырабатываемая дизельгенератором (ГРЩ) – {0} I
    Расход топлива – {1} кг/ч
    Температура воздуха  в машинном отделении – {2} 
    Температура уходящих газов tуг  по цилиндрам – {3} %
    Средняя температура уходящих газов – {4}°
    Давление  сжатия  в  цилиндрах  – {5}рс
    Давление сгорания в цилиндре – {6} 
    Давление охлаждающей воды за циркуляционным насосом системы охлаждения ДГ - {7} Р2
    Давление охлаждающей воды на всасывании циркуляционного насоса  – {8} P1
    Напор, создаваемый насосом – {9} 
    Расход охлаждающей воды – {10} 
    Температура охлаждающей воды на входе в охладитель – {11} t1
    Температура  охлаждающей  воды на выходе из водоохладителя: {12} t2
    """.format(
            self.amperage,
            self.fuel,
            self.temp,
            self.exit_gas_temp,
            self.average_temp_exit,
            self.compression_pressure,
            self.combustion_pressure,
            self.cold_water_of,
            self.cold_water_exit,
            self.pressure,
            self.consump_water,
            self.temp_cold_water_in,
            self.temp_cold_water_out,
        )

    def repr_dict(self, time):
        dict_repr = {
            "Время": time,
            "Сила тока, вырабатываемая дизельгенератором": self.amperage,
            "Расход топлива": self.fuel,
            "Температура воздуха  в машинном отделении": self.temp,
            "Температура уходящих газов tуг  по цилиндрам": self.exit_gas_temp,
            "Средняя температура уходящих газов": self.average_temp_exit,
            "Давление  сжатия  в  цилиндрах": self.compression_pressure,
            "Давление сгорания в цилиндре": self.combustion_pressure,
            "Давление охлаждающей воды за циркуляционным насосом системы охлаждения ДГ": self.cold_water_of,
            "Давление охлаждающей воды на всасывании циркуляционного насоса": self.cold_water_exit,
            "Напор, создаваемый насосом": self.pressure,
            "Расход охлаждающей воды": self.consump_water,
            "Температура охлаждающей воды на входе в охладитель": self.temp_cold_water_in,
            "Температура  охлаждающей  воды на выходе из водоохладителя": self.temp_cold_water_out,
        }
        return dict_repr

    def reload(self):
        new_data = get_item(BOILER_MODEL_ID, item_id=self._id)["state"]
        self.amperage = new_data["amperage"]
        self.fuel = new_data["fuel"]
        self.temp = new_data["temp"]
        self.exit_gas_temp = new_data["exit_gas_temp"]
        self.average_temp_exit = new_data["average_temp_exit"]
        self.compression_pressure = new_data["compression_pressure"]
        self.combustion_pressure = new_data["combustion_pressure"]
        self.cold_water_of = new_data["cold_water_of"]
        self.cold_water_exit = new_data["cold_water_exit"]
        self.pressure = new_data["pressure"]
        self.consump_water = new_data["consump_water"]
        self.temp_cold_water_in = new_data["temp_cold_water_in"]
        self.temp_cold_water_out = new_data["temp_cold_water_out"]


class Generator:
    def __init__(
        self,
        model,
        power,
        voltage,
        amperage,
        frequency,
        efficiency,
        cos,
    ):
        self.model = model
        self.power = power
        self.voltage = voltage
        self.amperage = amperage
        self.frequency = frequency
        self.efficiency = efficiency
        self.cos = cos

    def __repr__(self):
        return """Модель: {0} м^3
Мощность: {1} кВт
Напряжение: {2} В
Сила тока: {3} А
Частота: {4} Гц
КПД: {5}%
COS: {6}""".format(
            self.model,
            self.power,
            self.voltage,
            self.amperage,
            self.frequency,
            self.efficiency,
            self.cos,
        )


class Diesel:
    def __init__(
        self,
        model,
        cylinder_diameter,
        piston_stroke,
        power,
        rpm,
        average_pressure,
        piston_speed,
        combustion_pressure,
        pisto_order,
        start_air_pressure,
        weight,
        compression_ratio,
        press_principle,
        normal_start_air_pressure,
        minimal_start_air_pressure,
        regulator,
    ):
        self.model = model
        self.cylinder_diameter = cylinder_diameter
        self.piston_stroke = piston_stroke
        self.power = power
        self.rpm = rpm
        self.average_pressure = average_pressure
        self.piston_speed = piston_speed
        self.combustion_pressure = combustion_pressure
        self.pisto_order = pisto_order
        self.start_air_pressure = start_air_pressure
        self.weight = weight
        self.compression_ratio = compression_ratio
        self.press_principle = press_principle
        self.normal_start_air_pressure = normal_start_air_pressure
        self.minimal_start_air_pressure = minimal_start_air_pressure
        self.regulator = regulator

    def __repr__(self):
        return """Модель – {0};
Диаметр цилиндра – {1} мм;
Ход поршня – {2} мм;
Мощность – {3} кВт;
Кол-во оборотов – {4} об/м;
Среднее эфективное давление – {5} бар;
Скорость поршня – {6} м/с;
Давление сгорания – {7} бар;
Порядок работы цилиндров – {8};
Давление пускового воздуха – {9} бар;
Вес – {10} тонн;
Степень сжатия – {11};
Принцип наддува: {12};
Давление пускового воздуха: Нормальное – {13} бар;
                            Минимальное – {14} бар;
регулятор   - {15}
""".format(
            self.model,
            self.cylinder_diameter,
            self.piston_stroke,
            self.power,
            self.rpm,
            self.average_pressure,
            self.piston_speed,
            self.combustion_pressure,
            self.pisto_order,
            self.start_air_pressure,
            self.weight,
            self.compression_ratio,
            self.press_principle,
            self.normal_start_air_pressure,
            self.minimal_start_air_pressure,
            self.regulator,
        )


class Ship:
    def __init__(
        self,
        name,
        flag,
        number,
        class_,
        body_type,
        main_engine,
        max_speed,
        developer,
        build_date,
        displacement,
        deadweight,
        lenght,
        width,
        max_height,
        boart_height,
        cargo_tanks,
    ):
        self.name = name
        self.flag = flag
        self.number = number
        self.class_ = class_
        self.body_type = body_type
        self.main_engine = main_engine
        self.max_speed = max_speed
        self.developer = developer
        self.build_date = build_date
        self.displacement = displacement
        self.deadweight = deadweight
        self.cargo_tanks = cargo_tanks
        self.lenght = lenght
        self.width = width
        self.max_height = max_height
        self.boart_height = boart_height

    def __repr__(self):
        return """1.	Название: {0}
2.	Флаг: {1}
3.	Номер: {2}
4.	Класс: {3}
5.	Тип корпуса: {4}
6.	Главный двигатель: {5}
7.	макс. скорость: {6} узлов (груз/балласт)
8.	Постройщик: {7}
9.	Дата постройки:	{8}
10.	Водоизмещение: {9} т
11.	Дедвейт: {10} т
12.	Грузовые танки: {11} т
13.	Длина {12} м
14.	Ширина {13} м
15.	Высота макс. {14} м
16.	Высота борта {15} м
""".format(
            self.name,
            self.flag,
            self.number,
            self.class_,
            self.body_type,
            self.main_engine,
            self.max_speed,
            self.developer,
            self.build_date,
            self.displacement,
            self.deadweight,
            self.cargo_tanks,
            self.lenght,
            self.width,
            self.max_height,
            self.boart_height,
        )


class CurrentEngine:

    columns = [
        "Время",
        "Engine speed",
        "Speed tc",
        "HT coll water engine inlet",
        "ET- cool water charge air",
        "Control air",
        "Lube oil engine",
        "Nozzle cool water",
        "Charge air",
        "Starting air",
        "Lube oil TC",
        "Fuel oil",
    ]

    def __init__(
        self,
        _id,
        engine_speed,
        speed_tc,
        water_engine_inlect,
        water_charge_air,
        control_air,
        lube_oil_engine,
        nozzle_cool_water,
        charge_air,
        starting_air,
        lube_oil_tc,
        fuel_oil,
        **kwargs,
    ):
        self._id = _id
        self.engine_speed = engine_speed
        self.speed_tc = speed_tc
        self.water_engine_inlect = water_engine_inlect
        self.water_charge_air = water_charge_air
        self.control_air = control_air
        self.lube_oil_engine = lube_oil_engine
        self.nozzle_cool_water = nozzle_cool_water
        self.charge_air = charge_air
        self.starting_air = starting_air
        self.lube_oil_tc = lube_oil_tc
        self.fuel_oil = fuel_oil

    def __repr__(self):
        return """Engine speed: {0} rpm
Speed tc: {1} tc
HT coll water engine inlet {2} bar
ET- cool water charge air: {3} bar
Control air: {4} bar
Lube oil engine: {5} bar
Nozzle cool water: {6} bar
Charge air: {7} bar
Starting air: {8} bar
Lube oil TC: {9} bar
Fuel oil: {10} bar
""".format(
            self.engine_speed,
            self.speed_tc,
            self.water_engine_inlect,
            self.water_charge_air,
            self.control_air,
            self.lube_oil_engine,
            self.nozzle_cool_water,
            self.charge_air,
            self.starting_air,
            self.lube_oil_tc,
            self.fuel_oil,
        )

    def repr_dict(self, time):
        dict_repr = {
            "Время": time,
            "Engine speed": self.engine_speed,
            "Speed tc": self.speed_tc,
            "HT coll water engine inlet": self.water_engine_inlect,
            "ET- cool water charge air": self.water_charge_air,
            "Control air": self.control_air,
            "Lube oil engine": self.lube_oil_engine,
            "Nozzle cool water": self.nozzle_cool_water,
            "Charge air": self.charge_air,
            "Starting air": self.starting_air,
            "Lube oil TC": self.lube_oil_tc,
            "Fuel oil": self.fuel_oil,
        }
        return dict_repr

    def reload(self):
        new_data = get_item(ENGINE_MODEL_ID, item_id=self._id)["state"]
        self.engine_speed = new_data["engine_speed"]
        self.speed_tc = new_data["speed_tc"]
        self.water_engine_inlect = new_data["water_engine_inlect"]
        self.control_air = new_data["control_air"]
        self.lube_oil_engine = new_data["lube_oil_engine"]
        self.nozzle_cool_water = new_data["nozzle_cool_water"]
        self.charge_air = new_data["charge_air"]
        self.starting_air = new_data["starting_air"]
        self.lube_oil_tc = new_data["lube_oil_tc"]
        self.fuel_oil = new_data["fuel_oil"]


class Engine:
    def __init__(
        self,
        type_,
        cylinder_number,
        piston_diameter,
        piston_stroke,
        max_power,
        max_rpm,
        nominal_power,
        nominal_rpm,
        max_pressure,
        jacket_cooling,
        launch_system,
        piston_cooling,
        purge_air_cooler_cooling,
        cylinder_order,
        fresh_water_temp,
        fuel_consumption,
        fuel_lower_energy_char,
    ):
        self.type_ = type_
        self.cylinder_number = cylinder_number
        self.piston_diameter = piston_diameter
        self.piston_stroke = piston_stroke
        self.max_power = max_power
        self.max_rpm = max_rpm
        self.nominal_power = nominal_power
        self.nominal_rpm = nominal_rpm
        self.max_pressure = max_pressure
        self.jacket_cooling = jacket_cooling
        self.launch_system = launch_system
        self.piston_cooling = piston_cooling
        self.purge_air_cooler_cooling = purge_air_cooler_cooling
        self.cylinder_order = cylinder_order
        self.fresh_water_temp = fresh_water_temp
        self.fuel_consumption = fuel_consumption
        self.fuel_lower_energy_char = fuel_lower_energy_char

    def __repr__(self):
        return """Тип: 	{0}
Число цилиндров: 	{1}
Диаметр поршня: 	{2} мм
Ход поршня: 	{3} мм
Максимальная мощность: 	{4} л/с,{5} кВт при {6} об/мин.
Номинальная мощность: 	{7} л/с,{8} кВт при {9} об/мин.
Максимальное давление: 	{10} бар
Охлаждение рубашки цилиндров: 	{11}
Система пуска:	{12} 
Охлаждение поршней: 	{13}
Охлаждение холодильника продувочного воздуха:	{14}
Порядок работы цилиндров: 	{15}
Температура пресной воды на входе: 	{16} oC
Расход топлива: 	{17} г/л/с/ч 
Нижняя энергетическая хар.топлива: 	{18} кДж/кг({19} ккал/кг)
""".format(
            self.type_,
            self.cylinder_number,
            self.piston_diameter,
            self.piston_stroke,
            self.max_power,
            self.max_power / 1.36,
            self.max_rpm,
            self.nominal_power,
            self.nominal_power / 1.36,
            self.nominal_rpm,
            self.max_pressure,
            self.jacket_cooling,
            self.launch_system,
            self.piston_cooling,
            self.purge_air_cooler_cooling,
            self.cylinder_order,
            self.fresh_water_temp,
            self.fuel_consumption,
            self.fuel_lower_energy_char,
            self.fuel_lower_energy_char / 4.184,
        )


class CurrentInfo:
    def __init__(
        self,
        depature_port,
        arrival_port,
        ATD,
        ETA,
        Vessel_Local_Time,
        Area,
        Latitude,
        Longitude,
        Status,
        Speed,
        Course,
        Wind,
        Wind_direction,
        Air_Temperature,
    ):
        self.depature_port = depature_port
        self.arrival_port = arrival_port
        self.ATD = ATD
        self.ETA = ETA
        self.Vessel_Local_Time = Vessel_Local_Time
        self.Area = Area
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.Status = Status
        self.Speed = Speed
        self.Course = Course
        self.Wind = Wind
        self.Wind_direction = Wind_direction
        self.Air_Temperature = Air_Temperature

    def __repr__(self):
        return """Порт отбытия: {0}
        Порт прибытия: {1}
        Актуальное время отбытия: {2}
        Предполагаемое время прибытия: {3}
        Актуальный часовой пояс судна: {4}
        Текущая область нахождения: {5}
        Широта: {6}° 
        Долгота: {7}°
        Статус судна: {8}
        Текущая скорость: {9} узл.
        Текущий курс: {10}°
        Скорость ветра: {11} узл.
        Направление ветра: {12}°
        Температура воздуха {13}°C
        """.format(
            self.depature_port,
            self.arrival_port,
            self.ATD,
            self.ETA,
            self.Vessel_Local_Time,
            self.Area,
            self.Latitude,
            self.Longitude,
            self.Status,
            self.Speed,
            self.Course,
            self.Wind,
            self.Wind_direction,
            self.Air_Temperature,
        )


class CrewMember:
    def __init__(
        self, name, position, current_location, current_occupation, picture_url
    ):
        self.name = name
        self.position = position
        self.current_location = current_location
        self.current_occupation = current_occupation
        self.picture_url = picture_url

    def __repr__(self):
        return """Должность: {0}
ФИО: {1}
Текущее местонахождение: {2}
Текущее занятие: {3}""".format(
            self.position,
            self.name,
            self.current_occupation,
            self.current_location,
        )

    def get_picture(self):
        return self.picture_url


class Cargo:
    def __init__(
        self,
        volume,
        fuel_volume,
        fuel,
        fuel_weight,
    ):
        self.volume = volume
        self.fuel_volume = fuel_volume
        self.fuel = fuel
        self.fuel_weight = fuel_weight

    def __repr__(self):
        return """Объем танка: {0} м^3
Груз: {1}
Объем груза: {2} м^3
Масса груза: {3} т.""".format(
            self.volume,
            self.fuel_volume,
            self.fuel,
            self.fuel_weight,
        )
