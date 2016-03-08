steps = [{'code': 'Animation', 'type': 'Step', 'id': 5, 'entity_type': 'Shot'},
		{'code': 'Lighting', 'type': 'Step', 'id': 7, 'entity_type': 'Shot'},
		{'code': 'Compositing', 'type': 'Step', 'id': 8, 'entity_type': 'Shot'},
		{'code': 'Art', 'type': 'Step', 'id': 9, 'entity_type': 'Asset'},
		{'code': 'Model', 'type': 'Step', 'id': 10, 'entity_type': 'Asset'},
		{'code': 'Rig', 'type': 'Step', 'id': 11, 'entity_type': 'Asset'},
		{'code': 'Surface', 'type': 'Step', 'id': 12, 'entity_type': 'Asset'},
		{'code': 'Layout', 'type': 'Step', 'id': 13, 'entity_type': 'Shot'},
		# {'code': 'Layout', 'type': 'Step', 'id': 17, 'entity_type': 'Sequence'},
		{'code': 'Render', 'type': 'Step', 'id': 43, 'entity_type': 'Shot'},
		{'code': 'texture', 'type': 'Step', 'id': 49, 'entity_type': 'Asset'},
		{'code': 'TechAnim', 'type': 'Step', 'id': 54, 'entity_type': 'Shot'},
		{'code': 'FX', 'type': 'Step', 'id': 55, 'entity_type': 'Shot'},
		{'code': 'SetDress', 'type': 'Step', 'id': 57, 'entity_type': 'Asset'},
		# {'code': 'General', 'type': 'Step', 'id': 59, 'entity_type': 'Asset'},
		# {'code': '2D', 'type': 'Step', 'id': 60, 'entity_type': 'Shot'},
		{'code': 'Hero', 'type': 'Step', 'id': 70, 'entity_type': 'Asset'}]

stepSgPipeMap = {
					'Animation': 'anim',
					'Lighting': 'light',
					'Compositing': 'comp',
					'Art': 'art',
					'Model': 'model',
					'Rig': 'rig',
					'Surface': 'surface',
					'Layout': 'layout',
					'Render': 'render',
					'texture': 'uv',
					'TechAnim': 'animClean',
					'FX': 'fx',
					'SetDress': 'setdress',
					'Hero': 'hero'
				}

publishMap = {'hi': ['model-model_hi', 'rig-rig_hi', 'rig-rigUV_hi', 'uv-uv_hi', 'surface-shade_hi'], 
				'md': ['model-model_md', 'rig-rig_md', 'rig-rigUV_md', 'uv-uv_md', 'surface-shade_md'], 
				'lo': ['model-model_lo', 'rig-rig_lo', 'rig-rigUV_lo', 'uv-uv_lo', 'surface-shade_lo']
				}