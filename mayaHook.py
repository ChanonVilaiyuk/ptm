import maya.cmds as mc
import maya.mel as mm 

def thisUser() : 
	return mc.optionVar(q = 'PTuser')


def openFile(fileName) : 
	result = mc.file(fileName, f = True, ignoreVersion = True, o = True) 

	return result 


def setOptionVar(name, data) : 
	mc.optionVar(sv=(name, str(data)) )


def getOptionVar(name) : 
	return mc.optionVar(q = name)

def newFile() : 
	mc.file(new = True, f = True)

def saveFile(fileName) : 
	mc.file(rename = fileName)
	mc.file(save = True, type = 'mayaAscii', f = True)