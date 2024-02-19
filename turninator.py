import re
from flask import json
import logging
#logging configuration
logging.basicConfig(datefmt='%H:%M:%S',
                    level=logging.DEBUG)
from data import AIF

class Turninator():
	def __init__(self) -> None:
		pass
	
	def dialog_turns(self,text: str) -> str:
		''' use regex to convert input text into dialog turns

		'''
		text = re.sub('<.*?>','',text, flags=re.DOTALL)
		return re.findall(r'([A-Za-z ]+): (.+\n)', text)

	def monolog_text(self, text: str) -> str:
		''' get the entire text if monolog
		'''
		text = re.sub('<.*?>','',text, flags=re.DOTALL)
		return text
	
	def is_json(self, file: str) -> bool:		
		''' check if the file is valid json
		'''

		try:
			json.loads(open(file).read())
		except ValueError as e:			
			return False

		return True

	def turninator_default(self, path):
		extended_json_aif = {}
		if path.endswith("json"):		
			is_json_file = self.is_json(path)
			nodes, edges, locutions, json_aif  = [], [], [], {}
			if is_json_file: 
				data =  open(path).read()					
				extended_json_aif = json.loads(data)
				if 'AIF' in extended_json_aif and 'text' in extended_json_aif:
					json_dict = extended_json_aif['AIF'] # gets the AIF section
					dialog = extended_json_aif.get('dialog',False)
					OVA = extended_json_aif.get('OVA',[])
					if isinstance(json_dict,str):
						logging.info('is str {}'.format(json_dict))
						if json_dict.startswith('"'):
							logging.info('starts with " {}'.format(json_dict))
							json_dict = json_dict.replace("\"", "")
							json_dict = dict(json_dict)
							logging.info('json dumps {}'.format(json_dict))

					logging.info(f'processing monolog text')
					logging.info('input type {}'.format(type(json_dict)))
					logging.info('json dumps {}'.format(json_dict))

					if not isinstance(json_dict,dict):
						json_dict = json.loads(json_dict)

					logging.info('input type {}'.format(type(json_dict)))
					logging.info('json dumps {}'.format(json_dict))
					schemefulfillments = json_dict.get('schemefulfillments')
					descriptorfulfillments = json_dict.get('descriptorfulfillments')
					participants = json_dict.get("participants",[])
					if isinstance(extended_json_aif['text'],dict):
						text = extended_json_aif['text']['txt']
					else:
						text = extended_json_aif['text'] # gets the text
						text = text+"\n"

					logging.info(' text {}'.format(text))
					if  isinstance(text,str):
						json_object = json.dumps(text)
						json_object = json.loads(json_object)					
					logging.info(' text {}'.format(text))
					is_dialog  = extended_json_aif.get('dialog')
					text_with_span = ""
					node_id,person_id = 0, 0			
					speakers_and_turns = self.dialog_turns(text)

					if is_dialog and len(self.dialog_turns(text)):
						speakers_and_turns = self.dialog_turns(text)
						nodes, locutions, participants, text_with_span, node_id, person_id = AIF.create_turn_entry(
							nodes,node_id, person_id, text_with_span, speakers_and_turns, locutions, participants, is_dialog)
					else:  #monolog
						if not is_dialog:
							logging.info(f'processing monolog text')
							speakers_and_turns = self.monolog_text(text)
							nodes, locutions, participants, text_with_span, node_id, person_id = AIF.create_turn_entry(
								nodes, node_id, person_id, text_with_span,speakers_and_turns, locutions, participants, is_dialog)
					json_aif.update( {'nodes' : nodes} )
					json_aif.update( {'edges' : edges} )
					json_aif.update( {'locutions' : locutions} )
					json_aif.update( {'schemefulfillments' : schemefulfillments} )
					json_aif.update( {'descriptorfulfillments' : descriptorfulfillments} )
					json_aif.update( {'participants' : participants} )
					extended_json_aif['AIF'] = json_aif
					extended_json_aif['text'] = {'txt':text_with_span}					
					extended_json_aif['OVA'] = OVA
					extended_json_aif['dialog'] = dialog
					return json.dumps(extended_json_aif)

				else:
					if 'text' in extended_json_aif:
						node_id,person_id = 0, 0
						if isinstance(extended_json_aif['text'], dict):
							text = extended_json_aif['text']['txt']
						else:
							text = extended_json_aif['text']+"\n"
						
						json_aif, OVA = {}, {}		
						text_with_span=""
						nodes, edges, schemefulfillments, descriptorfulfillments, participants, locutions =[], [], [], [], [], []
						speakers_and_turns = self.monolog_text(text)					
						nodes, locutions, participants, text_with_span, node_id, person_id = AIF.create_turn_entry(
							nodes, node_id, person_id, text_with_span, speakers_and_turns, locutions, participants,	False)
						json_aif.update( {'nodes' : nodes} )
						json_aif.update( {'edges' : edges} )
						json_aif.update( {'locutions' : locutions} )
						json_aif.update( {'schemefulfillments' : schemefulfillments} )
						json_aif.update( {'descriptorfulfillments' : descriptorfulfillments} )
						json_aif.update( {'participants' : participants} )
						extended_json_aif['AIF'] = json_aif
						extended_json_aif['OVA'] = OVA
						extended_json_aif['dialog'] = False
						extended_json_aif['text'] = {'txt':text_with_span}
						return json.dumps(extended_json_aif)

			else:
				logging.info(f'the file is not in a correct json format')
				return("Invalid json")	
		
		else:
			# non json data is treated as monolog
			node_id,person_id = 0,0
			data=open(path).read()+"\n"			
			json_aif, OVA = {}, {}		
			text_with_span=""
			nodes, edges, schemefulfillments, descriptorfulfillments, participants, locutions =[], [], [], [], [], []
			speakers_and_turns = self.monolog_text(data)					
			nodes, locutions, participants, text_with_span, node_id, person_id = AIF.create_turn_entry(
				nodes, node_id, person_id,text_with_span, speakers_and_turns, locutions, participants, False)
			json_aif.update( {'nodes' : nodes} )
			json_aif.update( {'edges' : edges} )
			json_aif.update( {'locutions' : locutions} )
			json_aif.update( {'schemefulfillments' : schemefulfillments} )
			json_aif.update( {'descriptorfulfillments' : descriptorfulfillments} )
			json_aif.update( {'participants' : participants} )
			extended_json_aif['AIF'] = json_aif
			extended_json_aif['OVA'] = OVA
			extended_json_aif['dialog'] = False
			extended_json_aif['text'] = {'txt':text_with_span}
			return json.dumps(extended_json_aif)

  
