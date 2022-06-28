import requests
import json

headers = {
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2MmJhZjZhNmRjM2UwYTAwMTA2ZGI1ZjEiLCJzdWIiOiI1ZTc1MDMyMWJiNWE0MzA3NTk5YmFlNWUiLCJncnAiOiI1ZTc1MDMyMGJiNWE0M2UyOTk5YmFlNTkiLCJvcmciOiI1ZTc1MDMyMGJiNWE0M2UyOTk5YmFlNTkiLCJsaWMiOnRydWUsInVzZyI6ImFwaSIsImZ1bGwiOmZhbHNlLCJyaWdodHMiOjEuNSwiaWF0IjoxNjU2NDIwMDA2LCJleHAiOjE2NjE4OTMyMDB9.WpYPc2_MLmF8VkNLAzkRhmY0LJrba96ynz8jA7HMxdE",
    "Content-Type": "application/json",
}


response = requests.get("https://dev.rightech.io/api/v1/models", headers=headers)


objects = requests.get("http://dev.rightech.io/api/v1/objects", headers=headers)
objects = json.loads(objects.text)
for obj in objects:
    if obj["model"] == "62bb4538dc3e0a00106db702":
        ids = obj["_id"]

        data = {
            "engine_speed": 90,
            "speed_tc": 13600,
            "water_engine_inlect": 2.8,
            "water_charge_air": 3.2,
            "control_air": 6,
            "lube_oil_engine": 4.3,
            "nozzle_cool_water": 3.8,
            "charge_air": 1.9,
            "starting_air": 22,
            "lube_oil_tc": 1.3,
            "fuel_oil": 7.4,
        }
