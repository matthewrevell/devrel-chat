from flask import Flask
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

pineconeAPIKey = os.getenv('PINECONE_API_KEY')

app = Flask(__name__)

pc = Pinecone(api_key=pineconeAPIKey)

@app.route('/')
def home():
    try:
        assistant = pc.assistant.describe_assistant(
            assistant_name='devrel-library'
        )

        # Handle error status codes if they're returned in the response
        if isinstance(assistant, dict) and 'status' in assistant:
            status = assistant.get('status')
            if status == 401:
                logger.warning(f"Unauthorized access attempt: {assistant}")
                return "Sorry, there's a problem accessing the DevRel Assistant.", 401
            elif status == 404:
                logger.warning(f"Assistant not found: {assistant}")
                return "Sorry, there's a problem accessing the DevRel Assistant.", 404
            elif status != 200:
                logger.error(f"Unexpected response status {status}: {assistant}")
                return "Sorry, there's a problem accessing the DevRel Assistant.", status

        # If we get here, we successfully retrieved the assistant
        assistant_name = assistant.name
        
        msg = Message(content="Please give me some tips on measuring developer relations success.")
        resp = assistant.chat(messages=[msg])

        
        print(resp)
        return("Waiting for an answer!")

    except AttributeError:
        logger.error("Unable to access assistant properties")
        return "Sorry, there's a problem accessing the DevRel Assistant.", 500
        
    except Exception as e:
        logger.error(f"Error accessing assistant: {str(e)}")
        return "Sorry, there's a problem accessing the DevRel Assistant.", 500

if __name__ == '__main__':
    app.run(debug=True)