# ImageEnginePython- Python Skill Exercise
Author: Charleen Chu

This module allows user to query and perform actions to files/folders.

## QueryOperation 
User can query a list of possible actions allowed to be performed on a file/folder, multiple files/folders, and files inside folders. User can also query a list of files that allows specific action

Usage Example:
###### All Files and Actions
> DataOperation(["TestData/file.txt,TestData/testFolder"],recurse=True).getAllAction() 

###### Files with specific actions allowed
> DataOperation(["TestData/file.txt,TestData/testFolder"],"openFile").getSpecificAction()

Data is stored in the following format:
> {"file.txt":{"printFile":True, "convertFile":True, "expandFile":False, "deleteFile":False }}

## RegisterOperation 
User can specified an action for each path, or set a set a global action for all paths (unless specified)
To specified action, user will need to but the filePath and the specified action in a tuple. If specific action is not given, user will need set a global action. 

Usage Example:
###### Custom Action
> DataOperation([("TestData/testFolder/file2.txt","openFile")]).registerAction([("TestData/testFolder/file2.txt","openFile")])

###### Global Action
>DataOperation(["TestData/testFolder/file2.txt","TestData/testFolder/"]).registerAction(["TestData/testFolder/file2.txt","TestData/testFolder/"],action="deleteFile",recurse=False)

## Current Limitations
- User can only set 1 global action

## Future Implementation
- features to allow more refined query settings
- features to register multiple actions 







