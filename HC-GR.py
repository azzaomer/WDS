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
    
    print("the initial solution")
    print(solution)
    print(cost)
    
    #defined variables :
    best_cost = cost
    
    best_c=cost
    
    best_iter = 0
    op = [0] * 9

    #Select LLH using Greedy approach : 
    
    for i in range(2):
            #Selected LLH using Greedy approche :
            print('i' , i)
            #print('before_itr' ,solution)
            for j in range(9):
	
                #print("#",j+1)
                operator = j
                print("B1",solution,"  i",id(solution))
                temp_solution = Operaters(solution,operator+1) 
                print("A1",temp_solution,"  i",id(solution))
                cost_n = runSim(f_name, PipeIDs, PipeSizesAvailable, CostPerEachPipeSizeAvailable, NodesRequireHeadLevelDict, DoesTheNodeDeficitConsiderEN_ELEVATION, temp_solution)
                
               # print('costn', cost_n , 'bestc', best_c)
                if cost_n <= best_c:
                    best_c = cost_n
                    #solution_new = solution.copy()
                    best_op = operator
                    #print('yes',best_c)
                
            print("                                        LLH = ",best_op)
    ##############################################################################
          
            print('solution before best op',solution,id(solution))
            print("B2",solution,"  i",id(solution))
       
            solution = Operaters(solution,best_op+1)
            print("A2",solution,"  i",id(solution))
            print(operator)
            cost_new = runSim(f_name, PipeIDs, PipeSizesAvailable, CostPerEachPipeSizeAvailable, NodesRequireHeadLevelDict, DoesTheNodeDeficitConsiderEN_ELEVATION, solution)
            print(cost_new)
            if cost_new <= best_cost:
                    best_cost = cost_new
                    solution_new = solution.copy()
                    op[operator] += 1
                    best_iter = i
                    
                    #print('iteration improved cost=' , best_cost)
            else:
                    solution = solution_new.copy() 
                    print('iteration solution',solution,id(solution))
            best_c = best_cost
    print("the best cost = " ,best_cost,"   iteration = ",best_iter,"   LLH = ",op)
    #print(solution)
 

   
##################################################LLHs :##########################################################
#1- change one pipe
 #1- change one pipe
def Change(solution, NumberOfPipeSizesAvailable):
    s = random.randint(0, len(solution) - 1)
    solution[s] =  random.randint(0, NumberOfPipeSizesAvailable - 1)
    return solution

 # 2- change 2 pipes randomly :
def ChangeTowPipes(solution, NumberOfPipeSizesAvailable):
    s = random.randint(0, len(solution) - 1)
    solution[s] =  random.randint(0, NumberOfPipeSizesAvailable - 1) 
    
    s = random.randint(0, len(solution) - 1)
    solution[s] =  random.randint(0, NumberOfPipeSizesAvailable - 1)
    return solution

# 3- swap operator :
def Swap_random(solution):
     idx = range(len(solution))
     i1, i2 = random.sample(idx, 2)
     solution[i1], solution[i2] = solution[i2], solution[i1] 
     return solution
     

# 4-Increase or Decrease all pipe sizes by one:     
def IncOrDecAllByOne(solution):
        k = random.randint(1,2)
        for s in range(len(solution)):
        #Increase   
            if(solution[s] < (NumberOfPipeSizesAvailable-1) and k==2):
                solution[s] += 1
        #Decrease
            elif(solution[s] > 0 and k==1):
                solution[s] -= 1
             
                
        return solution
              
#5-Increase or decrease a randomly selected pipe diameter by one pipe size:
def IncOrDecRandomly(solution,NumberOfPipeSizesAvailable):
    s = random.randint(0, len(solution) - 1)
    k = random.randint(1,2)
    #Increase
    if(solution[s] < (NumberOfPipeSizesAvailable-1) and k==1):
        solution[s] += 1
    #Decrease
    elif (solution[s] > 0 and k==2):
        solution[s] -= 1    
    return solution
  
#6- randomly change from 1 to 5 pipes :
def ChangeInRange(solution,NumberOfPipeSizesAvailable):
    k = random.randint(1,5)
    #print(k ," pipes will be changed")
    idx= range(len(solution))
    s= random.sample(idx,k)
    ##print(s)
    for i in range(len(s)):
        solution[s[i]]=random.randint(0,NumberOfPipeSizesAvailable-1)
    return solution
   

#7-randomly initalize solution and pick 2 random pipes increase one and decrease one
def IncreaseAndDecreaseP2(solution,NumberOfPipes,NumberOfPipeSizesAvailable):
    
    s = random.randint(0, len(solution) - 1)
    if solution[s] < (NumberOfPipeSizesAvailable-1):
        solution[s] += 1
    r = random.randint(0, len(solution) - 1)
    if solution[r] > 0 and r!= s:
        solution[r] -= 1
    return solution

#8-pick 4 rando pipes +2 and -2
def IncreasndDecreaseP4(solution,NumberOfPipes,NumberOfPipeSizesAvailable):
    s = random.randint(0, len(solution) - 1)
    if solution[s] < (NumberOfPipeSizesAvailable-1):
        solution[s] += 1
    p = random.randint(0, len(solution) - 1)
    if solution[p] < (NumberOfPipeSizesAvailable-1) and p!=s:
        solution[p] += 1
    r = random.randint(0, len(solution) - 1)
    if solution[r] > 0 and r!= s and r!= p:
        solution[r] -= 1
    n = random.randint(0, len(solution) - 1)
    if solution[n] > 0 and n!=s and n!=p and n!=r:
        solution[n] -= 1
    return solution
#9
def Randomise(solution, NumberOfPipes, NumberOfPipeSizesAvailable):
    for s in range(NumberOfPipes):
            solution[s] = random.randint(0, NumberOfPipeSizesAvailable - 1) 
    return solution
    


def Operaters(solution,LLH):
    result = solution
   # print ('LLH' , LLH)
    operator_sol = solution.copy()
    if LLH == 1 :
        result =  Change(operator_sol, NumberOfPipeSizesAvailable)
    elif LLH == 2 :
        result = ChangeTowPipes(operator_sol, NumberOfPipeSizesAvailable)
    elif LLH == 3:
        result = Swap_random(operator_sol)
    elif LLH == 4:
        result = IncOrDecAllByOne(operator_sol)
    elif LLH == 5:
        result = IncOrDecRandomly(operator_sol,NumberOfPipeSizesAvailable)
    elif LLH == 6:
        result = ChangeInRange(operator_sol,NumberOfPipeSizesAvailable)
    elif LLH == 7:
        result =IncreaseAndDecreaseP2(operator_sol,NumberOfPipes,NumberOfPipeSizesAvailable)
    elif LLH == 8:
        result =IncreasndDecreaseP4(operator_sol,NumberOfPipes,NumberOfPipeSizesAvailable)
    elif LLH == 9:
        result =Randomise(operator_sol, NumberOfPipes, NumberOfPipeSizesAvailable)

    return result

#    
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

