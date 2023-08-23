import streamlit as st
from langchain_helper import ArticleGenerator
from langchain.callbacks import StreamlitCallbackHandler

# Set page config
st.set_page_config(page_title='uHoo Content Draft Generator', page_icon=':potted_plant:', layout='centered', initial_sidebar_state='collapsed')

# Define custom colors for layout
primaryColor = "#4E89AE"
startGradientColor = "#ffaa00"
endGradientColor = "#FFFFFF"
textColor = "#2E5266"
font = "Roboto, sans-serif"
secondaryBackgroundColor = "#fcdede"
buttonColor = "#ffaa00"

custom_css = f"""
<style>
    body {{
        background: linear-gradient(90deg, {startGradientColor}, {endGradientColor});
        color: {textColor};
        font-family: {font};
        line-height: 1.6;
    }}
    .stButton > button {{
        background-color: {buttonColor};
        color: {endGradientColor};
        font-family: {font};
        border-radius: 10px;
        border: none;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .stTextInput > div > div > input, 
    textarea {{
        color: {textColor};
        border-radius: 10px;
        border: 2px solid {secondaryBackgroundColor}; /* Changed to gradient start color */
        padding: 10px 15px;
    }}
    .css-2trqyj {{
        background-color: rgba(255, 170, 0, 0.1); /* Light version of gradient start color for readability */
        color: {textColor};
        font-family: {font};
        border-radius: 10px;
        padding: 10px;
        margin-top: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .newest_message {{
        background-color: rgba(78, 137, 174, 0.2);
        padding: 15px;
        border-radius: 15px;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
st.title("🪴 uHoo Content Draft Generator | DashoContent")
st.text("")

expander_info = st.expander('How Does This Work?', expanded=False)
with expander_info:
    st.write("### **How the Content Draft Generator Works**")
    
    st.write("The Content Draft Generator by DashoContent is a powerful tool that harnesses the capabilities of AI to craft written content tailored to your needs. Below is an overview of how the application operates:")

    st.markdown("**1. Content Length Selection**")
    st.write("- Choose between three content lengths: Short, Medium, and Long.")
    st.write("- Short: Good for captions and short descriptions.")
    st.write("- Medium: Good for call-to-action messages and newsletters.")
    st.write("- Long: Good for longer blog posts and articles, as well as short stories and poems.")

    st.markdown("**2. Input Details**")
    st.write("- Provide details about your target audience, content type, topic, and writing style.")
    st.write("- The more accurate your inputs, the better the generated content will align with your expectations.")

    st.markdown("**3. Content Generation**")
    st.write("- Click the 'Generate Draft' button.")
    st.write("- The AI will use your inputs to generate a draft. This process may take a few moments, so your patience is appreciated.")

    st.markdown("**4. Review AI Analysis and First Draft**")
    st.write("- The application will display an AI analysis of your inputs, which gives insights into how the AI perceived your inputs.")
    st.write("- You'll then see the first draft of the content.")

    st.markdown("**5. AI's Second Round of Analysis**")
    st.write("- The AI will critically assess the first draft.")
    st.write("- A second, more refined draft is then presented based on this analysis.")

    st.markdown("**6. Feedback and Revisions**")
    st.write("- If the content isn't quite right, provide feedback in the designated field.")
    st.write("- Click 'Send Feedback', and the AI will generate a new version of the content considering your comments.")

    st.markdown("**7. Feedback Thread**")
    st.write("- This section displays all previous feedback and the AI's corresponding responses.")
    st.write("- It's a great way to track changes and see the evolution of the content.")

    st.write("With these steps, the Content Draft Generator ensures that you receive quality written content, tailored to your specific requirements.")

expander_inputs = st.expander('Inputs', expanded=True)
with expander_inputs:

    # Initialize state variables
    if 'article_gen' not in st.session_state:
        st.session_state['article_gen'] = None
    if 'feedbacks' not in st.session_state:
        st.session_state['feedbacks'] = []
    if 'outputs' not in st.session_state:
        st.session_state['outputs'] = []
    if 'output_generated' not in st.session_state:
        st.session_state['output_generated'] = False
    if 'show_output' not in st.session_state:
        st.session_state['show_output'] = True

    content_type_options = ['', 'Article', 'Blog Post', 'Email Newsletter', 'Newsletter', 'Infographics', 'Short Story', 'Poem', 'Press Release', 'Product Description', 'Product Review', 'Social Media Captions', 'Twitter Captions', 'Advertisement', 'Shortform Video Script', 'SEO-Optimized Article', 'Social Media Post']
    content_type = st.selectbox('Content Type:', sorted(content_type_options))
    token_length_options = {
    'Short': 150,
    'Medium': 550,
    'Long': 1022
    }
    selected_token_length = st.selectbox('Content Length:', list(token_length_options.keys()))
    topic = st.text_input('Topic:', '')
    writing_style = st.text_input('Writing Style:', '')
    target_audience_options = ['', 'Homeowners', 'Renters', 'Parents', 'Asthma, Allergy Patients', 'Architects and Interior Designers (Influencers)']
    target_audience = st.selectbox('Target Audience:', sorted(target_audience_options))
    additional_instructions = st.text_area('Additional Information (Optional):', '')


if content_type and topic and writing_style and target_audience and st.button('Generate Draft'):
    st.markdown("---")
    if not st.session_state['article_gen']:
        st.session_state['article_gen'] = ArticleGenerator(content_type, topic, writing_style, target_audience, additional_instructions, token_length_options[selected_token_length])
    container = st.empty()  # Use empty to be able to continually update the output
    st_callback = StreamlitCallbackHandler(container)  # Initialize the Streamlit callback handler
    response = st.session_state['article_gen'].generate(st_callback)  # Pass the callback handler to the generate method
    st.session_state['output_generated'] = True
    st.session_state['current_response'] = response
    container.write("")  # Clears the container after use

output_expander = st.expander("Show/Hide Output", expanded=True)

with output_expander:
    if st.session_state['output_generated']:
        response = st.session_state.get('current_response', {})
        st.header("FINAL OUTPUT")

        # Display AI Analysis
        st.subheader("AI Analysis")
        st.write(response['AI_analysis'].strip())

        # Display First Draft
        st.subheader("First Draft")
        st.write(response['first_draft'].strip())

        # Display Second AI Analysis
        st.subheader("AI Analysis of First Draft")
        article_text = response['AI_analysis_2'].strip().split("|")
        for section in article_text:
            st.write(" ", section)

        # Display Second Draft
        st.subheader("Second Draft")
        st.write(response['final_output'].strip())
    
if st.session_state['output_generated']:
    st.markdown("---")
    if 'user_feedback' not in st.session_state:
        st.session_state['user_feedback'] = ''

    user_feedback = st.text_input('Feedback:', value=st.session_state['user_feedback'])

    if st.button('Send Feedback') and user_feedback:
        # Initialize the Streamlit callback handler and generate the output
        st_callback = StreamlitCallbackHandler(st.empty())  # Initialize the Streamlit callback handler
        new_response = st.session_state['article_gen'].generate_with_feedback(user_feedback, st_callback)  # Pass the callback handler to the generate_with_feedback method

        # Update session state with the new feedback and output
        st.session_state['feedbacks'].append(user_feedback)
        st.session_state['outputs'].append(new_response['final_output_with_feedback'].strip())

        # Clear the feedback input field
        st.session_state['user_feedback'] = ''

# Feedback thread rendering should be done outside st.empty() context
if st.session_state['feedbacks']:
    st.markdown("---")
    st.subheader("Feedback Thread")
    
    # Start from the last feedback since it's the newest
    for index, (feedback, output) in enumerate(zip(reversed(st.session_state['feedbacks']), reversed(st.session_state['outputs']))):
        
        if index == 0:  # If it's the newest message
            st.markdown(f'<div class="newest_message"><caption>Feedback: {feedback}</caption><br>Output: {output}</div>', unsafe_allow_html=True)
        else:
            st.caption(f"Feedback: {feedback}")
            st.write(f"Output: {output}")
        
        st.markdown("---")
st.caption("© 2023 DashoContent. All rights reserved.")
