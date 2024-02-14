'''
as input:

model name
params
feature method
dataset
-------
as process:

load model
train model
evaluate model
save results
------
as output:

show results
show model and params
'''

from view.main_view_structure import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
