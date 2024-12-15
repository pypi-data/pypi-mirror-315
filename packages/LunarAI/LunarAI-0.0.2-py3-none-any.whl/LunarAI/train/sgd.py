#SGD
from LunarAI.loss.loss import *

class SGD:
    def __init__(self, learning_rate=0.01, loss_function = mean_squared_error) -> None:
        self.learning_rate = learning_rate
        self.loss = loss_function
        return None
    def __update(self, params, grid) -> None:
        for key in params.keys():
            params[key] -= ( self.learning_rate * grid[key] )
            continue
        return None
    def __call__(self, x_train, y_train, model):
        P = model(x_train)
        L = self.loss(y_train,P)
        print(f'loss={L}')
        params , grid = {} , {}
        for i in range(len(model.net)):
            i -= len(model.net)
            deda = self.loss.deda(P)
            dadz = model.net[i].a.dadz(model.net[i].Z)
            for neuron in range(model.net[i].size):
                dedz = deda[neuron]*dadz[neuron]
                for p in model.net[i].params.keys():
                    dzdp = model.net[i].d[p]()
                    dedp = dedz * dzdp
                    params[p] = model.net[i].params[p]
                    grid[p] = dedp
                    self.__update(params,grid)
                    continue
                continue
            continue
        return None