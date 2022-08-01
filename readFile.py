import os
import utilMod
import unitTest

class QueryOp:
    def __init__(self, filePaths, action=None, recurse = False):
        self.ogFilePath = filePaths
        self.fileAllPaths = self.getAllPaths(filePaths,recurse) #list of paths
        self.recurse = recurse
        self.actionType = action
        self.actionDict = self.getFileInfo()  

    def getAllPaths(self,filePaths,recurse = False):
        '''
        take in list of paths, and cursively g
        '''
        if recurse:
            tempFileList = []
            for eachPath in filePaths:
             # for recursive files in nested folders 
                if os.path.isdir(eachPath):
                    # get all files recursively
                    nFileList = [os.path.join(dirPath, file) for dirPath, dirName, filenames in os.walk(eachPath) for file in filenames if os.path.splitext(file)[1] != '']
                else:
                    nFileList = [eachPath]
                tempFileList.append(nFileList)

            return set(sum(tempFileList, []))
        else:
            return set(filePaths) 
        
    def getFileInfo(self):
        '''
        return: dictionary of all files with their action options 
        '''
        tempDict = {}
        
        for myFile in self.fileAllPaths: 
            try:
                # for files ONLY
                fileExt = os.path.splitext(myFile)[1] 
                fileMode = oct(os.stat(myFile).st_mode)[-3:] #444 == readOnly
                tempDict[myFile] = {"printFile": os.path.exists(myFile),
                                    "expandFile":self.isCompressed(myFile), # can only unCompressed a compressedObj
                                    "convertFile":self.isConvertable(fileExt,fileMode), # check for access permission and fileExt
                                    "openFile":True,
                                    "deleteFile":self.isDeletable(fileExt,fileMode) # same as isConvertable() for now, since we might adjust it later on to make it more specific
                                    }
            except:
                # for folders and invalid filepath 
                tempDict[myFile] = {"printFile":False,
                                    "expandFile":False,
                                    "convertFile":False,
                                    "openFile":False,
                                    "deleteFile":False
                                    }  
    
        return tempDict

    ## check fileInfo ##
    def isReadOnly(self,fileMode):
        ''' 
        return True if file is ReadOnly, otherwise False
        '''
        if fileMode == "444": #readOnly
            return True
        return False

    def isCompressed(self,myFile):
        '''
        return True if file is compressed, otherwise False
        '''
        with open(myFile, 'r') as f:
            try:
                f.read()
                return False
            except:
                return True
    
    def isConvertable(self,fileExt,fileMode):
        '''
        return True if it's a valid file and the file is not locked, other return False
        '''
        if fileExt and not self.isReadOnly(fileMode):
            return True
        return False
    
    def isDeletable(self,fileExt,fileMode):
        '''
        return True if it's a valid file and the file is not locked, other return False
        '''
        if fileExt and not self.isReadOnly(fileMode):
            return True
        return False

    ## ACTIONS ##
    def getSpecificAction(self):
        '''
        print items with specific action = True
        '''
        outputDict = {}
        for i in self.actionDict:
            if self.actionDict[i].get(self.actionType) == True:
                outputDict[i] = self.actionDict[i]
                print("%s:%s" %(i,self.actionDict[i])) #for DISPLAY
        return outputDict

    def getAllAction(self):
        '''
        print state of all actions for all items
        '''
        for i in self.actionDict:
            print("%s:%s" %(i,self.actionDict[i])) #for DISPLAY
        return self.actionDict

    def registerAction(self,filePaths,action=None,recurse=False):
        '''
        register actions, return result in dictionary. "N/A" means action not available
        '''
        outputDict = {}
        processedFile = self.processList(filePaths,action,recurse)
        
        for file in processedFile: 
            #print(file)
            #print(processedFile[file])
            #print(self.actionDict[file])
            try:
                if self.actionDict[file][processedFile[file]] == True:
                    outputDict[file] = processedFile[file]
            except:
                outputDict[file] = "N/A" # action invalid
        
        self.runActions(outputDict)
        return outputDict

    def processList(self,filePath,globalAction,recurse):
        outputDict = {}
        for i in self.getAllPaths(filePath,recurse):
            if type(i) == str:
                if globalAction:
                    outputDict[i] = globalAction
                else:
                    outputDict[i] = "N/A"
            elif type(i) == tuple:
                outputDict[i[0]] = i[1]

        self.fileAllPaths = outputDict.keys()
        self.actionDict = self.getFileInfo()
        return outputDict

    def runActions(self,outputDict):
        '''
        read the outputDict and trigger the right function for each task
        '''
        print("## Action-Results ##")
        for i in outputDict:
            if outputDict[i] == "deleteFile":
                utilMod.deleteFile(i)
            elif outputDict[i] == "openFile":
                utilMod.openFile(i)
            elif outputDict[i] == "compressFile":
                utilMod.compressFile(i)   
            elif outputDict[i] == "expandFile":
                utilMod.expandFile(i)
            elif outputDict[i] == "printFile":
                utilMod.printFile(i)             
        print("#############")
    

    ## for checkExpect ##
    def checkExpectFunc(self,ogFilePaths,actionType):
        '''
        return True if it's a valid file and action is enabled for the file, othewise return False
        '''
        actionDict = self.getFileInfo()  
        if actionType:
            for filePath in ogFilePaths:
                try:
                    return actionDict[filePath][actionType]
                except:
                    return False # NOT IN dictionary

class RegisterOp:
    '''
    {"filepath":["a1","a2"]..}, or ["filepath"..]
    #single action only
    '''
    def __init__(self, filePaths, action=None, recurse = False):
        self.ogFilePath = filePaths
        self.fileAllPaths = QueryOp([i[0] for i in filePaths],recurse).getAllPaths([i[0] for i in filePaths],recurse)
        #print(self.fileAllPaths)
        self.globalAction = action
        self.recurse = recurse

        if self.catchError():
            self.actionDict = QueryOp(self.fileAllPaths,recurse).getFileInfo()
            self.outputDict = self.registerAction(self.fileAllPaths,self.globalAction)

    
    def catchError(self): # need to think of a better func name
        '''
        make sure there's an action assigned for all filePaths. 
        '''
        if str in self.ogFilePath and not self.globalAction:
            print("global Action not specified")
            return False
        else:
            return True
    
    def registerAction(self,fileAllPaths,action=None):
        '''
        register actions, return result in dictionary. "N/A" means action not available
        '''
        for file in fileAllPaths: 
            outputDict = {}
            if type(file) == tuple: # custom specification takes priority
                try:
                    if self.actionDict[file[0]][file[1]] == True:
                       
                        outputDict[file[0]] = file[1]
                    else:
                        outputDict[file[0]] = "N/A" # action invalid
                except:
                    outputDict[file[0]] = "N/A" # note: not work on folders

            else:
                if action:
                    try:
                        if self.actionDict[file][self.globalAction] == True:
                            outputDict[file] = action
                        else:
                            outputDict[file] = "N/A" # action invalid
                    except:
                        outputDict[file] = "N/A"  # note: not work on folders

        return outputDict     

#TODO
#clean up, restruct code if needed
# write readMe
# potential improvements


#### create Class Objs to check file ####
FILEPATH = ["TestData/testFolder/file2.txt"] #single paths
FILEPATHS = ["TestData/testFolder/file2.txt","TestData/testFolder/"] # for multiple Paths
#action opts: openFile, compressFile, unCompressFile, deleteFile, printFile

queryFile = QueryOp(FILEPATHS,recurse=True).getAllAction() #DONE #Query list of actions
print("specific")
specificFile = QueryOp(["TestData/file.txt"],"openFile").getSpecificAction()

S_FILEPATH=[("TestData/testFolder/file2.txt","openFile")] #custom
M_FILEPATHS=["TestData/testFolder/file2.txt","TestData/testFolder/"] #multipleFiles
R_FILEPATH = ["TestData/testFolder"] #recursive

print("registerFile")
#registerFile  = QueryOp(S_FILEPATH).registerAction(R_FILEPATH)
#registerFile  = QueryOp(M_FILEPATHS).registerAction(M_FILEPATHS,action="deleteFile")
#registerFile  = QueryOp(R_FILEPATH).registerAction(R_FILEPATH,action="deleteFile",recurse=True)


### checkExpect ####
'''
#openFile
#unitTest.checkExpect(QueryOp(["TestData/testFolder"],"openFile").checkExpectFunc(["TestData/file.txt"],"openFile"),"openFile",False) #folder

#unCompressFile
unitTest.checkExpect(QueryOp(["TestData/file.txt"],"unCompressFile").checkExpectFunc(["TestData/file.txt"],"unCompressFile"),"unCompressFile",False) #normalFile
unitTest.checkExpect(QueryOp(["TestData/compressedTF"],"unCompressFile").checkExpectFunc(["TestData/compressedTF"],"unCompressFile"),"unCompressFile",False) #normalFolder
unitTest.checkExpect(QueryOp(["TestData/file2.zip"],"unCompressFile").checkExpectFunc(["TestData/file2.zip"],"unCompressFile"),"unCompressFile",True) #compressedFile
unitTest.checkExpect(QueryOp(["TestData/compressedTF.tgz"],"unCompressFile").checkExpectFunc(["TestData/compressedTF.tgz"],"unCompressFile"),"unCompressFile",True) #compressedFolder with different .ext

#convertFile
unitTest.checkExpect(QueryOp(["TestData/testFolder/file3.txt"],"convertFile").checkExpectFunc(["TestData/testFolder/file3.txt"],"convertFile"),"convertFile",False) #readOnlyFile
unitTest.checkExpect(QueryOp(["TestData/testFolder/"],"convertFile").checkExpectFunc(["TestData/testFolder/"],"convertFile"),"convertFile",False) #folder
unitTest.checkExpect(QueryOp(["TestData/testFolder/file.txt"],"convertFile").checkExpectFunc(["TestData/testFolder/file.txt"],"convertFile"),"convertFile",True) #normalFile in subFolder

#deleteFile
unitTest.checkExpect(QueryOp(["TestData/testFolder/file3.txt"],"deleteFile").checkExpectFunc(["TestData/testFolder/file3.txt"],"deleteFile"),"deleteFile",False) #readOnlyFile
unitTest.checkExpect(QueryOp(["TestData/testFolder"],"deleteFile").checkExpectFunc(["TestData/testFolder"],"deleteFile"),"deleteFile",False) #folder

#printFile
unitTest.checkExpect(QueryOp(["TestData/testFolder/file.txt"],"printFile").checkExpectFunc(["TestData/testFolder/file.txt"],"printFile"),"printFile",True) #normalFile
unitTest.checkExpect(QueryOp(["TestData/testFolder"],"printFile").checkExpectFunc(["TestData/testFolder"],"printFile"),"printFile",False) #folder

#getAllPaths(test recurse)
unitTest.checkExpect(QueryOp(["TestData/testFolder"],recurse = True).getAllPaths(["TestData/testFolder"],recurse = True),"getAllPaths",{'TestData/testFolder/file3.zip', 'TestData/testFolder/file2.txt', 'TestData/testFolder/file2.txt.zip', 'TestData/testFolder/file.txt', 'TestData/testFolder/file3.txt'}) #folder
unitTest.checkExpect(QueryOp(["TestData/testFolder/file.txt"],recurse = True).getAllPaths(["TestData/testFolder/file.txt"],recurse = True),"getAllPaths",{'TestData/testFolder/file.txt'}) #folder
unitTest.checkExpect(QueryOp(["TestData/testFolder"]).getAllPaths(["TestData/testFolder"]),"getAllPaths",{'TestData/testFolder'}) #folder
unitTest.checkExpect(QueryOp(["TestData/testFolder/file.txt"]).getAllPaths(["TestData/testFolder/file.txt"]),"getAllPaths",{'TestData/testFolder/file.txt'}) #file

#registerAction
unitTest.checkExpect(QueryOp([("TestData/testFolder",'openFile')]).registerAction([("TestData/testFolder",'openFile')]),"registerAction",{'TestData/testFolder':"N/A"})
unitTest.checkExpect(QueryOp([("TestData/testFolder/file.txt",'deleteFile')]).registerAction([("TestData/testFolder/file.txt",'deleteFile')]),"registerAction",{'TestData/testFolder/file.txt':"deleteFile"})
unitTest.checkExpect(QueryOp(["TestData/testFolder","TestData/testFolder/file.txt"]).registerAction(["TestData/testFolder","TestData/testFolder/file.txt"],"deleteFile"),"registerAction",{'TestData/testFolder':"N/A",'TestData/testFolder/file.txt':"deleteFile"})
unitTest.checkExpect(QueryOp(["TestData/testFolder","TestData/testFolder/file.txt"]).registerAction(["TestData/testFolder","TestData/testFolder/file.txt"],"deleteFile",recurse=True),"registerAction",{'TestData/testFolder/file2.txt.zip': 'deleteFile', 'TestData/testFolder/file2.txt': 'deleteFile', 'TestData/testFolder/file.txt': 'deleteFile', 'TestData/testFolder/file3.txt': 'N/A', 'TestData/testFolder/file3.zip': 'deleteFile'})
'''
