from flask import Flask, request, jsonify
from api import auth, terms
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/healthCheck', methods=['GET'])
def health_check():
    response_data = {
        'status': 'healthy'
    }
    return jsonify(response_data), 200


@app.before_request
def check_token():
    return auth.check_auth_token()


app.add_url_rule('/signup', 'signup', auth.signup, methods=['POST'])
app.add_url_rule('/checkEmail', 'checkEmail', auth.check_email, methods=['POST'])
app.add_url_rule('/signin', 'signin', auth.signin, methods=['POST'])
app.add_url_rule('/terms', 'Terms and Conditions', terms.terms, methods=['GET', 'POST', 'PUT', 'DELETE'])
app.add_url_rule('/', 'check', auth.check, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)