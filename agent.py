from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage,SystemMessage
from langchain.agents import initialize_agent
from langchain.tools import StructuredTool
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class PostInput(BaseModel):
    topic: str
    tone: str

class HashtagInput(BaseModel):
    topic: str

llm=ChatOpenAI(model_name="gpt-4")

def generate_post(topic,tone):
    system_message=SystemMessage(content=f"You are a professional LinkedIn writer. Write a {tone} tone post on: {topic}. Max 2200 characters, no emojis.")
    user_msg = HumanMessage(content="Generate the LinkedIn post.")

    response = llm([system_message,user_msg])
    return response.content

def generate_hashtags(topic):
    prompt = HumanMessage(content=f"Generate 5 trending hashtags for a LinkedIn post about '{topic}', no # symbol.")
    return llm.invoke([prompt]).content

tools=[
    StructuredTool(name="Postwriter",func=generate_post,description="Writes a LinkedInPost",args_schema=PostInput),
    StructuredTool(name="HashtagGenerator",func=generate_hashtags,description="Generates the hashtag",args_schema=HashtagInput)
]

agent=initialize_agent(tools,llm,agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

inputs = {
    "topic": input("Topic of the post: "),
    "tone": input("Tone of the post: ")
}

response = agent.invoke({
    "input": f"Write a LinkedIn post and suggest hashtags for topic: {inputs['topic']} with a {inputs['tone']} tone."
})

print(response)