import re
import numpy as np
import math
from currency_converter import CurrencyConverter
from numpy import genfromtxt

np.set_printoptions(suppress=True)
filename = 'WK1_Airbnb_Amsterdam_listings_proj.csv'

#Task 1
my_data = genfromtxt(filename, delimiter="|", dtype="unicode")

# Remove the first column and row
#Task 2
matrix = my_data[1:, 1:]

#Task 3
matrix2 = matrix.T

#matrix2 = np.array([re.sub('$', '', a) for a in matrix2]) 

#Task 4
matrix2 = np.char.replace(matrix2, "$", "")
matrix2 = np.char.replace(matrix2, ",", "")

#Task 5
matrix2[np.char.find(matrix2, "$") > -1]

#Task 6
matrix2 = matrix2.astype(np.float32)

#Task 7
cc = CurrencyConverter()
cc.currencies
array = matrix2[:, 1]

def currency_convert(column, pair1, pair2, array):
    converted_rate = cc.convert(column, pair1, pair2)
    array = array * converted_rate
    print("%s to %s: %s" % (pair1, pair2, matrix2[:, 1]))
    return array

this_currency = currency_convert(1, "USD", "GBP", array)

#Task 8
def inflation_convert(rate, array):
    inflation = array * rate
    print("Inflated at %s: %s" % (rate, inflation))
    return inflation

this_inflation = inflation_convert(1.07, this_currency)

#Task 9
def round_down(array):
    array = np.round(matrix2[:, 1], 2)
    print("Rounded Down:", array)

round_down(this_inflation)

#Task 10

def from_location_to_airbnb_listing_in_meters(lat1: float, lon1: float, lat2: list, lon2: list):
    # Source: https://community.esri.com/t5/coordinate-reference-systems-blog
    # /distance-on-a-sphere-the-haversine-formula/ba-p/902128

    R = 6371000  # Radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c  # Output distance in meters

    return round(meters, 0)

latitude = 52.3600
longitude = 4.8852

#%%timeit -r 4 -n 100
conv_to_meters = np.vectorize(from_location_to_airbnb_listing_in_meters)
conv_to_meters(latitude, longitude, matrix2[:, 2], matrix2[:, 3])

#meters = from_location_to_airbnb_listing_in_meters(
#    latitude, longitude, matrix2[:, 2], matrix2[:, 3]
#)
#meters = meters.reshape(-1,1)
#
#matrix2 = np.concatenate((matrix2, meters), axis=1)
#
#colors = np.zeros(meters.shape)
#matrix2 = np.concatenate((matrix2, colors), axis=1)
matrix2[:5, :]

np.savetxt("JJ_WK1_Airbnb_Amsterdam_listings_proj_solutions.csv", matrix2, delimiter=",")
