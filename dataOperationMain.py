import os
import utilMod


class DataOperation:
    def __init__(self, filePaths, action=None, recurse = False):
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
            try:
                if self.actionDict[file][processedFile[file]] == True:
                    outputDict[file] = processedFile[file]
                else:
                    outputDict[file] = "N/A"
            except:
                outputDict[file] = "N/A" # action invalid
        
        #self.runActions(outputDict) 
        return outputDict

    def processList(self,filePath,globalAction,recurse):
        '''
        takes in a list string and/or tuple 
        return a dictionary with its action assigned to the path
        '''
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
 