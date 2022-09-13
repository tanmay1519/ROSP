
import copy
import random
import math
import support
# assuming here we are using cross validation and we are giving 
# n sets as training data  and all sets have equal amount of data
def naiveBayes (arr_data,features,query):
    boxsize=len(features)//9
    if len(arr_data[0])!=(len(features)//len(arr_data)):
        
        return False
    distinct_features = set(features)
    newfeatures = list(distinct_features)
    feature_prob = []
    width = len(arr_data[0][0])
    freqData = []
    for i in range (0,len(newfeatures)):
        temp=[]
        for j in range (0,width):
            temp.append(0)
        freqData.append(temp)

    records=len(features)
    for i in range(0,len(newfeatures)):
        feature_prob.append(0)
    for i in features :
        pos = newfeatures.index(i) 
        feature_prob[pos]+=1
    feature_val = copy.copy(feature_prob)
    for i in range(0,len(feature_prob)) :
        feature_prob[i]=feature_prob[i]/records

    # for i in range (0,len(arr_data)):
    #     for j in range (0,len(features)):
    #         rowData = arr_data[i][j]
    #         for k in range(0,len(query)):
    #             pos2 = newfeatures.index(q)
    for i in range (0,len(query)):
        val = query [i]
        for j in range (0,len(arr_data)):
            for k in range (0,len(arr_data[0])):
                queryval = arr_data[j][k][i]
                if (val==queryval):
                    newpos=newfeatures.index(features[j*boxsize+k])#changed here 1000 to boxsize
                    freqData[newpos][i]+=1
    prob=[]
    for i in range(0,len(freqData)):
        mult = 1
        row=freqData[i]
        for j in row :
            mult=mult*j/feature_val[i]
        prob.append(mult)
    max = prob[0]
    for i in prob :
        if i>max :
            max =i
    return prob.index(max)

                     

def convertstr ( data,Columns ) :
    options = []
    num_Column=data.columns[Columns]
    for i in range (0,len(data)):
        query  = data.iloc[i][num_Column]
        if query in options :
            data.at[i,num_Column]=options.index(query)

        else  :
            options.append(query)
            data.at[i,num_Column]=options.index(query)
    return data
    # options=[]
    # k=[]
    # for i in Columns :
    #     options.append({})
    #     k.append(0)
    
    # for i in  range(0,len(data)) :
    #     for j in range (0,len(Columns)):
    #     # try :
    #     #     x=options[data.iloc[i][column]]
    #     #     data.at[i,data.columns[column]]=x
    #     # except :
    #     #     options[str(data.iloc[i][column])]=k
    #     #     data.loc[i,data.columns[column]]=k
             
    #     #     k+=1
    #         try :
    #             x=options[j][data.iloc[i][Columns[j]]]
    #             data.at[i,data.columns[Columns[j]]]=x
    #         except :
    #             options[j][str(data.iloc[i][Columns[j]])]=k[j]
    #             data.loc[i,data.columns[Columns[j]]]=k[j]
    #             k[j]+=1
    # return data
  
#     if we want to make 5 values dicrete then send positions and values are the  values to divide each row at position as per array
def make_discrete (data,positions,values) :
        if len(positions)!=len(values) :
            return False
        min = []
        for i in positions :
            min.append(data.iloc[0][i])
        
        for i in range (0,len(data) ):
                  for j in range(0,len(positions)) :
                      if data.iloc[i][positions[j]] < min [j] :
                          min[j] = data.iloc[i][positions[j]]
        for i in range(0,len(min)) :
                  min[i]=min[i]//values[i]
        for i in range (0,len(data)):
            row = data.iloc[i]
            for j in range (0,len(positions)):
                data.at[i,data.columns[positions[j]]]=(row[positions[j]]//values[j])-min[j]
        return data

def split (data,target) :
    newData = []
    features=[]
    for i in range (0,len(data)):
        line=[]
        row=data.iloc[i]
        for j in range(0,len(row)):
            if (j==target) :
                features.append(row[j])
            else :
                line.append(row[j])
        newData.append(line)
    return newData,features
            
        
    #  length of data and features be a multiple of 10  is preferable
import math
def makeSets (data,features,counts):
    uniqueFeatures = list(set(features))
    percentages=[]
    numbox=[]
    box=[]
    featureBox=[]
    n=len(features)
    for i in counts :
        percentages.append(math.floor(i*100/n))
    for i in uniqueFeatures :
        numbox.append([])
    for i in range(0,n):
        numbox[uniqueFeatures.index(features[i])].append(i)
    
    boxsize = n//10
    for i in range (0,10) :
        temp_counts=copy.copy(counts)
        tempBox=[]
        for j in range  (0,len(temp_counts) ):
            time=math.floor(percentages[j]*boxsize/100)
            while time!=0 :
                time-=1
                # try  :
                pos=numbox[j][0]
                # except:
                #     return [j,numbox,boxsize,percentages]
                tempBox.append(data[pos])
                featureBox.append(features[numbox[j][0]])
                numbox[j].remove(numbox[j][0])
        box.append(tempBox)
    return box,featureBox
            
        
def crossValidation (data,features):
    boxsize =len(features)//10
    crossOutput=[]
    Accuracy=[]
    for i in range (0,10):
        train=copy.copy(data)
        test = train.pop(i)
        trainfeatures = copy.copy(features)
        test_features=[]
        n=copy.copy(boxsize)
        correct=0
        output = []
        uniquefeatures = list(set(features))
        for i in uniquefeatures :
            box=[]
            for j in uniquefeatures :
                box.append(0)
            output.append(box)
        while n :

            test_features.append(trainfeatures.pop(round(i*boxsize)))
            n-=1
        for j in range(0,len(test)) :
            ans = support.naiveBayes(train,trainfeatures,test[j])
           
            if ans == round(test_features[j]):
                correct+=1
                
            output[ans][round(test_features[j])]+=1
        Accuracy.append(round(correct*100/boxsize,3))
        # print(round(correct*100/boxsize,2))
        crossOutput.append(output)
    return crossOutput,Accuracy



