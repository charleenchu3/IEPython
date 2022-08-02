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


### checkExpect ####
'''
#openFile
unitTest.checkExpect(DataOperation(["TestData/testFolder"],"openFile").checkExpectFunc(["TestData/testFolder"],"openFile"),"openFile",False) #folder
unitTest.checkExpect(DataOperation(["TestData/testFolder/file2.txt"],"openFile").checkExpectFunc(["TestData/testFolder/file2.txt"],"openFile"),"openFile",True) #folder))
#unCompressFile
unitTest.checkExpect(DataOperation(["TestData/file.txt"],"expandFile").checkExpectFunc(["TestData/file.txt"],"expandFile"),"expandFile",False) #normalFile
unitTest.checkExpect(DataOperation(["TestData/compressedTF"],"expandFile").checkExpectFunc(["TestData/compressedTF"],"expandFile"),"expandFile",False) #normalFolder
unitTest.checkExpect(DataOperation(["TestData/file2.zip"],"expandFile").checkExpectFunc(["TestData/file2.zip"],"expandFile"),"expandFile",True) #compressedFile
unitTest.checkExpect(DataOperation(["TestData/compressedTF.tgz"],"expandFile").checkExpectFunc(["TestData/compressedTF.tgz"],"expandFile"),"expandFile",True) #compressedFolder with different .ext

#convertFile
unitTest.checkExpect(DataOperation(["TestData/testFolder/file3.txt"],"convertFile").checkExpectFunc(["TestData/testFolder/file3.txt"],"convertFile"),"convertFile",False) #readOnlyFile
unitTest.checkExpect(DataOperation(["TestData/testFolder/"],"convertFile").checkExpectFunc(["TestData/testFolder/"],"convertFile"),"convertFile",False) #folder
unitTest.checkExpect(DataOperation(["TestData/testFolder/file.txt"],"convertFile").checkExpectFunc(["TestData/testFolder/file.txt"],"convertFile"),"convertFile",True) #normalFile in subFolder

#deleteFile
unitTest.checkExpect(DataOperation(["TestData/testFolder/file3.txt"],"deleteFile").checkExpectFunc(["TestData/testFolder/file3.txt"],"deleteFile"),"deleteFile",False) #readOnlyFile
unitTest.checkExpect(DataOperation(["TestData/testFolder"],"deleteFile").checkExpectFunc(["TestData/testFolder"],"deleteFile"),"deleteFile",False) #folder

#printFile
unitTest.checkExpect(DataOperation(["TestData/testFolder/file.txt"],"printFile").checkExpectFunc(["TestData/testFolder/file.txt"],"printFile"),"printFile",True) #normalFile
unitTest.checkExpect(DataOperation(["TestData/testFolder"],"printFile").checkExpectFunc(["TestData/testFolder"],"printFile"),"printFile",False) #folder

#getAllPaths(test recurse)
unitTest.checkExpect(DataOperation(["TestData/testFolder"],recurse = True).getAllPaths(["TestData/testFolder"],recurse = True),"getAllPaths",{'TestData/testFolder/file3.zip', 'TestData/testFolder/file2.txt', 'TestData/testFolder/file2.txt.zip', 'TestData/testFolder/file.txt', 'TestData/testFolder/file3.txt'}) #folder
unitTest.checkExpect(DataOperation(["TestData/testFolder/file.txt"],recurse = True).getAllPaths(["TestData/testFolder/file.txt"],recurse = True),"getAllPaths",{'TestData/testFolder/file.txt'}) #folder
unitTest.checkExpect(DataOperation(["TestData/testFolder"]).getAllPaths(["TestData/testFolder"]),"getAllPaths",{'TestData/testFolder'}) #folder
unitTest.checkExpect(DataOperation(["TestData/testFolder/file.txt"]).getAllPaths(["TestData/testFolder/file.txt"]),"getAllPaths",{'TestData/testFolder/file.txt'}) #file

#registerAction
unitTest.checkExpect(DataOperation([("TestData/testFolder",'openFile')]).registerAction([("TestData/testFolder",'openFile')]),"registerAction",{'TestData/testFolder':"N/A"})
unitTest.checkExpect(DataOperation([("TestData/testFolder/file.txt",'deleteFile')]).registerAction([("TestData/testFolder/file.txt",'deleteFile')]),"registerAction",{'TestData/testFolder/file.txt':"deleteFile"})
unitTest.checkExpect(DataOperation(["TestData/testFolder","TestData/testFolder/file.txt"]).registerAction(["TestData/testFolder","TestData/testFolder/file.txt"],"deleteFile"),"registerAction",{'TestData/testFolder':"N/A",'TestData/testFolder/file.txt':'deleteFile'})
unitTest.checkExpect(DataOperation(["TestData/testFolder","TestData/testFolder/file.txt"]).registerAction(["TestData/testFolder","TestData/testFolder/file.txt"],"deleteFile",recurse=True),"registerAction",{'TestData/testFolder/file2.txt.zip': 'deleteFile', 'TestData/testFolder/file2.txt': 'deleteFile', 'TestData/testFolder/file.txt': 'deleteFile', 'TestData/testFolder/file3.txt': 'N/A', 'TestData/testFolder/file3.zip': 'deleteFile'})
'''
