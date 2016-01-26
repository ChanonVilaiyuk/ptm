import sys,platform, os
from datetime import datetime

if platform.system() == 'Windows':
	sys.path.append('O:/studioTools/lib')
	sys.path.append('//10.66.1.12/dsGlobal/studioTools/lib')
else:
	sys.path.append('/Volumes/dsGlobal/studioTools/lib')

from shotgun_api3 import Shotgun

# connection to server
server = 'https://pts.shotgunstudio.com'
script = 'ptTools'
id = 'ec0b3324c1ab54cf4e21c68d18d70f2f347c3cbd'
sg = Shotgun(server, script, id)

print 'PT Shotgun Utils @ O:/studioTools/shotgun/sg_utils.py'

def sgGetProjectInfo(projName) : 
	proj = sg.find_one("Project", [["name", "is", projName]])
	return proj

def sgGetProjects() :
	filters = []
	fields = ['name', 'id'] 
	projects = sg.find('Project', filters, fields)

	return projects 


def sgGetUser(filters, fields) : 
	users = sg.find('HumanUser', filters, fields)

	return users 


def sgGetSteps(filters, fields) : 
	filters = [['entity_type', 'is', entity]]
	fields = ['code', 'id'] 
	steps = sg.find('Step', filters, fields)

	return steps


def sgGetTask(filters, fields) : 
	taskEntities = sg.find('Task', filters, fields)

	return taskEntities


def sgUpdateTask(taskID, data) : 
	return sg.update('Task', taskID, data)