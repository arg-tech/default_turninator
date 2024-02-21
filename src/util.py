import traceback
from flask import jsonify
# Decorator for error handling
def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return jsonify({'error': 'File not found in request'}), 400
        except Exception as e:
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500
    return wrapper