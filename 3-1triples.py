'''
Given a list (2 <= len <= 2000) of integers (0 < int < 1000000) e.g. [1,2,3,4,5,6], 
return the number of unique lucky triples that can be found.

A lucky triple is some tuple (x,y,z) s.t. x dividing y and y dividing z AND x <= y <= z. 
Also ensure that given a list L, and a triple (L_i, L_j, L_k), where i,j,k are list indices, 
i<j<k, for the triple to count as a lucky triple.

So for [1,2,3,4,5,6], there are 3 lucky triples:
- (1,2,4)
- (1,3,6)
- (1,2,6)

'''

def solution(l):

    n = len(l)
    numMultiples = [0] * n
    # numMultiples[i] will hold how many multiples of element i are contained in the list infront. 
    # E.g. if l = [1,2,3,4,8,10], numMultiples = [4,3,0,1,0,0]
    # Key is to realise that for eg if we take the i=1 element (i.e. 2) where numMultiples[1] = 3
    # and see that it divides cleanly by the i=0 element (1) that is before 2nd element,
    # we have found 3 triplets! (1,2,4), (1,2,8), and (1,2,10).
    # i.e. numMultiples holds how many triplets can be formed with element i in the middle.
    # thus, all we need to check in the end, once numMultiples is formed, is:
    # how many "twins" can be formed with the "i=1 element" at the end. 
    # twin = (1,2) where 2%1 = 0 and 2 is at the end.
    # code was taken from dev.to/itepsilon/foorbar-find-the-access-codes-367c
    for i in range(n):
        for j in range(i+1,n):
            if l[j] % l[i] == 0:
                numMultiples[i] +=1
    res = 0
    for i in range(n):
        for j in range(i+1,n):
            if l[j] % l[i] == 0:
                res += numMultiples[j]
    return res
print(solution([1,2,4,6,7,8]))


# I tried many many ways to make this work. 
# 1st attempt: Goes through the whole list in 3 nested for-loops, checks each triple. 
# (This didnt work because I forgot the index rule L_i, L_j, L_k where i<j<k) 

# Attempt 2: Goes through only what remains after each nesting. 
# So we fix i, then check all js greater than i, and then all ks greater than j. 

# STILL DOESNT WORK. So Last attempt is to reduce load even more by realising (with some DuckDuckGo-ing) that:
# given a triple (x,y,z).  

def moduWork(a,b, modu, nonmodu):
    if b not in nonmodu[a] and b not in modu[a]:
        if b >= a and b%a == 0:
            modu[a].append(b)
            return modu,nonmodu,True
        else:
            nonmodu[a].append(b)
            return modu,nonmodu,False
    elif b in modu[a]:
        return modu,nonmodu,True
    else:
        return modu,nonmodu,False

def solution(li):
    ans = []
    # creates triples and tests them
    if len(li) < 3:
        return 0
    nonmodu = {x:[] for x in li}
    modu = {x:[] for x in li}
    for i in range(len(li)):
        x = li[i]
        li1 = li[i+1:]
        
        for j in range(len(li1)):
            y=li1[j]
            modu,nonmodu,check = moduWork(x,y,modu, nonmodu)
            if not check:
                continue
            li2=li1[j+1:]

            for k in range(len(li2)):
                z = li2[k]
                modu,nonmodu,check = moduWork(y,z,modu, nonmodu)
                if not check:
                    continue
                ans.append((x,y,z))
    return ans

# print(solution([1,2,3,5,10])) # == 3
# print(solution([9,8,7,6,5,4,3,2,1])) # == 3
# print(solution([1,1,1]))
# print(solution([1,2,3,4,5,6,7,11,13,999999]))




# print(1, checker(1,2,4) == 0)
# print(2, checker(1,2,5) == 3)
# print(3, checker(2,3,4) == 2)
# print(4, checker(4,3,5) == 1)