import pandas as pd
import random
import math
from epanettools import epanet2 as et

def runSim(fileName, PipeIDs, PipeSizesAvailable, CostPerEachPipeSizeAvailable, NodesRequireHeadLevelDict, DoesTheNodeDeficitConsiderEN_ELEVATION, solution):

	errorCode=0
	totalCost = 0.0
    
	errorCode=et.ENopen(fileName+".inp",fileName+".rpt","")

	if (checkEpanetErrorCodes(errorCode) < 0):
		print("Error!1")
		return -1

	errorCode=et.ENopenH()
	if (checkEpanetErrorCodes(errorCode) < 0):
		print("Error!3")		
		et.ENclose()
		return -1

	errorCode=et.ENinitH(0)
	if (checkEpanetErrorCodes(errorCode) < 0):
		print("Error!4")		
		et.ENcloseH()
		et.ENclose()
		return -1
	
	errorCode, t=et.ENrunH()
	if (checkEpanetErrorCodes(errorCode) < 0):
		print("Error!5")
		et.ENcloseH()
		et.ENclose()
		return -1

	for counter in range(len(PipeIDs)):

		nodePipeDiameter=0.0
		errorCode, nodeIndex = et.ENgetlinkindex(PipeIDs[counter])        
		
		if (checkEpanetErrorCodes(errorCode) < 0):
			print("Error!6")
			et.ENcloseH()
			et.ENclose()
			return -1
		
		nodePipeDiameter = PipeSizesAvailable[solution[counter]]
		errorCode = et.ENsetlinkvalue(nodeIndex, et.EN_DIAMETER, nodePipeDiameter)	

		if (checkEpanetErrorCodes(errorCode) < 0):
			print("Error!7")
			et.ENcloseH()
			et.ENclose()
			return -1
		
		errorCode, pipe_length = et.ENgetlinkvalue(nodeIndex, et.EN_LENGTH)

		if (checkEpanetErrorCodes(errorCode) < 0):
			print("Error!8")
			et.ENcloseH()
			et.ENclose()
			return -1
		
		totalCost += CostPerEachPipeSizeAvailable[solution[counter]] * pipe_length

	errorCode, t = et.ENrunH()

	if (checkEpanetErrorCodes(errorCode) < 0):
		print("Error!9")
		et.ENcloseH()
		et.ENclose()
		return -1
	
	for i in range(len(NodesRequireHeadLevelDict)):

		errorCode, nodeIndex = et.ENgetnodeindex(list(NodesRequireHeadLevelDict.keys())[i])

		if (checkEpanetErrorCodes(errorCode) < 0):
			print("Error!10")			
			et.ENcloseH()
			et.ENclose()
			return -1
	
		errorCode, value = et.ENgetnodevalue(nodeIndex, et.EN_HEAD)

		if (checkEpanetErrorCodes(errorCode) < 0):
			print("Error!11")
			et.ENcloseH()
			et.ENclose()
			return -1
		
		if DoesTheNodeDeficitConsiderEN_ELEVATION == 1:
			errorCode, retrievedData = et.ENgetnodevalue(nodeIndex, et.EN_ELEVATION)			
			if (checkEpanetErrorCodes(errorCode) < 0):
				print("Error!Problem2")
				et.ENcloseH()
				et.ENclose()
				return -1

			nodeDeficit = (value - (NodesRequireHeadLevelDict[(list(NodesRequireHeadLevelDict.keys())[i])] + retrievedData))
		else:
			nodeDeficit = (value - NodesRequireHeadLevelDict[(list(NodesRequireHeadLevelDict.keys())[i])])
		
		if (nodeDeficit < 0.0):
			penalityCost = (-nodeDeficit) * 1000000000000.0
			totalCost += penalityCost
	
	errorCode = et.ENcloseH()

	if (checkEpanetErrorCodes(errorCode) < 0):
		print("Error!12")
		et.ENcloseH()
		et.ENclose()
		return -1
	errorCode = et.ENclose()

	if (checkEpanetErrorCodes(errorCode) < 0):
		print("Error!13")
		et.ENcloseH()
		et.ENclose()
		return -1

	return totalCost

def checkEpanetErrorCodes(errorCode):	
	if (errorCode != 0):
		if (errorCode == 1 or errorCode == 2 or errorCode == 3 or errorCode == 4 or errorCode == 5 or errorCode == 6):
			return 0
		else:
			return -1
	else:
		return 0
	 
def Randomise(solution, NumberOfPipes, NumberOfPipeSizesAvailable):
	for s in range(NumberOfPipes):
		solution[s] = random.randint(0, NumberOfPipeSizesAvailable - 1)    

def ReadFile(f_name):

    data = []
    with open(f_name+"_settings.txt") as infile:
        [data.append(line.split()) for line in infile]

    return data

def HillClimbing(f_name, PipeIDs, PipeSizesAvailable, CostPerEachPipeSizeAvailable, NodesRequireHeadLevelDict, DoesTheNodeDeficitConsiderEN_ELEVATION, solution):
    #1- calculate intial solution
    #2- calculate initial cost
    cost = runSim(f_name, PipeIDs, PipeSizesAvailable, CostPerEachPipeSizeAvailable, NodesRequireHeadLevelDict, DoesTheNodeDeficitConsiderEN_ELEVATION, solution)
    solution_new = solution.copy()
    print(cost)
    
    #3-specify L :
    k=10
    l = [cost]*k
    print(l)
   
    i=0
 
    while (i<20):
        
        Randomise(solution, NumberOfPipes, NumberOfPipeSizesAvailable)
        cost_new = runSim(f_name, PipeIDs, PipeSizesAvailable, CostPerEachPipeSizeAvailable, NodesRequireHeadLevelDict, DoesTheNodeDeficitConsiderEN_ELEVATION, solution)
        
        
        v = i % k
        print("Is ",cost_new ,"< = ", l[v])
        #move acceptance
        if cost_new <= l[v]:
            print("yes")
            
            cost = cost_new
            l[v] = cost
            solution_new = solution.copy()
            
            print(i)
            i=i+1
            
            print(v)
            print(cost)
            
        else:
            solution = solution_new.copy()
    print(cost)
    print(l)
    
    #print(l)

def Change(sol, NumberOfPipeSizesAvailable):
    s = random.randint(0, len(solution) - 1)
    sol[s] =  random.randint(0, NumberOfPipeSizesAvailable - 1)

f_name = "NYTUN_imperial"
data = ReadFile(f_name)

NumberOfPipes = int(data[0][1])

PipeIDs = [item for sublist in data[2:2 + NumberOfPipes] for item in sublist]

NumberOfPipeSizesAvailable = int(data[NumberOfPipes + 2][1])

PipeSizesAvailable = [float(item) for sublist in data[NumberOfPipes + 4:NumberOfPipes + 4 + NumberOfPipeSizesAvailable] for item in sublist]

CostPerEachPipeSizeAvailable = [float(item) for sublist in data[NumberOfPipes + NumberOfPipeSizesAvailable + 5:NumberOfPipes + NumberOfPipeSizesAvailable + 5 + 

NumberOfPipeSizesAvailable] for item in sublist]

NumberOfNodesRequireHeadLevels = int(data[NumberOfPipes + NumberOfPipeSizesAvailable*2 + 5][1])

NodesRequireHeadLevel = data[NumberOfPipes + NumberOfPipeSizesAvailable*2 + 7:NumberOfPipes + NumberOfPipeSizesAvailable*2 + 7 + NumberOfNodesRequireHeadLevels]

for x in range(len(NodesRequireHeadLevel)):
    NodesRequireHeadLevel[x][1] = float(NodesRequireHeadLevel[x][1])

NodesRequireHeadLevelDict = dict(NodesRequireHeadLevel)

DoesTheNodeDeficitConsiderEN_ELEVATION = int(data[NumberOfPipes + NumberOfPipeSizesAvailable*2 + NumberOfNodesRequireHeadLevels + 7][1])

solution = [0] * NumberOfPipes

HillClimbing(f_name, PipeIDs, PipeSizesAvailable, CostPerEachPipeSizeAvailable, NodesRequireHeadLevelDict, DoesTheNodeDeficitConsiderEN_ELEVATION, solution)


