#!/usr/bin/env python
# -- coding: utf-8 --
import sys
sys.path.append('O:/studioTools/shotgun')
import sg_utils as sgUtils
filters = [['project.Project.name', 'is', 'Lego_Pipeline']]
fields = ['subject', 'content']
notes = sgUtils.sg.find('Note', filters, fields)

for each in notes : 
	text = each['content']
	print text