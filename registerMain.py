import os
from unitTest import checkExpect
import utilMod
import glob
import unitTest

class Registry:
    def __init__(self, keyWord, action=None):
        
        if os.path.exists(keyWord):
            self.filePathList = [keyWord] 
        else:
            self.keyword = keyWord
            self.filePathList = self.getAllPaths() # if no specific filePath, use current Dir

        self.actionType = action
        self.actionDict = self.getFileInfo()

    def getAllPaths(self):
        '''
        take in list of paths, and cursively g
        '''
        testDir = "%s/TestData/" % os.getcwd() #temp for testing

        #print(glob.glob(testDir+ self.keyword))
        return glob.glob(testDir + self.keyword)

        
    def getFileInfo(self):
        '''
        return: dictionary of all files with their action options 
        '''
        tempDict = {}
        for filePath in self.filePathList:
            try:
                # for files ONLY
                fileExt = os.path.splitext(filePath)[1] 
                fileMode = oct(os.stat(filePath).st_mode)[-3:] #444 == readOnly
                tempDict[filePath] = {"printFile": os.path.exists(filePath),
                                    "expandFile":self.isCompressed(filePath), # can only unCompressed a compressedObj
                                    "convertFile":self.isConvertable(fileExt,fileMode), # check for access permission and fileExt
                                    "openFile":not(self.isCompressed(filePath)),# can only open non-compressed file
                                    "deleteFile":self.isDeletable(fileExt,fileMode) # same as isConvertable() for now, since we might adjust it later on to make it more specific
                                    }
            except:
                # for folders and invalid filepath 
                tempDict[filePath] = { "printFile":False,
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


###########################################
    def validateOp(self,filePath):
        '''
        return True if operation available, else return False
        '''
        return self.actionDict[filePath][self.actionType]


    def fetchOp(self):
        '''
        fetch result if given operation is available for the file
        '''
        for filePath in self.filePathList:
            if self.validateOp(filePath):
                print("{} available for {}".format(filePath, self.actionType))
            else:
                print("{} NOT available for {}".format(filePath, self.actionType))
                

    def registerOp(self):
        '''
        register operations
        '''
        for filePath in self.filePathList:
            if self.validateOp(filePath):
                self.run(filePath)
            else:
                print("action fail")
                
    def run(self,filePath):
        if self.actionType == "deleteFile":
            utilMod.deleteFile(filePath)
        elif self.actionType == "openFile":
            utilMod.openFile(filePath)
        elif self.actionType == "compressFile":
            utilMod.compressFile(filePath)   
        elif self.actionType == "expandFile":
            utilMod.expandFile(filePath)
        elif self.actionType == "printFile":
            utilMod.printFile(filePath)             




########## EXAMPLES ##########

print("\n## fetchOp() ##")
Registry("TestData/testFolder/file.txt","openFile").fetchOp() # TestData/testFolder/file.txt available for expandFile
Registry("TestData/testFolder/","openFile").fetchOp() # TestData/testFolder/ NOT available for openFile
Registry("TestData/file2.zip","expandFile").fetchOp() # TestData/file2.zip NOT available for openFile
Registry("TestData/file.txt","expandFile").fetchOp() # TestData/file.txt NOT available for expandFile

Registry("*.txt","expandFile").fetchOp() # /Users/charleenchu/Desktop/tmpDev/IEPython/TestData/file.txt NOT available for expandFile
Registry("*.zip","expandFile").fetchOp() # /Users/charleenchu/Desktop/tmpDev/IEPython/TestData/file2.zip available for expandFile
Registry("*","printFile").fetchOp() 
# /Users/charleenchu/Desktop/tmpDev/IEPython/TestData/file.txt available for printFile
# /Users/charleenchu/Desktop/tmpDev/IEPython/TestData/testFolder NOT available for printFile
# /Users/charleenchu/Desktop/tmpDev/IEPython/TestData/recurseFolder NOT available for printFile
# /Users/charleenchu/Desktop/tmpDev/IEPython/TestData/compressedTF NOT available for printFile
# /Users/charleenchu/Desktop/tmpDev/IEPython/TestData/file2.zip available for printFile
# /Users/charleenchu/Desktop/tmpDev/IEPython/TestData/compressedTF.tgz available for printFile



print("\n## registerOp() ##")
Registry("TestData/testFolder/","openFile").registerOp() # action fail
Registry("TestData/testFolder/file2.txt","openFile").registerOp() # openFile:TestData/testFolder/file2.txt
Registry("TestData/compressedTF.tgz","openFile").registerOp() # action fail
Registry("TestData/compressedTF.tgz","expandFile").registerOp() # expandFile:TestData/compressedTF.tgz

Registry("*.txt","expandFile").registerOp() # action fail
Registry("*.zip","expandFile").registerOp() # expandFile:/Users/charleenchu/Desktop/tmpDev/IEPython/TestData/file2.zip
Registry("*","printFile").registerOp() 
# printFile:/Users/charleenchu/Desktop/tmpDev/IEPython/TestData/file.txt
# action fail
# action fail
# action fail
# printFile:/Users/charleenchu/Desktop/tmpDev/IEPython/TestData/file2.zip
# printFile:/Users/charleenchu/Desktop/tmpDev/IEPython/TestData/compressedTF.tgz