###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                    Optimizers                               #
#                                                                             #
###############################################################################
"""From here the optimizer Eve can be loaded.

Which is an implementation from:

Paper
https://arxiv.org/pdf/1611.01505v1.pdf

Code
https://github.com/rooa/eve
"""

# Packages
###############################################################################

# Deeplearning tools imports
import keras.backend as K
from keras.optimizers import Optimizer

# Data tools imports
import numpy as np

# Eve
###############################################################################


def fmin_pos(dtype):
    """Return the smallest positive number representable
    in the given data type.
    Arguments:
        dtype: a numpy datatype like "float32", "float64" etc.
    """
    return np.nextafter(np.cast[dtype](0), np.cast[dtype](1))


def fmin_pos_floatx():
    """Return the smallest positive number representable
    using the Keras floatX data type.
    """
    return fmin_pos(K.floatx())


class Eve(Optimizer):

    """Eve optimizer.
    Arguments:
        lr: float > 0. Learning rate.
        beta_1: float in (0, 1). Decay rate for first moment estimate.
        beta_2: float in (0, 1). Decay rate for second moment estimate.
        beta_3: float in (0, 1). Decay rate for Eve coefficient.
        c: float > 0. Clipping parameter for Eve.
        epsilon: float > 0. Fuzz factor.
        decay: float > 0. Learning rate linear decay rate.
        loss_min: float. Minimum of the loss function.
    """

    def __init__(
        self,
        lr=0.001,
        beta_1=0.9,
        beta_2=0.999,
        beta_3=0.999,
        c=10.,
        epsilon=1e-8,
        decay=0.,
        loss_min=0.,
        **kwargs
    ):
        super(Eve, self).__init__(**kwargs)
        self.iterations = K.variable(0)
        self.lr = K.variable(lr)
        self.beta_1 = K.variable(beta_1)
        self.beta_2 = K.variable(beta_2)
        self.beta_3 = K.variable(beta_3)
        self.c = c  # K.variable(c)
        self.epsilon = K.variable(epsilon)
        self.decay = K.variable(decay)
        self.loss_min = K.variable(loss_min)
        self.fmin_pos = K.variable(fmin_pos_floatx())
        self.d_num = K.variable(0)
        self.d_den = K.variable(0)
        self.d = K.variable(0)
        self.lr_eff = K.variable(0)

    def get_updates(self, params, constraints, loss):
        grads = self.get_gradients(loss, params)

        self.updates = [K.update_add(self.iterations, 1)]
        t = self.iterations + 1

        shapes = [K.get_variable_shape(p) for p in params]
        ms = [K.zeros(shape) for shape in shapes]
        vs = [K.zeros(shape) for shape in shapes]

        loss_prev = K.variable(0)
        self.updates.append(K.update(loss_prev, loss))

        # Calculate the numerator of the Eve coefficient
        d_num_t = K.abs(loss_prev - loss)
        self.updates.append(K.update(self.d_num, d_num_t))

        # Calculate the denominator of the Eve coefficient
        d_den_t = K.abs(K.minimum(loss_prev, loss) - self.loss_min)
        self.updates.append(K.update(self.d_den, d_den_t))

        # Calculate the Eve coefficient. At the first iteration, it is 1.
        d_tilde_t = K.clip(
            (d_num_t + self.fmin_pos) / (d_den_t + self.fmin_pos),
            1. / self.c,
            self.c,
        )
        d_t = (self.beta_3 * self.d) + (1. - self.beta_3) * d_tilde_t
        d_t = K.switch(K.greater(t, 1), d_t, K.constant(1))
        self.updates.append(K.update(self.d, d_t))

        # Calculate the effective learning rate as lr / (d * decay)
        lr_eff_t = self.lr / (d_t * (1. + (self.iterations * self.decay)))
        self.updates.append(K.update(self.lr_eff, lr_eff_t))

        # Apply bias correction to the learning rate
        lr_hat_t = (
            lr_eff_t
            * K.sqrt(1. - K.pow(self.beta_2, t))
            / (1. - K.pow(self.beta_1, t))
        )

        # Update per parameter
        for p, g, m, v in zip(params, grads, ms, vs):
            m_t = (self.beta_1 * m) + (1. - self.beta_1) * g
            self.updates.append(K.update(m, m_t))

            v_t = (self.beta_2 * v) + (1. - self.beta_2) * K.square(g)
            self.updates.append(K.update(v, v_t))

            p_t = p - lr_hat_t * m_t / (K.sqrt(v_t) + self.epsilon)
            new_p = p_t
            # Apply constraints
            if p in constraints:
                c = constraints[p]
                new_p = c(new_p)
            self.updates.append(K.update(p, new_p))
        return self.updates

    def get_config(self):
        config = {
            "lr": float(K.get_value(self.lr)),
            "beta_1": float(K.get_value(self.beta_1)),
            "beta_2": float(K.get_value(self.beta_2)),
            "beta_3": float(K.get_value(self.beta_3)),
            "c": float(K.get_value(self.c)),
            "epsilon": float(K.get_value(self.epsilon)),
            "decay": float(K.get_value(self.decay)),
            "loss_min": float(K.get_value(self.loss_min)),
        }
        base_config = super(Eve, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))
