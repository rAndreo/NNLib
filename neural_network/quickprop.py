import numpy as np
from optimizer import Optimizer


class Quickprop(Optimizer):
    """
    Quickpropagation optimizer.
        method(str) - declares that the optimizer is a Quickprop optimizer
        lr(float) - current value of learning rate
        lr_init(float) - initial value of learning rate
        prev_updates(list) - takes trace of the weights update at the previous iteration
        prev_gradients(list) - takes trace of the gradients at the previous iteration
        lr_sched(str) -  the technique of the learning rate's update
    """
    def __init__(self, lr_init=0.1, lr_sched=None):
        super(Quickprop, self).__init__()
        self.method = 'Quickprop'
        self.lr = lr_init
        self.lr_init = lr_init
        self.lr_sched = lr_sched
        self.prev_updates = None
        self.prev_gradients = None

    def init_optimizer(self, layers):
        """
        Prepares the additional informations of the optimizer.
        :param layers: layers of the neural network.
        """
        self.prev_updates = [(np.ones(layer.d_weights.shape),
                             (np.ones(layer.d_bias.shape))) for layer in layers]
        self.prev_gradients = [(np.random.uniform(low=-0.001, high=0.001, size=layer.d_weights.shape),
                               (np.random.uniform(low=-0.001, high=0.001, size=layer.d_bias.shape))) for layer in layers]

    def weights_update(self, w_grad, bias_grad):
        """
        Function for the weight update by Quickpropagation.
        :param w_grad: weights' current gradient
        :param bias_grad: bias current gradient
        :return: the value for the weights and bias update by Quickpropagation
        """
        prev_up_weights, prev_up_bias = self.prev_updates.pop(0)
        prev_g_weights, prev_g_bias = self.prev_gradients.pop(0)
        w_update = self.lr * (prev_up_weights * (w_grad / (prev_g_weights - w_grad)))
        bias_update = self.lr * (prev_up_bias * (bias_grad / (prev_g_bias - bias_grad)))
        self.prev_updates.append((w_update, bias_update))
        self.prev_gradients.append((w_grad, bias_grad))
        return w_update, bias_update

    def epoch_change(self, epoch=None):
        """
        Updates the learning rate with the technique described by lr_sched
        :param epoch: current epoch's number
        """
        if self.lr_sched is not None:
            self.lr = self.lr_sched.lr_update((self.lr, self.lr_init), epoch)
        for i in range(len(self.prev_gradients)):
            self.prev_updates[i] = (np.ones(self.prev_updates[i][0].shape),
                                    np.ones(self.prev_updates[i][1].shape))
            self.prev_gradients[i] = (np.random.uniform(low=-0.001, high=0.001, size=self.prev_gradients[i][0].shape),
                                      np.random.uniform(low=-0.001, high=0.001, size=self.prev_gradients[i][1].shape))
