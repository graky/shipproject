import requests
import json
import random
import time

headers = {
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2MmJhZjZhNmRjM2UwYTAwMTA2ZGI1ZjEiLCJzdWIiOiI1ZTc1MDMyMWJiNWE0MzA3NTk5YmFlNWUiLCJncnAiOiI1ZTc1MDMyMGJiNWE0M2UyOTk5YmFlNTkiLCJvcmciOiI1ZTc1MDMyMGJiNWE0M2UyOTk5YmFlNTkiLCJsaWMiOnRydWUsInVzZyI6ImFwaSIsImZ1bGwiOmZhbHNlLCJyaWdodHMiOjEuNSwiaWF0IjoxNjU2NDIwMDA2LCJleHAiOjE2NjE4OTMyMDB9.WpYPc2_MLmF8VkNLAzkRhmY0LJrba96ynz8jA7HMxdE",
    "Content-Type": "application/json",
}

BOILER_MODEL_ID = "62bb0fe3dc3e0a00106db636"
GENERATOR_MODEL_ID = "62bb406edc3e0a00106db6fd"
ENGINE_MODEL_ID = "62bb4538dc3e0a00106db702"

pls_min = [1, -1]
while True:
    time.sleep(1)
    objects = requests.get("http://dev.rightech.io/api/v1/objects", headers=headers)
    objects = json.loads(objects.text)
    for obj in objects:
        if obj["model"] == BOILER_MODEL_ID:
            ids = obj["_id"]
            obj = obj["state"]
            prct_list = list(range(1, 25, 1))
            data = {
                "boiler_load": obj["boiler_load"]
                + int(
                    random.choice(prct_list)
                    * 0.01
                    * (random.choice(pls_min) if obj["boiler_load"] < 100 else -1)
                    * obj["boiler_load"]
                ),
                "fuel": round(
                    obj["fuel"]
                    + (
                        random.choice(prct_list)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["fuel"]
                    ),
                    3,
                ),
                "feed_pump_pressure": round(
                    obj["feed_pump_pressure"]
                    + (
                        random.choice(prct_list)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["feed_pump_pressure"]
                    ),
                    3,
                ),
                "fuel_pressure": round(
                    obj["fuel_pressure"]
                    + (
                        random.choice(prct_list)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["fuel_pressure"]
                    ),
                    3,
                ),
                "circulatory_pump_pressure": round(
                    obj["circulatory_pump_pressure"]
                    + (
                        random.choice(prct_list)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["circulatory_pump_pressure"]
                    ),
                    3,
                ),
            }
            response = requests.post(
                "https://dev.rightech.io/api/v1/objects/" + str(ids) + "/packets",
                headers=headers,
                json=data,
            )
        elif obj["model"] == GENERATOR_MODEL_ID:
            ids = obj["_id"]
            obj = obj["state"]
            prct_list = list(range(1, 25, 1))
            data = {
                "amperage": obj["amperage"]
                + int(
                    random.choice(prct_list)
                    * 0.01
                    * random.choice(pls_min)
                    * obj["amperage"]
                ),
                "fuel": obj["fuel"]
                + int(
                    random.choice(prct_list)
                    * 0.01
                    * random.choice(pls_min)
                    * obj["fuel"]
                ),
                "temp": round(
                    obj["temp"]
                    + (
                        random.choice(prct_list)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["temp"]
                    ),
                    3,
                ),
                "exit_gas_temp": list(
                    map(
                        lambda x: round(
                            x
                            + random.choice(prct_list)
                            * 0.01
                            * random.choice(pls_min)
                            * x,
                            2,
                        ),
                        obj["exit_gas_temp"],
                    )
                ),
                "average_temp_exit": round(
                    obj["average_temp_exit"]
                    + (
                        random.choice(prct_list)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["average_temp_exit"]
                    ),
                    3,
                ),
                "combustion_pressure": list(
                    map(
                        lambda x: round(
                            x
                            + random.choice(prct_list)
                            * 0.01
                            * random.choice(pls_min)
                            * x,
                            2,
                        ),
                        obj["combustion_pressure"],
                    )
                ),
                "cold_water_of": round(
                    obj["cold_water_of"]
                    + (
                        random.choice(prct_list)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["cold_water_of"]
                    ),
                    3,
                ),
                "cold_water_exit": round(
                    obj["cold_water_exit"]
                    + (
                        random.choice(prct_list)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["cold_water_exit"]
                    ),
                    3,
                ),
                "pressure": round(
                    obj["pressure"]
                    + (
                        random.choice(prct_list)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["pressure"]
                    ),
                    3,
                ),
                "consump_water": round(
                    obj["consump_water"]
                    + (
                        random.choice(prct_list)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["consump_water"]
                    ),
                    3,
                ),
                "temp_cold_water_in": round(
                    obj["temp_cold_water_in"]
                    + (
                        random.choice(prct_list)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["temp_cold_water_in"]
                    ),
                    3,
                ),
                "temp_cold_water_out": round(
                    obj["temp_cold_water_out"]
                    + (
                        random.choice(prct_list)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["temp_cold_water_out"]
                    ),
                    3,
                ),
            }
            response = requests.post(
                "https://dev.rightech.io/api/v1/objects/" + str(ids) + "/packets",
                headers=headers,
                json=data,
            )
        elif obj["model"] == ENGINE_MODEL_ID:
            ids = obj["_id"]
            obj = obj["state"]
            prct_list = list(range(1, 6, 1))
            prct_list2 = list(range(1, 42, 1))
            data = {
                "engine_speed": obj["engine_speed"]
                + int(
                    random.choice(prct_list)
                    * 0.01
                    * random.choice(pls_min)
                    * obj["engine_speed"]
                ),
                "speed_tc": obj["speed_tc"]
                + int(
                    random.choice(prct_list)
                    * 0.01
                    * random.choice(pls_min)
                    * obj["speed_tc"]
                ),
                "water_engine_inlect": round(
                    obj["water_engine_inlect"]
                    + (
                        random.choice(prct_list2)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["water_engine_inlect"]
                    ),
                    3,
                ),
                "water_charge_air": round(
                    obj["water_charge_air"]
                    + (
                        random.choice(prct_list2)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["water_charge_air"]
                    ),
                    3,
                ),
                "control_air": round(
                    obj["control_air"]
                    + (
                        random.choice(prct_list)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["control_air"]
                    ),
                    3,
                ),
                "lube_oil_engine": round(
                    obj["lube_oil_engine"]
                    + (
                        random.choice(prct_list)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["lube_oil_engine"]
                    ),
                    3,
                ),
                "nozzle_cool_water": round(
                    obj["nozzle_cool_water"]
                    + (
                        random.choice(prct_list2)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["nozzle_cool_water"]
                    ),
                    3,
                ),
                "charge_air": round(
                    obj["charge_air"]
                    + (
                        random.choice(prct_list2)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["charge_air"]
                    ),
                    3,
                ),
                "starting_air": round(
                    obj["starting_air"]
                    + (
                        random.choice(prct_list)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["starting_air"]
                    ),
                    3,
                ),
                "lube_oil_tc": round(
                    obj["lube_oil_tc"]
                    + (
                        random.choice(prct_list)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["lube_oil_tc"]
                    ),
                    3,
                ),
                "fuel_oil": round(
                    obj["fuel_oil"]
                    + (
                        random.choice(prct_list2)
                        * 0.01
                        * random.choice(pls_min)
                        * obj["fuel_oil"]
                    ),
                    3,
                ),
            }
            response = requests.post(
                "https://dev.rightech.io/api/v1/objects/" + str(ids) + "/packets",
                headers=headers,
                json=data,
            )
