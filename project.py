from langchain.tools import StructuredTool
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from pydantic import BaseModel
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv
load_dotenv()
from mail import send_email
from db import collection  
import asyncio
import datetime
import sys

class mailInputs(BaseModel):
    topic: str
    recipient_name: str
    tone: str = "professional"  

llm = ChatOpenAI(model="gpt-4")

def mail_generator(topic, recipient_name, tone):
    system_message = SystemMessage(
        content=f"You are an expert email writer. Write a {tone} email to {recipient_name} about: {topic}, with a subject line."
    )
    human_message = HumanMessage(content=f"Write a {tone} mail")
    response = llm.invoke([system_message, human_message])
    return response.content

tools = [
    StructuredTool(
        description="Generates the mail based on tone, topic, and recipient",
        func=mail_generator,
        name="Mail generator",
        args_schema=mailInputs,
        return_direct=True
    )
]

agent = initialize_agent(llm=llm, tools=tools, agent=AgentType.OPENAI_MULTI_FUNCTIONS, verbose=True)

inputs = {
    "topic": input("Enter the topic for mail : "),
    "recipient_name": input("Enter the recipient_name : "),
    "recipient_email": input("Enter the recipient email address : "),
    "tone": input("Mention tone : ") or "professional",
    "name_of_sender": input("Mention your name : "),
    "contact_deatils": input("Mention your contact information : ")
}

tags = {
    "purpose": input("Enter purpose (e.g., follow-up): "),
    "status": input("Enter status (e.g., sent): "),
    "recipient_type": input("Enter recipient type (e.g., client): ")
}


async def check_duplicate(recipient_email, topic):
    recent_mail = await collection.find_one({
        "recipient_email": recipient_email,
        "topic": topic,
        "timestamp": {
            "$gte": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=3)
        }
    })
    return recent_mail is not None

async def insert_mail_record(record):
    await collection.insert_one(record)

async def main():
    duplicate = await check_duplicate(inputs["recipient_email"], inputs["topic"])
    if duplicate:
        print("A similar email was already sent to this recipient in the last 3 days. Aborting.")
        sys.exit()

    response = agent.invoke({
        "input": f"Write the mail to {inputs['recipient_name']} about the topic:{inputs['topic']}"
    })

    response_text = response['output']
    lines = response_text.split('\n')

    subject = ""
    body_lines = []

    for line in lines:
        if line.lower().startswith("subject:"):
            subject = line[len("Subject:"):].strip()
        else:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()

    body = body.replace("[Your Name]", inputs['name_of_sender'])
    body = body.replace("[Your Contact Information]", inputs['contact_deatils'])
    body = body.replace("[Your Position]", "_")

    send_email(
        receiver_email=inputs["recipient_email"],
        subject=subject,
        body=body
    )

    await insert_mail_record({
        "topic": inputs["topic"],
        "recipient_name": inputs["recipient_name"],
        "recipient_email": inputs["recipient_email"],
        "tone": inputs["tone"],
        "name_of_sender": inputs["name_of_sender"],
        "contact_details": inputs["contact_deatils"],
        "subject": subject,
        "body": body,
        "timestamp": datetime.datetime.now(datetime.timezone.utc),
        "tags": tags
    })


if __name__ == "__main__":
    asyncio.run(main())
