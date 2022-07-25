import os

class ReadFile:
    def __init__(self, filePaths, action=None):
        self.fileAllPaths = self.getAllPaths(filePaths) #list of paths
        self.actionType = action
        self.actionDict = self.getFileInfo()  

    def getAllPaths(self,filePaths):
        '''
        take in list of paths, and cursively g
        '''
        tempFileList = []
        for eachPath in filePaths:
            '''
            # for recursive files in nested folders 
            if os.path.isdir(eachPath):
                # get all files recursively
                nFileList = [os.path.join(dirPath, file) for dirPath, dirName, filenames in os.walk(eachPath) for file in filenames if os.path.splitext(file)[1] != '']
            else:
                nFileList = [eachPath]
            '''
            tempFileList.append(eachPath)
        
        return set(tempFileList)

    def getFileInfo(self):
        '''
        return: dictionary of all files with their action options 
        '''
        tempDict = {}

        for myFile in self.fileAllPaths: 
            try:
                # for files
                fileExt = os.path.splitext(myFile)[1] 
                fileMode = oct(os.stat(myFile).st_mode)[-3:] #444 == readOnly
                tempDict[myFile] = { "printFile": os.path.exists(myFile),
                                    "unCompressFile":self.isCompressed(), # can only unCompressed a compressedObj
                                    "convertFile":self.isConvertable(fileExt,fileMode), # check for access permission and fileExt
                                    "openFile":True,
                                    "deleteFile":self.isDeletable(fileExt,fileMode) # same as isConvertable() for now, since we might adjust it later on to make it more specific
                                    }
                
            except:
                # for folders and invalid filepath
                tempDict[myFile] = { "printFile":False,
                                    "compressFile":False,
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

    def isCompressed(self):
        '''
        return True if file is compressed, otherwise False
        '''
        with open(self.filePath, 'r') as f:
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
    def runFunc(self):
        '''
        return True if it's a valid file and action is enabled for the file, othewise return False
        '''
        if self.actionType:
            try:
                return self.actionDict[self.filePath][self.actionType]
            except:
                return False

        return "Undefined actionType"


    def queryActionFunc(self):
        '''
        return a dictionary of the actions state for the file
        '''
        try:
            return self.actionDict
        except:
            return "Invalid File Type"
    
    def registerActionFunc(self): #TODO
        '''
        register the actions for the filePath
        '''
        # get self.actionDict and check if "proposed" actions are doable
        # update(maybe create) and applyDict 
        #return applyDict
        pass


#### create Class Objs to check file ####
FILEPATH = ["TestData/testFolder/file2.txt"] #single paths
FILEPATHS = ["TestData/testFolder/file2.txt","TestData/testFolder/"] # for multiple Paths
#action opts: openFile, compressFile, unCompressFile, deleteFile, printFile
#myFile = ReadFile(FILEPATH,"unCompressFile") 
##print(myFile.runFunc()) #result
queryFile = ReadFile(FILEPATHS,False)
print(queryFile.queryActionFunc())
registerFile = ReadFile(FILEPATHS,"unCompressFile") #Does this need to be a dict? to store actions
print(queryFile.registerActionFunc())



##### UNIT TEST #####
TESTDATA_FILEPATH = "TestData/testFolder/file2.zip"
def checkExpect(inputObj,inputAction,expectedVal):
    '''
    inputArg = ReadFile("TestData/file.txt",Action)
    '''
    if ReadFile(inputObj,inputAction).runFunc() == expectedVal:
        print("<PASS> %s: %s" % (inputAction,inputObj))
    else:
        print("<FAIL> %s: %s" % (inputAction,inputObj))

'''
#openFile
checkExpect("TestData/file.txt","openFile",True) #normalFile
checkExpect("TestData/testFolder","openFile",False) #folder

#unCompressFile
checkExpect("TestData/file.txt","unCompressFile",False) #normalFile
checkExpect("TestData/compressedTF","unCompressFile",False) #normalFolder
checkExpect("TestData/file2.zip","unCompressFile",True) #compressedFile
checkExpect("TestData/compressedTF.tgz","unCompressFile",True) #compressedFolder with different .ext

#convertFile
checkExpect("TestData/testFolder/file3.txt","convertFile",False) #readOnlyFile
checkExpect("TestData/testFolder/","convertFile",False) #folder
checkExpect("TestData/testFolder/file.txt","convertFile",True) #normalFile in subFolder

#deleteFile
checkExpect("TestData/testFolder/file3.txt","deleteFile",False) #readOnlyFile
checkExpect("TestData/testFolder","deleteFile",False) #folder

#printFile
checkExpect("TestData/testFolder/file.txt","printFile",True) #normalFile
checkExpect("TestData/testFolder","openFile",False) #folder
'''




# do we also want it to work on folders? or just files