#Copyright (C) 2007 Roland Memisevic
#
#This program is distributed WITHOUT ANY WARRANTY; without even the implied 
#warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
#LICENSE file for more details.
#
#
#
#This example file shows how to build a simple model using monte, how to 
#train the model using the provided trainers, and how to apply the trained 
#model to some data.

from numpy import array
from pylab import randn
from monte.models.crf import ChainCrfLinear #ready-to-use models are in 
                                            #monte.models
from monte import train #trainers are in monte.train

#Make a linear-chain CRF:
mycrf = ChainCrfLinear(3,2)

#Make a trainer (that does 5 steps per call), and register mycrf with it:
mytrainer = train.Conjugategradients(mycrf,5)

#Alternatively, we could have used one of these, for example:
#mytrainer = trainers.OnlinegradientNocost(mycrf,0.95,0.01)
#mytrainer = trainers.Bolddriver(mycrf,0.01)
#mytrainer = trainers.GradientdescentMomentum(mycrf,0.95,0.01)

#Produce some stupid toy data for training:
inputs = randn(10,3)
outputs = array([0,1,1,0,0,0,1,0,1,0])

#Train the model. Since we have registered our model with this trainer, 
#calling the trainers step-method trains our model (for a number of steps):
for i in range(20):
    mytrainer.step((inputs,outputs),0.001)
    print mycrf.cost((inputs,outputs),0.001)

#Apply to some stupid test data:
testinputs = randn(15,3)
predictions = mycrf.viterbi(testinputs)
print predictions

