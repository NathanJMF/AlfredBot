from quart import Quart, request, jsonify
from brains import brain_query, set_up_model


app = Quart(__name__)
model = None


@app.before_serving
async def start_up():
    global model
    model = await set_up_model()


@app.route('/generate', methods=['POST'])
async def generate_response():
    current_request = await request.get_json()
    prompt = current_request.get('prompt', '')
    response = await brain_query(prompt, model)
    return jsonify({'response': response}), 200


@app.route('/', methods=['get'])
async def test():
    return jsonify({'response': "I'M ALIVE"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
