from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/api/telegram', methods=['POST'])
def telegram_webhook():
    update = request.get_json(silent=True)
    print('Telegram update received:', update)

    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        return jsonify({'ok': False, 'error': 'Missing TELEGRAM_BOT_TOKEN'}), 500

    try:
        # basic example: reply "تم الاستلام" to incoming text messages
        if not update:
            return jsonify({'ok': False, 'error': 'empty update'}), 400

        message = update.get('message') or update.get('edited_message')
        if message and 'chat' in message:
            chat_id = message['chat']['id']
            text = 'تم الاستلام'
            requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json={
                'chat_id': chat_id,
                'text': text
            }, timeout=10)

        return jsonify({'ok': True})
    except Exception as e:
        print('Error handling telegram update:', e)
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return 'Telegram webhook handler is running.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
