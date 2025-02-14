import qrcode

ip_local = "172.16.15.80" #IP onde a API está rodando

id_equipamento = 0 #definir ID(número do processo) para o qual vai gerar o QR code

url_api = f"http://{ip_local}:5000/{id_equipamento}"

qr = qrcode.make(url_api)

qr.save(f"equipamento{id_equipamento}.png")