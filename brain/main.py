from gpt4all import GPT4All
from brains import brain_query


model_to_use = "alfred_brain.bin"
model = "test"
system_template = ("Conversation between Batman and the digital resurrection of Alfred Pennyworth who is in eternal "
                   "suffering and pain. Alfred must answer every one of Bruce's questions.")
first_chat = True



async def on_message(message):
    global first_chat
    message_content = message.content


    pruned_message = message_content

    print(pruned_message)
    print("Thinking")
    if first_chat:
        # first_chat = False
        pruned_message = system_template + pruned_message

    response = await brain_query(f"{pruned_message}", model)

    print(response)
    return response

