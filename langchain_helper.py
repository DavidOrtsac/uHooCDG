# langchain_helper.py

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from secret_key import openapi_key
import os

os.environ['OPENAI_API_KEY'] = openapi_key

class ArticleGenerator:
    def __init__(self, content_type, brand, brand_description, topic, writing_style, target_audience, additional_instructions):
        self.llm = OpenAI(temperature=0.8, max_tokens=822)
        self.content_type = content_type
        self.brand = brand
        self.brand_description = brand_description
        self.topic = topic
        self.writing_style = writing_style
        self.target_audience = target_audience
        self.additional_instructions = additional_instructions

        # Initialize the templates and chains here
        self.initialize_templates_and_chains()

    def initialize_templates_and_chains(self):
        self.setup()

    def setup(self):
        prompt_template_1 = PromptTemplate(
            input_variables=['content_type', 'brand', 'brand_description', 'topic', 'target_audience','writing_style', 'additional_instructions'],
            template="Instructions: Create a {content_type} for {brand} in the {writing_style} writing style. Description of {brand}: {brand_description}. Target Audience: {target_audience} \n Topic of the {content_type}: {topic}\nAdditional Instructions: {additional_instructions}\nBased on the instructions, I want you to rewrite and summarize it based on how you understood them. Format your analysis like this: \n '- WHAT I UNDERSTOOD' \n '- REASONING' \n '- PLAN' \n After the analysis, reiterate the instructions to yourself. Write your answer in a conversational and instructional way as if you are reiterating the instructions to someone else. YOUR INSTRUCTIONS MUST BE ORGANIZED WITH BULLET POINTS. There must be seven items in your instructions. Separate each instructional item with '|' as a delimiter. THEN, after your analysis, write the requirements for creating a {content_type} for {topic}. \n A guide question you should answer is this: What is the structure of creating the {content_type}? Does it need chapters?\nOutput:"
        )

        prompt_template_2 = PromptTemplate(
            input_variables=['AI_analysis', 'content_type', 'brand', 'target_audience'],
            template="Instructions: {AI_analysis}\n\nBased on the instructions, create a {content_type} for {brand}. Target Audience: {target_audience}\nOutput:"
        )

        prompt_template_3 = PromptTemplate(
            input_variables=['first_draft', 'content_type', 'brand', 'topic'],
            template="First Draft: {first_draft}\n\nMake a short and concise analysis of this first draft of a/an {content_type} for {brand}. Note that the topic of the {content_type} is {topic}. Follow this format for the analysis (append bullet points): \n 'DRAFT SUMMARY:' \n 'CRITICISM AND SUGGESTIONS:' \n 'PLAN:' \nOutput:"
        )

        prompt_template_4 = PromptTemplate(
            input_variables=['AI_analysis_2', 'content_type', 'brand', 'first_draft'],
            template="First Draft of {brand}'s {content_type}: {first_draft} \n Suggestions on how to improve the {content_type}: {AI_analysis_2}\n\n Write the improved draft:"
        )

        prompt_template_5 = PromptTemplate(
            input_variables=['content_type', 'brand', 'user_feedback', 'final_output'],
            template="Latest draft of {brand}'s {content_type}: {final_output}\nThis draft of had the following user feedback: {user_feedback} \n Output based on user feedback:"
        )
        chain_1 = LLMChain(llm=self.llm, prompt=prompt_template_1, output_key="AI_analysis")
        chain_2 = LLMChain(llm=self.llm, prompt=prompt_template_2, output_key="first_draft")
        chain_3 = LLMChain(llm=self.llm, prompt=prompt_template_3, output_key="AI_analysis_2")
        chain_4 = LLMChain(llm=self.llm, prompt=prompt_template_4, output_key="final_output")
        self.chain_5 = LLMChain(llm=self.llm, prompt=prompt_template_5, output_key="final_output_with_feedback")

        self.sequential_chain = SequentialChain(
            chains=[chain_1, chain_2, chain_3, chain_4],
            input_variables=['content_type', 'brand', 'brand_description', 'topic', 'writing_style', 'target_audience', 'additional_instructions'],
            output_variables=['AI_analysis', 'first_draft', 'AI_analysis_2', 'final_output']
        )

    def generate(self):
        input_data = {
            'content_type': self.content_type,
            'brand': self.brand,
            'brand_description': self.brand_description,
            'topic': self.topic,
            'writing_style': self.writing_style,
            'target_audience': self.target_audience,
            'additional_instructions': self.additional_instructions
        }

        response = self.sequential_chain(input_data)
        self.previous_response = response  # Save the output to the state
        return response

    def generate_with_feedback(self, user_feedback):
        input_data = {
            'content_type': self.content_type,
            'brand': self.brand,
            'brand_description': self.brand_description,
            'topic': self.topic,
            'writing_style': self.writing_style,
            'target_audience': self.target_audience,
            'additional_instructions': self.additional_instructions,
            'user_feedback': user_feedback,
            'AI_analysis_2': self.previous_response['AI_analysis_2'],  # Now we're accessing it from the saved state
            'final_output': self.previous_response['final_output']
        }

        response = self.chain_5(input_data)
        return response