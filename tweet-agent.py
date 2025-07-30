from langgraph.graph import StateGraph,END
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict

class TweetState(TypedDict):
    topic: str
    tweet: str

load_dotenv()

llm = ChatOpenAI(model="gpt-4")

def write_tweet(state):
    prompt=f"Write tweet about {state['topic']}"
    tweet=llm.invoke(prompt).content
    return {"tweet":tweet,"topic":state['topic']}


def judge_tweet(state):
    tweet = state["tweet"]
    prompt = f"Rate the quality of this tweet on a scale of 1 to 10. Tweet: {tweet}. Just return the number."
    score = int(llm.invoke(prompt).content.strip())

    if score >= 7:
        return "end"
    else:
        return "improve"

    
workflow = StateGraph(TweetState)    
workflow.add_node("write_tweet",write_tweet)
workflow.add_conditional_edges("write_tweet",judge_tweet, {
    "improve": "write_tweet",
    "end": END
})
workflow.set_entry_point("write_tweet")


graph = workflow.compile()
result = graph.invoke({"topic":"Agentic AI"})
print(result)