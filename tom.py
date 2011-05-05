import read_questions
import re
import operator
import itertools

def colocation_ngram(q_id,n,direction='after'):
  pass

def is_number(answer):
  return(re.match('.*[0-9].*',answer))

def measurement_unit(answer):
  ''' Take the full answer string and
      return preceeding and proceeding potential units.
  '''
  if is_number(answer):
  #If it's a number question, return potential units
    return re.split('[0-9. ]*',answer)
  else:
  #If not, return nothing
    return []

def find_units(q_id):
  pass


def interactions(predictors,rmax=None):
  ''' Given a list of main effects, return a list of the interactions
      of order up to rmax. If rmax is not given, all orders of
      interactions are returned. The main effects are not returned.
  '''
  if rmax==None:
    rmax=len(predictors)
  beta=[]
  for r in range(2,rmax+1):
    for combination in list(itertools.combinations(predictors,r=r)):
      beta.append(reduce(operator.mul, combination))
  return beta


def main():
#  return map(measurement_unit,['about 570','saguaro,','Guglielmo Marconi','Africa','$1.5883'])
  return interactions(range(2,5),45)

print(main())
