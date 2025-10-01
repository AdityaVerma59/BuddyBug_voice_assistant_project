import asyncio
import edge_tts
import tempfile
import os
import pygame

VOICE = "en-AU-WilliamNeural"

async def speak_async(text: str):
    clean_text = text.replace("<think>", "").replace("</think>", "").strip()
    if not clean_text:
        return

    # Create temporary MP3 file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        filename = f.name

    # Generate speech
    communicate = edge_tts.Communicate(clean_text, VOICE)
    await communicate.save(filename)

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Wait until finished
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

    # Stop mixer and quit
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Safe removal
    try:
        os.remove(filename)
    except PermissionError:
        await asyncio.sleep(0.5)
        os.remove(filename)

def say(text: str):
    asyncio.run(speak_async(text))
