'''
Given an integer (as a string) with < 309 digits, find the fastest way (and number of moves required in this way) to turn it into zero. The only available operations are:
1. Add 1 to the number
2. Subtract 1 from the number
3. If the number is even, divide it by 2.

E.g. Input 8. Output should be 3: 8 -> 4 -> 2 -> 1 (3 arrows)
E.g. Input 15. Output should be 5: 15 -> 16 -> 8-> 4 -> 2 -> 1

Idea:

0-2: add or subtract 1 to reach the endpoint.
3-5: add/subtract 1 to reach power of 2 (i.e. 4) then divide all the way to endpoint.
6: 6 -> 3 -> 2 -> 1
7: 7 -> 8 -> 4 -> 2 -> 1
8: sol(7) - 1
9: turn to 8
10: 10 -> 5 -> 4 -> 2 -> 1
11: 11 -> 12 -> 6 -> 3 -> 2 -> 1 OR 11 -> 10 -> 5 -> 4 -> 2 -> 1

Key seems to be to divide as soon as possible, or make it divisible ASAP. 
'''
# first idea: just raw processing power!! let recursion do everything.
from re import sub


def worker1(n):
    if n == 1:
        return [1]
    # if n is odd, make it even
    if int(str(n)[-1]) not in [0,2,4,6,8]:
        # compare if adding 1 or subtracting 1 would be better
        if len(worker1(n+1)) > len(worker1(n-1)):
            return [n] + worker1(n-1)
        else:
            return [n] + worker1(n+1)
    
    # if n is even, divide by 2
    if int(str(n)[-1]) in [0,2,4,6,8]:
        # n is even
        return [n]+worker1(int(n/2))

# first idea streamlined: let it only push counter between recursions instead of whole lists
def worker2(n):
    if n == 1:
        return 0
    # 1. if n is odd, make it even
    elif int(str(n)[-1]) not in [0,2,4,6,8]:
        # compare if adding 1 or subtracting 1 would be better
        if worker2(n+1) > worker2(n-1):
            return 1 + worker2(n-1)
        else:
            return 1 + worker2(n+1)
    
    # 2. if n is even, divide by 2
    elif int(str(n)[-1]) in [0,2,4,6,8]:
        # n is even
        return 1+worker2(int(n/2))

def worker3(n, dict1):
    # incremental idea: pass a dict of all values along for checked things 
    # (the bottleneck is when comparing in Step 1)
    # dict holds the min num of steps required for each n. 
    # e.g. dict1 = {1:0, 2:1, 3:2, 4:2, ...}
    if n  not in dict1.keys():    
        if int(str(n)[-1]) not in [0,2,4,6,8]:
            # n is odd, calculate paths if added or subbed, and then decide.
            addedSteps = worker3(n+1, dict1)
            subedSteps = worker3(n-1, dict1)
            if addedSteps[0] > subedSteps[0]:
                dict1[n] = subedSteps[0]+1
            else:
                dict1[n] = addedSteps[0]+1
        
        elif int(str(n)[-1]) in [0,2,4,6,8]:
            temp = worker3(int(n/2), dict1)
            dict1[n] = temp[0] + 1
    else:
        pass
    
    return [dict1[n], dict1]

def worker4(n, dict1):
    # current issue is that if you give too long a number, the division fails: "integer division result too large for a float".
    # this happens because normal division returns a float, and a float is fixed in memory size. On the other hand, python
    # handles integers of any length. 

    # incremental idea: use the floor division operator "//" which returns an int for an int.

    # Problem: Now the new issue is that recursion depth is exceeded (the largest input string can only be like 200-ish digits 
    # long). Proceed to worker5 I guess.

    if n not in dict1.keys():    
        if int(str(n)[-1]) not in [0,2,4,6,8]:
            # n is odd, calculate paths if added or subbed, and then decide.
            addedSteps = worker4(n+1, dict1)
            subedSteps = worker4(n-1, dict1)
            if addedSteps[0] > subedSteps[0]:
                dict1[n] = subedSteps[0]+1
            else:
                dict1[n] = addedSteps[0]+1
        
        elif int(str(n)[-1]) in [0,2,4,6,8]:
            temp = worker4(int(n//2), dict1)
            dict1[n] = temp[0] + 1
    else:
        pass
    
    return [dict1[n], dict1]

def worker5(n,dict1):
    # Idea: reduce recursion depth by going up towards the desired number. I.e. if the number is 200 digits long, figure out the dict1 for maybe 200, then 300 digits then proceed. 
    if n not in dict1.keys():
        
        remLen = len(str(n))
        i = 200
        while remLen > 200:
            # craft a number whose digits go up in multiples of 200
            n1 = ["9" for x in range(202)]
            n1 = "".join(n)
            dict1 = worker5(int(n1), dict1)[1]

        if int(str(n)[-1]) not in [0,2,4,6,8]:
            # n is odd, calculate paths if added or subbed, and then decide.
            addedSteps = worker5(n+1, dict1)
            subedSteps = worker5(n-1, dict1)
            if addedSteps[0] > subedSteps[0]:
                dict1[n] = subedSteps[0]+1
            else:
                dict1[n] = addedSteps[0]+1
        
        elif int(str(n)[-1]) in [0,2,4,6,8]:
            temp = worker5(int(n//2), dict1)
            dict1[n] = temp[0] + 1
    else:
        pass
    
    return [dict1[n], dict1]


def solution(n):
    dict1 = {1:0}
    i = 200
    while len(n) > i:
        
        n1 = ["9" for x in range(200)]
        n1 = "".join(n)
        dict1 = worker4(int(n1), dict1)[1]
    return worker4(int(n),dict1)[0]

n = ["9" for x in range(220)]
n = "".join(n)
# print(int(str(n)[-1]))
print(solution(n))

# print(1, worker(8))
# print(1, worker(15))
# print(solution(4) == 2)
# print(solution(15) == 5)
# abs(15-2) 13
# abs(15-4) 11
# abs(15-8) 7
# abs(15-16) 1
# abs(15-32)

# import time

# # start = time.time_ns()
# # n=1000
# # while n < 5000:
# #     n+= 1
# #     worker1(n)
# # print((time.time_ns() - start)/1000000000, "s") # 8.52 s to run all nums from 1000 to 5000 via worker1

# start = time.time_ns()
# anskey = {}
# n=1000
# while n < 5000:
#     n+= 1
#     anskey[n]=(worker2(n))
# print((time.time_ns() - start)/1000000000, "s") # 7.63 s to run all nums from 1000 to 5000 via worker2

# start = time.time_ns()
# n=1000
# while n < 5000:
#     n+= 1
#     assert(anskey[n] == worker3(n,{1:0})[0])
# print((time.time_ns() - start)/1000000000, "s") # 0.1565 s to run all nums from 1000 to 5000 via worker3