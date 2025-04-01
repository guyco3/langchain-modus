from langchain_modus import create_modus_tools
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

MODUS_API_KEY = os.getenv("MODUS_API_KEY")
predicates_tool, validate_tool = create_modus_tools(api_key=MODUS_API_KEY)

DOCUMENT_ID = '67eb4d0644b294e4e8890074'  # use your desired project id here
# Get predicates
predicates = predicates_tool.run({"project_id": DOCUMENT_ID})
print("Predicates:", predicates)

# Prepare assignments based on predicates
assignments = {predicate["alias"]: True for predicate in predicates if isinstance(predicate, dict)}
print("Assignments:", assignments)


assignments = json.dumps({'P1': True, 'P2': True, 'P3': True, 'P4': True, 'P5': True, 'P6': True,
 'P7': True, 'P8': True, 'P9': True, 'P10': True, 'P11': True, 'P12': True,
 'P13': True, 'P14': True, 'P15': True, 'Q1': True, 'Q2': False})


# Validate assignments
validation_result = validate_tool.run({
    "project_id": DOCUMENT_ID,
    "assignments": assignments,
})
print("Validation Result:", validation_result)

