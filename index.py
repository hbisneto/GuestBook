import codecs
import http.server
import socketserver
import urllib
from datetime import datetime

PORT = 8000

GUESTBOOK_ENTRIES = []

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            ### TEST CODE ###
                # html = """
                # <html><body>
                # <h1>Guestbook</h1>
                # <form action="/sign" method="post">
                # Nome: <input type="text" name="nome"><br>
                # Mensagem: <input type="text" name="mensagem"><br>
                # <input type="submit" value="Enviar">
                # </form>
                # <h2>Entradas:</h2>
                # """
            ### TEST CODE ###
            html = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>GuestBook</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  </head>
  <body>
    <div class="container">
        <form action="/sign" method="post">
            <h1 style="text-align: center;">GuestBook</h1>
            <div class="mb-3">
                <label for="exampleFormControlInput1" class="form-label">Nome</label>
                <input type="text" name="nome" class="form-control" id="exampleFormControlInput1" placeholder="Escreva seu nome">
            </div>
            <div class="mb-3">
                <label for="exampleFormControlTextarea1" class="form-label">Mensagem</label>
                <textarea class="form-control" name="mensagem" id="exampleFormControlTextarea1" rows="3" placeholder="Escreva qualquer mensagem..."></textarea>
            </div>
            <input class="btn btn-outline-primary" type="submit" value="Enviar" style="display: block; margin: 0 auto;">
        </form>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <br>
    <div class="container">
        <div class="list-group">
            """
            for entry in GUESTBOOK_ENTRIES:
                html+="""
                <a href="#" class="list-group-item list-group-item-action list-group-item-success" aria-current="true">
                    <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1">{}</h5>
                        <small>{}</small>
                    </div>
                    <p class="mb-1">{}</p>
                </a>
                """.format(*entry)
            html += "</div></div></body></html>"
            self.wfile.write(html.encode())
        else:
            self.send_response(404)

    def do_POST(self):
        if self.path == '/sign':
            length = int(self.headers['Content-Length'])
            post_data = urllib.parse.parse_qs(self.rfile.read(length).decode())
            nome = post_data.get('nome')[0] 
            mensagem = post_data.get('mensagem')[0]
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            GUESTBOOK_ENTRIES.insert(0, (nome, current_date, mensagem))
            with codecs.open('mensagens.txt', "r+", encoding="utf-8-sig") as custom_file:
                content = custom_file.read()
                custom_file.seek(0,0)
                custom_file.write(current_date + f': {nome} escreveu {mensagem}\n{content}')

            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_response(404)

handler_object = MyHttpRequestHandler

my_server = socketserver.TCPServer(("localhost", PORT), handler_object)
print("Servindo em localhost na porta", PORT)

try:
    my_server.serve_forever()
except KeyboardInterrupt:
    pass

my_server.server_close()
