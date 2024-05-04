import os 
from dotenv import load_dotenv
load_dotenv()

LOG_PATH = os.path.join(os.getcwd(), "logs")

SPEECH_KEY = "ab7f0c0c72b44c1e8726a6a086a3de04"

SPEECH_REGION = "centralus"



CHUNK_SIZE = 50