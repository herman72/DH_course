# import package
import numpy as np
import pandas as pd 
from datetime import datetime
import sympy as sym


def convert_timestamps(timestamps): #  panda series ==to==> [Hours][Minutes] (list)
    """
        This function converts a pandas series of timestamps into a list of hours and minutes.
        
        Args:
            timestamps (pd.Series): A pandas series of timestamps.

        Returns:
            list: A list of tuples where each tuple contains the hour and minute of the timestamp.
    """
    # rest of your function here
    hh_mm = [0, 0]*len(timestamps)   
    for i in range(len(timestamps)):
        t = timestamps.iloc[i][0]
        d = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')       
        h,m = d.hour, d.minute
        hh_mm[i] = h, m       
    return hh_mm

def read_subject(cohort,subj): # read subject data from the folder; 
    filename = cohort+"_"+str(subj)+".csv";
    file = pd.read_csv("data/"+cohort+"/"+filename,header=0)
    timestamps = file.iloc[:,[0]]
    dates = file.iloc[:,[1]]
    activity = file.iloc[:,[2]]     
    HH_MM = convert_timestamps(timestamps)
    
    # convert dataframe to array
    activity = np.array(activity)
    activity = activity.reshape(-1)

    return HH_MM, activity

def rearrange_in_days(HH_MM, activity):
    minutesinaday = 1439 # from 00:00 to 23:59 there are 1439 minutes
    # stacks days of recorded activity
    midnights = idx(HH_MM,(0,0))    
    for i in range(0,len(midnights)-1):
        day_i = activity[midnights[i]:(midnights[i+1]-1)]
        if i==0: rec = day_i
        elif len(day_i)==minutesinaday: rec = np.vstack((rec,day_i))
    return rec

def gather_data(cohort,subj): # bridge function: use rearrange_in_days and read_subject together
    HH_MM,activity = read_subject(cohort,subj)
    days = rearrange_in_days(HH_MM, activity) 
    return days

def idx(l, target): # returns the pos. of every occurence of 'target'
    output = [];
    for i in range(len(l)):
        if l[i]==target:
            output.append(i)
    return output

def get_subj_index(cohort,subj,I): # helps us finding specific subjects' data in a structured array
    if cohort == "condition":
        subj = subj+32  
    i = np.where(I == subj)
    istart = i[0][0]
    iend = i[0][-1]
    return (istart, iend)

def visualize_data(x,y,style,col = 'black',T ='', l='',xl='', yl='',xlimit=None):
    import matplotlib.pyplot as plt
    if style =='plot':
        plt.plot(x,y,color = col, label = l)
    if style =='scatter':
        plt.scatter(x,y,color = col, label = l)  
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.title(T)
    if not(xlimit is None):
        plt.xlim((xlimit[0],xlimit[1]))
    return None  
    
def feature_extract(X):
    featurevec = []
    t = np.linspace(0,360-(360/1439),1439)
    for day in X:
        f1 = np.mean(day)
        f2 = np.std(day)
        f3 = np.max(day)
        f,f4,f5,f6= cosinor(t,day)
        f8 = np.sum(day)**2
        featurevec.append([f1,f2,f3,f5,f6])
        
    X_feat = np.array(featurevec)
    return X_feat


# cosinor function: doing the fit ourselves
def cosinor(t,y):  
    t = t/360

    w=np.pi*2
    n=len(t)

    x = np.cos(w*t)
    z = np.sin(w*t)

    NE = sym.Matrix(   [[n,         np.sum(x),    np.sum(z),    np.sum(y)  ],
                    [np.sum(x), np.sum(x**2), np.sum(x*z),  np.sum(x*y)],
                    [np.sum(z), np.sum(x*z),  np.sum(z**2), np.sum(z*y)]]   )
    RNE = NE.rref()
    RNE = np.array(RNE[0])

    M = float(RNE[0][3])
    beta = float(RNE[1][3])
    gamma = float(RNE[2][3])

    import math
    Amp = math.sqrt((beta**2 + gamma**2))
    theta = np.arctan2(np.abs(gamma),np.abs(beta))

    # Calculate acrophase (phi) and convert from radians to degrees
    a = np.sign(beta);
    b = np.sign(gamma);
    if (a == 1 or a == 0) and b == 1:
        phi = -theta;
    elif a == -1 and (b == 1 or b == 0):
        phi = -np.pi + theta;
    elif (a == -1 or a == 0) and b == -1:
        phi = -np.pi - theta;
    elif a == 1 and (b == -1 or b == 0):
        phi = -2*np.pi + theta
    
    phi = float(phi)
    
    f = M + Amp*np.cos(w*t+phi)
    
    return f,M,Amp,phi
    # plt.figure()
    # visualize_data(t,f,style="plot",col="red")
    # visualize_data(t,y,style="scatter",col="blue")
    # plt.show()