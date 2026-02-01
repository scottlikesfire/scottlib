# this module contains utility functions for common unit conversions. It is also 
# a fun experiment in letting copilot do its thing. I will someday check its math....
# at some point i would like to experiment with making a dynamic library with unit typing and deriving 
# conversions and caching them, and updating the actual repo. Doing experiments sort of like prolog truth evaluation
# would be neat too. We will see if that ever happens


# Constants
FREEZING_POINT_C = 0.0  # freezing point of water in Celsius
BOILING_POINT_C = 100.0  # boiling point of water in Celsius
FREEZING_POINT_F = 32.0  # freezing point of water in Faren
BOILING_POINT_F = 212.0  # boiling point of water in Farenheit
GRAVITATIONAL_CONSTANT_G = 6.67430e-11  # gravitational constant in m^3 kg^-1 s^-2
EARTH_GRAVITY_MPS2 = 9.80665  # acceleration due to gravity on Earth in m/s^2
SPEED_OF_LIGHT_MPS = 299792458  # speed of light in meters per second
SPEED_OF_LIGHT_MPH = 670616629.384  # speed of light in miles per hour


# Distances
def feet_to_inches(feet):
    """Convert feet to inches."""
    return feet * 12.0
def inches_to_feet(inches):
    """Convert inches to feet."""
    return inches / 12.0
def inches_to_cm(inches):
    """Convert inches to centimeters."""
    return inches * 2.54 

def cm_to_inches(cm):
    """Convert centimeters to inches."""
    return cm / 2.54

def feet_to_meters(feet):
    """Convert feet to meters."""
    return feet * 0.3048

def meters_to_feet(meters):
    """Convert meters to feet."""
    return meters / 0.3048
def cm_to_feet(cm):
    """Convert centimeters to feet."""
    return cm / 30.48
def feet_to_feetandinches_string(feet):
    """Convert feet to a string in feet and inches format."""
    total_inches = feet * 12
    whole_feet = int(total_inches // 12)
    inches = total_inches % 12
    return f"{whole_feet}' {inches:.2f}\""

# speeds
def kilometers_to_miles(km):
    """Convert kilometers to miles."""
    return km * 0.621371
def miles_to_kilometers(miles):
    """Convert miles to kilometers."""
    return miles / 0.621371
def kt_to_mps(kt):
    """Convert knots to meters per second."""
    return kt * 0.514444
def kt_to_mph(kt):
    """Convert knots to miles per hour."""
    return kt * 1.15078
def mps_to_kt(mps):
    """Convert meters per second to knots."""
    return mps / 0.514444
def mph_to_kt(mph):
    """Convert miles per hour to knots."""
    return mph / 1.15078
def mph_to_fractional_c(mph):
    """Convert miles per hour to fractional speed of light."""
    speed_of_light_mph = 670616629.384 # miles per hour
    return mph / speed_of_light_mph
def fractional_c_to_mph(fractional_c):
    """Convert fractional speed of light to miles per hour."""
    return fractional_c * SPEED_OF_LIGHT_MPH
def mps_to_fractional_c(mps):
    """Convert meters per second to fractional speed of light."""
    return mps / SPEED_OF_LIGHT_MPS
def fractional_c_to_mps(fractional_c):
    """Convert fractional speed of light to meters per second."""
    return fractional_c * SPEED_OF_LIGHT_MPS
def furlong_per_fortnight_to_kmph(furlong_per_fortnight):
    """Convert furlongs per fortnight to kilometers per hour."""
    return furlong_per_fortnight * 0.000598715 # I did check the math on this one and it was off by an order of magnitude. I fixed it.

# Mass/weight
def pounds_to_kg(pounds):
    """Convert pounds to kilograms."""
    return pounds * 0.45359237

def kg_to_pounds(kg):
    """Convert kilograms to pounds."""
    return kg / 0.45359237  
def pounds_to_newtons(pounds):
    """Convert pounds to newtons."""
    return pounds * 4.44822
def newtons_to_pounds(newtons):
    """Convert newtons to pounds."""
    return newtons / 4.44822
def kg_to_stone(kg):
    """Convert kilograms to stone."""
    return kg / 6.35029318
def stone_to_kg(stone):
    """Convert stone to kilograms."""
    return stone * 6.35029318   
def pounds_to_stone(pounds):
    """Convert pounds to stone."""
    return pounds / 14.0
def stone_to_pounds(stone):
    """Convert stone to pounds."""
    return stone * 14.0

# Volume
def gallons_to_liters(gallons):
    """Convert gallons to liters."""
    return gallons * 3.785414   

def liters_to_gallons(liters):
    """Convert liters to gallons."""
    return liters / 3.785414

# Temperature
def farenheit_to_celsius(farenheit):
    """Convert Farenheit to Celsius."""
    return (farenheit - 32) * 5.0/9.0

def celsius_to_farenheit(celsius):
    """Convert Celsius to Farenheit."""
    return (celsius * 9.0/5.0) + 32

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15

def celsius_to_kelvin(celsius):
    """Convert Celsius to Kelvin."""
    return celsius + 273.15

def farenheit_to_kelvin(farenheit):
    """Convert Farenheit to Kelvin."""
    return celsius_to_kelvin(farenheit_to_celsius(farenheit))

