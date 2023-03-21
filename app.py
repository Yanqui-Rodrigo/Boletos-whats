import cv2
import qrcode
from flask import Flask, request, jsonify, render_template

#CODIGO FLASK
app = Flask(__name__)
@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data['message'])
    response_data = {'message': 'Webhook recibido'}
    datos = data['message'].split()

    comando = datos[0]  # '/invi'
    id_usuario = datos[1]  # '70555522'
    nombre = ' '.join(datos[2:])  # 'Ana Cotrado Marino'

    #CODIGO QR
    input = 'https://boletos.onrender.com/boleto/'+datos[1]
    qr = qrcode.QRCode(version=1,box_size=10,border=2)
    qr.add_data(input)
    qr.make(fit=True)
    img = qr.make_image(fill='black',back_color='white')
    img.save('codigoqr.png')

    #REEMPLAZO DE IMAGEN
    fondo = cv2.imread('fondo.png')
    codigoqr = cv2.imread('codigoqr.png')
    # Configurar texto
    texto = nombre
    font = cv2.FONT_HERSHEY_SIMPLEX
    escala = 3
    color = (255, 255, 255)  # Blanco
    grosor = 12
    posicion = (250, 1115)  # Coordenadas (x, y)

    # Escribir texto en imagen
    cv2.putText(fondo, texto, posicion, font, escala, color, grosor)

    filas,columnas,canales = codigoqr.shape
    print(filas,columnas)
    fondo[1200:filas+1200,390:columnas+390]=codigoqr
    cv2.imwrite('static/images/'+id_usuario+'.png',fondo)

    response = jsonify(response_data)
    return response

@app.route('/post_to_webhook', methods=['POST'])
def post_to_webhook():
    data = {'message ': '/invi 2017059555 Rodrigo Yanqui', 'numero': 30}
    
    headers = {'Content-type': 'application/json'}
    response = request.post('https://boletos.onrender.com/webhook', json=data, headers=headers)
    return "ok"

@app.route('/boleto/<codigo>')
def boleto(codigo):
    data={
        'imagen': 'Rodrigo',
        'codigo': codigo
    }
    return render_template('contacto.html',data=data)

@app.route('/boleto/img/<codigo>.png')
def mostrar_imagen(codigo):
    return app.send_static_file('images/'+codigo+'.png')


if __name__ == '__main__':
    app.run(debug=True, port=5000)




