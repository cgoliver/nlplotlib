"""
Simple Neural Network EA with training by numeric reward.
"""
import pickle
import numpy as np

def nn_create(in_dim, out_dim, hidden_dim):
    """
    Create single layer neural network.
    """ 
    W1 = np.random.randn(in_dim, hidden_dim) / np.sqrt(in_dim)
    b1 = np.zeros((1, hidden_dim))
    W2 = np.random.randn(hidden_dim, out_dim) / np.sqrt(hidden_dim)
    b2 = np.zeros((1, out_dim))

    return {'W1': W1, 'b1': b1, 'W2': W2, 'b2':b2, 'tested': 0, 'score': 0}

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

def select(pop):
    """
    Select from `pop` and return next population.
    """
    scores = [nn['score'] for nn in pop]
    fitnesses = scores / np.sum(scores)
    children = np.random.choice(pop, size=len(pop), replace=True, p=fitnesses)
    return [replicate(c) for c in children]

def dump_state(pops):
    pickle.dump(pops, open("static/EA.pickle", "wb"))

def load_state():
    return pickle.load(open("static/EA.pickle", "rb"))

def query_predict(x, pops):
    """
    Pick an nn that has not been tested and produce a prediction.
    If all have been tested, create next generation and produce prediction.
    """
    pops = load_state()
    current_pop = pops[-1]
    #if we find an untested NN in current gen, get prediction
    for i, nn in enumerate(current_pop):
        if nn['tested'] == 0:
            return predict(nn, x)
    #else, get new gen and get prediction
    next_gen = select(current_pop) 
    pops.append(next_gen)
    test_nn, index = random.choice(enumerate(next_gen))
    dump_state(pops)
    return (predict(test_nn, x), index)

def update_EA(score, index):
    """
    Store the score of an nn at the current generation and dump to pickle.
    """
    pops = load_state()
    current_pop = pops[-1]
    current_pop[index]['score'] = score
    dump_state(pops)
    return 0

def ea():
    """
    Main loop of EA, used to interface with user feedback and update model.
    """
    in_dim = 2
    out_dim = 1
    hidden_dim = 5
    nn_ind = 0
    pop = [nn_create(in_dim, out_dim, hidden_dim) for _ in range(100)]
    while True:
        if nn_ind == len(pop):
            nn_ind = 0
            pop = select(pop)
        # get input vector
        x = yield
        pred = predict(pop[nn_ind], x)
        #for now yield 1
        yield 1
        # yield pred
        score = yield
        pop[nn_ind]['score'] = score
        # update_EA(score, nn_ind)
        nn_ind += 1

def test_ea():
    g = ea()
    next(g)
    query = np.array([2, 2])
    pred = g.send(query)
    next(g)
    score = 1.2
    g.send(score)
    
if __name__ == "__main__":
    in_dim = 2
    out_dim = 1
    hidden_dim = 5
    x = [1, 2]
    pop = [nn_create(in_dim, out_dim, hidden_dim) for _ in range(100)]
    # print(predict(nn_create(2, 2, 3), x))
    test_ea()
    pass
