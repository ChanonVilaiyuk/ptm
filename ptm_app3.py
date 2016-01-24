#
#Import python modules
import sys, os, re
import subprocess

from datetime import datetime

sys.path.append('O:/studioTools/tools')
sys.path.append('O:/studioTools/shotgun')
sys.path.append('O:/studioTools')
sys.path.append('O:/studioTools/lib')
sys.path.append('O:/studioTools/maya/python')
sys.path.append('O:/globalMaya/resources/PyQt_Pt')

# Import GUI
from qtshim import QtCore, QtGui
from qtshim import Signal
from qtshim import wrapinstance

from ptm import ui
from ptm import customWidget
from ptm import userDialog as dialog
reload(ui)
reload(dialog)
reload(customWidget)

from ptm import mayaHook as hook 
reload(hook)

from ptm import config, setting
reload(config)
reload(setting)

from ptm import ptm_sg as sgUtils
reload(sgUtils)

from tool.utils import fileUtils
reload(fileUtils)

from tool.utils import customLog
logger = customLog.customLog()
logger.setLevel(customLog.DEBUG)

moduleDir = sys.modules[__name__].__file__

# If inside Maya open Maya GUI

def getMayaWindow():
	ptr = mui.MQtUtil.mainWindow()

	if ptr is None:
		raise RuntimeError('No Maya window found.')

	window = wrapinstance(ptr)
	assert isinstance(window, QtGui.QMainWindow)
	return window

import maya.OpenMayaUI as mui
getMayaWindow()


class MyForm(QtGui.QMainWindow):

	def __init__(self, parent=None):
		self.count = 0
		#Setup Window
		super(MyForm, self).__init__(parent)
		self.ui = ui.Ui_taskManager()
		self.ui.setupUi(self)

		# start 
		self.start = datetime.now()

		# setup all data variable 
		self.initData()

		# run functions
		self.initFunctions()

		# init signal
		self.initSignal()

		# run after signal
		self.initFunctionAfterSignal()

		# finish loading data 
		self.finish = datetime.now()
		self.logTime(self.start, self.finish)


	def initData(self) : 
		# icons
		self.logo = '%s/%s' % (os.path.dirname(moduleDir), 'icons/logo.png')
		self.okIcon = '%s/%s' % (os.path.dirname(moduleDir), 'icons/ok_icon.png')
		self.xIcon = '%s/%s' % (os.path.dirname(moduleDir), 'icons/x_icon.png')

		self.iconPath = '%s/icons' % os.path.dirname(moduleDir)
		self.iconList = ['Show All', 'Ready to Start', 'In Progress', 'Need Update', 'Daily', 'Approved', 'Waiting for Client', 'Client Approved']
		self.sgStatusMap = {'all': 'Show All', 'rdy': 'Ready to Start', 'ip': 'In Progress', 'udt': 'Need Update', 'daily': 'Daily', 'noaprv': 'Approved', 'intapr': 'Waiting for Client', 'aprv': 'Client Approved'}
		self.sgStatusIcon = {'Show All': {'iconName': 'all_icon.png', 'sg_status_list': 'all'},
								'Ready to Start': {'iconName': 'sg_rdy_icon.png', 'sg_status_list': 'rdy'},
								'In Progress': {'iconName': 'sg_ip_icon.png', 'sg_status_list': 'ip'},
								'Need Update': {'iconName': 'needUpdate.png', 'sg_status_list': 'udt'},
								'Daily': {'iconName': 'daily_icon.png', 'sg_status_list': 'daily'},
								'Approved': {'iconName': 'red_icon.png', 'sg_status_list': 'noaprv'},
								'Waiting for Client': {'iconName': 'yellow_icon.png', 'sg_status_list': 'intapr'},
								'Client Approved': {'iconName': 'green_icon.png', 'sg_status_list': 'aprv'}}

		self.stepMap = {'Model': 'model', 'Rig': 'rig', 'texture': 'uv', 'Surface': 'shade'}
		self.extIcon = {'ma': '%s/icons/maya_icon.png' % (os.path.dirname(moduleDir))}

		self.projectFilters = ['Lego_', 'TVC_']
		self.server = 'P:'
		self.entity = {'Shot': 'Shot', 'Asset': 'Asset', 'Sequence': 'Sequence'}
		self.optionVarName = 'ptm'
		self.optionVar = {'data': {'user': '', 'project': '', 'entity': '', 'step': ''}}

		self.widgetColor = [[0, 0, 0], [20, 20, 20]]

		self.allSgUsers = None
		self.user = os.environ['USERNAME']
		self.projectConfig = 'P:/.config/projectConfig'
		self.episodeConfig = 'P:/.config/episodeConfig'

		self.initOptionVar(self.optionVar)


	def initFunctions(self) : 
		# setup initial ui
		self.setUI()

		# list all data in ui 
		self.setProjectUI()
		self.setEntityUI()
		self.setStepUI()
		self.setLabelUI()


	def initFunctionAfterSignal(self) : 
		self.listContent()
		# self.setEntityTypeUI()
		# self.setTaskUI()
		# self.setEntityUI()
		# self.listWorkAreaUI()


	def initSignal(self) : 
		logger.debug('init signal')
		self.ui.user_comboBox.currentIndexChanged.connect(self.refreshUI)
		# self.ui.status_comboBox.currentIndexChanged.connect(self.setEntityTypeUI)
		self.ui.entity_comboBox.currentIndexChanged.connect(self.entitySignal)
		# self.ui.task_listWidget.itemSelectionChanged.connect(self.setProjectUI)
		self.ui.project_comboBox.currentIndexChanged.connect(self.refreshUI)
		self.ui.step_comboBox.currentIndexChanged.connect(self.refreshUI)
		self.ui.status_listWidget.itemSelectionChanged.connect(self.setTaskUI)
		self.ui.task_listWidget.itemSelectionChanged.connect(self.listEntity)
		# self.ui.work_comboBox.currentIndexChanged.connect(self.listWorkFileUI)
		# self.ui.open_pushButton.clicked.connect(self.doOpen)
		# self.ui.filter1_checkBox.stateChanged.connect(self.filterAction)
		# self.ui.filter2_checkBox.stateChanged.connect(self.filterAction)
		# self.ui.filter1_comboBox.currentIndexChanged.connect(self.filterAction)
		# self.ui.filter2_comboBox.currentIndexChanged.connect(self.filterAction)
		# self.ui.list_pushButton.clicked.connect(self.refreshUI)


	def setUI(self) : 
		self.setUser()
		self.setLogo()
		# self.setStatusUI()


	def refreshUI(self) : 
		self.listContent()
		self.setSelectionData()
		# self.setEntityTypeUI()


	def setUser(self) : 
		logger.debug('setUser ...')

		self.allSgUsers = getAllSgUser()
		allSgUsers = self.allSgUsers
		self.ui.user_comboBox.clear()

		i = 0 
		userIndex = 0
		foundUser = False

		for user in sorted(allSgUsers) : 
			localUser = allSgUsers[user]['localuser']
			thisuser = thisUser()

			if localUser : 
				if localUser.lower() == thisuser.lower() : 
					userIndex = i
					foundUser = True
					logger.debug('found user %s' % localUser)
			
			self.ui.user_comboBox.addItem(user)

			i += 1 

		if not foundUser : 
			dialog = userDialog()
			result = dialog.exec_()
			value = dialog.returnValue()

			if value : 
				userIndex = self.setUser()

		self.ui.user_comboBox.setCurrentIndex(userIndex)

		return userIndex



	def initOptionVar(self, data) : 
		value = hook.getOptionVar(self.optionVarName)

		if value == 0 : 
			hook.setOptionVar(self.optionVarName, self.optionVar)


	def setSelectionData(self) : 
		project = str(self.ui.project_comboBox.currentIndex())
		user = str(self.ui.user_comboBox.currentIndex())
		entity = str(self.ui.entity_comboBox.currentIndex())
		step = str(self.ui.step_comboBox.currentIndex())

		self.optionVar['data']['project'] = project 
		self.optionVar['data']['user'] = user
		self.optionVar['data']['entity'] = entity 
		self.optionVar['data']['step'] = step

		hook.setOptionVar(self.optionVarName, str(self.optionVar))



	def getPreviousSelection(self, data, dataType) : 
		# read optionVar
		logger.debug('get data')
		var = eval(hook.getOptionVar(self.optionVarName))

		if var : 
			index = var['data'][dataType]

			if index and index.isdigit() : 
				return int(index)


	def setStatusUI(self) : 
		# add comboBox items
		i = 0
		self.ui.status_listWidget.clear()
		listWidget = 'status_listWidget'

		for each in self.taskInfo.keys() : 
			sg_status_list = each
			displayStatus = self.sgStatusMap[sg_status_list]
			iconFile = self.sgStatusIcon[displayStatus]['iconName']
			iconPath = '%s/%s' % (self.iconPath, iconFile)
			bgColor = [0, 0, 0]
			text2 = '()'
			size = 14
			self.addEntityListWidget(listWidget, displayStatus, text2, bgColor, iconPath, size)

		# self.ui.status_listWidget.addItems(sorted(self.taskInfo.keys()))
		# logger.debug('setCurrentRow')
		self.ui.status_listWidget.setCurrentRow(0)

		



# 	def setStatusListUI(self, sgStatus, i) : 
# 		if sgStatus in self.sgStatusMap.keys() : 
# 			text = self.sgStatusMap[sgStatus]
# 			iconName = self.sgStatusIcon[text]['iconName']
# 			iconPath = '%s/%s' % (self.iconPath, iconName)

# 			self.addComboBoxItem(i, text, iconPath)

# 			return True 




	def listContent(self) : 
		self.taskInfo = self.getTaskInfo()
		self.setStatusUI()


	def listEntity(self) : 
		self.ui.entities_listWidget.clear()
		listWidget = 'status_listWidget'
		itemStatus = self.getEntityListWidget(listWidget)[0]
		status = self.sgStatusIcon[itemStatus]['sg_status_list']
		task = str(self.ui.task_listWidget.currentItem().text())
		print self.taskInfo

		if task in self.taskInfo[status].keys() : 
			entityInfo = self.taskInfo[status][task]

			for each in sorted(entityInfo) : 
				name = each

				sgStatus = entityInfo[each]['status']
				displayStatus = self.sgStatusMap[sgStatus]
				iconName = self.sgStatusIcon[displayStatus]['iconName']
				iconPath = '%s/%s' % (self.iconPath, iconName)

				display = '%s' % name
				color = [0, 0, 0]
				listWidget = 'entities_listWidget'
				self.addListWidgetItem(listWidget, display, iconPath, color)





# 	def setEntityTypeUI(self) : 

# 		sgStatus = self.getStatusUI()

# 		# clear UI
# 		self.ui.entities_comboBox.clear()
# 		self.ui.task_listWidget.clear()
# 		self.ui.project_comboBox.clear()
# 		self.ui.entities_listWidget.clear()
# 		self.ui.work_comboBox.clear()
# 		self.ui.path_lineEdit.setText('')
# 		self.ui.work_listWidget.clear()

# 		if sgStatus in sorted(self.taskInfo.keys()) : 
# 			for each in self.taskInfo[sgStatus].keys() : 
# 				self.ui.entities_comboBox.addItem(each)

# 			logger.debug('setEntityUI 	%s' % sgStatus)


	def setTaskUI(self) : 
		logger.debug('setTaskUI')
		# status = self.ui.status_listWidget.currentItem()
		listWidget = 'status_listWidget'
		itemStatus = self.getEntityListWidget(listWidget)[0]
		status = self.sgStatusIcon[itemStatus]['sg_status_list']

		if status : 
			tasks = self.taskInfo[status].keys()

			self.ui.task_listWidget.clear()
			self.ui.task_listWidget.addItems(tasks)
			self.ui.task_listWidget.setCurrentRow(0)



	def setProjectUI(self) : 
		# clear UI
		self.ui.project_comboBox.clear()
		self.projects = self.getProjectList()
		projects = [a for a in sorted(self.projects)]

		self.ui.project_comboBox.addItems(sorted(projects))

		# set selection 
		index = self.getPreviousSelection(projects, 'project')

		if index : 
			self.ui.project_comboBox.setCurrentIndex(index)
		

	def setEntityUI(self) : 
		self.ui.entity_comboBox.clear()
		self.ui.entity_comboBox.addItems(sorted(self.entity.keys()))

		# set selection 
		index = self.getPreviousSelection(self.entity.keys(), 'entity')

		if index : 
			self.ui.entity_comboBox.setCurrentIndex(index)


	def entitySignal(self) : 
		self.setStepUI()
		self.setLabelUI()


	def setStepUI(self) : 
		entity = str(self.ui.entity_comboBox.currentText())
		steps = setting.steps
		self.ui.step_comboBox.clear()
		entitySteps = []
		self.steps = dict()

		for each in steps : 
			name = each['code']

			if each['entity_type'] == entity : 
				entitySteps.append(name)

			self.steps.update({name: each})

		self.ui.step_comboBox.addItems(sorted(entitySteps))

		# set selection
		index = self.getPreviousSelection(entitySteps, 'step')

		if index : 
			self.ui.step_comboBox.setCurrentIndex(index)





	def setLabelUI(self) : 
		entity = str(self.ui.entity_comboBox.currentText())

		if entity == 'Asset' : 
			self.ui.filter1_checkBox.setText('Type')
			self.ui.filter2_checkBox.setText('SubType')

		if entity == 'Shot' : 
			self.ui.filter1_checkBox.setText('Episode')
			self.ui.filter2_checkBox.setText('Sequence')




# 	def setEntityUICmd(self) : 

# 		entityInfo = self.entityInfo
# 		# clear UI
# 		self.ui.entities_listWidget.clear()
# 		self.ui.work_comboBox.clear()
# 		self.ui.path_lineEdit.setText('')
# 		self.ui.work_listWidget.clear()

# 		i = 0

# 		for each in sorted(entityInfo) : 
# 			entityName = each['entityName']
# 			entitySub1 = each['entitySub1']
# 			entitySub2 = each['entitySub2']
# 			displayName = each['displayName']
# 			status = each['status']

# 			# self.ui.entities_listWidget.addItem(displayName)
# 			# self.addEntityListWidget(displayName, entitySub1, entitySub2, bgColor, iconPath, size)
# 			iconFile = self.sgStatusIcon[self.sgStatusMap[status]]['iconName']
# 			iconPath = '%s/%s' % (self.iconPath, iconFile)
# 			bgColor = self.widgetColor[i%2]
# 			size = 16
# 			listWidget = 'entities_listWidget'

# 			# filter area 
# 			filter1 = str(self.ui.filter1_comboBox.currentText())
# 			filter2 = str(self.ui.filter2_comboBox.currentText())
# 			display1 = True
# 			display2 = True

# 			if self.ui.filter1_checkBox.isChecked() : 
# 				display1 = False 

# 				if filter1 == entitySub1 : 
# 					display1 = True

# 			if self.ui.filter2_checkBox.isChecked() : 
# 				display2 = False 

# 				if filter2 == entitySub2 : 
# 					display2 = True 

# 			# display area 
# 			if display1 and display2 : 
# 				self.addListWidgetItem(listWidget, displayName, iconPath, bgColor)

# 				i += 1


# 	def setFilter(self, entityType) : 

# 		entityInfo = self.entityInfo
# 		logger.debug('set filter')
# 		# clear UI
# 		self.ui.filter1_comboBox.clear()
# 		self.ui.filter2_comboBox.clear()

# 		filter1 = []
# 		filter2 = []

# 		if entityType == 'Asset' : 
# 			self.ui.filter1_checkBox.setText('Type')
# 			self.ui.filter2_checkBox.setText('Sub Type')

# 		if entityType == 'Shot' : 
# 			self.ui.filter1_checkBox.setText('Episode')
# 			self.ui.filter2_checkBox.setText('Sequence')

# 		for each in sorted(entityInfo) : 
# 			entitySub1 = each['entitySub1']
# 			entitySub2 = each['entitySub2']

# 			print entitySub1, entitySub2

# 			if not entitySub1 in filter1 : 
# 				filter1.append(entitySub1)
				
# 			if not entitySub2 in filter2 : 
# 				filter2.append(entitySub2)	

# 		for each in sorted(filter1) : 
# 			self.ui.filter1_comboBox.addItem(each)

# 		for each in sorted(filter2) : 
# 			self.ui.filter2_comboBox.addItem(each)		


# 	def filterAction(self) : 
# 		self.setEntityUICmd()


# 	def listWorkAreaUI(self) : 
# 		# clear UI
# 		self.ui.work_comboBox.clear()
# 		self.ui.path_lineEdit.setText('')
# 		self.ui.work_listWidget.clear()

# 		sgStatus = self.getStatusUI()
# 		taskEntity = str(self.ui.entities_comboBox.currentText())

# 		if self.ui.task_listWidget.currentItem() : 
# 			task = str(self.ui.task_listWidget.currentItem().text())
# 			project = str(self.ui.project_comboBox.currentText())

# 			if self.ui.entities_listWidget.currentItem() : 
# 				entity = str(self.ui.entities_listWidget.currentItem().text())

# 				if taskEntity == 'Asset' : 
# 					entity1 = self.entities[entity]['entitySub1']
# 					entity2 = self.entities[entity]['entitySub2']
# 					entityName = self.entities[entity]['entityName']
# 					step = self.entities[entity]['step']
# 					stepDisplay = self.stepMap[step]
# 					path = self.getEntityPath(taskEntity, project, entity1, entity2, entityName, step, task)
# 					logger.debug('setPath %s' % path)

# 				if taskEntity == 'Shot' : 
# 					entity1 = self.entities[entity]['entitySub1']
# 					entity2 = self.entities[entity]['entitySub2']
# 					entityName = self.entities[entity]['entityName']
# 					step = self.entities[entity]['step']
# 					path = self.getEntityPath(taskEntity, project, entity1, entity2, entityName, step, task)
# 					logger.debug('setPath %s' % path)

# 				logger.debug(path)
# 				self.ui.path_lineEdit.setText(path)
# 				self.setPathUI(path)

# 				if os.path.exists(path) : 
# 					dirs = fileUtils.listFolder(path)
# 					self.setWorkAreaComboBox(dirs)

# 				logger.debug('listWorkAreaUI 	%s %s %s %s %s' % (sgStatus, taskEntity, task, project, entity))


# 	def listWorkFileUI(self) : 
# 		# clear UI
# 		self.ui.work_listWidget.clear()

# 		path = str(self.ui.path_lineEdit.text())
# 		workArea = str(self.ui.work_comboBox.currentText()) 

# 		browsePath = '%s/%s' % (path, workArea)

# 		files = fileUtils.listFile(browsePath)
# 		listWidget = 'work_listWidget'

# 		i = 0

# 		for each in files : 
# 			ext = each.split('.')[-1]
# 			iconPath = ''
# 			bgColor = self.widgetColor[i%2]

# 			if ext in self.extIcon.keys() : 
# 				iconPath = self.extIcon[ext]
# 				print iconPath
# 			# self.ui.work_listWidget.addItem(each)
# 			self.addListWidgetItem(listWidget, each, iconPath, bgColor)

# 			i += 1



# 	def doOpen(self) : 
# 		path = str(self.ui.path_lineEdit.text())
# 		workArea = str(self.ui.work_comboBox.currentText()) 
# 		if self.ui.work_listWidget.currentItem() : 
# 			fileName = str(self.ui.work_listWidget.currentItem().text())
# 			filePath = '%s/%s/%s' % (path, workArea, fileName)

# 			if os.path.exists(filePath) : 
# 				hook.openFile(filePath)

# 			else : 
# 				title = 'Error'
# 				description = 'File not found %s' % filePath
# 				self.messageBox(title, description)



# 	def setWorkAreaComboBox(self, lists) : 
# 		default = 'work'
# 		self.ui.work_comboBox.clear() 

# 		i = 0 
# 		index = 0 
# 		for each in lists : 
# 			if each == default : 
# 				index = i 

# 			self.ui.work_comboBox.addItem(each)

# 			i += 1 

# 		self.ui.work_comboBox.setCurrentIndex(index)


# 	def setPathUI(self, path) : 
# 		if os.path.exists(path) : 
# 			self.setLabel(True)
# 			dirs = fileUtils.listFolder(path)

# 		else : 
# 			self.setLabel(False)
# 			logger.info('%s not exists' % path)



	def getProjectList(self) : 
		sgProjects = sgUtils.sgGetProjects()
		svProjects = fileUtils.listFolder(self.server)
		projects = dict()

		for each in sgProjects : 
			projName = each['name']

			for eachFilter in self.projectFilters : 
				if eachFilter in projName and projName in svProjects : 
					projects.update({projName: {'type': 'Project', 'id': each['id']}})

		return projects 

# 	def getStatusUI(self) : 
# 		status = str(self.ui.status_comboBox.currentText())

# 		if status in self.sgStatusIcon.keys() : 
# 			sgStatus = self.sgStatusIcon[status]['sg_status_list']

# 			return sgStatus


	def getTaskInfo(self) : 
		logger.debug('get task entities')
		start = datetime.now()

		# get task
		taskInfo = self.getTaskEntities()
		logger.debug('%s' % (datetime.now() - start))

		infoDict = dict()

		for each in taskInfo : 
			status = each['sg_status_list']
			taskName = each['content']
			entity = each['entity']
			entities = dict()

			if entity : 
				entityType = entity['type']

				if entityType == 'Asset' : 
					assetName = each['entity.Asset.code']
					assetType = each['entity.Asset.sg_asset_type']
					assetSubType = each['entity.Asset.sg_subtype']
					entityName = assetName
					entitySub1 = assetType
					entitySub2 = assetSubType
					displayName = assetName
					# entities.update({displayName: {'entityName': entityName, 'entitySub1': entitySub1, 'entitySub2': entitySub2, 'status': status}})
					entities = {displayName: {'status': status}}

				if entityType == 'Shot' : 
					shotName = each['entity.Shot.code']
					sequenceName = each['entity.Shot.sg_sequence']
					episodeName = each['entity.Shot.sg_scene']
					entityName = shotName
					displayName = shotName

					if episodeName : 
						entitySub1 = episodeName['name']
						# episodeCode = self.getEpisodeCode(episodeName['name'])

					if sequenceName : 
						entitySub2 = sequenceName['name']

					# entities.update({displayName: {'entityName': entityName, 'entitySub1': entitySub1, 'entitySub2': entitySub2, 'status': status}})
					entities = {displayName: {'status': status}}
			
			if not status in infoDict.keys() : 
				infoDict.update({status: {taskName: entities}})

			else : 
				if not taskName in infoDict[status].keys() : 
					infoDict[status].update({taskName: entities})

				else : 
					infoDict[status][taskName].update(entities)

			

		return infoDict 


	def addAll(self) : 
		allDict = dict()
		for each in self.taskInfo : 
			taskName = self.taskInfo[each]

			for eachTask in taskName : 
				if not eachTask in allDict : 
					allDict.update({eachTask: taskName[eachTask]})

				else : 
					allDict[eachTask].update(taskName[eachTask])


	def getTaskEntities(self) : 
		# get filters 
		user = str(self.ui.user_comboBox.currentText())
		userEntity = self.allSgUsers[user]

		project = str(self.ui.project_comboBox.currentText())
		projectEntity = self.projects[project]

		step = str(self.ui.step_comboBox.currentText())
		if step in self.steps.keys() : 
			stepEntity = self.steps[step]

			filters = self.taskFilters(userEntity, projectEntity, stepEntity)
			fields = self.taskFields()
			taskEntities = sgUtils.sgGetTask(filters, fields)

			return taskEntities



	def taskFilters(self, userEntity, projectEntity, stepEntity) : 
		filters = [['task_assignees', 'is', userEntity], ['step', 'is', stepEntity], ['project', 'is', projectEntity]]
		advancedFilter1 = { 
							"filter_operator": "any", 
							"filters": [ 
							["sg_status_list", "is", "ip"], 
							["sg_status_list", "is", "rdy"], 
							["sg_status_list", "is", "wtg"], 
							["sg_status_list", "is", "aprv"], 
							["sg_status_list", "is", "noaprv"], 
							["sg_status_list", "is", "intapr"], 
							["sg_status_list", "is", "udt"], 
							["sg_status_list", "is", "daily"], 
							] 
						}

		filters.append(advancedFilter1)

		return filters


	def taskFields(self) : 
		fields = ['content', 'entity', 'step', 'project', 'sg_status_list']
		assetFields = ['entity.Asset.code', 'entity.Asset.sg_asset_type', 'entity.Asset.sg_subtype']
		shotFields = ['entity.Shot.code', 'entity.Shot.sg_sequence', 'entity.Shot.sg_scene']

		fields = fields + assetFields
		fields = fields + shotFields 

		return fields



		



# 	def getEntityPath(self, taskEntity, project, entity1, entity2, entityName, step, task) : 
		
# 		path = str() 
# 		dept = str()
# 		subDir = str()
# 		if taskEntity == 'Asset' : 
# 			if step == 'Model' : 
# 				dept = 'model' 
# 				subDir = task 

# 			if step == 'Rig' : 
# 				dept = 'rig' 
# 				subDir = 'maya'

# 			if step == 'texture' : 
# 				dept = 'uv'
# 				subDir = 'maya' 

# 			if step == 'Surface' : 
# 				dept = 'shade' 
# 				subDir = 'maya' 


# 			path = 'P:/%s/asset/3D/%s/%s/%s/%s/%s' % (project, entity1, entity2, entityName, dept, subDir)

# 		if taskEntity == 'Shot' : 
# 			subDir = 'scenes'
			
# 			if step == 'Animation' : 
# 				dept = 'anim'

# 			if step == 'TechAnim' : 
# 				dept = 'animClean'

# 			if step == 'Lighting' : 
# 				dept = 'light'

# 			if step == 'Layout' : 
# 				dept = 'layout'

# 			if step == 'FX' : 
# 				dept = 'fx'

# 			path = 'P:/%s/film/%s/%s/%s/%s/%s' % (project, entity1, entity2, entityName, dept, subDir)

# 		return path 



# 	def findTaskEntities(self) : 
# 		user = str(self.ui.user_comboBox.currentText())
# 		status = str(self.ui.status_comboBox.currentText())

# 		userEntity = self.allSgUsers[user]
# 		# all task
# 		# sgStatus = self.sgStatusIcon[status]['sg_status_list']
# 		sgStatus = ''
# 		fields = ['content', 'entity', 'step', 'project', 'sg_status_list']
# 		assetFields = ['entity.Asset.code', 'entity.Asset.sg_asset_type', 'entity.Asset.sg_subtype']
# 		shotFields = ['entity.Shot.code', 'entity.Shot.sg_sequence', 'entity.Shot.sg_scene']

# 		fields = fields + assetFields
# 		fields = fields + shotFields 

# 		filters = [['task_assignees', 'is', userEntity], ['step', 'is_not', {'type': 'Step', 'id': 43}]]
# 		advancedFilter1 = { 
# 							"filter_operator": "any", 
# 							"filters": [ 
# 							["sg_status_list", "is", "ip"], 
# 							["sg_status_list", "is", "rdy"], 
# 							# ["sg_status_list", "is", "wtg"], 
# 							["sg_status_list", "is", "aprv"], 
# 							["sg_status_list", "is", "noaprv"], 
# 							["sg_status_list", "is", "intapr"], 
# 							["sg_status_list", "is", "udt"], 
# 							["sg_status_list", "is", "daily"], 
# 							] 
# 						} 

# 		# active project 
# 		projects = config.activeProject
# 		subFilters = []

# 		for each in projects : 
# 			subFilters.append(["project.Project.name", "is", "%s" % each])

# 		advancedFilter2 = { 
# 							"filter_operator": "any", 
# 							"filters": subFilters
# 						}

# 		filters.append(advancedFilter1)
# 		filters.append(advancedFilter2)

# 		# taskEntities = sgUtils.sgGetTask(userEntity, sgStatus, fields)
# 		taskEntities = sgUtils.sgGetTask(filters, fields)

# 		return taskEntities



# 	def getProjectCode(self, project) : 
# 		f = open(self.projectConfig, 'r')
# 		data = f.readlines()
# 		f.close() 

# 		projectCode = str()

# 		for line in data : 
# 			projectName = line.split(':')[0]
# 			id = line.split(':')[1]
# 			shortCode = line.split(':')[2]
# 			frameRate = line.split(':')[3]

# 			if projectName == project : 
# 				projectCode = shortCode 

# 		return projectCode 


# 	def getEpisodeCode(self, episode) : 
# 		f = open(self.episodeConfig, 'r')
# 		data = f.readlines()
# 		f.close() 

# 		episodeCode = str() 

# 		for line in data : 
# 			projectName = line.split(':')[0]
# 			episodeName = line.split(':')[1]
# 			id = line.split(':')[2]
# 			shortCode = line.split(':')[3].replace('\r\n', '')

# 			if episodeName == episode : 
# 				episodeCode = shortCode

# 		return episodeCode 


	# UI area 
	def setLogo(self) : 
		self.ui.logo_label.setPixmap(QtGui.QPixmap(self.logo).scaled(200, 60, QtCore.Qt.KeepAspectRatio))
		# self.ui.logo2_label.setPixmap(QtGui.QPixmap(self.logo2).scaled(200, 60, QtCore.Qt.KeepAspectRatio))

	# add widget area
	def setLabel(self, img) : 
		iconPath = self.xIcon
		
		if img : 
			iconPath = self.okIcon

		self.ui.status_label.setPixmap(QtGui.QPixmap(iconPath).scaled(16, 16, QtCore.Qt.KeepAspectRatio))


	def addComboBoxItem(self, i, text, iconPath) : 
		self.ui.status_comboBox.addItem(text)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.ui.status_comboBox.setItemIcon(i, icon)


	def addEntityListWidget(self, listWidget, text1, text2, bgColor, iconPath, size) : 
		myCustomWidget = customWidget.customQWidgetItem()
		myCustomWidget.setText1(text1)
		myCustomWidget.setText2(text2)
		# myCustomWidget.setText3(text3)

		myCustomWidget.setTextColor1([200, 200, 200])
		myCustomWidget.setTextColor2([120, 120, 120])
		# myCustomWidget.setTextColor3([120, 120, 120])

		# myCustomWidget.setIcon(iconPath, size)

		item = eval('QtGui.QListWidgetItem(self.ui.%s)' % listWidget)
		item.setSizeHint(myCustomWidget.sizeHint())
		item.setBackground(QtGui.QColor(bgColor[0], bgColor[1], bgColor[2]))

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(iconPath),QtGui.QIcon.Normal,QtGui.QIcon.Off)
		item.setIcon(icon)

		eval('self.ui.%s.addItem(item)' % listWidget)
		eval('self.ui.%s.setItemWidget(item, myCustomWidget)' % listWidget)


	def getEntityListWidget(self, listWidget) : 
		item = eval('self.ui.%s.currentItem()' % listWidget)
		customWidget = eval('self.ui.%s.itemWidget(item)' % listWidget)
		text1 = customWidget.text1()
		text2 = customWidget.text2()

		return [text1, text2]


	def addListWidgetItem(self, listWidget, text, iconPath, color) : 
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(iconPath),QtGui.QIcon.Normal,QtGui.QIcon.Off)
		cmd = 'QtGui.QListWidgetItem(self.ui.%s)' % listWidget
		item = eval(cmd)
		item.setIcon(icon)
		item.setText(text)
		item.setBackground(QtGui.QColor(color[0], color[1], color[2]))
		size = 90

		cmd2 = 'self.ui.%s.setIconSize(QtCore.QSize(%s, %s))' % (listWidget, size, size)
		eval(cmd2)
		# QtGui.QApplication.processEvents()


	def messageBox(self, title, description) : 
		# result = QtGui.QMessageBox.question(self,title,description ,QtGui.QMessageBox.AcceptRole, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
		result = QtGui.QMessageBox.question(self,title,description ,QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)

		return result



	def logTime(self, start, finish) : 
		duration = finish - start 
		logger.info('===================')
		logger.info(str(duration))



# class userDialog(QtGui.QDialog, MyForm):

# 	def __init__(self, parent = None):
# 		QtGui.QDialog.__init__(self, parent)
# 		self.ui = dialog.Ui_Dialog()
# 		self.ui.setupUi(self)

# 		self.result = None
# 		self.users = getAllSgUser()
# 		self.setLocalUser()
# 		self.setUser()
# 		self.ui.setUser_pushButton.clicked.connect(self.assignLocalUser)


# 	def setUser(self) : 
# 		self.ui.user_listWidget.clear()

# 		for user in sorted(self.users) : 
# 			self.ui.user_listWidget.addItem(user)


# 	def setLocalUser(self) : 
# 		self.ui.localUser_lineEdit.setText(thisUser())

# 	def assignLocalUser(self) : 
# 		user = str(self.ui.localUser_lineEdit.text())
# 		if self.ui.user_listWidget.currentItem() : 
# 			sgUser = str(self.ui.user_listWidget.currentItem().text())

# 			userEntity = self.users[sgUser]
# 			userID = userEntity['id']
# 			data = {'sg_localuser': user}

# 			self.result = sgUtils.sg.update('HumanUser', userID, data)

# 			logger.debug('Assigned result')
# 			logger.debug(self.result)

# 			super(userDialog, self).accept()


# 	def returnValue(self) : 
# 		return self.result


def getAllSgUser() : 
	filters = []
	fields = ['name', 'id', 'sg_localuser']
	users = sgUtils.sgGetUser(filters, fields)
	userInfo = dict()

	for user in users : 
		name = user['name']
		id = user['id']
		localName = user['sg_localuser']
		entityType = user['type']

		userInfo.update({name: {'type': entityType, 'id': id, 'localuser': localName}})

	return userInfo 


def thisUser() : 
	return hook.thisUser()
# 	# return 'Ob'