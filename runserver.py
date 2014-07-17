from musicbox import app
from OpenSSL import SSL
#context = SSL.Context(SSL.SSLv23_METHOD)
#context.use_privatekey_file('keys/server.key')
#context.use_certificate_file('keys/server.crt')

app.run(debug=True)
#app.run(host='127.0.0.1', debug=True, ssl_context=context)
