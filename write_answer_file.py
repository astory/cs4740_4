def answerLine(candidate):
	return str(candidate[2])+' '+candidate[1]+' '+candidate[0]

def header():
        return '<s> <s>\n'

def answerFile(candidates):
	return header()+"\n".join(map(answerLine,candidates))

def writeAnswers(candidates,filename='tmp-answers.txt'):
        answersHandle=open(answersFile,'w')
        answersHandle.write(answers)
        answersHandle.close()

def demo():
	a=[('. extremely', 'AP881018-0156', 313, 'S'),('elephants', 'A34891018-0156', 313, 'S')]
	print answerFile(a)

if __name__ == "__main__":
	demo()
