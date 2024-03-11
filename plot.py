import matplotlib.pyplot as plt
import numpy as np

from app.models.db_models.database_model import ModelDA
from datetime import datetime


def plot_results(id):
    model_da = ModelDA()
    result = model_da.read_result(id)
    result = result[0]
    print(result)
    title = result[1]
    train_acc = eval(result[11])
    val_acc = eval(result[12])
    train_loss = eval(result[13])
    val_loss = eval(result[14])

    # val_acc = [x if x > 0.6 else 0.6 for x in val_acc]

    plt.title(title)
    plt.plot(train_acc, label='train Acc')
    plt.plot(val_acc, label='val Acc')
    plt.plot(train_loss, label='train loss')
    plt.plot(val_loss, label='val loss')
    plt.legend()
    plt.show()

plot_results(18)

# for i in range(5, 9):
#     print(i)
#     plot_results(i)