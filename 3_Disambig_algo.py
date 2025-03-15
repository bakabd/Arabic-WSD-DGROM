# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 22:16:02 2021

@author: Bekhouche Abdelaali 
"""
import random
import csv
from math import sqrt


N=196       
Np=10
t_max=200    
GF=fi=1.618034

def corect_sens():
    myFile = open(path_gold_BERT, 'r')
    reader = csv.reader(myFile)
    myList = []
    for record in reader:
        myList.append(record)
    data= [[int(item) for item in sublist] for sublist in myList]
    return(data)


def extract_sim_values(path_sim):
     file = open(path_sim, "r")
     data = list(csv.reader(file, delimiter=","))
     file.close()
     data= [[float(item) for item in sublist] for sublist in data]
     return(data)

def extract_sim_doc2vec():
    with open(path_sim_Doctovec, 'r') as read_obj: 
        csv_reader = csv.reader(read_obj) 
        # convert string to list 
        list_of_csv = list(csv_reader)
    lst_lst=[]
    l=[]
    for i in range (len(list_of_csv)):
        if (len(list_of_csv[i])==2):
            l.append(list_of_csv[i])
        else :
            lst=[x for x in sorted(l, key=lambda x: x[0])]
            lst_lst.append(lst)
            l=[]
    lst=[x for x in sorted(l, key=lambda x: x[0])]
    lst_lst.append(lst)
    lstt=[]
    for ls in lst_lst:
        lst=[]
        for lss in ls:
            lst.append(lss[1])
        lstt.append(lst)
    data= [[float(item) for item in sublist] for sublist in lstt]
    return(data)


def sol_best_file(path,lst_sol):
     with open(path, "w") as f:
        for row in lst_sol:
            f.write("%s\n" % ','.join(str(col) for col in row))

def Fs_best_file(path,lst):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(lst)

def ini_pop(nbr_sense,Np):
    pop=[]
    for j in range (Np):
       sol=[]
       for i in range (N):
           sol.append(random.randint(0,nbr_sense[i]-1))
       pop.append(sol)
    return(pop)



def fitnes_func(pop,l_sim,j):
    s=0
    for i in range (N):
        s=s+l_sim[i][pop[j][i]]
    return(s)
def fitnes_vec(vec,l_sim):
    s=0
    for i in range(N):
      s=s+l_sim[i][vec[i]]  
    return(s)
    

def av_vector(lst): 
    l=[]
    for i in range (len(lst[0])):
        list=[item[i] for item in lst]
        l.append(max(list, key = list.count))
    return l

def best_med_worst(lst):
    op = {i: lst[i] for i in range(0, len(lst), 1)}
    op = sorted(op.items(), key=lambda item: item[1])
    index_medium =list(op)[len(op)//2][0]
    index_best=lst.index(max(lst))
    index_worst=lst.index(min(lst))
    value_worst=min(lst)
    value_best=max(lst)
    return index_best,index_medium,index_worst,value_worst,value_best
 
def split_list(l, n):
    return [l[int(i*len(l)/n):int((i+1)*len(l)/n)] for i in range(n)]


def plus_op(v1,v2):
    v1=split_list(v1,2)
    v2=split_list(v2,2)
    R1=v1[0]+v2[1]
    R2=v2[0]+v1[1]
    return R1,R2


def minus_op(v1,v2):
    v1=split_list(v1,3)
    v2=split_list(v2,3)
    R1=v1[0]+v2[1]+v1[2]
    R2=v2[0]+v1[1]+v2[2]
    return R1 , R2


def mul_op(v,v_sens,r):
    nbr_elm=round((len(v)*r)/100)
    index=[]
    result=v[:]
    for i in range (nbr_elm):
        idx=random.randint(0,len(v)-1)
        """while  idx  in index :
            idx=random.randint(0,len(v)-1)""" 
        index.append(idx)
        for j in index:
            result[j]=random.randint(0,v_sens[j]-1)
    return result

def GROM(sim,Np):
   
    nbr_sense=[len(listElem) for listElem in sim]
    X=ini_pop(nbr_sense,Np)
    Fs_lst=[]
    for j in range(Np):
        Fs_lst.append(fitnes_func(X,sim,j))
    Sol_best=[]
    Fs_best=[]
    t=1
    while t <= t_max:
        # Obtain X_ave which is the mean value of all the solutions
        X_av=av_vector(X)
        # Set the solution with the worst fitness as X_w
        best,med,worst,Fs_w,Fs_b=best_med_worst(Fs_lst)
        X_w=X[worst][:]
        Fs_av=fitnes_vec(X_av,sim)
        if Fs_av>Fs_w :
           X_w=X_av
        #======First phase=========================#
        for i in range (len(X)):
            j=random.randint(0, len(X)-1)
            while j == i :
                j=random.randint(0, len(X)-1)
            # Calculate fitness function of X[i] and X[j]
            Fs_i= fitnes_vec(X[i],sim)
            Fs_j= fitnes_vec(X[j],sim)
            # Set the best, medium and  worst solution
            lst=[X_w,X[i],X[j]]
            best_idx,med_idx,worst_idx,Fs_w,Fs_b=best_med_worst([Fs_av,Fs_i,Fs_j]) #--------->Equ (3)
            X_best=X[best_idx][:]
            X_worst=X[worst_idx][:]
            X_medium=X[med_idx][:]
            # Update Xi based on equations
            v1,v2= minus_op(X_medium,X_worst)
            Fs_v1=fitnes_vec(v1,sim)
            Fs_v2=fitnes_vec(v2,sim)
            if Fs_v1>Fs_v2:
               X_t= v1[:]
            else :
               X_t= v2[:]
            T=t/t_max
            F_t=GF*((fi)**T-(1-T))/sqrt(5)
            r1=round((1-F_t)*100)
            v1=mul_op(X_best,nbr_sense,r1)
            r2=round((random.random()*F_t*100))
            v2=mul_op(X_t,nbr_sense,r2)
            v1,v2=plus_op(v1,v2)
            Fs_v1=fitnes_vec(v1,sim)
            Fs_v2=fitnes_vec(v2,sim)
            if Fs_v1>Fs_v2:
               X_new= v1[:]
               Fs_new=Fs_v1 
            else :
               X_new= v2[:]
               Fs_new=Fs_v2
            if Fs_new>Fs_i:
               X[i]=X_new[:]
               Fs_lst[i]=fitnes_vec(X_new,sim)
        
         #======Second phase=========================#  
            for i in range (len(X)): 
                best_idx,med_idx,worst_idx,Fs_w,Fs_b=best_med_worst(Fs_lst) #--------->Equ (3)
                X_best=X[best_idx][:]
                X_worst=X[worst_idx][:]
                v1,v2= minus_op(X_best,X_worst)
                Fs_v1=fitnes_vec(v1,sim)
                Fs_v2=fitnes_vec(v2,sim)
                if Fs_v1>Fs_v2:
                   X_r3= v1[:]
                else :
                   X_r3= v2[:]
                r3= round((random.random()*0.618*100))
                v=mul_op(X_r3,nbr_sense,r3)
                v1,v2=plus_op(X[i],v)
                Fs_v1=fitnes_vec(v1,sim)
                Fs_v2=fitnes_vec(v2,sim)
                if Fs_v1>Fs_v2:
                   X_new= v1[:]
                   Fs_new=Fs_v1 
                else :
                   X_new= v2[:]
                   Fs_new=Fs_v2
                Fs_i=fitnes_vec(X[i],sim)
                if Fs_new>Fs_i:
                   X[i]=X_new[:]
                   Fs_lst[i]=fitnes_vec(X_new,sim)
        best_idx,med_idx,worst_idx,Fs_w,Fs_b=best_med_worst(Fs_lst)
        Sol_best.append(X[best_idx])
        Fs_best.append(fitnes_vec(X[best_idx],sim))
        print(t)
        t+=1
    return Sol_best,Fs_best


def main():
    sim1= extract_sim_values(path_sim_BERT)
    sim2= extract_sim_values(path_sim_SentTrans)
    sim3= extract_sim_doc2vec()
    
    Sol_best,Fs_best=GROM(sim2,Np)
    Fs_best_file(path_Fs_best.format("_T="+str(t_max)+"_Np="+str(Np)),Fs_best)
    sol_best_file(path_Sol_best.format("_T="+str(t_max)+"_Np="+str(Np)),Sol_best)    
if __name__=="__main__":
    main()
       
