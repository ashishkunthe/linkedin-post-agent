from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage,SystemMessage
from dotenv import load_dotenv

load_dotenv()

llm=ChatOpenAI(model_name="gpt-4")

def generate_post(post_type,topic,tone):
    system_message=SystemMessage(content=f"You are a professional LinkedIn content writer who writes engaging posts. Write a post in a {tone} tone about a {post_type} on '{topic}'. Do not use emojis. Keep it under 2200 characters.")
    user_msg = HumanMessage(content="Generate the LinkedIn post.")

    response = llm([system_message,user_msg])
    return response.content

if __name__ == "__main__":
    print("🚀 LinkedIn Post Generator")
    post_type = input("What type of post? (e.g., project, learning, job update): ")
    topic = input("What is it about?: ")
    tone = input("Tone? (e.g., humble, confident, storytelling): ")

    post = generate_post(post_type, topic, tone)
    print("\n📝 Your LinkedIn Post:\n")
    print(post)

    