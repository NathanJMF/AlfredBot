import asyncio

from gpt4all import GPT4All
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)
lock = asyncio.Lock()


async def set_up_model():
    print("Setting up the brain...")
    # Parameters
    model_name = "alfred_brain.bin"
    model_path = "/app/"
    device = "cpu"

    model = GPT4All(
        model_name=model_name,
        model_path=model_path,
        device=device,
        allow_download=False
    )

    print("Brain has been set up!")
    return model


async def brain_query(prompt, model):
    try:
        async with lock:
            print("Inside generate_response")
            print("Generating response")
            response = await use_brain(model, prompt)
            print("Response generated")

        response = await chunk_response(response)
        return response
    except Exception as error:
        error = f"THIS ERROR!\n{error}"
        print(error)
        return [error]


async def chunk_response(current_response):
    max_len = 2000
    chunks = []
    start = 0
    while start < len(current_response):
        end = min(start + max_len, len(current_response))
        chunks.append(current_response[start:end])
        start = end

    return chunks


async def use_brain(model, prompt):
    with model.chat_session():
        return model.generate(prompt, max_tokens=2000, temp=0.5)
