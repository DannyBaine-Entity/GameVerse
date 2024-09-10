from flask import Flask, request, jsonify

app = Flask(__name__)

# Define your authentication route
@app.route('/auth', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username == 'admin' and password == 'admin':
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Login failed'})

if __name__ == '__main__':
    app.run()