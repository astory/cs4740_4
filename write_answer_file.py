def check_answer(candidate):
	writeAnswers(answerLine(candidate))

def answerLine(candidate):
	return str(candidate[2])+' '+candidate[1]+' '+candidate[0]

def answerFile(candidates):
	return "\n".join(map(answerLine,candidates))

def writeAnswers(stuff,filename='tmp-answers.txt'):
        answersHandle=open(filename,'w')
        answersHandle.write(stuff)
        answersHandle.close()

def demo():
	a=[('. extremely', 'AP881018-0156', 313, 'S'),('elephants', 'A34891018-0156', 313, 'S')]
#	writeAnswers(answerFile(a))
	b=('California','top_docs.208',208,'NNP')
	check_answer(b)

if __name__ == "__main__":
	demo()
