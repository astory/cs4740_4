#Copyright (C) 2007 Roland Memisevic
#
#This program is distributed WITHOUT ANY WARRANTY; without even the implied
#warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#LICENSE file for more details.


from numpy import double, sum, zeros, argmax, newaxis, exp, random, concatenate
from pylab import randn, find
from monte.models.contrastive.contrastive import Contrastive
from monte.models.contrastive.scorefunc import scorefunc
from monte.util import logsumexp, onehot
from monte import train

class Isl(Contrastive):
    """Backprop network with one sigmoid hidden and one linear output layer."""

    def __init__(self,numin,numhid,numout,params=None):
        self.numin  = numin
        self.numhid = numhid
        self.numout = numout
        self.params = params
        if self.params == None:
            self.params = 0.01 * randn(self.numin*self.numhid+self.numhid+\
                                       self.numhid*self.numout+self.numout)
        self.scorefuncs = [scorefunc.SigmoidhiddenLinearoutputScore\
                                       (numin,numhid,numout,self.params)]
        Contrastive.__init__(self,normalizeacrosscliques=False)

    def posdata(self,data):
        return (((data[0],data[1]),),)

    def negdata(self,data):
        return ([],)   #no negdata: scorefunc takes care of it

    def cost(self,data,weightcost):
        if type(data)!=type([]):
            data = [data]
        numcases = len(data)
        cost = 0.0
        for i in range(numcases):
            input = data[i][0]
            desiredoutput = data[i][1]
            output = self.scorefuncs[0](input) #why not use self.apply()?
            if len(input.shape) >= 2:
                cost += sum((output-desiredoutput)**2)/\
                                                double(numcases*input.shape[1])
            else:
                cost += sum((output-desiredoutput)**2)/double(numcases)
        cost += 0.5 * weightcost * sum(self.params**2)
        return cost

    def hiddens(self,inputs):
        if type(inputs) != type([]):
            inputs = [inputs]
        numcases = len(inputs)
        result = []
        for i in range(numcases):
           result.append(self.scorefuncs[0].bpnet.hiddenlayer.fprop(inputs[i]))
        return result

    def from_hiddens(self, hiddens):
        if type(hiddens) != type([]):
            hiddens = [hiddens]
        numcases = len(hiddens)
        result = []
        for i in range(numcases):
           result.append(self.scorefuncs[0].bpnet.outputlayer.fprop(hiddens[i]))
        return result

    def apply(self, inputs):
        if type(inputs) != type([]):
            inputs = [inputs]
        numcases = len(inputs)
        result = []
        for i in range(numcases):
            result.append(self.scorefuncs[0].bpnet.fprop(inputs[i]))
        return result


class Islsl(Contrastive):
    """ Network with the structure
        input -> sigmoid -> linear -> sigmoid -> linear
        Useful e.g. as an autoencoder. """

    def __init__(self,numin,numhid1,numhid2,numhid3,numout):
        self.numin  = numin
        self.numhid1 = numhid1
        self.numhid2 = numhid2
        self.numhid3 = numhid3
        self.numout = numout
        self.params = 0.1 * randn(scorefunc.Islsl.numparams(\
                                         numin,numhid1,numhid2,numhid3,numout))
        self.scorefuncs = [scorefunc.Islsl(\
                             numin,numhid1,numhid2,numhid3,numout,self.params)]
        Contrastive.__init__(self,normalizeacrosscliques=False)

    def posdata(self,data):
        return (((data[0],data[1]),),)

    def negdata(self,data):
        return ([],)   #no negdata: scorefunc takes care of it

    def cost(self,data,weightcost):
        if type(data)!=type([]):
            data = [data]
        numcases = len(data)
        cost = 0.0
        for i in range(numcases):
            input = data[i][0]
            desiredoutput = data[i][1]
            output = self.scorefuncs[0](input)
            if len(input.shape) >= 2:
                cost += sum((output-desiredoutput)**2)/\
                                                double(numcases*input.shape[1])
            else:
                cost += sum((output-desiredoutput)**2)/double(numcases)
        cost += 0.5 * weightcost * sum(self.params**2)
        return cost

    def hiddens(self,inputs):
        if type(inputs) != type([]):
            inputs = [inputs]
        numcases = len(inputs)
        result = []
        for i in range(numcases):
            result.append(self.scorefuncs[0].bpnet.layer1.fprop(inputs[i]))
        return result

    def apply(self,inputs):
        if type(inputs) != type([]):
            inputs = [inputs]
        numcases = len(inputs)
        result = []
        for i in range(numcases):
            result.append(self.scorefuncs[0].bpnet.fprop(inputs[i]))
        return result


class LinearRegression(Contrastive):
    """ Simple linear neural network that can be used, for example, to perform
        linear regression.
    """

    def __init__(self,numin,numout):
        self.numin  = numin
        self.numout = numout
        self.params = 0.01 * randn(numin*numout+numout)
        self.scorefunc = scorefunc.LinearRegressionScore(numin,numout,self.params)
        self.scorefuncs = [self.scorefunc]
        Contrastive.__init__(self,normalizeacrosscliques=False)

    def posdata(self,data):
        return (((data[0],data[1]),),)

    def negdata(self,data):
        return ([],)

    def cost(self,data,weightcost):
        if type(data)!=type([]):
            data = [data]
        numcases = len(data)
        cost = 0.0
        for i in range(numcases):
            input = data[i][0]
            desiredoutput = data[i][1]
            output = self.scorefuncs[0](input)
            if len(input.shape) >= 2:
                cost += sum((output-desiredoutput)**2)/\
                                          double(numcases*input.shape[1])
            else:
                cost += sum((output-desiredoutput)**2)/double(numcases)
        cost += 0.5 * weightcost * sum(self.params**2)
        return cost

    def apply(self,inputs):
        if type(inputs) != type([]):
            inputs = [inputs]
        numcases = len(inputs)
        result = []
        for i in range(numcases):
            result.append(self.scorefuncs[0].bpnet.fprop(inputs[i]))
        return result


class LogisticRegression(Contrastive):

    def __init__(self,numin,numclasses):
        self.numin  = numin
        self.numclasses = numclasses
        self.params = 0.01 * randn(self.numin*self.numclasses+self.numclasses)
        self.scorefunc = logreg_score(self.numin,self.numclasses,self.params)
        self.scorefuncs = [scorefunc]
        Contrastive.__init__(self,normalizeacrosscliques=False)

    def posdata(self,data):
        return (((data[0],data[1]),),)

    def negdata(self,data):
        return ([],)   #no negdata: scorefunc takes care of it

    def cost(self,data,weightcost):
        if type(data)!=type([]):
            data = [data]
        numcases = len(data)
        cost = 0.0
        for i in range(numcases):
            input = data[i][0]
            output = data[i][1]
            modeloutput = self.scorefuncs[0](input)
            cost += sum(modeloutput[output]-logsumexp(modeloutput,0))/\
                                                double(numcases*input.shape[1])
        cost += 0.5 * weightcost * sum(self.params**2)
        return cost

    def apply(self,inputs):
        if type(inputs) != type([]):
            inputs = [inputs]
        numcases = len(inputs)
        result = []
        for i in range(numcases):
            result.append(self.scorefuncs[0].bpnet.fprop(inputs[i]))
        return result


class DeepNN(Contrastive):

    def __init__(self, n_nodes):
        self.n_nodes = zip(n_nodes[:-1], n_nodes[1:])
        self.params = 0.01 * randn(sum(map(lambda (a,b): (a+1)*b + (b+1)*a, self.n_nodes)))
        self.layers = []
        start, stop = 0, self.params.shape[0]
        for (numin, numhid) in self.n_nodes:
            _in = (numin+1)*numhid
            _out = (numhid+1)*numin
            assert start+_in <= stop-_out, (start, _in, stop, _out)
            idx = range(start, start+_in) + range(stop-_out, stop)
            start += _in
            stop -= _out
            self.layers += [Isl(numin, numhid, numin, self.params[idx])]
        Contrastive.__init__(self, normalizeacrosscliques=False)

    def posdata(self, data):
        return (((data[0], data[1]),),)

    def negdata(self, data):
        return ([],)   #no negdata: scorefunc takes care of it

    def cost(self, data, weightcost, gap=0):
        if type(data) != type([]):
            data = [data]
        numbatches = len(data)
        cost = 0.0
        for i in range(numbatches):
            inputs = data[i][0]
            outputs = self.apply(inputs, gap)[0]
            targets = data[i][1]
            if len(inputs.shape) >= 2:
                cost += sum((outputs-targets)**2)/double(numbatches*inputs.shape[1])
            else:
                cost += sum((outputs-targets)**2)/double(numbatches)
        cost += 0.5 * weightcost * sum(self.params**2)
        return cost

    def apply(self, inputs, gap=0):
        #print "apply %s, gap %d" % (inputs.shape, gap)
        if type(inputs) != type([]):
            inputs = [inputs]
        numbatches = len(inputs)
        result = []
        for i in range(numbatches):
            for layer in self.layers[:len(self.layers)-gap]:
                hiddens = layer.hiddens(inputs)
                inputs = hiddens
            for layer in reversed(self.layers[:len(self.layers)-gap]):
                outputs = layer.from_hiddens(hiddens)
                hiddens = outputs
            result.append(outputs[0])
        return result

    def prepare(self, inputs, iterations=10, batchsize=200):
        print "Greedy training %d layers" % len(self.layers)
        indexes = range(inputs.shape[1])
        batches = range(0, inputs.shape[1], batchsize)
        training = inputs
        for num, layer in enumerate(self.layers):
            itrainer = train.Conjugategradients(layer, 5)
            count = iterations
            print "Training layer %d: %d iterations with %s samples" % (num, iterations, inputs.shape)
            while count > 0:
                random.shuffle(indexes)
                for nbatch, batch in enumerate(batches):
                    selection = indexes[batch:batch + batchsize]
                    itrainer.step((inputs[:,selection], inputs[:,selection]), 0.0001)
                    cost = self.cost((training[:,selection], training[:,selection]), 0.0001)
                    yield len(self.layers)-num, count, len(batches)-nbatch, cost
                count -= 1
            hiddens = [layer.hiddens(inputs[:,i:i+batchsize])[0]
                       for i in range(0, inputs.shape[1], batchsize)]
            inputs = concatenate(hiddens, axis=1)

