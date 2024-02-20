import json

class TurninatorOutput:
    @staticmethod
    def format_output(nodes, edges, locutions, schemefulfillments, descriptorfulfillments, participants, OVA, text_with_span,dialog=False):
        json_aif = {
            'nodes': nodes,
            'edges': edges,
            'locutions': locutions,
            'schemefulfillments': schemefulfillments,
            'descriptorfulfillments': descriptorfulfillments,
            'participants': participants
        }
        extended_json_aif = {
            'AIF': json_aif,
            'OVA': OVA,
            'dialog': dialog,
            'text': {'txt': text_with_span}
        }
        return json.dumps(extended_json_aif)
