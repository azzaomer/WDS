import pandas as pd
import random
import math
from epanettools import epanet2 as et

import numpy as np

#import LowLevelHeuristics as LLH

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
	 


def ReadFile(f_name):

    data = []
    with open(f_name+"_settings.txt") as infile:
        [data.append(line.split()) for line in infile]

    return data

def HillClimbing(f_name, PipeIDs, PipeSizesAvailable, CostPerEachPipeSizeAvailable, NodesRequireHeadLevelDict, DoesTheNodeDeficitConsiderEN_ELEVATION, solution):

    cost = runSim(f_name, PipeIDs, PipeSizesAvailable, CostPerEachPipeSizeAvailable, NodesRequireHeadLevelDict, DoesTheNodeDeficitConsiderEN_ELEVATION, solution)
    solution_new = solution.copy()
    print(cost)
    
    best_cost = cost
    best_iter = 0
    best_op = 0

    #Select LLH using Random Descent method (RD):
    operator = random.randint(1,9)
    
    for i in range(40000):
            
            Operaters(operator)
            #calculate the new cost :
            cost_new = runSim(f_name, PipeIDs, PipeSizesAvailable, CostPerEachPipeSizeAvailable, NodesRequireHeadLevelDict, DoesTheNodeDeficitConsiderEN_ELEVATION, solution)
           
            #move acceptance :
            if cost_new <= best_cost:
                best_cost = cost_new
                best_iter = i
                
                best_op = operator
                
                solution_new = solution.copy()
                print(best_cost)
            else:
                solution = solution_new.copy()
                #change the operator randomly :
                operator = random.randint(1,9)
	
        
    print("best cost = " ,best_cost,"   iteration = ",best_iter,"   LLH ",best_op)
    print(solution)
    

   
##################################################LLHs :##########################################################
    #1- change one pipe
def Change(solution, NumberOfPipeSizesAvailable):
    s = random.randint(0, len(solution) - 1)
    solution[s] =  random.randint(0, NumberOfPipeSizesAvailable - 1)
    
    # 2- change 2 pipes randomly :

def ChangeTowPipes(solution, NumberOfPipeSizesAvailable):
    s = random.randint(0, len(solution) - 1)
    solution[s] =  random.randint(0, NumberOfPipeSizesAvailable - 1) 
    
    s = random.randint(0, len(solution) - 1)
    solution[s] =  random.randint(0, NumberOfPipeSizesAvailable - 1)
  
    # 3- swap operator :
def swap_random(solution):
     idx = range(len(solution))
     i1, i2 = random.sample(idx, 2)
     solution[i1], solution[i2] = solution[i2], solution[i1] 
     print(i1, i2)
     
     #Decrease :
     # 4-Decrease all pipe sizes by one:
     
def decreaseAllPipesByOne(solution):
        for s in range(len(solution)):
            if solution[s]>0:
              solution[s] -= 1
     #5-decrease a randomly selected pipe diameter by one pipe size:
def RandomlyDecrease(solution,NumberOfPipeSizesAvailable):
    s = random.randint(0, len(solution) - 1)
    if solution[s] > 0:
        solution[s] -= 1
    #print("changed pipe index = ",s)
    
    #increase :
    #6- Increase all pipes :
def IncreaseAllPipesBy1(solution):
     for s in range(len(solution)):
         if solution[s]<15:
           solution[s] += 1
            
    #7- Randomly Increase one pipe :
def RandomlyIncrease(solution,NumberOfPipeSizesAvailable):
    s = random.randint(0, len(solution) - 1)
    if solution[s] < 16:
        solution[s] += 1
    #print("changed pipe index = ",s)
    
    #8- randomly change from 1 to 5 pipes :
def changeInRange(solution,NumberOfPipeSizesAvailable):
    k = random.randint(1,5)
    print(k ," pipes will be changed")
    idx= range(len(solution))
    s= random.sample(idx,k)
    print(s)
    for i in range(len(s)):
        solution[s[i]]=random.randint(0,NumberOfPipeSizesAvailable-1)
    print(solution)
    
    # 9-
def Randomise(solution, NumberOfPipes, NumberOfPipeSizesAvailable):
	for s in range(NumberOfPipes):
		solution[s] = random.randint(0, NumberOfPipeSizesAvailable - 1)

#Dictionary mapping for functions 
def Operaters(LLH):
    switcher = {
        1: lambda : Change(solution, NumberOfPipeSizesAvailable),
        2: lambda :ChangeTowPipes(solution, NumberOfPipeSizesAvailable),
        3: lambda :swap_random(solution),
        4: lambda :decreaseAllPipesByOne(solution),
        5: lambda :RandomlyDecrease(solution,NumberOfPipeSizesAvailable),
        6: lambda :IncreaseAllPipesBy1(solution),
        7: lambda :RandomlyIncrease(solution,NumberOfPipeSizesAvailable),
        8: lambda :changeInRange(solution,NumberOfPipeSizesAvailable),
        9: lambda :Randomise(solution, NumberOfPipes, NumberOfPipeSizesAvailable)
    }
    # Get the function from switcher dictionary
    func = switcher.get(LLH, lambda: "Invalid operator")
    return func()
    
##################################################################################################################

    
  
    
     
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

solution = [1] * NumberOfPipes

HillClimbing(f_name, PipeIDs, PipeSizesAvailable, CostPerEachPipeSizeAvailable, NodesRequireHeadLevelDict, DoesTheNodeDeficitConsiderEN_ELEVATION, solution)



