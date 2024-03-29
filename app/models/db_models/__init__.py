import time

import mysql.connector
from mysql.connector import Error


def create_database_connection(host_name, user_name, user_password, database_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=database_name
        )
        print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def check_table_exists(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchone()
    if result:
        print(f"Table '{table_name}' exists")
        return True
    else:
        return False


def create_table(connection, create_table_sql):
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_sql)
        print("Table created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# database information
host_name = "localhost"
user_name = "root"
user_password = "root123"
database_name = "dlws"

# SQL command to create tables
create_model_storage_table = """
CREATE TABLE model_storage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    model_path VARCHAR(300) NOT NULL, 
    pretrained TINYINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);
"""

create_model_results_table = """
CREATE TABLE model_training_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(100),
    dataset_name VARCHAR(100),
    epoch_nums INT,
    batch_size INT,
    pretrained TINYINT,
    output_classes INT,
    feature_method VARCHAR(100),
    optimizer VARCHAR(100),
    loss_func VARCHAR(100),
    learning_rate FLOAT,
    train_acc_list TEXT,
    val_acc_list TEXT,
    train_loss_list TEXT,
    val_loss_list TEXT,
    running_time FLOAT(4, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);
"""

# Connect to the Database
connection = create_database_connection(host_name, user_name, user_password, database_name)

# Check if Tables Exists, and Create them if Not
if connection is not None:
    if not check_table_exists(connection, "model_storage"):
        create_table(connection, create_model_storage_table)
    if not check_table_exists(connection, "model_results"):
        create_table(connection, create_model_results_table)
    connection.close()
else:
    print("Failed to connect to the database")
