	##################################################LLHs :##########################################################
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
def IncreaseAndDecreaseP2(NumberOfPipes,NumberOfPipeSizesAvailable):
    
    s = random.randint(0, len(solution) - 1)
    if solution[s] < (NumberOfPipeSizesAvailable-1):
        solution[s] += 1
    r = random.randint(0, len(solution) - 1)
    if solution[r] > 0 and r!= s:
        solution[r] -= 1
    return solution

#8-pick 4 rando pipes +2 and -2
def IncreasndDecreaseP4(NumberOfPipes,NumberOfPipeSizesAvailable):
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
    
#Dictionary mapping for functions 
def Operaters(LLH):
  
    switcher = {
        1: lambda :Change(solution, NumberOfPipeSizesAvailable),
        2: lambda :ChangeTowPipes(solution, NumberOfPipeSizesAvailable),
        3: lambda :Swap_random(solution),
        4: lambda :IncOrDecAllByOne(solution),
        5: lambda :IncOrDecRandomly(solution,NumberOfPipeSizesAvailable),
        6: lambda :ChangeInRange(solution,NumberOfPipeSizesAvailable),
        7: lambda :IncreaseAndDecreaseP2(NumberOfPipes,NumberOfPipeSizesAvailable),
        8: lambda :IncreasndDecreaseP4(NumberOfPipes,NumberOfPipeSizesAvailable),
        9: lambda :Randomise(solution, NumberOfPipes, NumberOfPipeSizesAvailable)
    }
    # Get the function from switcher dictionary
    func = switcher.get(LLH, lambda: "Invalid operator")
    return func()
