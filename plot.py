import matplotlib.pyplot as plt
from app.models.db_models.database_model import ModelDA

model_da = ModelDA()
result = model_da.read_result(21)
train_acc = eval(result[0][10])
val_acc = eval(result[0][11])
train_loss = eval(result[0][12])
val_loss = eval(result[0][13])

# train_loss = [x if x < 1 else 0.7 for x in train_loss]

plt.title(result[0][1])
plt.plot(train_acc, label='train Acc')
plt.plot(val_acc, label='val Acc')
plt.plot(train_loss, label='train loss')
plt.plot(val_loss, label='val loss')
plt.legend()
plt.show()