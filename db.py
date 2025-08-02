import motor.motor_asyncio
from dotenv import load_dotenv
import os
load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["mongodburi"])
db = client["mail-agent"]
collection = db["mail-details"]
