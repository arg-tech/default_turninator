# Default Turninator

This Flask app provides a default implementation of Turninator, an AMF component that parses arguments into dialog turns. The app can handle both monological and dialogical texts, using simple regular expressions for parsing.

## Endpoints

### /turninator-01

- **Methods**: GET, POST
- **Description**: 
  - **GET**: Returns information about the Turninator component and its usage.
  - **POST**: Expects a file upload containing either dialogical or monological text in the form of 'speaker:text' formats. Parses the input and returns the processed output in xIAF format.

## Usage

- Use the `/turninator-01` endpoint to interact with the Turninator:
   - For GET requests, visit the endpoint URL to get information about Turninator usage.
   - For POST requests, upload a file containing dialogical or monological text to parse and receive the processed output.

## Input Format

The Turninator accepts input in both plain text and xIAF formats:
- **Plain Text**: Dialogical or monological text in 'speaker:text' format.
- **xIAF**: Input can be provided in the text field of xIAF format. The argument type (dialog vs. monolog) can be specified in xIAF if needed; otherwise, it is considered monological.

## Output Format

The processed output is returned in xIAF format, containing parsed nodes, edges, locutions, schemefulfillments, descriptorfulfillments, participants, OVA, and text with span.

## Notes

- This app serves as a starting point for creating an argument mining pipeline using Turninator.
- It provides basic functionality for parsing dialogical and monological texts but can be extended for more advanced use cases.
