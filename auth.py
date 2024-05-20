from app import app
from flask import Flask, request, make_response
from functools import wraps

app = Flask(__name__)

def auth_required(f): #função que cria o nome do decorador e ativa a autenticação na api
    @wraps(f)
    def decorated(*args, **kwargs): #pega qualquer argumento passado para função
        auth = request.authorization
        if auth and auth.username == 'sara' and auth.password == 'teste':
            return f(*args, **kwargs)
        return make_response('Você não está logado!', 401, {'WWW-Authenticate': 'Basic realm="Login necessário!"'})
    return decorated
  
if __name__ == "__main__":
    app.run(debug=True)