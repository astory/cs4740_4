import read_questions
import re

def colocation_ngram(q_id,n,direction='after'):
  pass

def measurement_unit(answer):
  ''' Take the full answer string and
      return preceeding and proceeding potential units.
  '''
  if re.match('.*[0-9].*',answer):
  #If it's a number question, return potential units
    return re.split('[0-9. ]*',answer)
  else:
  #If not, return nothing
    return []

def find_units(q_id):
  pass

def main():
  return map(measurement_unit,['about 570','saguaro,','Guglielmo Marconi','Africa','$1.5883'])

print(main())
