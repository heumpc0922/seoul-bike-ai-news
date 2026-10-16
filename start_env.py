
from pathlib import Path
from dotenv import load_dotenv
import uvicorn

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000)
