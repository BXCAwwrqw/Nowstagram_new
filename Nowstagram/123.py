def replace(s):
    for i in range(len(s)-1):
        if s[i] == ' ':
            s[i] = '%20'
        print s
        return
s = 'hello world'
# s[0] = 'a'
print s
res = s.replace(' ', '%20')
print res

def coin(n, list=[]):
    if n==0:
        pass
    #if n == 2:
     #   list.append(2)
    #elif n == 1:
     #   list.append(1)
    elif n % 2 == 0:
        n = (n-2)/2
        coin(n, list)
        list.append(2)
        res=''
        for i in list:
            res+=str(i)
        return res
    else:
        n = (n-1)/2
        coin(n, list)
        list.append(1)
        res=''
        for i in list:
            res+=str(i)
        return res


def reversenum(n,res=0):
    res2=0
    while n != 0:
        temp=res
        mo=n%10#//5 4
        n = n/10#//4 0
        res*=10#//0 50
        #print res+mo#//5 54
        res+=mo
    return res

# print reversenum(int(n))+int(n)
def averagenum(str):
    i=0
    list=[]
    for j in range(len(str)):
        if j!=0 and j!= len(str):
            if str[j]!=str[j-1]:
                res=j-i
                list.append(res)
                i=j
        if j == len(str)-1 :#1?
            res=j-i+1
            list.append(res)
            i=j
    return list
n = raw_input()
#res=0
#print averagenum(n)
#for i in averagenum(n):
#    res+=i
#res =round(float(res)/len(averagenum(n)),2)
#print '{:.2f}'.format(res)

def stringlist(str):
    list=str.split(' ')
    for i in range(len(list)):
        list[i]=int(list[i])
    return list
def foutrtimes(list):
    map={"0":0, "1":0, "2":0}
    for i in list:
        res = 0
        while( i%2==0 and i!=0):
            i=i/2
            res+=1
        if res == 0:
            map["0"]+=1
        elif res == 1:
            map["1"]+=1
        else:
            map["2"]+=1
    return map
list=[1,10,100]
# print foutrtimes(list)
def test(dict):
    x=dict["0"]
    y=dict["1"]
    z=dict["2"]
    if x>=2:
        x1=4*x-4
    else:
        x1=2*x
    need=x1/4
    #if y>=0:
     #   need+=1
    #if z>=need:
     #   return True
   #return False
    if z>=x:
        return True
    else:
        return False
def res(n,res=[]):
    for i in range(n):
        raw_input()
        str=raw_input()
        list=stringlist(str)
        dict=foutrtimes(list)
        if test(dict):
            res.append('Yes')
        else:
            res.append("No")
    return res

for i in res(int(n)):
    print i