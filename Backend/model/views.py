from rest_framework.views import APIView
# from .models import *
from rest_framework.response import Response
import pandas as pd
import support
import copy
data = pd.read_csv("neo.csv")

data=data.drop(['id','name',"orbiting_body","sentry_object"],axis=1)

data=support.convertstr(copy.copy(data),5)
for i in range (0,len(data)) : 
    data.at[i,'miss_distance']=  data.at[i,'miss_distance']/10000
import copy
data = support.make_discrete(copy.copy(data),[0,1,2,3,4],[ 1,1,5000,400,4])

arr,features = support.split(copy.copy(data),5)
train_features=arr[:80000]
train_target=features[:80000]
test_features=arr[80000:90000]
test_target=features[80000:90000]
class Test (APIView):
    def post (self,request) :
        diametermin =  request.data["diametermin"]
        diametermax=  request.data["diametermax"]
        velocity =  request.data["velocity"]
        distance =  request.data["distance"]
        magnitude=  request.data["magnitude"]
        output={}
        test_row= [diametermin,diametermax,velocity,distance,magnitude]
        try : 
            op = support.naiveBayes(train_features,train_target,test_row)
            output["status"]="success"
            output["ans"] = op
        except :
            output["status"]="failed"
       
        
        return Response(output)
        