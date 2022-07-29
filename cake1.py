def checker(mnm, toTest):
    '''
    given mnm='abcabc', and toTest='abc', check if 
    1. mnm starts with toTest
    2. else return 0'''

    #Check if mnm long enough
    if len(mnm) < len(toTest) and len(mnm) > 0:
        return "N" #"N" is code for "This toTest doesnt work".
    elif len(mnm) == 0:
        # the string has ended and we have found exactly repeating patterns
        return 0
    elif len(mnm) > 0 and len(mnm) >= len(toTest):
        #here we get a chance to test.
        if mnm.startswith(toTest):
            #found a matching partial pattern, need to check the rest
            j = len(toTest)
            toRet = checker(mnm[j:], toTest)
            if toRet != "N":
                return toRet + 1
            else:
                #partial match found but no match after that
                return toRet
        else:
            #no matching pattern
            return "N"

def worker(mnm,i):
    ''' Tests if there could be a possible match, hands over test strs to checker.'''
    toTest = mnm[0:i]
    if mnm.startswith(toTest):
        toRet = checker(mnm, toTest)
        if toRet != "N":
            return toRet
        elif toRet == "N":
            return worker(mnm, i+1)

def solution(mnm):
    return worker(mnm, 1)

print(solution("abccbaabccba") == 2)
print(solution("cba") == 1)
print(solution("ababc")== 1)
print(solution("aabbccdd") == 1)
print(solution("aabbccaabbcc") == 2)
print(solution("cbacba") == 2)
print(solution("abccbaabccba") == 2)



    # if len(mnm) > 0:
    #     if mnm.startswith(toTest):
    #         i = len(toTest)
    #         # print(toTest, mnm[i:], mnm)
    #         if len(mnm[i:]) >= i:
    #             toRet = checker(mnm[i:],toTest)
    #             # print(toRet)
    #             if toRet != "N":
    #                 return toRet+1
    #     return "N"
    # else:
    #     return 0