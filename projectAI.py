import numpy as np
class create:
    def __init__(self,nurses,h_rqst):
        self.num_nurses=nurses
        self.schdl=[[],[],[],[],[],[],[]]
        self.holidays=h_rqst
        self.valid=True
        self.problems=0
        self.fit=0
        self.shifts=['d','n','ln']
        
    def NewSchedule(self):
        for i in range(7):
            newday=[]
            allnurses_d=[]
            for j in range(3):
                nurse=np.random.randint(0,10000000)%self.num_nurses
                nurse+=1
                while nurse in allnurses_d:
                    nurse=np.random.randint(1,self.num_nurses+1)
                allnurses_d.append(nurse)
                newday.append((nurse,self.shifts[j]))
            self.schdl[i]=newday   
            
    def AlldaysNursesWorking(self):
        working_days=[]
        for nurse in range(1,self.num_nurses+1):
            nurse_days=[]
            i=0
            for day in self.schdl:
                if((nurse,'d')in day or(nurse,'n') in day or(nurse,'ln')in day):
                    nurse_days.append(i)
                i+=1    
            working_days.append(nurse_days)
        return working_days    
        
        
    def IsScheduleValid(self):
        W_Days=self.AlldaysNursesWorking()
        last=-1        
        for day in self.schdl:
            for i,j in day:
                if j=='d':
                    if last==i:
                        self.valid=False
                        self.problems+=5
                if j=='ln':
                    last=i                        
        for  i,j in self.holidays:
            if j in W_Days[i-1]:
                self.valid=False
                self.problems+=2
    def fitness(self):
        self.problems=0
        self.valid=True
        self.IsScheduleValid()
        if self.problems==0:
            self.fit=1
        else:
            self.fit=round(1/self.problems,5)


class population:
    def __init__(self,n_pop,n_nurses,h_rqsts):
        self.numofpop=n_pop
        self.numofnurses=n_nurses
        self.holidays=h_rqsts
        self.parents=[]
        self.sub=[]
    def NewTable(self,table,state):
        if state:
            for i in self.parents:
                if table==i:
                    return False
        else:
            for i in self.sub:
                if i==table:
                    return False
        return True        
    def MakePopulation(self):
        for i in range(self.numofpop):
            s=create(self.numofnurses,self.holidays)
            s.NewSchedule()
            while self.NewTable(s,True)==False:
                s.NewSchedule()
            s.fitness()
            self.parents.append(s)
        print("Population Done")    
    def AddSub(self,Newparents):
        for i in Newparents:
            if self.NewTable(i, False):
                self.sub.append(i)
                
        
        
class GeneticAlgorathim:
    def __init__(self,popul):
        self.pop=popul
        self.pop.sub=list(self.pop.parents)
        self.children=[]
    def MatingPool(self):
        self.pop.sub.sort(key=lambda x: x.fit, reverse=True)
        self.pop.sub=self.pop.sub[0:3]
        PoorParents=[]
        for i in range(3):
            index=np.random.randint(int(self.pop.numofpop/3))
            PoorParents.append(self.pop.parents[-index])
        self.pop.AddSub(PoorParents)
        return self.pop.sub[0]
    def CrossOver(self):
        self.children=[]
        for i in range(len(self.pop.sub)):
            for j in range(i+1,len(self.pop.sub)):
                child1=create(self.pop.numofnurses, self.pop.holidays)
                child2=create(self.pop.numofnurses, self.pop.holidays)
                child1.schdl=list(self.pop.sub[i].schdl)
                child2.schdl=list(self.pop.sub[i].schdl)
                temp=child1.schdl
                change=np.random.randint(2,5)
                child1.schdl[change:]=child2.schdl[change:]
                child2.schdl[change:]=temp[change:]
                child1.fitness()
                child2.fitness()
                self.children.append(child1)
                self.children.append(child2)
                self.children.sort(key=lambda x : x.fit , reverse=True)
                self.pop.AddSub(list(self.children[:6]))
                

    def Mutation(self):
        for child in self.children:
            day1=np.random.choice([0,1,2])
            day2=np.random.choice([3,4,5,6])
            temp=child.schdl[day1]
            child.schdl[day1]=child.schdl[day2]
            child.schdl[day2]=temp
            child.fitness()
        self.children.sort(key=lambda x:x.fit,reverse=True)
        self.pop.AddSub(list(self.children[:6]))
                
            
        
              
    
        
n=int(input())
holidays=[]
while True:
    condation=input("Do you want to add anthor holiday: ")
    if condation=='No':
        break
    nurse=int(input("please enter number of nurse: "))
    holiday=int(input("please enter day of holiday{str=0,sun=1,....,fri=6}: "))
    holidays.append((nurse,holiday))
pop=population(6, n, holidays)
pop.MakePopulation()
solve=GeneticAlgorathim(pop)
best=solve.MatingPool()
i=0
while best.fit < 1 and i<=100:
    solve.CrossOver()
    solve.Mutation()
    best=solve.MatingPool()
    i+=1
print("fitness is :"+str(best.fit))
print("problem is : "+str(best.problems))  
weak=["str","sun","mon","tuse","wed","thr","fri"]
cnt=0
shifts=['d','n','ln']
for i in range(3):
    if i==0:
        print("days",end=" ")
    print(shifts[i],end=" ")   
print("\n")  
for day in best.schdl:
    print(weak[cnt],end="  ")
    cnt+=1
    for i,j in day:
        print(i,end=" ")
    print("\n")    



                        