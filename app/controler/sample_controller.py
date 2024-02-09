from model.da.item.item_da import ItemDA
from model.entity.item import *
from controller.tools.validator import *


# todo: add correct message to errors

class ItemController:
    @classmethod
    def add_car_item(self, code, name, model, color, plate, rec_time):
        try:
            item_da = ItemDA()
            car = Car(name, model, plate, color, 0, rec_time)
            item_da.add_car_item(car)
            return True, car
        except Exception as e:
            return False, e

    @classmethod
    def add_person_item(self, code, first_name, last_name, national_code, phone, rec_time):
        try:
            item_da = ItemDA()
            person = Person(first_name, last_name, national_code, phone, 0, rec_time)
            item_da.add_person_item(person)
            return True, person
        except Exception as e:
            return False, e

    @classmethod
    def add_object_item(self, code, count, name, rec_time):
        try:
            item_da = ItemDA()
            object = Object(name, count, 0, rec_time)
            item_da.add_object_item(object)
            return True, object
        except Exception as e:
            return False, e

    @classmethod
    def remove_item(self, code):
        try:
            if code_validator(code):
                item_da = ItemDA()
                item = item_da.find_by_code(code)
                if item:
                    item_da.remove_item(code)
                    return True, item
                else:
                    return ("There is no item with this code.")
            else:
                raise ValueError("Invalid Code")
        except Exception as e:
            return False, "Error" + str(e)

    @classmethod
    def find_all(self):
        try:
            item_da = ItemDA()
            return True, item_da.find_all()
        except Exception as e:
            return False, "Error" + str(e)

    @classmethod
    def find_by_code(self, code):
        try:
            if code_validator(code):
                item_da = ItemDA()
                return True, item_da.find_by_code(code)
            else:
                raise ValueError("Invalid Code")
        except Exception as e:
            return False, "Error" + str(e)

    @classmethod
    def find_by_person_name(self, name, exact=True):
        try:
            if name_validator(name):
                item_da = ItemDA()
                if exact:
                    return True, item_da.find_by_person_name(name)
                else:
                    return True, item_da.find_by_person_name("%" + name + "%")
            else:
                raise ValueError("Invalid Code")
        except Exception as e:
            return False, "Error" + str(e)

    @classmethod
    def find_by_car_plate(self, plate):
        try:
            if plate_validator(plate):
                item_da = ItemDA()
                return True, item_da.find_by_car_plate(plate)
            else:
                raise ValueError("Invalid Code")
        except Exception as e:
            return False, "Error" + str(e)

    @classmethod
    def find_by_object_name(self, name, exact=True):
        try:
            if object_name_validator(name):
                item_da = ItemDA()
                if exact:
                    return True, item_da.find_by_object_name(name)
                else:
                    return True, item_da.find_by_object_name("%" + name + "%")
            else:
                raise ValueError("Invalid Code")
        except Exception as e:
            return False, "Error" + str(e)

    @classmethod
    def find_by_time(self, time):
        try:
            if time_validator(time):
                item_da = ItemDA()
                return True, item_da.find_by_time(time)
            else:
                raise ValueError("Invalid Code")
        except Exception as e:
            return False, "Error" + str(e)

#
# item_controller = ItemController()
# print(item_controller.add_car_item(23, "azera", "fr90  ", "red", "12d23455", "sfdg546"))
# print(item_controller.add_object_item(45, "45", "siman", "324"))
# print(item_controller.add_person_item(4, "mahd iar", "man souri", "0022667441", "09123123121", "34"))
# print(item_controller.remove_item(42))
# print(item_controller.find_by_code(100))
