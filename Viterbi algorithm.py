import math
import string

from matplotlib import pyplot as plt
from numpy import double

# input
with open('initialStateDistribution.txt') as file:
    line_s = file.readlines()
pi=[None for i in range(len(line_s))]
for i in range(len(line_s)):
    pi[i]=double(line_s[i].replace("\n",""))

with open('../emissionMatrix.txt') as file:
    line_s = file.readlines()
b=[[None for j in range(2)]for i in range(len(line_s))]
for i in range(len(line_s)):
    line=line_s[i].replace("\n","")
    nums=line.split("\t")
    b[i][0]=double(nums[0])
    b[i][1]=double(nums[1])

with open('../transitionMatrix.txt') as file:
    line_s = file.readlines()
a=[[None]for i in range(len(line_s))]
for i in range(len(line_s)):
    line=line_s[i].replace(" \n","")
    nums=line.split(" ")
    a[i]=[None for j in range(len(nums))]
    for j in range(len(nums)):
        a[i][j]=double(nums[j])

with open('../observations.txt') as file:
    line_s = file.readlines()
o=[]
for i in range(len(line_s)):
    line=line_s[i].replace(" \n","")
    nums=line.split(" ")
    for j in range(len(nums)):
        o.append(int(nums[j]))

#o=o[0:1000]
print("total length: ",len(o))

n=len(pi)
T=len(o)
# ll(t,n) matrix & phi(t,n; choice record) matrix(t,n)
ll=[[None for i in range(n)] for j in range(T)]
phi=[[None for i in range(n)] for j in range(T)]

# for t=1(index 0)
for i in range(n):
    ll[0][i]= math.log(pi[i])+math.log(b[i][o[0]])

# for t>=2(inde 0--T-1)
print("process indicator, how many has been processed")
for t in range(T-1):
    if t % 10000==0 :
        print(t)
    for j in range(n):
        max = ll[t][0] + math.log(a[0][j])
        max_i = 0
        for i in range(n):
            thisvalue = ll[t][i] + math.log(a[i][j])
            if max < thisvalue:
                max = thisvalue
                max_i = i
        ll[t + 1][j]=max+math.log(b[j][o[t+1]])
        phi[t+1][j]=max_i

#backtracking
state=[None for i in range(T)]

# t=T(index T-1)
max=ll[T-1][0]
max_i=0
for i in range(n):
    if max<ll[T-1][i]:
        max=ll[T-1][i]
        max_i=i
state[T-1]=max_i

# 1<=t<=T-1 (index: T-2<--0)
for t in reversed(range(T-1)):
    state[t]=phi[t+1][state[t+1]]


# the hidden sentence is:
letter=list(string.ascii_lowercase)
letter.append(' ')
print("the hidden sentence is:")
sentence=""
prestate=-1
for t in range(T):
    if state[t]!=prestate:
        prestate=state[t]
        sentence +=letter[prestate]
print(sentence)

# plot
y_mark=letter
y_value=[*range(27)]
print("plot")
plt.title(sentence)
plt.xlabel("time")
plt.ylabel("letter")
plt.yticks(y_value,y_mark)
time=range(T)
plt.plot(time,state,color='r')
plt.show()




