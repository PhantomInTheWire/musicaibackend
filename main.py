from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
from crew import MelodyCrew
from custom_tools.suno_ai_tool import SunoTool
import time
import requests
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# Path to the audio file
AUDIO_PATH = "file.mp3"

def get_song(task_id: str):
    API_KEY = "61bae17e319aa548fefced575ab52883926eca0a84b5f58be834f7afae65d2cd"
    GET_TASK_ENDPOINT = f"https://api.piapi.ai/api/v1/task/{task_id}"
    headers = {"X-API-KEY": API_KEY}

    # Poll for task status
    while True:
        time.sleep(10)  # Wait between status checks
        response = requests.get(GET_TASK_ENDPOINT, headers=headers)

        if response.status_code != 200:
            print("Failed to fetch task status")
            raise HTTPException(status_code=500, detail="Failed to check task status")

        data = response.json()

        if data.get("code") == 200:
            task_data = data.get("data", {})
            status = task_data.get("status")

            if status == "completed":
                # Extract audio_url
                clips = task_data.get("output", {}).get("clips", {})
                for clip_id, clip_data in clips.items():
                    audio_url = clip_data.get("audio_url")
                    if audio_url:
                        audio_response = requests.get(audio_url)
                        with open("file.mp3", "wb") as audio_file:
                            audio_file.write(audio_response.content)
                        print("Audio downloaded successfully!")
                        return "file.mp3"
                raise HTTPException(status_code=500, detail="No audio URL in completed task")
            elif status == "failed":
                error = task_data.get("error", {})
                raise HTTPException(status_code=500, detail=f"Task failed: {error.get('message', 'Unknown error')}")
            elif status in {"pending", "processing"}:
                print(f"Task still {status}...")
                continue
            else:
                print(f"Unknown status: {status}")
                continue
        else:
            raise HTTPException(status_code=500, detail=data.get("message", "Failed to check task status"))


def song_gen(lyrics: str):
    endpoint = "https://api.piapi.ai/api/v1/task"
    headers = {"X-API-KEY": "61bae17e319aa548fefced575ab52883926eca0a84b5f58be834f7afae65d2cd"}

    data = {
        "model": "suno",
        "task_type": "generate_music_custom",
        "input": {
            "gpt_description_prompt": "A calm and relaxing melody for an autumn evening",
            "make_instrumental": False,
            "model_version": "chirp-v3-0",
            "prompt": lyrics,
            "tags": "relaxing, calm, piano",
            "title": "Autumn Night Breeze"
        },
        "config": {
            "service_mode": "",
            "webhook_config": {
                "endpoint": "",
                "secret": ""
            }
        }
    }
    print("function song_gen here!")
    response = requests.post(endpoint, headers=headers, json=data)

    if response.status_code == 200:
        print("Request successful!")
        return response.json()  # Return the response data
    else:
        print("Request failed!")
        print("Status Code:", response.status_code)
        print("Response:", response.json())
        return None


@app.get("/audio")
async def get_audio(topic: str, genre: str, response_class=FileResponse):
    melody_crew = MelodyCrew(topic, genre)
    result = melody_crew.run()
    out = song_gen(result)

    if out is None:
        raise HTTPException(status_code=500, detail="Failed to generate song")

    task_id = out.get("data", {}).get("task_id")
    if not task_id:
        raise HTTPException(status_code=500, detail="No task ID in response")

    get_song(task_id)

    # Check if the audio file exists
    if not os.path.exists(AUDIO_PATH):
        raise HTTPException(status_code=404, detail="Audio file not found")

    # Return the audio file with appropriate headers
    return FileResponse(
        path=AUDIO_PATH,
        media_type="audio/mpeg",
        filename="file.mp3"
    )

