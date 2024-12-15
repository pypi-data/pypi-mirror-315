import LunarAI as ai
from random import randint

model = ai.model.Model()
model.add(ai.layers.layer.Layer(size = 20, inputs = 1))
model.add(ai.layers.layer.Layer(size = 3, inputs = 20))
model.add(ai.layers.layer.Layer(size = 10, inputs = 3, activation = ai.sigmoid))
print(model(ai.ai_libs.array_type.Array([[23424234]])))

def get(n):
    x_train, y_train = [],[]
    for i in range(n):
        x = randint(-100,100)
        x_train.append([x])
        if (x >= 10) or (x <= -10):
            y = 0
        else:
            y = 1
        y_train.append([y])
        continue
    return x_train, y_train
        

print('\n\n\n\nPress Ctrl+C to quit...')
while True:
    try:
        pass
    except:
        exit()
