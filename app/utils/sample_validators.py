import re


# todo: add persian to validator


def name_validator(name):
    return bool(re.match("[A-Za-z\s]+$", name))


# def last_name_validator(last_name):
#     return bool(re.match("[A-Za-z]+$", last_name))


def national_code_validator(national_code):
    return bool(re.match("[0-9]{10}$", national_code))


def time_validator(time):
    return True


# todo: insert datetime type for birth-date validator and register date

def birth_date_validator(birth_date):
    return bool(re.match("[0-9/]{10}$", birth_date))


def register_date_validator(register_date):
    return bool(re.match("[0-9/]{10}$", register_date))


def phone_validator(phone):
    return bool(re.match("[0-9]{11}$", phone))


def user_name_validator(user_name):
    return bool(re.match("[A-Za-z0-9]+$", user_name))


def password_validator(password):
    return bool(re.match("[A-Za-z0-9@*]+$", password))


def access_level_validator(access_level):
    return bool(re.match("[01]{4}$", access_level))


def id_number_validator(id_number):
    return type(id_number) == int and id_number > 0


def code_validator(code):
    return type(code) == int and code > 0


def car_name_validator(car_name):
    return bool(re.match("[A-Za-z0-9\s]+$", car_name))


def model_validator(model):
    return bool(re.match("[A-Za-z0-9\s]+$", model))


def color_validator(color):
    return bool(re.match("[A-Za-z\s]+$", color))


def plate_validator(plate):
    return bool(re.match("^[0-9]{2}\s?[A-Za-z]\s?[0-9]{3}\s?[0-9]{2}$", plate))


def object_name_validator(object_name):
    return bool(re.match("[A-Za-z0-9\s]+$", object_name))


def count_validator(count):
    return bool(re.match("[0-9.]+$", count))

# TEST !!1

# print(model_validator("azera 2008 er 45"))
# print(plate_validator("23 e 123 44"))
# print(car_name_validator("azera 2008"))
# print(code_validator(6))
# print(time_validator("34"))
# print(national_code_validator("0022667441"))
# print(access_level_validator("1110"))
# print(birth_date_validator("1378/23/23"))
# print(name_validator("hamed"))