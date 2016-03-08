import maya.cmds as mc
import maya.mel as mm 

def thisUser() : 
	return mc.optionVar(q = 'PTuser')

def setOptionVar(name, data) : 
	mc.optionVar(sv=(name, str(data)) )

def getOptionVar(name) : 
	return mc.optionVar(q = name)

def newFile() : 
	mc.file(new = True, f = True)

def openFile(fileName) : 
	result = mc.file(fileName, f = True, ignoreVersion = True, o = True) 
	return result 

def saveFile(fileName) : 
	mc.file(rename = fileName)
	mc.file(save = True, type = 'mayaAscii', f = True)

def createReference(namespace, path) : 
	result = mc.file(path, reference = True, ignoreVersion = True, gl = True, loadReferenceDepth = 'all', namespace = namespace, options = 'v=0')

def importFile(file) : 
	return mc.file(file,  i = True, type = 'mayaAscii', options = 'v=0', pr = True, loadReferenceDepth = 'all')

def newFile() : 
	mc.file(force=True , new=True )