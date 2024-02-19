from flask import Flask, request
from turninator import Turninator 
from utility import get_file
import logging
#logging configuration
logging.basicConfig(datefmt='%H:%M:%S',
                    level=logging.DEBUG)


app = Flask(__name__)
	
@app.route('/turninator-01', methods = ['GET', 'POST'])
def turninator_defult():
	if request.method == 'POST':
		print("posted")
		file_obj = request.files['file']
		f_name = get_file(file_obj)
		
		turninator = Turninator()
		result=turninator.turninator_default(f_name)
		return result	

	if request.method == 'GET':
		info = """Turninanator is an AMF compononet that parses arguments into dialog turns.  
		This is the default implmentation of a turninanator that parses arguments using a simple regular expressions. 
		It expects dialogical texts to be specified in the form of 'speaker:text' formats. 
		It takes an input both in  text  and xIAF formats (where the input is specified in the text field of xIAF) to return xIAF as an output. 
		Please note that the argument type (dialog vs monolog) can be specified in xIAF if the input is in xIAF format otherwise it is considered as monological argument. 
		The component can be used as a starting point for creating an argument mining pipeline that takes monological or dialogical text specified as a regular text or xIAF."""
		return info


	
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5006"), debug=False)	  
