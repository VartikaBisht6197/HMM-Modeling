#Emission Matrix
EmissionMatrix = [ [0.04 , 0.04, 0.88, 0.04] , [0.40, 0.40, 0.04, 0.16] ]

#Hidden State legends Matrix
HiddenMatrix = {0:'I' , 1:'D' , 2:'M' , 3:'Mi'} 

#Prior Matrix
StartingProbability = []
for i in range(4):
    sp = (EmissionMatrix[0][i] + EmissionMatrix[1][i])*0.5
    StartingProbability.append(sp)

   
#Transition Matrix
TransitionMatrix = []
for i in range(4):
    TransitionMatrixRow = []
    for j in range(4):
        Prob_i2j = StartingProbability[i] * StartingProbability[j]
        TransitionMatrixRow.append(Prob_i2j)
    TransitionMatrix.append(TransitionMatrixRow)

 
#Given two lists A and B, it multiplies respective elemets of the list and returns a list AB (Specifically for [I D M MI] probability multiplivcation)
def MultiEle(A , B):
    AB = []
    #As all the multiplication is needed while calulating the [I D M MI] probability so the number of elements in each list is 4
    for a in range(4):
        AB.append(A[a]*B[a])
    return AB

 
#Fills in the Observation Matrix. It take VMat after FillInsDel as an input and returns the Filled Matrix
def FillMat(VMat, str1, str2):
    for let1 in range(1,len(str1)):
        for let2 in range(1,len(str2)):
            if(str1[let1] == str2[let2]):
                simi = 0
            else:
                simi = 1
            VMat[let1][let2][0] =  EmissionMatrix[simi][0] * max(MultiEle( VMat[let1][let2-1] , TransitionMatrix[0]))
            VMat[let1][let2][1] =  EmissionMatrix[simi][1] * max(MultiEle( VMat[let1-1][let2] , TransitionMatrix[1]))
            VMat[let1][let2][2] =  EmissionMatrix[simi][2] * max(MultiEle( VMat[let1-1][let2-1] , TransitionMatrix[2]))
            VMat[let1][let2][3] =  EmissionMatrix[simi][3] * max(MultiEle( VMat[let1 -1][let2-1] , TransitionMatrix[3]))
    return VMat

   
#Fills the first row for Insertion and first column for deletion    
def FillInsDel(VMat , l1 , l2):
    VMatcount = 1
    for let in l2[1:]:
        if(l1[0] == let):
           VMat[0][VMatcount][0] = max(MultiEle(EmissionMatrix[0],VMat[0][VMatcount - 1]))
        else:
            VMat[0][VMatcount][0] = max(MultiEle(EmissionMatrix[1],VMat[0][VMatcount - 1]))
        VMatcount = VMatcount + 1      
    VMatcount = 1
    for let in l1[1:]:
        if(l2[0] == let):
            VMat[VMatcount][0][1] = max(MultiEle(EmissionMatrix[0],VMat[VMatcount - 1][0]))
        else:
            VMat[VMatcount][0][1] = max(MultiEle(EmissionMatrix[1],VMat[VMatcount - 1][0]))
        VMatcount = VMatcount + 1
    return VMat
     

 #Given VMat filled as an Input, it returns the most probable path
def Viterbi(VMat,m,n):
    path = []
    MaxAtEach = [[[0 for z in range(2)]for y in range(n)] for x in range(m)]
    for i in range(m):
        for j in range(n):
            MaxAtEach[i][j][0] = max(VMat[i][j])
            MaxAtEach[i][j][1] = HiddenMatrix[VMat[i][j].index(max(VMat[i][j]))]
    g = m - 1
    h = n - 1
    while(g >0 and h >0):
        check = [MaxAtEach[g-1][h][0] , MaxAtEach[g][h-1][0] , MaxAtEach[g-1][h-1][0]]
        if(check.index(max(check)) == 0):
            path.append([g,h,MaxAtEach[g][h][1]])
            g  = g - 1
        if(check.index(max(check)) == 1):
            path.append([g,h,MaxAtEach[g][h][1]])
            h  = h - 1
        if(check.index(max(check)) == 2):
            path.append([g,h,MaxAtEach[g][h][1]])
            g  = g - 1
            h  = h - 1
    path.append([g,h,MaxAtEach[g][h][1]])
    if(g == 0):
        for w in range(h-1,-1,-1):
           path.append([g,h,MaxAtEach[g][h][1]]) 
    if(h == 0):
        for u in range(g-1,-1,-1):
            path.append([g,h,MaxAtEach[g][h][1]])
    return(path)


str1 = 'ATTACATTAC' #input1
str2 = 'GATTACA' #input2

#Observation Matrix according to str1 and str2 
VMat = [[[0 for z in range(4)]for y in range(len(str2))] for x in range(len(str1))]

#Fill in the (0,0) position using the prior matrix
if(str1[0] == str2[0]):
    VMat[0][0] = MultiEle(EmissionMatrix[0],StartingProbability)
else:
    VMat[0][0] = MultiEle(EmissionMatrix[1],StartingProbability)

#Fill the Matrix
FillInsDel(VMat,str1,str2)
FillMat(VMat , str1,str2)

#Print the path
print(Viterbi(VMat, len(str1) , len(str2)))