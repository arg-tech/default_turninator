import re

class DialogExtractor:
    def dialog_turns(self, text: str):
        '''Extract dialog turns from input text using regex.'''
        # Remove any HTML tags
        text = re.sub('<.*?>', '', text, flags=re.DOTALL)
        # Regular expression to capture speaker and their corresponding text
        return re.findall(r'([A-Za-z0-9 ]+)\s*:\s*((?:.|\n)*?)(?=\n[A-Za-z0-9 ]+\s*:\s*|\Z)', text)

# Example usage
text = """
Speaker 1 : There is at least one apple. Therefore there are some apples.
Speaker 2 : There is at least one apple2. Therefore there are some apples3.
Speaker 2 : There is at least one apple4. Therefore there are some apples5.
"""

extractor = DialogExtractor()
turns = extractor.dialog_turns(text)

for turn in turns:
    print(f'Name: {turn[0]}')
    print(f'Text: {turn[1].strip()}\n')
