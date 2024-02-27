import pickle
import mysql.connector
from mysql.connector import Error
from app.models.dl_models.dl_models import BaseModel, Result


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
        self.cursor.execute("insert into model_storage (model_name, model_path, pretrained) values (%s, %s, %s)",
                            [model.name, model.path, model.pretrained])
        self.disconnect(commit=True)

    def add_model_result(self, result):
        self.connect()
        self.cursor.execute("insert into model_training_results (model_name, epoch_nums, batch_size, pretrained,"
                            " output_classes, feature_method, optimizer, loss_func, learning_rate, train_acc_list,"
                            " val_acc_list, train_loss_list, val_loss_list)"
                            " values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            [result.model_name, result.epoch_nums, result.batch_size, result.pretrained,
                             result.output_classes, result.feature_method, result.optimizer, result.loss_function,
                             result.learning_rate, str(result.train_acc_list), str(result.val_acc_list), str(result.train_loss_list),
                             str(result.val_loss_list)])
        self.disconnect(commit=True)

    def read_result(self, id):
        self.connect()
        self.cursor.execute("select * from model_training_results where id = %s", [id])
        result = self.cursor.fetchall()
        self.disconnect()
        # result = Result(result.model_name)
        return result

    def remove_model(self, code):
        self.connect()
        self.cursor.execute("delete from model_storage where id= %s", [id])
        self.disconnect(commit=True)

    def get_model_names(self):
        self.connect()
        self.cursor.execute("select model_name from model_storage where pretrained= %s", [0])
        model_names = self.cursor.fetchall()
        self.disconnect()
        return model_names

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
        model = BaseModel(model.model_name, model.model_path, model.pretrained)
        return model

    def find_by_model_name(self, model_name):
        self.connect()
        self.cursor.execute("select model_name, model_path, pretrained from model_storage where model_name= %s",
                            [model_name])
        models = self.cursor.fetchall()
        self.disconnect()
        return models

    def find_by_model_name_pretrained(self, model_name, pretrained):
        self.connect()
        self.cursor.execute(
            "select model_name, model_path, pretrained from model_storage where model_name= %s and pretrained=%s",
            [model_name, pretrained])
        model = self.cursor.fetchone()
        self.disconnect()
        return model

# model_da = ModelDA()
# model = model_da.find_by_model_name('alexnet')
# print(model)
