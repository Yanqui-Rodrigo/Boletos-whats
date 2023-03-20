import cv2
import qrcode
from flask import Flask, request, jsonify

#CODIGO FLASK
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hola CHATBOT!'

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
    input = data
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
    cv2.imwrite(id_usuario+'.jpg',fondo)

    response = jsonify(response_data)
    return response

@app.route('/post_to_webhook', methods=['POST'])
def post_to_webhook():
    data = {'name': 'John', 'age': 30}
    headers = {'Content-type': 'application/json'}
    response = request.post('http://localhost:5000/webhook', json=data, headers=headers)
    return "ok"

if __name__ == '__main__':
    app.run(debug=True, port=5000)

