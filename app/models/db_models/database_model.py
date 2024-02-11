import pickle
import mysql.connector
from mysql.connector import Error
from app.models.dl_models.dl_models import BaseModel


class ModelDA:
    def connect(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="dlws",
            ssl_disabled=True)
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
        self.cursor.execute("insert into model_storage (model_name, model_structure, pretrained) values (%s, %s, %s)",
                            [model.name, model.structure, model.pretrained])
        self.disconnect(commit=True)

    def add_model_result(self, result):
        pass

    #     self.connect()
    #     self.cursor.execute("insert into item_table (rec_time) values (%s)", [person.rec_time])
    #     self.cursor.execute("select code from item_table order by code desc limit 1")
    #     code = self.cursor.fetchone()
    #     self.cursor.execute(
    #         "insert into person_item (code, rec_time, first_name, last_name, national_code, phone) "
    #         "values (%s, %s, %s, %s, %s, %s)",
    #         [code[0], person.rec_time, person.first_name, person.last_name, person.national_code, person.phone])
    #     self.disconnect(commit=True)

    def remove_model(self, code):
        self.connect()
        self.cursor.execute("delete from model_storage where id= %s", [id])
        self.disconnect(commit=True)

    def find_all(self):
        self.connect()
        self.cursor.execute("select * from model_storage")
        ilist = self.cursor.fetchall()
        self.disconnect()
        model_list = []
        if ilist:
            for i in ilist:
                model = BaseModel(*i)
                model_list.append(model)
            return model_list

    def find_by_id(self, id):
        self.connect()
        self.cursor.execute("select * from model_storage where id=%s", [id])
        model = self.cursor.fetchone()
        self.disconnect()
        model = BaseModel(model.model_name, model.architecture, model.weights)
        return model

    def find_by_model_name(self, name):
        self.connect()
        self.cursor.execute("select model_name, model_structure, pretrained from model_storage where model_name= %s", [name])
        model = self.cursor.fetchone()
        self.disconnect()
        if model is not None:
            model_name, model_structure, pretrained_flag = model
            # Return pretrained_flag value from 0 & 1 to boolean for actual pretrained value
            if pretrained_flag == 1:
                pretrained = True
            else:
                pretrained = False
            architecture = pickle.loads(model_structure)
            return BaseModel(model_name, architecture, pretrained)
        else:
            return None

    def load_model_from_db(self, model_name):
        self.connect()
        self.cursor.execute("SELECT * FROM model_storage WHERE model_name = %s", (model_name,))
        row = self.cursor.fetchone()
        self.disconnect()

        if row:
            architecture_blob, weights_blob = row
            model = pickle.loads(architecture_blob)
            model.load_state_dict(pickle.loads(weights_blob))
            return model
        else:
            raise ValueError(f"Model with name {model_name} not found in database.")
