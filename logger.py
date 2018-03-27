import logging

def log_gen():
    trainlog = logging.getLogger('myapp')
    hdlr = logging.FileHandler('training.log')
    trainlog.addHandler(hdlr)
    trainlog.setLevel(logging.INFO)
    while True:
        query, parse, embed, plotpath = yield
        # trainlog.info(",".join([query, str(parse), str(embed), plotpath]))
        score = yield
        trainlog.info(",".join([query, str(parse), str(embed), plotpath,\
            str(score)]))
if __name__ == "__main__":
    g = log_gen()
    next(g)
    g.send(('a', 'b', 'c', 'd'))
    g.send('s')
