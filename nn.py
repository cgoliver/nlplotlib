"""
Simple Neural Network EA with training by numeric reward.
"""
import numpy as np

def nn_create(in_dim, out_dim, hidden_dim):
    """
    Create single layer neural network.
    """ 
    W1 = np.random.randn(in_dim, hidden_dim) / np.sqrt(in_dim)
    b1 = np.zeros((1, hidden_dim))
    W2 = np.random.randn(hidden_dim, out_dim) / np.sqrt(hidden_dim)
    b2 = np.zeros((1, out_dim))

    return {'W1': W1, 'b1': b1, 'W2': W2, 'b2':b2}

def predict(nn,x, activation=np.tanh):
    """
    Forward propagation of NN to get prediction on input x.
    """
    W1, b1, W2, b2 = nn['W1'], nn['b1'], nn['W2'], nn['b2']
    z1 = x.dot(W1) + b1
    a1 = activation(z1)
    z2 = a1.dot(W2) + b2
    a2 = activation(z2)
    exp_scores = np.exp(z2)
    probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
    return np.argmax(probs, axis=1)

def pop_create(in_dim, out_dim, hidden_dim, pop_size):
    """
    Create population of networks.
    """
    return [nn_create(in_dim, out_dim, hidden_dim) for _ in range(pop_size)]

def score(pred):
    """
    Return score of prediction.
    """
    return 1

def mutate(param, sigma=0.25):
    """
    Shift parameters with by N(0, sigma)
    """
    mut_array = sigma * np.random.randn(*param.shape)
    return param + mut_array

def replicate(nn):
    """
    Return the child of `nn` with weights shifted by Gaussian noise.
    """
    for param in nn:
        nn[param] = mutate(param)
    return nn

def select(pop, xs):
    """
    Select from `pop` and return next population.
    """
    scores = [score(predict(nn, x) for nn,x in zip(pop, xs)]
    fitnesses = scores / np.sum(scores)
    pass
if __name__ == "__main__":
    in_dim = 2
    out_dim = 1
    hidden_dim = 5
    pop = [nn_create(in_dim, out_dim, hidden_dim) for _ in range(100)]
    print(predict(nn_create(2, 2, 3), x))
    pass
