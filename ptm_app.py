#!/usr/bin/env python
# -- coding: utf-8 --

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

from tool.utils import entityInfo2 as entityInfo 
reload(entityInfo)

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

		self.setWindowTitle('PT Shotgun Task Manager v.2.0')

		# start 
		self.start = datetime.now()

		# setup all data variable 
		self.initData()

		# run functions
		self.initFunctions()

		# init signal
		self.initSignal()

		# run after signal
		# self.initFunctionAfterSignal()

		# finish loading data 
		self.finish = datetime.now()
		self.logTime(self.start, self.finish)


	def initData(self) : 
		# icons
		self.logo = '%s/%s' % (os.path.dirname(moduleDir), 'icons/logo.png')
		self.logo2 = '%s/%s' % (os.path.dirname(moduleDir), 'icons/shotgun_logo.png')
		self.okIcon = '%s/%s' % (os.path.dirname(moduleDir), 'icons/ok_icon.png')
		self.xIcon = '%s/%s' % (os.path.dirname(moduleDir), 'icons/x_icon.png')

		self.iconPath = '%s/icons' % os.path.dirname(moduleDir)
		self.iconList = ['Show All', 'Ready to Start', 'In Progress', 'Need Update', 'Daily', 'Approved', 'Pending Client', 'Client Approved']
		self.sgStatusMap = {'all': 'Show All', 'rdy': 'Ready to Start', 'ip': 'In Progress', 'udt': 'Need Update', 'daily': 'Daily', 'noaprv': 'Pending Internal', 'intapr': 'Pending Client', 'aprv': 'Client Approved', 'wtg': 'Waiting to Start'}
		self.sgStatusIcon = {'Show All': {'iconName': 'all_icon.png', 'sg_status_list': 'all'},
								'Ready to Start': {'iconName': 'sg_rdy_icon.png', 'sg_status_list': 'rdy'},
								'In Progress': {'iconName': 'sg_ip_icon.png', 'sg_status_list': 'ip'},
								'Need Update': {'iconName': 'needUpdate.png', 'sg_status_list': 'udt'},
								'Daily': {'iconName': 'daily_icon.png', 'sg_status_list': 'daily'},
								'Pending Internal': {'iconName': 'red_icon.png', 'sg_status_list': 'noaprv'},
								'Pending Client': {'iconName': 'yellow_icon.png', 'sg_status_list': 'intapr'},
								'Client Approved': {'iconName': 'green_icon.png', 'sg_status_list': 'aprv'}, 
								'Waiting to Start': {'iconName': 'wtg_icon.png', 'sg_status_list': 'wtg'}}

		self.stepMap = {'Model': 'model', 'Rig': 'rig', 'texture': 'uv', 'Surface': 'surface'}
		self.extIcon = {'ma': '%s/icons/maya_icon.png' % (os.path.dirname(moduleDir))}

		self.projectFilters = ['Lego_', 'TVC_']
		self.server = 'P:'
		self.entity = {'Shot': 'Shot', 'Asset': 'Asset', 'Sequence': 'Sequence'}
		self.optionVarName = 'ptm'
		self.optionVar = {'data': {'user': '', 'project': '', 'entity': '', 'step': ''}}
		self.sourceFileInfo = dict()

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
		self.setEpisodeUI()
		self.setEntityComboBox()
		self.setStepUI()
		self.setLabelUI()
		self.listContent()
		



	def initFunctionAfterSignal(self) : 
		self.listContent()
		# self.setEntityTypeUI()
		# self.setTaskUI()
		# self.setEntityUI()
		# self.listWorkAreaUI()


	def initSignal(self) : 
		logger.debug('init signal')
		self.ui.refresh_pushButton.clicked.connect(self.refreshUI)
		self.ui.user_comboBox.currentIndexChanged.connect(self.refreshUI)
		# self.ui.status_comboBox.currentIndexChanged.connect(self.setEntityTypeUI)
		self.ui.entity_comboBox.currentIndexChanged.connect(self.entityComboBoxSignal)
		# self.ui.task_listWidget.itemSelectionChanged.connect(self.setProjectUI)
		self.ui.project_comboBox.currentIndexChanged.connect(self.setEpisodeUI)
		self.ui.step_comboBox.currentIndexChanged.connect(self.refreshUI)
		self.ui.episode_comboBox.currentIndexChanged.connect(self.refreshUI)

		self.ui.status_listWidget.itemSelectionChanged.connect(self.setTaskUI)
		self.ui.task_listWidget.itemSelectionChanged.connect(self.setEntityUI)
		self.ui.entities_listWidget.itemSelectionChanged.connect(self.entityListAction)
		# self.ui.work_comboBox.currentIndexChanged.connect(self.listWorkFileUI)

		self.ui.open_pushButton.clicked.connect(self.doOpen)
		self.ui.new_pushButton.clicked.connect(self.doNewFile)
		# self.ui.filter1_checkBox.stateChanged.connect(self.filterAction)
		# self.ui.filter2_checkBox.stateChanged.connect(self.filterAction)
		# self.ui.filter1_comboBox.currentIndexChanged.connect(self.filterAction)
		# self.ui.filter2_comboBox.currentIndexChanged.connect(self.filterAction)
		# self.ui.search_lineEdit.textChanged.connect(self.filterAction)
		
		self.ui.showAll_checkBox.stateChanged.connect(self.showNoteAction)
		# self.ui.list_pushButton.clicked.connect(self.refreshUI)

		self.ui.work_radioButton.clicked.connect(self.listWorkFileUI)
		self.ui.publish_radioButton.clicked.connect(self.listWorkFileUI)
		self.ui.source_radioButton.clicked.connect(self.listWorkFileUI)

		# right click 
		self.ui.work_listWidget.customContextMenuRequested.connect(self.showMenu)
		self.ui.status_label.customContextMenuRequested.connect(self.showMenu2)


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


	def showMenu(self,pos):
		# mode 
		work = self.ui.work_radioButton.isChecked()
		publish = self.ui.publish_radioButton.isChecked()
		sourceFile = self.ui.source_radioButton.isChecked()

		selItem = str(self.ui.work_listWidget.currentItem().text())

		if not '==' in selItem : 
			if publish : 
				if self.ui.work_listWidget.currentItem() : 
					menu=QtGui.QMenu(self)
					# menu.addAction('Rename')
					# menu.addAction('Delete')

					subMenu = QtGui.QMenu('Open', self)
					subMenu.addAction('Open')
					subMenu.addAction('Open as work file')

					subMenu2 = QtGui.QMenu('Import', self)
					subMenu2.addAction('Import')
					subMenu2.addAction('Import to new file')

					subMenu3 = QtGui.QMenu('Reference', self)
					subMenu3.addAction('Reference')
					subMenu3.addAction('Reference to new file')
					# items = self.getPlayblastFile()

					# for each in items : 
					# 	subMenu3.addAction(each)

					menu.addMenu(subMenu)
					menu.addMenu(subMenu2)
					menu.addMenu(subMenu3)

					menu.popup(self.ui.work_listWidget.mapToGlobal(pos))
					result = menu.exec_(self.ui.work_listWidget.mapToGlobal(pos))

					if result : 
						self.menuCommand(result.text(), result.parentWidget().title())


	def showMenu2(self, pos) : 
		path = str(self.ui.path_lineEdit.text())

		if path : 
			if not os.path.exists(path) : 
				menu = QtGui.QMenu(self)
				menu.addAction('Create work dir')

				menu.popup(self.ui.status_label.mapToGlobal(pos))
				result = menu.exec_(self.ui.status_label.mapToGlobal(pos))

				if result.text() == 'Create work dir' : 
					os.makedirs(path)
					self.setLabel(True)



	def menuCommand(self, command, categories) : 
		fileName = str(self.ui.work_listWidget.currentItem().text())
		path = str(self.ui.path_lineEdit.text())
		filePath = self.publishFileMap[fileName]
		asset = entityInfo.info(path)

		if os.path.exists(filePath) : 

			if categories == 'Open' : 
				if command == 'Open' : 
					hook.openFile(filePath)

				if command == 'Open as work file' : 
					workFile = asset.nextVersion(asset.department(), asset.task())
					hook.openFile(filePath)
					hook.saveFile(workFile)
					# print workFile

			if categories == 'Import' : 
				if command == 'Import' : 
					hook.importFile(filePath)

				if command == 'Import to new file' : 
					hook.newFile()
					hook.importFile(filePath)

			if categories == 'Reference' : 
				namespace = asset.name()

				if command == 'Reference' : 
					hook.createReference(namespace, filePath)

				if command == 'Reference to new file' : 
					hook.newFile()
					hook.createReference(namespace, filePath)

		else : 
			self.messageBox('Error', 'File %s not exists' % filePath)



	def initOptionVar(self, data) : 
		value = hook.getOptionVar(self.optionVarName)

		if value == 0 : 
			hook.setOptionVar(self.optionVarName, self.optionVar)


	def setSelectionData(self) : 
		project = str(self.ui.project_comboBox.currentIndex())
		episode = str(self.ui.episode_comboBox.currentIndex())
		user = str(self.ui.user_comboBox.currentIndex())
		entity = str(self.ui.entity_comboBox.currentIndex())
		step = str(self.ui.step_comboBox.currentIndex())

		self.optionVar['data']['project'] = project 
		self.optionVar['data']['episode'] = episode 
		self.optionVar['data']['user'] = user
		self.optionVar['data']['entity'] = entity 
		self.optionVar['data']['step'] = step

		hook.setOptionVar(self.optionVarName, str(self.optionVar))


	def getPreviousSelection(self, data, dataType) : 
		# read optionVar
		logger.debug('get data')
		var = eval(hook.getOptionVar(self.optionVarName))

		if var : 
			if dataType in var['data'].keys() : 
				index = var['data'][dataType]

				if index and index.isdigit() : 
					return int(index)


	def setStatusUI(self) : 

		# add comboBox items
		i = 0
		self.ui.status_listWidget.clear()
		self.ui.task_listWidget.clear()
		self.ui.entities_listWidget.clear()
		self.ui.comment_plainTextEdit.clear()
		self.ui.sourceFiles_listWidget.clear()

		listWidget = 'status_listWidget'

		statuses = ['all']
		statusDict = dict()

		if self.taskInfo : 

			for each in sorted(self.taskInfo.keys()) : 
				sg_status_list = each
				displayStatus = self.sgStatusMap[sg_status_list]
				iconFile = self.sgStatusIcon[displayStatus]['iconName']
				iconPath = '%s/%s' % (self.iconPath, iconFile)
				bgColor = self.widgetColor[0]
				
				show = True 

				if show : 
					count = 0
					for eachTask in self.taskInfo[each] : 
						count += len(self.taskInfo[each][eachTask])

					text2 = '(%s)' % str(count)

					self.addEntityListWidget(listWidget, displayStatus, text2, bgColor, iconPath)

				i += 1

			self.ui.status_listWidget.setCurrentRow(0)


		else : 
			self.addEntityListWidget(listWidget, 'No Data', '', [0, 0, 0], '')


	def listContent(self) : 
		result = self.getTaskInfo()

		if result : 
			self.taskInfo =  result[0]
			self.sgTaskInfo = result[1]
			self.statusInfo = result[2]
			self.setStatusUI()
			self.setTaskUI()
			self.setEntityUI()


	def setEntity(self) : 
		# set filters
		
		# list UI
		self.setEntityUI()


	def getSelStatus(self) : 
		# get status 
		statusListWidget = 'status_listWidget'
		itemStatus = self.getEntityListWidget(statusListWidget)

		if itemStatus : 
			status = self.sgStatusIcon[itemStatus[0]]['sg_status_list']

			return status 

	def getSelTask(self) : 
		# get task 
		taskListWidget = 'task_listWidget'
		task = self.getEntityListWidget(taskListWidget)

		if task : 
			return task[0]

	def getSelEntity(self) : 
		# get entity 
		entityListWidget = 'entities_listWidget'
		entity = self.getEntityListWidget2(entityListWidget)

		return entity



	def setEntityUI(self) : 
		logger.debug('setEntityUI')
		status = self.getSelStatus()
		task = self.getSelTask()
		entityType = str(self.ui.entity_comboBox.currentText())

		self.ui.entities_listWidget.clear()
		self.ui.comment_plainTextEdit.clear()
		self.ui.sourceFiles_listWidget.clear()
		self.ui.work_listWidget.clear()

		searchValue = str(self.ui.search_lineEdit.text())


		# list content 
		i = 0 

		if status in self.taskInfo.keys() : 
			if task in self.taskInfo[status].keys() : 
				entities = self.taskInfo[status][task]

				for eachEntity in entities : 
					entitySub1 = eachEntity['entitySub1']
					entitySub2 = eachEntity['entitySub2']
					sgStatus = eachEntity['status']
					taskName = eachEntity['taskName']
					name = eachEntity['entityName']

					# icon path 
					displayStatus = self.sgStatusMap[sgStatus]
					iconName = self.sgStatusIcon[displayStatus]['iconName']
					iconPath = '%s/%s' % (self.iconPath, iconName)

					# display 
					display = '%s' % name
					color = self.widgetColor[i%2]
					listWidget = 'entities_listWidget'

					show = True

					if searchValue : 
						if not searchValue in name : 
							show = False

					# add items 
					if show : 
						# self.addListWidgetItem(listWidget, display, iconPath, color)
						self.addEntityListWidget2(listWidget, display, entitySub1, entitySub2, color, iconPath, size = 16)

						i += 1 

		displayText = ''
		if entityType == 'Asset' : 
			displayText = 'Asset : %s assets - %s' % (i, task)

		if entityType == 'Shot' : 
			displayText = 'Shot : %s shots - %s' % (i, task)

		self.ui.entity_label.setText(displayText)


	def setTaskUI(self) : 
		logger.debug('setTaskUI')
		# status = self.ui.status_listWidget.currentItem()
		statusListWidget = 'status_listWidget'
		status = self.getSelStatus()

		if status : 
			if status in self.taskInfo.keys() : 
				tasks = self.taskInfo[status].keys()

				self.ui.task_listWidget.clear()
				self.ui.entities_listWidget.clear()
				self.ui.comment_plainTextEdit.clear()
				self.ui.sourceFiles_listWidget.clear()
				self.ui.work_listWidget.clear()

				taskListWidget = 'task_listWidget'
				i = 0

				for each in tasks : 
					taskName = each
					count = len(self.taskInfo[status][taskName])
					text2 = '(%s)' % str(count)
					bgColor = self.widgetColor[i%2]
					iconPath = ''
					self.addEntityListWidget(taskListWidget, taskName, text2, bgColor, iconPath)

					i += 1

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

	def setEpisodeUI(self) : 
		# clear UI
		self.ui.episode_comboBox.clear()
		project = str(self.ui.project_comboBox.currentText())
		self.episodes = self.getEpisodeList(project)

		if self.episodes : 
			for each in sorted(self.episodes) : 
				episode = self.episodes[each]['code']

				# fill comboBox
				self.ui.episode_comboBox.addItem(episode)

		# set selection 
		index = self.getPreviousSelection(self.episodes, 'episode')

		if index : 
			self.ui.episode_comboBox.setCurrentIndex(index)


		

	def setEntityComboBox(self) : 
		self.ui.entity_comboBox.clear()
		self.ui.entity_comboBox.addItems(sorted(self.entity.keys()))

		# set selection 
		index = self.getPreviousSelection(self.entity.keys(), 'entity')

		if index : 
			self.ui.entity_comboBox.setCurrentIndex(index)


	def entityComboBoxSignal(self) : 
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

		# if entity == 'Asset' : 
		# 	self.ui.filter1_checkBox.setText('Type')
		# 	self.ui.filter2_checkBox.setText('SubType')

		# if entity == 'Shot' : 
		# 	self.ui.filter1_checkBox.setText('Episode')
		# 	self.ui.filter2_checkBox.setText('Sequence')



	def entityListAction(self) : 
		# find associate path
		selStatus = self.getSelStatus()
		selTask = self.getSelTask()
		selEntity = self.getSelEntity()
		selProject = str(self.ui.project_comboBox.currentText())
		entityType = str(self.ui.entity_comboBox.currentText())		
		step = str(self.ui.step_comboBox.currentText())
		serverStep = setting.stepSgPipeMap[step]

		entityName = selEntity[0]
		entitySub1 = selEntity[1]
		entitySub2 = selEntity[2]

		self.asset = entityInfo.info2(entityType, selProject, entityName, entitySub1, entitySub2)
		workDir = self.asset.workDir(serverStep, selTask)
		self.asset2 = entityInfo.info(workDir)

		# set UI
		self.ui.path_lineEdit.setText(workDir)
		self.setPathUI(workDir)

		# list work area
		self.listWorkFileUI()

		# list note 
		self.showNoteAction()

		# list source file
		# self.showSourceFile()



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


	# def setFilter(self) : 
	# 	sgEntityInfo = self.sgEntityInfo
	# 	entitiesSub1 = []
	# 	entitiesSub2 = []

	# 	for each in sgEntityInfo : 
	# 		entities = sgEntityInfo[each]

	# 		for eachEntity in entities : 
	# 			entitySub1 = eachEntity['entitySub1']
	# 			entitySub2 = eachEntity['entitySub2']

	# 			if not entitySub1 in entitiesSub1 : 
	# 				entitiesSub1.append(entitySub1)

	# 			if not entitySub2 in entitiesSub2 : 
	# 				entitiesSub2.append(entitySub2)


	# 	self.ui.filter1_comboBox.clear()
	# 	self.ui.filter2_comboBox.clear()
	# 	self.ui.filter1_comboBox.addItems(sorted(entitiesSub1))
	# 	self.ui.filter2_comboBox.addItems(sorted(entitiesSub2))

	# def filterAction(self) : 
	# 	self.setEntityUI()


	# def listWorkAreaUI(self) : 
	# 	# clear UI
	# 	self.ui.work_comboBox.clear()
	# 	self.ui.path_lineEdit.setText('')
	# 	self.ui.work_listWidget.clear()

	# 	sgStatus = self.getStatusUI()
	# 	taskEntity = str(self.ui.entities_comboBox.currentText())

	# 	if self.ui.task_listWidget.currentItem() : 
	# 		task = str(self.ui.task_listWidget.currentItem().text())
	# 		project = str(self.ui.project_comboBox.currentText())

	# 		if self.ui.entities_listWidget.currentItem() : 
	# 			entity = str(self.ui.entities_listWidget.currentItem().text())

	# 			if taskEntity == 'Asset' : 
	# 				entity1 = self.entities[entity]['entitySub1']
	# 				entity2 = self.entities[entity]['entitySub2']
	# 				entityName = self.entities[entity]['entityName']
	# 				step = self.entities[entity]['step']
	# 				stepDisplay = self.stepMap[step]
	# 				path = self.getEntityPath(taskEntity, project, entity1, entity2, entityName, step, task)
	# 				logger.debug('setPath %s' % path)

	# 			if taskEntity == 'Shot' : 
	# 				entity1 = self.entities[entity]['entitySub1']
	# 				entity2 = self.entities[entity]['entitySub2']
	# 				entityName = self.entities[entity]['entityName']
	# 				step = self.entities[entity]['step']
	# 				path = self.getEntityPath(taskEntity, project, entity1, entity2, entityName, step, task)
	# 				logger.debug('setPath %s' % path)

	# 			logger.debug(path)
	# 			self.ui.path_lineEdit.setText(path)
	# 			self.setPathUI(path)

	# 			if os.path.exists(path) : 
	# 				dirs = fileUtils.listFolder(path)
	# 				self.setWorkAreaComboBox(dirs)

	# 			logger.debug('listWorkAreaUI 	%s %s %s %s %s' % (sgStatus, taskEntity, task, project, entity))


	def listWorkFileUI(self) : 
		# clear UI
		self.ui.work_listWidget.clear()

		# mode 
		work = self.ui.work_radioButton.isChecked()
		publish = self.ui.publish_radioButton.isChecked()
		sourceFile = self.ui.source_radioButton.isChecked()

		self.publishFileMap = dict()

		listWidget = 'work_listWidget'
		
		if work : 
			# hide new button 
			self.ui.new_pushButton.setEnabled(True)

			path = str(self.ui.path_lineEdit.text())
			# workArea = str(self.ui.work_comboBox.currentText()) 

			files = fileUtils.listFile(path)

			self.listFileListWidget(listWidget, files)

		if publish : 
			# hide new button 
			self.ui.new_pushButton.setEnabled(False) 
			self.ui.open_pushButton.setText('Open As')

			step = self.stepMap[str(self.ui.step_comboBox.currentText())]
			task = self.getSelTask()
			key = '%s-%s' % (step, task)
			colorMap = [[20, 0, 0], [0, 20, 0], [0, 0, 20]]
			colorMap = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

			i = 0 
			for each in setting.publishMap : 
				keyList = setting.publishMap[each]
				displayList = []
				colorShift = colorMap[i%3]

				if key in keyList : 
					for eachKey in keyList : 
						eStep = eachKey.split('-')[0]
						eTask = eachKey.split('-')[-1]
						publishDir = self.asset.publishDir(eStep, eTask)
						
						displayList.append('== %s ==' % eachKey)
						filenames = []

						if os.path.exists(publishDir) : 
							files = fileUtils.listFile(publishDir, 'ma')
							# filenames = [os.path.basename(a) for a in files]
							displayList = displayList + files

							for eachFile in files : 
								self.publishFileMap.update({eachFile: '%s/%s' % (publishDir, eachFile)})

						if not filenames : 
							displayList.append('No File')

					self.listFileListWidget(listWidget, displayList, colorShift = colorShift) 

				i += 1 
			
			
		if sourceFile : 
			# hide new button 
			self.ui.new_pushButton.setEnabled(False)

			self.showSourceFile()

		# print work, publish, sourceFile 


	def listFileListWidget(self, listWidget, items, colorShift = [0, 0, 0]) : 
		i = 0

		if items : 
			for each in items : 
				ext = each.split('.')[-1]
				iconPath = ''
				bgColor = self.widgetColor[i%2]
				bgColor = [bgColor[0] + colorShift[0], bgColor[1] + colorShift[1], bgColor[2] + colorShift[2]]
				# print bgColor

				if ext in self.extIcon.keys() : 
					iconPath = self.extIcon[ext]
				# self.ui.work_listWidget.addItem(each)
				self.addListWidgetItem(listWidget, each, iconPath, bgColor)

				i += 1

		else : 
			self.addListWidgetItem(listWidget, 'No file', '', [0, 0, 0])



	def doOpen(self) : 
		# mode 
		work = self.ui.work_radioButton.isChecked()
		publish = self.ui.publish_radioButton.isChecked()
		sourceFile = self.ui.source_radioButton.isChecked()

		if self.ui.work_listWidget.currentItem() : 
			path = str(self.ui.path_lineEdit.text())
			fileName = str(self.ui.work_listWidget.currentItem().text())
			filePath = '%s/%s' % (path, fileName)
			
			if work : 
				# workArea = str(self.ui.work_comboBox.currentText()) 

				if os.path.exists(filePath) : 
					hook.openFile(filePath)

					# set task status 
					ipCheckBox = self.ui.ip_checkBox.isChecked()
					setTask = True

					if not ipCheckBox : 
						result = self.messageBox2('Confirm Dialog', 'Set task status to "in progress"?')

						if not result == QtGui.QMessageBox.Yes : 
							setTask = False

					if setTask : 
						result2 = self.setTaskStatus()

				else : 
					title = 'Error'
					description = 'File not found %s' % filePath
					self.messageBox(title, description)

			if publish : 
				if fileName in self.publishFileMap.keys() : 
					path = self.publishFileMap[fileName]

					if os.path.exists(path) : 
						hook.openFile(path)

					else : 
						title = 'Error'
						description = 'File not found %s' % filePath
						self.messageBox(title, description)

				else : 
					logger.debug('%s not in kyes' % fileName)

			if sourceFile : 
				fileName = str(self.ui.work_listWidget.currentItem().text())
				if fileName in self.sourceFileInfo.keys() : 
					path = self.sourceFileInfo[fileName]

					if os.path.exists(path) : 
						hook.openFile(path)

					else : 
						self.messageBox('Warning', 'File %s not exists' % path)



	def doNewFile(self) : 
		hook.newFile()
		step = str(self.ui.step_comboBox.currentText())
		task = self.getSelTask()
		name = self.asset.nextVersion(step, task)
		logger.info(name)
		hook.saveFile(name)
		self.listWorkFileUI()
		# print name




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


	def setPathUI(self, path) : 
		if os.path.exists(path) : 
			self.setLabel(True)
			dirs = fileUtils.listFolder(path)

		else : 
			self.setLabel(False)
			logger.info('%s not exists' % path)


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


	def getEpisodeList(self, project) : 
		filters = [['project.Project.name', 'is', project]]
		fields = ['id', 'code']
		episodeEntities = sgUtils.sg.find('Scene', filters, fields)

		episodes = {'-': {'code': '-'}}

		for each in episodeEntities : 
			episode = each['code']
			episodes.update({episode: each})

		return episodes


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
		sgTaskInfo = dict()
		statusInfo = dict()

		if taskInfo : 
			for each in taskInfo : 
				status = each['sg_status_list']
				taskName = each['content']
				taskID = each['id']
				entity = each['entity']
				step = each['step']
				entities = dict()

				entityName = str()

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
						entities.update({'entityName': entityName, 'entitySub1': entitySub1, 'entitySub2': entitySub2, 'status': status, 'step': step, 'taskID': taskID, 'taskName': taskName, 'status': status})
						# entities = {'name': displayName, 'status': status}

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

						entities.update({'entityName': entityName, 'entitySub1': entitySub1, 'entitySub2': entitySub2, 'status': status, 'step': step, 'taskID': taskID, 'taskName': taskName, 'status': status})
						# entities = {'name': displayName, 'status': status}
				
				statuses = [status, 'all']

				for eachStatus in statuses : 
					if eachStatus in infoDict.keys() : 
						if taskName in infoDict[eachStatus].keys() : 
							infoDict[eachStatus][taskName].append(entities)

						else : 
							infoDict[eachStatus].update({taskName: [entities]})

					else : 
						infoDict.update({eachStatus: {taskName: [entities]}})

				# taskInfo 
				if entityName in sgTaskInfo.keys() : 
					if taskName in sgTaskInfo[entityName] : 
						sgTaskInfo[entityName][taskName] = each

					else : 
						sgTaskInfo[entityName].update({taskName: each})

				else : 
					sgTaskInfo.update({entityName: {taskName: each}})



		return [infoDict, sgTaskInfo, statusInfo]


	def getTaskEntities(self) : 
		# get filters 
		user = str(self.ui.user_comboBox.currentText())
		userEntity = self.allSgUsers[user]

		project = str(self.ui.project_comboBox.currentText())
		projectEntity = self.projects[project]

		episode = str(self.ui.episode_comboBox.currentText())
		if episode in self.episodes.keys() : 
			episodeEntity = self.episodes[episode]

			step = str(self.ui.step_comboBox.currentText())

			if step in self.steps.keys() : 
				stepEntity = self.steps[step]

				filters = self.taskFilters(userEntity, projectEntity, episodeEntity, stepEntity)
				fields = self.taskFields()
				taskEntities = sgUtils.sgGetTask(filters, fields)

				return taskEntities



	def taskFilters(self, userEntity, projectEntity, episodeEntity, stepEntity) : 
		entity = str(self.ui.entity_comboBox.currentText())
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

		if not episodeEntity['code'] == '-' : 

			if entity == 'Asset' : 
				filters.append(['entity.Asset.scenes', 'is', episodeEntity])

			if entity == 'Shot' : 
				filters.append(['entity.Shot.sg_scene', 'is', episodeEntity])		

		return filters


	def taskFields(self) : 
		fields = ['content', 'entity', 'step', 'project', 'sg_status_list', 'sg_workfile']
		assetFields = ['entity.Asset.code', 'entity.Asset.sg_asset_type', 'entity.Asset.sg_subtype', 'entity.Asset.scenes']
		shotFields = ['entity.Shot.code', 'entity.Shot.sg_sequence', 'entity.Shot.sg_scene', 'entity.Shot.sg_scene']

		fields = fields + assetFields
		fields = fields + shotFields 

		return fields


	def setTaskStatus(self) : 
		taskEntity = self.getCurrentTaskEntity()

		taskID = taskEntity['id']
		data = {'sg_status_list': 'ip'}

		result = sgUtils.sgUpdateTask(taskID, data)
		self.refreshUI()

		logger.debug(result)

		return result


	def showNoteAction(self) : 
		showNote = self.ui.note_checkBox.isChecked()
		showAll = self.ui.showAll_checkBox.isChecked()

		if showNote : 
			notes = self.noteData(showAll = showAll)
			texts = []

			if notes : 
				for each in sorted(notes.keys()) : 
					text1 = 'Subject : %s' % notes[each]['subject']
					text2 = '- %s' % notes[each]['content']
					texts.append(text1)
					texts.append(text2)
					texts.append('-------------------------------------------')

				rawText = ('\n').join(texts)
				text = self.translateUTF8(rawText)
				self.ui.comment_plainTextEdit.setPlainText(text)

			else : 
				text = 'No note'
				self.ui.comment_plainTextEdit.setPlainText(text)


	def noteData(self, showAll = True) : 
		notes = self.getSgNote()
		selTask = self.getSelTask()
		data = dict()

		if notes : 
			i = 0
			for each in notes : 
				tasks = each['tasks']
				show = True
				for task in tasks : 
					taskName = task['name']

					if not showAll : 
						if not taskName == selTask : 
							show = False

				if show : 
					content = each['content']
					subject = each['subject']
					data[i] = {'subject': subject, 'content': content}

					i += 1 

		return data

	def translateUTF8(self, text) : 
		return QtGui.QApplication.translate("taskManager", text, None, QtGui.QApplication.UnicodeUTF8)
				

	def getSgNote(self) : 
		taskEntity = self.getCurrentTaskEntity()

		if taskEntity : 
			if 'entity' in taskEntity.keys() : 
				entity = taskEntity['entity']

				filters = [['note_links', 'is', entity]]
				fields = ['tasks', 'content', 'subject']

				result = sgUtils.sg.find('Note', filters, fields)
				return result 


	def showSourceFile(self) : 
		logger.debug('show source file')
		self.ui.work_listWidget.clear()

		taskEntity = self.getCurrentTaskEntity()
		filePaths = []
		displayFilePaths = []

		if taskEntity : 
			if taskEntity['sg_workfile'] : 
				filePaths = [taskEntity['sg_workfile']['local_path_windows']]
				displayFilePaths = [os.path.basename(a) for a in filePaths]

				if filePaths : 
					for each in filePaths : 
						self.sourceFileInfo.update({os.path.basename(each): each})

		self.listFileListWidget('work_listWidget', displayFilePaths)


	def getCurrentTaskEntity(self) : 
		selStatus = self.getSelStatus()
		selTask = self.getSelTask()
		selEntity = self.getSelEntity()

		if selEntity : 
			entityName = selEntity[0]

			if entityName in self.sgTaskInfo.keys() : 
				if selTask in self.sgTaskInfo[entityName].keys() : 
					taskEntity = self.sgTaskInfo[entityName][selTask]
					return taskEntity


		



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
		self.ui.logo2_label.setPixmap(QtGui.QPixmap(self.logo2).scaled(200, 60, QtCore.Qt.KeepAspectRatio))
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


	def addEntityListWidget(self, listWidget, text1, text2, bgColor, iconPath) : 
		myCustomWidget = customWidget.customQWidgetItem()
		myCustomWidget.setText1(text1)
		myCustomWidget.setText2(text2)

		myCustomWidget.setTextColor1([200, 200, 200])
		myCustomWidget.setTextColor2([120, 120, 120])

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

		if customWidget : 
			text1 = customWidget.text1()
			text2 = customWidget.text2()

			return [text1, text2]


	def addEntityListWidget2(self, listWidget, text1, text2, text3, bgColor, iconPath, size) : 
		myCustomWidget = customWidget.customQWidgetItem2()
		myCustomWidget.setText1(text1)
		myCustomWidget.setText2(text2)
		myCustomWidget.setText3(text3)

		myCustomWidget.setTextColor1([200, 200, 200])
		myCustomWidget.setTextColor2([120, 120, 120])
		myCustomWidget.setTextColor3([120, 120, 120])

		myCustomWidget.setIcon(iconPath, size)

		item = eval('QtGui.QListWidgetItem(self.ui.%s)' % listWidget)
		item.setSizeHint(myCustomWidget.sizeHint())
		item.setBackground(QtGui.QColor(bgColor[0], bgColor[1], bgColor[2]))


		eval('self.ui.%s.addItem(item)' % listWidget)
		eval('self.ui.%s.setItemWidget(item, myCustomWidget)' % listWidget)


	def getEntityListWidget2(self, listWidget) : 
		item = eval('self.ui.%s.currentItem()' % listWidget)

		if item : 
			customWidget = eval('self.ui.%s.itemWidget(item)' % listWidget)
			text1 = customWidget.text1()
			text2 = customWidget.text2()
			text3 = customWidget.text3()

			return [text1, text2, text3]


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


	def messageBox2(self, title, description) : 
		# result = QtGui.QMessageBox.question(self,title,description ,QtGui.QMessageBox.AcceptRole, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
		result = QtGui.QMessageBox.question(self,title,description ,QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

		return result



	def logTime(self, start, finish) : 
		duration = finish - start 
		logger.info('===================')
		logger.info(str(duration))



class userDialog(QtGui.QDialog, MyForm):

	def __init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = dialog.Ui_Dialog()
		self.ui.setupUi(self)

		self.result = None
		self.users = getAllSgUser()
		self.setLocalUser()
		self.setUser()
		self.ui.setUser_pushButton.clicked.connect(self.assignLocalUser)


	def setUser(self) : 
		self.ui.user_listWidget.clear()

		for user in sorted(self.users) : 
			self.ui.user_listWidget.addItem(user)


	def setLocalUser(self) : 
		self.ui.localUser_lineEdit.setText(thisUser())

	def assignLocalUser(self) : 
		user = str(self.ui.localUser_lineEdit.text())
		if self.ui.user_listWidget.currentItem() : 
			sgUser = str(self.ui.user_listWidget.currentItem().text())

			userEntity = self.users[sgUser]
			userID = userEntity['id']
			data = {'sg_localuser': user}

			self.result = sgUtils.sg.update('HumanUser', userID, data)

			logger.debug('Assigned result')
			logger.debug(self.result)

			super(userDialog, self).accept()


	def returnValue(self) : 
		return self.result


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