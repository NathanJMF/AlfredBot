from pyllamacpp.model import Model


async def thinking(prompt):
    model = Model(ggml_model='.\gpt4all-converted.bin', n_ctx=512)
    generated_text = model.generate(prompt, n_predict=55)
    return generated_text
