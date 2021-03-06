"""
Simple Neural Network EA with training by numeric reward.
"""
import pickle
import numpy as np
import random

def mlp_build(shape):
    """
    Multi-layer perceptron.
    shape: (input_size, [hidden_sizes], output_size)
    """
    nn = {'score': 0, 'model': [], 'scored': False}
    for i in range(len(shape)-1):
        W = np.random.randn(shape[i], shape[i+1]) / np.sqrt(shape[i])
        b = np.zeros((1, shape[i+1]))
        nn['model'].append((W,b))
        
    return nn
    
def mlp_predict(nn, x, activation=np.tanh):
    """
    Generate prediction on given neural net.
    """
    z = None
    cur_input = x
    for layer in nn['model']:
        W, b = layer
        z = cur_input.dot(W) + b
        cur_input = activation(z)
        
    exp_scores = np.exp(cur_input)
    probs = np.exp(exp_scores) / np.sum(exp_scores, axis=1, keepdims=True)
    return np.argmax(probs)

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
    exp_scores = np.exp(a2)
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
    new_nn = {'score': 0, 'scored': False}
    new_model = []
    for layer in nn['model']:
        W, b = layer
        new_model.append((mutate(W), mutate(b)))
    new_nn['model'] = new_model
    return new_nn

def select(pop, max_score=5):
    """
    Select from `pop` and return next population.
    """
    scores = [nn['score'] for nn in pop]
    N = np.sum([np.exp(nn['score']) for nn in pop])
    fitnesses = [np.exp(nn['score'])/N for nn in pop]
    children = np.random.choice(pop, size=len(pop), replace=True, p=fitnesses)
    return [replicate(c) for c in children]

def avg_score(pop):
    scores = [nn['score'] for nn in pop]
    return (np.mean(scores), np.std(scores))
def dump_state(pops, pickle_path):
    pickle.dump(pops, open(pickle_path, "wb"))

def load_state(pickle_path):
    return pickle.load(open(pickle_path, "rb"))

def query_predict(x, pickle_path):
    """
    Pick an nn that has not been tested and produce a prediction.
    If all have been tested, create next generation and produce prediction.
    """
    pops = load_state(pickle_path)
    current_pop = pops[-1]
    #if we find an untested NN in current gen, get prediction
    for i, nn in enumerate(current_pop):
        if nn['scored'] == False:
            return (mlp_predict(nn, x), i)
    #else, get new gen and get prediction
    with open("static/fitness.csv", "a+") as fit:
        fit.write(f"{len(pops)},{avg_score(current_pop)[0]}\n")
    next_gen = select(current_pop) 
    pops.append(next_gen)
    ind, test_nn = random.choice(list(enumerate(next_gen)))
    dump_state(pops, pickle_path)
    return (mlp_predict(test_nn, x), ind)

def update_EA(score, index, pickle_path):
    """
    Store the score of an nn at the current generation and dump to pickle.
    """
    pops = load_state(pickle_path)
    current_pop = pops[-1]
    current_pop[index]['score'] = score
    current_pop[index]['scored'] = True 
    dump_state(pops, pickle_path)
    mean, std = avg_score(current_pop)
    gen = len(pops) - 1 
    return mean, std, gen

def genesis(shape, pickle_path, popsize=20):
    """
    Make first generation
    """
    pops = [[mlp_build(shape) for _ in range(popsize)]]
    dump_state(pops, pickle_path)
    pass

def ea(shape, popsize=20):
    """
    Main loop of EA, used to interface with user feedback and update model.
    """
    nn_ind = 0
    pop = [mlp_build(shape) for _ in range(popsize)]
    gen = 0
    while True:
        if nn_ind == len(pop):
            nn_ind = 0
            pop = select(pop)
            gen += 1
            print(f"NEWGEN: {gen}")
        # get input vector
        x = yield
        pred = mlp_predict(pop[nn_ind], x)
        #for now yield 1
        yield pred 
        # yield pred
        score = yield
        pop[nn_ind]['score'] = score
        nn_ind += 1
        sc = avg_score(pop)
        yield (gen, sc)
        # update_EA(score, nn_ind)

def test_ea(shape):
    g = ea(shape)
    next(g)
    for _ in range(100):
        query = np.array(np.random.randn((shape[0])))
        pred = g.send(query)
        print(pred)
        next(g)
        score = 1.2
        sc = g.send(score)
        print(sc)
        next(g)
        # print(sc)
        
def pickle_test(pickle_path):
    genesis((10, 14, 3))
    for _ in range(10):
        for _ in range(20):
            cur_gen = load_state(pickle_path)[-1]
            p, ind = query_predict(np.zeros((10)))
            update_EA(random.randint(0, 6), ind)
        
if __name__ == "__main__":
    # in_dim = 2
    # out_dim = 1
    # hidden_dim = 5
    # x = [1, 2]
    # pop = [nn_create(in_dim, out_dim, hidden_dim) for _ in range(100)]
    # print(predict(nn_create(2, 2, 3), x))
    # test_ea()
    # mlp = mlp_build((50, 20, 20, 10))
    # print(mlp)
    # print(mlp_predict(mlp, np.array(np.zeros((50)))))
    # test_ea((50, 20, 20, 10))
    genesis((15,10,6), "static/ea_SO.pickle")
    genesis((50,28,6),"static/ea_glove.pickle")
    pass
