from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime
import time

app = Flask(__name__)

# Алфавит для шифрования
ALPHABET = " ,.:(_)-0123456789АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

# Словарь пользователей и их паролей
users = {
    "user1": {"secret": "password1"},
    "user2": {"secret": "password2"},
    "user3": {"secret": "password3"}
}

# Словари для методов шифрования и сессий
methods = {}
sessions = {}
session_id_counter = 1

# Функция шифра Цезаря
def caesar_cipher(text, shift, decrypt=False):
    if decrypt:
        shift = -shift
    return ''.join(ALPHABET[(ALPHABET.index(c) + shift) % len(ALPHABET)] if c in ALPHABET else c for c in text)

# Функция шифра Виженера
def vigenere_cipher(text, key, decrypt=False):
    key = key.upper()
    key_indices = [ALPHABET.index(k) for k in key if k in ALPHABET]
    key_length = len(key_indices)
    result = []
    for i, char in enumerate(text):
        if char in ALPHABET:
            text_index = ALPHABET.index(char)
            key_index = key_indices[i % key_length]
            if decrypt:
                new_index = (text_index - key_index) % len(ALPHABET)
            else:
                new_index = (text_index + key_index) % len(ALPHABET)
            result.append(ALPHABET[new_index])
        else:
            result.append(char)
    return ''.join(result)

# Маршруты Flask
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/users', methods=['POST'])
def add_user():
    # Добавление нового пользователя
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_users():
    # Получение списка пользователей
    return jsonify([{"login": login} for login in users]), 200

@app.route('/users/list', methods=['GET'])
def list_users():
    # Отображение списка пользователей
    return render_template('users.html', users=list(users.keys()))

@app.route('/methods', methods=['GET'])
def get_methods():
    # Отображение списка методов шифрования
    return render_template('methods.html', methods=list(methods.values()))

@app.route('/encrypt', methods=['GET'])
def encrypt_form():
    # Форма для шифрования
    method_id = request.args.get('method_id')
    method = methods.get(method_id)
    if method:
        return render_template('encrypt.html', method=method, users=list(users.keys()))
    else:
        return redirect(url_for('get_methods'))

@app.route('/encrypt', methods=['POST'])
def encrypt():
    # Обработка запроса на шифрование
    global session_id_counter
    data = request.form
    user_id = data['user_id']
    method_id = data['method_id']
    action = data['action']
    data_in = data['data_in']
    params = {}

    if user_id in users and method_id in methods and len(data_in) <= 1000:
        data_in_filtered = ''.join([c for c in data_in.upper() if c in ALPHABET])
        start_time = time.time()

        # Выбор метода шифрования
        if methods[method_id]['caption'] == 'Caesar':
            shift = int(data['shift'])
            params['shift'] = shift
            data_out = caesar_cipher(data_in_filtered, shift, decrypt=(action == 'decrypt'))
        elif methods[method_id]['caption'] == 'Vigenere':
            key = data['key']
            params['key'] = key
            data_out = vigenere_cipher(data_in_filtered, key, decrypt=(action == 'decrypt'))
        else:
            return jsonify({"message": "Invalid method"}), 400

        end_time = time.time()
        # Создание сессии шифрования
        session = {
            'id': session_id_counter,
            'user_id': user_id,
            'method_id': method_id,
            'data_in': data_in,
            'params': params,
            'data_out': data_out,
            'status': 'completed',
            'created_at': datetime.now().isoformat(),
            'time_op': end_time - start_time
        }
        sessions[session_id_counter] = session
        session_id_counter += 1
        return redirect(url_for('get_sessions'))
    else:
        return jsonify({"message": "Invalid input"}), 400

@app.route('/sessions', methods=['GET'])
def get_sessions():
    # Отображение списка сессий
    return render_template('sessions.html', sessions=sessions.values())

@app.route('/sessions/<int:session_id>', methods=['GET'])
def get_session(session_id):
    # Получение деталей сессии
    session = sessions.get(session_id)
    if session:
        return render_template('session.html', session=session)
    else:
        return jsonify({"message": "Session not found"}), 404

@app.route('/sessions/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    # Удаление сессии
    data = request.form
    secret = data['secret']
    session = sessions.get(session_id)
    if session and users[session['user_id']]['secret'] == secret:
        del sessions[session_id]
        return jsonify({"message": "Сессия удалена успешно"}), 200
    else:
        return jsonify({"message": "Неправильный секрет"}), 400

@app.route('/sessions/<int:session_id>/delete', methods=['POST'])
def delete_session_form(session_id):
    # Форма для удаления сессии
    session = sessions.get(session_id)
    if session:
        secret = request.form['secret']
        user_id = session['user_id']
        if users[user_id]['secret'] == secret:
            del sessions[session_id]
            return redirect(url_for('get_sessions'))
        else:
            return render_template('session.html', session=session, error="Invalid secret")
    else:
        return jsonify({"message": "Сессия не найдена"}), 404

if __name__ == '__main__':
    # Добавление методов шифрования по умолчанию
    methods['1'] = {'id': '1', 'caption': 'Caesar', 'json_params': '{"shift": "int"}',
                    'description': 'Шифр Цезаря'}
    methods['2'] = {'id': '2', 'caption': 'Vigenere', 'json_params': '{"key": "str"}',
                    'description': 'Шифр Вижинера'}

    app.run(debug=True)
