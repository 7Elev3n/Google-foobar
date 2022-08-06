'''
Task: Given a list of 'version numbers' such as '1.1.1' and '2.0' and so on, return a sorted list such as [1.1.1, 2.0]

Inputs can start with 0, 1, 2, ...
Inputs are at maximum, 3 levels deep. I.e. 1.0 to 1.2.3. You will not be given 1.2.3.4 

If 2 or more versions are equivalent, (e.g. 1.0 and 1.0.0) sort from shortest to longest.
'''

# Idea: implement a left-right sort. Find a starting point, then for each next item to add in, see if before or after is better, then recurse.

def solution(li):
    # Start the list off
    toRet = [li.pop(0)]
    for val in li:
        toRet = worker(val, toRet)
    return toRet

def worker(val, toRet):
    # check if the current val against the remaining list.
    if not checker(val, toRet[0]):
        if len(toRet) > 1:
            # if the current val should be later than the first item on the remaining list, then pass the work onto the next worker. Take whatever they return and add on the first item and pass it along.
            return [toRet[0]] + worker(val, toRet[1:])
        else:
             
            return [toRet[0]] + [val]
    else:
        # if you are the worker with the first case of "val should be before the first item of the remaining list", then you don't need more workers. Just return the val with the remaining list behind it.
        return [val] + toRet

def checker(val2, val1):
    '''
    Compares the value against val2.
    For val1 = 1.2 and val2 = 1.0, it returns False, else True.
    i.e. asks "Is this ordering correct?" 
    '''
    val1 = val1.split(".")
    val2 = val2.split(".")

    #Equalise lengths
    if len(val1) < len(val2):
        val1.extend([None] * (len(val2) - len(val1)))
    else:
        val2.extend([None] * (len(val1) - len(val2)))

    toCompare = list(zip(val1, val2))
    #now go through 2 at a time to compare each level.
    for tup in toCompare:
        if tup[0] == None and int(tup[1]) == 0: 
            return False
        elif tup[1] == None and int(tup[0]) == 0:
            return True
        elif tup[0] == None:
            return False
        elif tup[1] == None:
            return True
        elif int(tup[0]) > int(tup[1]):
            return True
        elif int(tup[0]) < int(tup[1]):
            return False

print(1, checker("1.1.1", "1.1.2") == True)
print(2, checker("1.1", "1.1.2") == True)
print(3, checker("1.1.1", "1.1") == False)
print(4, checker("1.1.0", "1.1") == False)
print(5, checker("1", "1.0") == True)

print(6, worker("1.1.1", ["1", "1.1", "1.2","2.1"]) == ['1', '1.1', '1.1.1', '1.2', '2.1'])
print(7, worker("1", ["1.0", "1.1", "1.2","2.1"]) == ['1', '1.0', '1.1', '1.2', '2.1'])
print(8, worker("1", ["1.0"]) == ["1", "1.0"])

print(9, solution(["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"]) == ["0.1","1.1.1","1.2","1.2.1","1.11","2","2.0","2.0.0"])
print(10, solution(["1.0"]) == ["1.0"])
