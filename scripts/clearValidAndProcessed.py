import os

import requests

PROCESSED_MEASUREMENT_EVERY_48_HOURS = (
    "/api/processed_measurements_before_48_hours/"
)
VALID_PROCESSED_MEASUREMENT_EVERY_48_HOURS = (
    "/api/valid_processed_measurements_before_48_hours/"
)
BASE_URL = str(os.environ.get("API_OPEN"))
# BASE_URL = 'https://openqairamapnapi.qairadrones.com'


# Frequency: daily, every 24 hours
# Deletes all data from valid_processed_measurement table that comply with the following conditions:
# 1. Data is 48 hours older than the current time when the script is ran. In other words, the only
# data that will be safe is the one between now and 2 days before.
# 2. qHAWAX type MUST be static, either interior or exterior.

# No need to verify if the qHAWAXs exist because they are all requested from the API itself.
# Just to map out who are STATIC, since we are ONLY deleting the data saved on those qHAWAX
# print(BASE_URL + PROCESSED_MEASUREMENT_EVERY_48_HOURS)
# Starting with processed_measurement
print("Deleting processed measurements")
response = requests.post(BASE_URL + PROCESSED_MEASUREMENT_EVERY_48_HOURS)
print(response.text)
# print(response.text)
# Continuing with valid processed measurement
# print(BASE_URL + VALID_PROCESSED_MEASUREMENT_EVERY_48_HOURS)
print("Deleting valid processed measurements")
response = requests.post(BASE_URL + VALID_PROCESSED_MEASUREMENT_EVERY_48_HOURS)
print(response.text)
