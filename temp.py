taskInfo = [{'entity.Asset.sg_subtype': 'main', 'entity.Shot.sg_sequence': None, 'entity.Asset.sg_asset_type': 'character', 'entity.Shot.sg_scene': None, 'entity': {'type': 'Asset', 'id': 9599, 'name': 'aaa_asset'}, 'project': {'type': 'Project', 'id': 180, 'name': 'Lego_Pipeline'}, 'step': {'type': 'Step', 'id': 10, 'name': 'Model'}, 'sg_status_list': 'aprv', 'entity.Asset.code': 'aaa_asset', 'content': 'model_md', 'type': 'Task', 'id': 152301, 'entity.Shot.code': None}, {'entity.Asset.sg_subtype': 'main', 'entity.Shot.sg_sequence': None, 'entity.Asset.sg_asset_type': 'character', 'entity.Shot.sg_scene': None, 'entity': {'type': 'Asset', 'id': 9599, 'name': 'aaa_asset'}, 'project': {'type': 'Project', 'id': 180, 'name': 'Lego_Pipeline'}, 'step': {'type': 'Step', 'id': 10, 'name': 'Model'}, 'sg_status_list': 'aprv', 'entity.Asset.code': 'aaa_asset', 'content': 'model_hi', 'type': 'Task', 'id': 152309, 'entity.Shot.code': None}, {'entity.Asset.sg_subtype': 'generic', 'entity.Shot.sg_sequence': None, 'entity.Asset.sg_asset_type': 'character', 'entity.Shot.sg_scene': None, 'entity': {'type': 'Asset', 'id': 13171, 'name': 'prj_assetName'}, 'project': {'type': 'Project', 'id': 180, 'name': 'Lego_Pipeline'}, 'step': {'type': 'Step', 'id': 10, 'name': 'Model'}, 'sg_status_list': 'aprv', 'entity.Asset.code': 'prj_assetName', 'content': 'model_hi', 'type': 'Task', 'id': 227793, 'entity.Shot.code': None}, {'entity.Asset.sg_subtype': 'generic', 'entity.Shot.sg_sequence': None, 'entity.Asset.sg_asset_type': 'character', 'entity.Shot.sg_scene': None, 'entity': {'type': 'Asset', 'id': 13376, 'name': 'sgi_old'}, 'project': {'type': 'Project', 'id': 180, 'name': 'Lego_Pipeline'}, 'step': {'type': 'Step', 'id': 10, 'name': 'Model'}, 'sg_status_list': 'rdy', 'entity.Asset.code': 'sgi_old', 'content': 'model_md', 'type': 'Task', 'id': 231537, 'entity.Shot.code': None}]

info = dict()
info2 = dict()
info3 = dict()
for each in taskInfo : 
	taskName = each['content']
	status = each['sg_status_list']
	assetName = each['entity.Asset.code']
	entities = {assetName: {'status': status, 'task': taskName}}
	# print entities
	
	if not status in info.keys() : 
		info.update({status: {taskName: entities}})

		
	else  :
		if not taskName in info[status].keys() : 
			info[status].update({taskName: entities})
			
		else : 
			info[status][taskName].update(entities)


	if not 'all' in info2.keys() : 
		info2.update({'all': {taskName: entities}})
		
	else  :
		if not taskName in info2['all'].keys() : 
			info2['all'].update({taskName: entities})
			
		else : 
			info2['all'][taskName].update(entities)
			
for each in taskInfo : 
	taskName = each['content']
	status = each['sg_status_list']
	assetName = each['entity.Asset.code']
	entities = {assetName: {'status': status, 'task': taskName}}
			
	if not 'all' in info3.keys() : 
		info3.update({'all': {taskName: entities}})
		
	else  :
		if not taskName in info3['all'].keys() : 
			info3['all'].update({taskName: entities})
			
		else : 
			info3['all'][taskName].update(entities)


print '============================'
print info['aprv']['model_md']
print info2['all']['model_md']
print info3['all']['model_md']