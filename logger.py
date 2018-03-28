import numpy as np
import logging

def log_gen():
    trainlog = logging.getLogger('myapp')
    hdlr = logging.FileHandler('training.log')
    trainlog.addHandler(hdlr)
    trainlog.setLevel(logging.INFO)
    while True:
        query, parse, embed, plotpath = yield

        query = query.strip()
        parse = str(parse).strip() 
        embed = np.array_repr(embed).replace('\n', '')
        plotpath = plotpath.strip()
        
        # trainlog.info(",".join([query, str(parse), str(embed), plotpath]))
        score = yield
        score = str(score).strip()
        logstring = ",".join([parse, embed, plotpath, score]) + "\n"
        logstring = "".join(logstring.split()) + "," +  query.strip() + "\n"
        trainlog.info(logstring)
if __name__ == "__main__":
    g = log_gen()
    next(g)
    g.send(('a', 'b', 'c', 'd'))
    g.send('s')
