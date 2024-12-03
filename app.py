from flask import Flask, render_template, request, redirect, url_for
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
from dotenv import load_dotenv
import os
import logging
import markdown2
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
pineconeAPIKey = os.getenv('PINECONE_API_KEY')
if not pineconeAPIKey:
    raise ValueError("PINECONE_API_KEY not found in environment variables")

app = Flask(__name__)

pc = Pinecone(api_key=pineconeAPIKey)

# Load prompts from the YAML file
try:
    with open('./data/prompts.yaml', 'r') as file:
        prompts = yaml.safe_load(file)
except FileNotFoundError:
    logger.error("prompts.yaml file not found")
    prompts = {}  # Default empty dict

    
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            question = request.form['message']
            experience_level = request.form.get('experience_level', 'beginner')

            experience_prefix = prompts.get(experience_level, prompts['beginner'])
            prompt_prefix = prompts.get('prefix')
            print(f"Experience level: {experience_level}")
            print(f"prefix: {experience_prefix}")

            full_question = f"{prompt_prefix} {experience_prefix} {question}"
            
            # Get the assistant
            try:
                assistant = pc.assistant.describe_assistant(
                    assistant_name='devrel-library'
                )
                if not assistant:
                    raise ValueError("Assistant returned None")
            except Exception as e:
                logger.error(f"Failed to initialize assistant: {str(e)}")
                return render_template('index.html', 
                                    error="Unable to connect to the assistant service")

            # Handle error status codes if they're returned in the response
            if isinstance(assistant, dict) and 'status' in assistant:
                status = assistant.get('status')
                if status == 401:
                    logger.warning(f"Unauthorized access attempt: {assistant}")
                    return render_template('index.html', 
                                        error="Unauthorized access to the DevRel Assistant.")
                elif status == 404:
                    logger.warning(f"Assistant not found: {assistant}")
                    return render_template('index.html', 
                                        error="DevRel Assistant not found.")
                elif status != 200:
                    logger.error(f"Unexpected response status {status}: {assistant}")
                    return render_template('index.html', 
                                        error="Error accessing the DevRel Assistant.")

            # Create message and get response
            msg = Message(content=full_question)
            resp = assistant.chat(messages=[msg])
            
            # Extract answer from response
            answer = resp['message']['content']
            
            html_content = markdown2.markdown(
                answer, 
                extras=['break-on-newline', 'cuddled-lists'],
                safe_mode='escape'  
            )
            print(html_content)            
            return render_template('index.html', answer=html_content)
        

        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            return render_template('index.html', 
                                error="Sorry, there was an error processing your question.")
            
    return render_template('index.html')

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