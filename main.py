import gradio as gr
import openai

# Set OpenAI API Key to your own 
openai.api_key = ""

# Initialize message history with bot role instructions
message_history = [
    {"role": "user", "content": "You are a technical interview preparation bot. Provide coding questions, concept explanations, and mock interview simulations. Offer feedback on responses to help users improve."},
    {"role": "assistant", "content": "Got it! I can give you coding challenges, help you with technical concepts, or start a mock interview. Let me know what you'd like to practice."}
]

# Define the prediction function
def predict(input, difficulty, topic, mode):
    if mode == "Coding Challenge":
        prompt = f"Provide a {difficulty} coding question on {topic}."
        message_history.append({"role": "user", "content": prompt})
    elif mode == "Mock Interview":
        prompt = "Let's start a mock interview. I'll ask a series of questions. Respond to each, and I'll provide feedback."
        message_history.append({"role": "user", "content": prompt})
    elif mode == "Request Feedback":
        prompt = f"Here's my answer: {input}. Please provide feedback on its accuracy and areas for improvement."
        message_history.append({"role": "user", "content": prompt})
    else:
        message_history.append({"role": "user", "content": input})
    
    # Call OpenAI API
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )
    reply_content = completion.choices[0].message.content
    message_history.append({"role": "assistant", "content": reply_content})
    
    return message_history

# Define custom CSS for the interface
css = """
    .gradio-container {background-color: #f7f9fc; font-family: Arial, sans-serif; max-width: 800px; margin: auto; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);}
    .gr-markdown {margin-bottom: 15px; font-size: 16px; color: #333;}
    .gr-textbox {border-radius: 8px; border: 1px solid #d1d9e0; padding: 10px; font-size: 16px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);}
    .gr-button {background-color: #4a90e2; color: white; border-radius: 6px; padding: 10px 15px; font-size: 16px; border: none; cursor: pointer; transition: background-color 0.3s;}
    .gr-button:hover {background-color: #357ABD;}
    .gr-row {display: flex; gap: 10px;}
    .gr-dropdown {border-radius: 8px; padding: 8px; font-size: 15px;}
"""

# Create Gradio interface
with gr.Blocks(css=css) as demo:
    # Header and instructions
    gr.Markdown("""
        # Technical Interview Preparation Bot
        Welcome to the Technical Interview Prep Bot! Here’s what I can help you with:
        - **Coding Challenges**: Select a topic and difficulty level to receive a question.
        - **Mock Interviews**: Engage in simulated interview questions.
        - **Feedback Mode**: Share your solutions, and I'll offer constructive feedback.
        Simply select a mode, difficulty level, and topic below, and type your question or response in the text box. 
    """)

    # Chatbot display area
    chatbot = gr.Chatbot(type="messages")

    # Input fields and options
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Type your question or response here...")
        difficulty = gr.Dropdown(["Easy", "Medium", "Hard"], label="Difficulty Level", value="Medium")
        topic = gr.Dropdown(["Arrays", "Strings", "Recursion", "Sorting", "Graphs", "Trees"], label="Topic", value="Arrays")
        mode = gr.Dropdown(["General Question", "Coding Challenge", "Mock Interview", "Request Feedback"], label="Mode", value="General Question")

    # Submit actions to handle user input and update the chatbot
    txt.submit(predict, inputs=[txt, difficulty, topic, mode], outputs=chatbot)
    txt.submit(lambda: "", None, txt)  # Clears the input field after submit

# Launch the app
demo.launch(share=True)
