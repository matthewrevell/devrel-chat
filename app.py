from flask import Flask, render_template, request
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
from dotenv import load_dotenv
import os
import logging
import markdown2


# Set up logging and send logs to the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the Pinecone API key from the environment
# and raise an error if it's not set
load_dotenv()
pineconeAPIKey = os.getenv('PINECONE_API_KEY')
if not pineconeAPIKey:
    raise ValueError("PINECONE_API_KEY environment variable is not set")

app = Flask(__name__)

# Initialise the Pinecone client
pc = Pinecone(api_key=pineconeAPIKey)

# Define the home route
# The GET method renders the page with or without the response
# The POST method sends the question to the assistant
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        assistant_to_use = 'devrel-library'

        # Check that the form data contains a message
        if 'message' not in request.form:
            logger.error("No message provided in form data")
            return render_template('index.html', 
                                error="Please provide a question.")
        
        # Check that the message is not empty
        question = request.form['message']
        if not question.strip():
            logger.warning("Empty message submitted")
            return render_template('index.html', 
                                error="Please enter a question.")

        try:
            assistant = pc.assistant.describe_assistant(
                assistant_name=assistant_to_use
            )
        except Exception as assistant_error:
            logger.error(f"Failed to find assistant '{assistant_to_use}': {str(assistant_error)}")
            return render_template('index.html', 
                                error="Assistant not found. Please check the configuration.")

        try:
            # Create a message object from the user's question
            msg = Message(content=question)

            # Send the message to Pinecone Assistant and get a response
            resp = assistant.chat(messages=[msg])
                
            # Reformat the response as HTML that we can display in the 
            # Flask template
            answer = resp['message']['content']
            try:
                html_content = markdown2.markdown(answer, extras=['break-on-newline', 'cuddled-lists'])
            except:
                html_content = answer  # Just use the raw text if markdown fails
                logger.error("Markdown conversion failed, using raw text")
                    
            # Send the HTML response to the Flask template and render it
            return render_template('index.html', answer=html_content)

        except Exception as e:
            if "connection" in str(e).lower():  # Check if it's connection-related
                logger.error(f"Connection error reaching Pinecone: {str(e)}")
                return render_template('index.html', 
                                    error="Unable to connect to the assistant service. Please try again later.")
            else:
                logger.error(f"Unexpected error: {str(e)}")
                return render_template('index.html', 
                                    error="An unexpected error occurred. Please try again later.")
    
    return render_template('index.html')



# A test route to display a static answer for checking UI
# without hitting the API
@app.route('/test')
def test():
    static_answer = """<p>Sure, here is a numbered list of content tips based on the provided snippets:</p>
<ol>
<li><p><strong>Create a Comprehensive Content Calendar</strong>: A content calendar helps in organizing and planning content effectively, ensuring that you avoid redundancy and keep your audience engaged with a cohesive story.</p></li>
<li><p><strong>Develop a Reliable Content Cadence</strong>: Establish a consistent schedule for publishing content. This helps your audience know when to expect new content, making them feel more connected and engaged.</p></li>
<li><p><strong>Understand Your Audience</strong>: Know who your audience is and create content that is accessible to both beginners and experts. This ensures that your content is inclusive and engaging for a wide range of users.</p></li>
<li><p><strong>Be Concise and Clear</strong>: Avoid unnecessary jargon and lengthy explanations. Aim to explain concepts clearly and concisely, making it easier for your audience to understand and engage with your content.</p></li>
<li><p><strong>Use Visuals Effectively</strong>: Incorporate diagrams, interactive videos, and other visual aids to help increase comprehension and engagement.</p></li>
<li><p><strong>Create Multilayered Content</strong>: Offer multiple learning paths and levels of content to cater to different expertise levels. This can include quick start guides for beginners and more in-depth use cases for advanced users.</p></li>
<li><p><strong>Pay Attention to Conversations</strong>: Listen to internal and external conversations, including support tickets, to gather ideas for content that addresses real user needs and questions.</p></li>
<li><p><strong>Write for Skimmers</strong>: Many people skim online content, so use catchy headlines, sub-headings, and concise sections to make your content easily digestible.</p></li>
<li><p><strong>Promote Your Content Internally and Externally</strong>: Ensure that your content is known within your organization and shared in places where your audience is likely to see it. This helps in building consistency and momentum.</p></li>
<li><p><strong>Seek Feedback and Iterate</strong>: Regularly test your content and seek feedback to improve it. This includes preparing specific questions for feedback givers and iterating based on their input.</p></li>
<li><p><strong>Use Meaningful Links</strong>: Ensure that link text is descriptive and meaningful, helping users understand where the link will take them.</p></li>
<li><p><strong>Write with Empathy</strong>: Approach content creation from the user's perspective, considering their needs and challenges. This includes creating personas and testing edge cases.</p></li>
<li><p><strong>Make Content Accessible</strong>: Use high-contrast text, meaningful alt text for images, and ensure that your content is navigable for screen reader users.</p></li>
<li><p><strong>Be Data-Driven</strong>: Use data and analytics to inform your content strategy, ensuring that you are addressing the right topics and meeting your audience's needs.</p></li>
<li><p><strong>Collaborate with Others</strong>: Partner with other people to create and co-market content. This can bring in new perspectives and expand your reach.</p></li>
</ol>
<p>These tips should help you create effective and engaging content for your audience.</p>"""

    return render_template('index.html', answer=static_answer)

if __name__ == '__main__':
    app.run(debug=True)