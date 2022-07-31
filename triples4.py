'''
Given a list (2 <= len <= 2000) of integers (0 < int < 1000000) e.g. [1,2,3,4,5,6], return the number of unique lucky triples that can be found.

A lucky triple is some tuple (x,y,z) s.t. x dividing y and y dividing z AND x <= y <= z.

So for [1,2,3,4,5,6], there are 3 lucky triples:
- (1,2,4)
- (1,3,6)
- (1,2,6)

'''

from itertools import permutations as perm

def checker(li):
    x,y,z = li
    # Return codes: 0 = lucky triple found, 1 = x<=y<=z not met, 2 = xy dont divide, 3 = xy divide but yz do not
    if x <= y and y <= z:
        if y%x == 0:
            if z%y == 0:
                return 0
            else:
                return 3
        else:
            return 2
    else:
        return 1


def solution(li):
    ans = []
    # creates triples and tests them
    if len(li) < 3: 
        return 0
    allPerms = perm(li, 3)
    for triple in allPerms:
        if triple not in ans and checker(triple) == 0:
            ans.append(triple)
    return ans

print(solution([1,2,3,4,5,6]) == 3)
print(solution([1,1,1])==1)
print(solution([1,2,3,5,7]))




# print(1, checker(1,2,4) == 0)
# print(2, checker(1,2,5) == 3)
# print(3, checker(2,3,4) == 2)
# print(4, checker(4,3,5) == 1)