#!/usr/bin/env python
import read_questions
import re
import operator
import itertools

def colocation_ngram(q_id,n,direction='after'):
  pass

#Is the answer one of the two numeric types?
def is_numeric(answer):
  return(re.match('.*[0-9].*',answer))

#Is the answer a raw number?
def is_number(answer):
  if is_numeric(answer):
    return max(measurement_unit(answer))==''
  else:
    return False

#Is the answer a quantity?
def is_quantity(answer):
  if is_numeric(answer):
    return max(measurement_unit(answer))!=''
  else:
    return False

def measurement_unit(answer):
  ''' Take the full answer string and
      return preceeding and proceeding potential units.
  '''
  if is_numeric(answer):
  #If it's a number question, return potential units
    return re.split('[0-9., ]*',answer)
  else:
  #If not, return nothing
    return []

def find_units(q_id):
  pass

def interactions(predictors,rmax=None):
  ''' Given a list of main effects, return a list of the interactions
      of order up to rmax. If rmax is not given, all orders of
      interactions are returned. The main effects are also returned.
  '''
  if rmax==None:
    rmax=len(predictors)
  beta=[]
  for r in range(1,int(rmax)+1):
    for combination in list(itertools.combinations(predictors,r=r)):
      beta.append(reduce(operator.mul, combination))
  return beta

def main():
#  return map(measurement_unit,['about 570','saguaro,','Guglielmo Marconi','Africa','$1.5883'])
  print interactions(range(2,5))

if __name__=='__main__':
	main()
