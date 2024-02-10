import mysql.connector
from datetime import datetime
from mysql.connector import Error


# Check connection
# Connect and disconnect for privacy
# Save models to database
# Read model from database
# Add model results to database
# Read results from database


class ModelDA:
    def connect(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="dlws")
        self.cursor = self.db.cursor()

    def disconnect(self, commit=False):
        if commit:
            self.db.commit()
        self.cursor.close()
        self.db.close()

    def check_connection(self):
        try:
            self.db = None
            self.connect()
            print("MySQL Database connection successful")
        except Error as e:
            print(f"The error '{e}' occurred!")
        return self.db

    def save_model_to_db(self, model):
        self.connect()
        self.cursor.execute("insert into item_table (rec_time) values (%s)", [car.rec_time])
        self.cursor.execute("select code from item_table order by code desc limit 1")
        code = self.cursor.fetchone()
        self.cursor.execute(
            "insert into car_item (code, rec_time, car_name, model, color, plate) values (%s,%s, %s, %s, %s, %s)",
            [code[0], car.rec_time, car.name, car.model, car.color, car.plate])
        self.disconnect(commit=True)

    def add_person_item(self, person):
        self.connect()
        self.cursor.execute("insert into item_table (rec_time) values (%s)", [person.rec_time])
        self.cursor.execute("select code from item_table order by code desc limit 1")
        code = self.cursor.fetchone()
        self.cursor.execute(
            "insert into person_item (code, rec_time, first_name, last_name, national_code, phone) "
            "values (%s, %s, %s, %s, %s, %s)",
            [code[0], person.rec_time, person.first_name, person.last_name, person.national_code, person.phone])
        self.disconnect(commit=True)

    def add_object_item(self, object):
        self.connect()
        self.cursor.execute("insert into item_table (rec_time) values (%s)", [object.rec_time])
        self.cursor.execute("select code from item_table order by code desc limit 1")
        code = self.cursor.fetchone()
        self.cursor.execute("insert into object_item(code, rec_time,  object_name, count) values (%s, %s, %s, %s)",
                            [code[0], object.rec_time, object.name, object.count])
        self.disconnect(commit=True)

    def remove_item(self, code):
        self.connect()
        self.cursor.execute("delete from item_table where code= %s", [code])
        self.cursor.execute("delete from car_item where code= %s", [code])
        self.cursor.execute("delete from person_item where code= %s", [code])
        self.cursor.execute("delete from object_item where code= %s", [code])
        self.disconnect(commit=True)

    def find_all(self):
        self.connect()
        self.cursor.execute("select * from item_table")
        ilist = self.cursor.fetchall()
        self.disconnect()
        item_list = []
        if ilist:
            for i in ilist:
                item = Item(*i)
                item_list.append(item)
            return item_list

    def recognizer(self, code):
        self.connect()
        self.cursor.execute("select * from car_item where code= %s", [code])
        car_item = self.cursor.fetchone()
        self.cursor.execute("select * from person_item where code= %s", [code])
        person_item = self.cursor.fetchone()
        self.cursor.execute("select * from object_item where code= %s", [code])
        object_item = self.cursor.fetchone()
        self.disconnect()
        if car_item:
            return "car"
        elif person_item:
            return "person"
        elif object_item:
            return "object"
        else:
            return "None"

    def find_by_code(self, code):
        recognizer = self.recognizer(code)
        self.connect()
        match recognizer:
            case "person":
                self.cursor.execute("select * from person_item where code=%s", [code])
                item = self.cursor.fetchone()
                self.disconnect()
                return "person", item
            case "car":
                self.cursor.execute("select * from car_item where code=%s", [code])
                item = self.cursor.fetchone()
                self.disconnect()
                return "car", item
            case "object":
                self.cursor.execute("select * from object_item where code=%s", [code])
                item = self.cursor.fetchone()
                self.disconnect()
                return "object", item
            case "None":
                self.disconnect()
                return "None"

    def find_by_car_plate(self, plate):
        self.connect()
        self.cursor.execute("select * from car_item where plate=%s", [plate])
        clist = self.cursor.fetchall()
        self.disconnect()
        return clist

    def find_by_object_name(self, name):
        self.connect()
        self.cursor.execute("select * from object_item where object_name= %s", [name])
        olist = self.cursor.fetchall()
        self.disconnect()
        return olist

    def find_by_person_name(self, name):
        self.connect()
        # todo: both first and last name should be covered!!
        self.cursor.execute("select * from person_item where first_name= %s ", [name])
        plist = self.cursor.fetchall()
        self.disconnect()
        return plist

    def find_by_time(self, time):
        self.connect()
        self.cursor.execute("select * from item_table where time=%s", [datetime.strptime(time, "%Y-%m-%d %H-%M-%S")])
        item_find = self.cursor.fetchone()
        item = Item(*item_find)
        self.disconnect()
        self.find_by_code(item.code)



