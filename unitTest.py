##### UNIT TEST #####
def checkExpect(inputObj,inputAction, expectedVal):
    '''
    unit Tests
    '''
    #print(inputObj)
    #print(expectedVal)
    if inputObj == expectedVal:
        print("<PASS> %s: %s" % (inputAction,inputObj))
    else:
        print("<FAIL> %s: %s" % (inputAction,inputObj))


