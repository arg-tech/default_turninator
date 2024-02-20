import re
from flask import json
import logging

logging.basicConfig(datefmt='%H:%M:%S', level=logging.DEBUG)

from data import AIF, Data
from turninator_output import TurninatorOutput

class Turninator():
    def __init__(self) -> None:
        pass
    
    def dialog_turns(self, text: str) -> str:
        '''Extract dialog turns from input text using regex.'''
        text = re.sub('<.*?>', '', text, flags=re.DOTALL)
        return re.findall(r'([A-Za-z ]+): (.+\n)', text)

    def monolog_text(self, text: str) -> str:
        '''Extract the entire text if monolog.'''
        return re.sub('<.*?>', '', text, flags=re.DOTALL)

    def turninator_default(self, path_obj):
        # Get the file path from the path object
        data = Data(path_obj)
        path = data.get_file_path()
        extended_json_aif = {}
        
        # Check if the file ends with ".json"
        if path.endswith("json"):
            nodes, edges, locutions = [], [], []
            # Check if the file is a valid JSON file
            if data.is_valid_json():
                # Get the AIF section from the data
                extended_json_aif = data.get_aif()
                # Check if 'AIF' and 'text' keys are present in the AIF section
                if 'AIF' in extended_json_aif and 'text' in extended_json_aif:
                    json_dict = extended_json_aif['AIF'] 
                    dialog = extended_json_aif.get('dialog', False)
                    OVA = extended_json_aif.get('OVA', [])
                    # Handle the case where 'json_dict' is a string
                    if isinstance(json_dict, str):
                        if json_dict.startswith('"'):
                            json_dict = json_dict.replace("\"", "")
                            json_dict = dict(json_dict)
                    logging.info(f'processing monolog text')
                    # Convert 'json_dict' to a dictionary if it's not already
                    if not isinstance(json_dict, dict):
                        json_dict = json.loads(json_dict)
                    # Extract values associated with specific keys from the AIF section
                    schemefulfillments, descriptorfulfillments = AIF.get_xAIF_arrays(['schemefulfillments', descriptorfulfillments])
                    participants = json_dict.get("participants", [])
                    # Extract text from the AIF section
                    if isinstance(extended_json_aif['text'], dict):
                        text = extended_json_aif['text']['txt']
                    else:
                        text = extended_json_aif['text']  # gets the text
                        text = text + "\n"
                    # Convert text to JSON object
                    if isinstance(text, str):
                        json_object = json.dumps(text)
                        json_object = json.loads(json_object)                    
                    is_dialog = extended_json_aif.get('dialog')
                    text_with_span = ""
                    node_id, person_id = 0, 0
                    # Extract dialog turns if it's a dialog, otherwise extract monolog text
                    speakers_and_turns = self.dialog_turns(text) if is_dialog and len(self.dialog_turns(text)) else self.monolog_text(text)
                    if is_dialog and len(self.dialog_turns(text)):
                        speakers_and_turns = self.dialog_turns(text)
                        nodes, locutions, participants, text_with_span, node_id, person_id = AIF.create_turn_entry(
                            nodes, node_id, person_id, text_with_span, speakers_and_turns, locutions, participants, is_dialog)
                    else:
                        if not is_dialog:
                            logging.info(f'processing monolog text')
                            speakers_and_turns = self.monolog_text(text)
                            nodes, locutions, participants, text_with_span, node_id, person_id = AIF.create_turn_entry(
                                nodes, node_id, person_id, text_with_span, speakers_and_turns, locutions, participants, is_dialog)
                    return TurninatorOutput.format_output(nodes, edges, locutions, schemefulfillments, descriptorfulfillments, participants, OVA, text_with_span, dialog)
                else:
                    if 'text' in extended_json_aif:
                        node_id, person_id = 0, 0
                        if isinstance(extended_json_aif['text'], dict):
                            text = extended_json_aif['text']['txt']
                        else:
                            text = extended_json_aif['text'] + "\n"
                        
                        json_aif, OVA = {}, {}        
                        text_with_span = ""
                        nodes, edges, schemefulfillments, descriptorfulfillments, participants, locutions = [], [], [], [], [], []
                        speakers_and_turns = self.monolog_text(text)                   
                        nodes, locutions, participants, text_with_span, node_id, person_id = AIF.create_turn_entry(
                            nodes, node_id, person_id, text_with_span, speakers_and_turns, locutions, participants, False)
                        return TurninatorOutput.format_output(nodes, edges, locutions, schemefulfillments, descriptorfulfillments, participants, OVA, text_with_span)
            else:
                logging.info(f'the file is not in a correct json format')
                return "Invalid json"
        else:
            # Non-json data is treated as monolog
            node_id, person_id = 0, 0
            data = open(path).read() + "\n"            
            json_aif, OVA = {}, {}        
            text_with_span = ""
            nodes, edges, schemefulfillments, descriptorfulfillments, participants, locutions = [], [], [], [], [], []
            speakers_and_turns = self.monolog_text(data)                    
            nodes, locutions, participants, text_with_span, node_id, person_id = AIF.create_turn_entry(
                nodes, node_id, person_id, text_with_span, speakers_and_turns, locutions, participants, False)
            return TurninatorOutput.format_output(nodes, edges, locutions, schemefulfillments, descriptorfulfillments, participants, OVA, text_with_span)
