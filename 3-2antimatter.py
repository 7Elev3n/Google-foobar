'''
Given an integer (as a string) with < 309 digits, find the fastest way (and number of moves required in this way) to turn it into zero. The only available operations are:
1. Add 1 to the number
2. Subtract 1 from the number
3. If the number is even, divide it by 2.

E.g. Input 8. Output should be 3: 8 -> 4 -> 2 -> 1 (3 arrows)
E.g. Input 15. Output should be 5: 15 -> 16 -> 8-> 4 -> 2 -> 1

Idea(s):
worker1: Takes 8.5s to run 4000 runs where 1000 < n < 5000 (time benchmark)
    recursion. for each number, if even, divide by 2 and 
    call yourself on the halved number. if odd, call 
    yourself twice, once with n+1 and once with n-1.
    Compare the 2 calls, return the shorter one upwards!
    This will split at every odd number, and divide at even numbers. 
    Returns list of the fastest way to get to n.

worker2: Takes 7.63s to run the same 4000 runs
    improves on worker1 by pushing a counter instead of a whole list 
    (since we do not care about what the fastest path is, just how long 
    it is).

worker 3: Takes 0.1565s to run the same 4000 runs
    improves on worker2 by reducing repetition. Uses a dict to hold all 
    values explored so far. Passes along this dict in its return value.

worker4: Same time as worker3
    improves on worker3 by using floor division "//" instead of normal division.
    Issue was that for long numbers, division fails: normal division "/"
    returns a float. (e.g. 4/2 = 4.0)
    Floor division turns it into an integer. (4//2 = 2) However, it also
    turns decimals into integers (5//2 = 2)
    We use floor division to fix long int divisions. Python handles 
    integers of arbitrary length, but floats are signed 64 bits.
    Too long a float and it will overflow. Not good when we want to solve
    309 digit n's.

worker5:  0.1080s 
    Issue now is still that the function cannot handle n > 200 digits, 
    due to max recursion depth reached. 
    We need to solve n = 309 digits.
    Improves on worker4 by skipping some recursion calls (checks within
    the same call if n can be divided by 2, then by 4, then by 8, etc.) 
    This skips out 0, 1, 2 calls respectively.
    
worker6: 1.270s
    Issue now is STILL the 309 digit requirement. worker5 can handle up
    to 304 digits. 
    This required a complete rework: from recursion to iterative. The 
    conversion makes it VERY hard to understand, but it is doing the 
    same thing as the recursive calls, except each call is saved in a 
    list instead of python stacks (where py usually keeps each function
    call).

    'work' is a list of all numbers to be checked. for 5, it would (at 
    some point), include 5 -> 6 and 4 -> 3, 2, 1. 
    'found' is a dictionary to store all numbers that have been solved.
    'found' is VERY necessary. It brings iterative calls down exponentially.
    'branches' is a list of all the splitted paths that have birthed 
    from the first number. 
    'ans' is a list of the shortest path till the current number.
'''

# first idea: just raw processing power!! let recursion do everything.
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
    # long). Should be manageable by a loop in solution itself to break down the problem and passing more complete dict1's to 
    # workers. 
    # Idea is that if you ask worker 4 to solve a long integer, it exceeds recursion depth. So just let it work up till that number.
    # IDEA DOESNT WORK. 

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

def worker5(n, dict1):
    # to solve the recursion depth issue, one way might be to reduce recursions by using shortcuts.
    # i.e. trying to divide by higher and higher powers of 2.
    if n not in dict1.keys():
        if n%2 == 1:
            # n is odd, calculate paths if added or subbed, and then decide.
            addedSteps = worker5(n+1, dict1)
            subedSteps = worker5(n-1, dict1)
            if addedSteps[0] > subedSteps[0]:
                dict1[n] = subedSteps[0]+1
                del dict1[n+1] # to reduce size of dict being passed around
            else:
                dict1[n] = addedSteps[0]+1
                del dict1[n-1]
        
        elif n%2==0:
            tempi = 1
            while n//(2**(tempi)) not in dict1.keys() and n%(2**(tempi+1)) == 0:
                tempi += 1
            temp = worker5(n//(2**tempi), dict1)
            dict1[n] = temp[0] + tempi
    
    return [dict1[n], dict1]

import copy
def worker6(n):
    n = int(n)
    work = [n]
    found = {1:[1]}
    branches = [[n]]
    ans = []
    while work != []:
        curr = work[-1]
        currBranches = []
        for i in range(len(branches)):
            branch = branches[i]
            if branch[-1] == curr:
                currBranches.append(branch)
        
        if len(currBranches) == 1:
            currBranch = currBranches[0]     
        else:
            # we have a point where we previously split!
            # I.e. currBranches should have 2 duplicates.
            branches.remove(currBranches[0])
            currBranch = currBranches[1]
        
        currAns = None
        currAnses = []
        for i in range(len(ans)):
            ansBranch = ans[i]
            if ansBranch[-1] == curr:
                currAnses.append(ansBranch)
        
        if len(currAnses) == 1:
            currAns = currAnses[0]
            # Also, from here onwards, anytime we see this curr, we already
            # know the min steps to solve it. So we record it.
            # This, however, only triggers with even numbers (only evens dont split)
            found[curr] = currAns    

        elif len(currAnses) > 1:
            # we have a point where we previously split!
            # I.e. currAnses should have 2 paths that start/end at 1/curr.
            # one of these is shorter. Remove the other!
            currAnses = sorted(currAnses, key=len)
            ans.remove(currAnses[1])
            currAns = currAnses[0]

            # Also, from here onwards, anytime we see this curr, we already
            # know the min steps to solve it. So we record it.
            # This, however, only triggers with odd numbers (only odds split)
            found[curr] = currAns
        
        # print("W", work, "B", branches, "A", ans, "F", found)
        # print()
        # print("c", curr, "cB", currBranch, "cA", currAns)
        # print("---------")
        # print()
        if curr == 1:
            currAns = found[curr]

        if curr in found.keys():
            work.pop()
            currBranch.pop()
            if len(currBranch) > 0: # only the starting number has no parent
                parent = currBranch[-1]
                ans.append(currAns+[parent])
            else:
                break
            continue

        if currAns:
            work.pop()
            currBranch.pop()
            if len(currBranch) > 0: # only the starting number has no parent
                parent = currBranch[-1]
                currAns.append(parent)
            else:
                break
            continue

        if curr % 2 == 0:
            child = curr//2
            work.append(child)
            currBranch.append(child)
            continue

        if curr % 2 == 1:
            child1 = curr + 1
            child2 = curr - 1
            work.append(child1)
            work.append(child2)

            child2Branch = copy.deepcopy(currBranch)
            currBranch.append(child1)
            child2Branch.append(child2)
            # currBranch is a reference, so it has modifed the actual branches list
            # child2Branch needs to be appended.
            branches.append(child2Branch)
            continue
    
    return len(found[n])-1

def solution(n):
    dict1 = {1:0}
    return worker5(int(n),dict1)

n = ["5" for x in range(310)]
n = "".join(n)


print(worker6(n))
print(worker5(int(n), {1:0})[0]) # Fails when n is > 303 digits long (recursion depth exceeds)



import time

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
#     worker3(n,{1:0})[0]
# print((time.time_ns() - start)/1000000000, "s") # 0.1565 s to run all nums from 1000 to 5000 via worker3

# start = time.time_ns()
# n=1000
# while n < 5000:
#     n+= 1
#     worker4(n,{1:0})[0]
# print((time.time_ns() - start)/1000000000, "s") # 0.1565 s to run all nums from 1000 to 5000 via worker4

# start = time.time_ns()
# n=1000
# while n < 5000:
#     n+= 1
#     worker5(n,{1:0})[0]
# print((time.time_ns() - start)/1000000000, "s") # 0.1089 s to run all nums from 1000 to 5000 via worker5

# start = time.time_ns()
# n=1000
# while n < 5000:
#     n+= 1
#     worker6(n)
# print((time.time_ns() - start)/1000000000, "s") # 1.270 s to run all nums from 1000 to 5000 via worker6