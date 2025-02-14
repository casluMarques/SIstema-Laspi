from flask import Flask, jsonify, request, render_template_string, send_file
import sqlite3
import qrcode
import os

app = Flask(__name__)

# Pasta para armazenar QR Codes temporariamente
QR_CODE_DIR = "qr_codes"
if not os.path.exists(QR_CODE_DIR):
    os.makedirs(QR_CODE_DIR)

# Função para gerar QR Code e salvar temporariamente
def gerar_qr_code(id_equipamento):
    ip_local = "192.168.1.100"  # Substitua pelo IP real do servidor
    url_api = f"http://{ip_local}:5000/equipamento/{id_equipamento}"
    
    qr = qrcode.make(url_api)
    qr_path = os.path.join(QR_CODE_DIR, f"equipamento{id_equipamento}.png")
    qr.save(qr_path)

    return qr_path  # Retorna o caminho do QR Code gerado

#Rota para buscar equipamentos pelo ID
@app.route("/equipamento/<int:id>", methods=["GET"])
def get_produto(id):
    connection = sqlite3.connect("equipamentos.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM equipamentos WHERE id = ?", (id,))
    equipamento = cursor.fetchone()

    connection.close()

    if equipamento:
        html = f"""
        <html>
            <head>
                <title>Equipamento</title>
            </head>
            <body>
                <h1>Processo: {equipamento[3]}</h1>
                <h2>Fabricante: {equipamento[2]}</h2>
                <p>Tipo: {equipamento[5]}<br>
                Data de Entrada: {equipamento[4]}<br>
                Descrição: {equipamento[6]}
                </p>
            </body>
        </html>
        """
        return render_template_string(html)
    else:
        return jsonify({"erro": "Equipamento não encontrado"}), 404

# Rota para exibir o formulário de adição de equipamento(GET)
@app.route("/", methods=["GET"])
def formulario_equipamento():
    html = """
    <html>
        <head>
            <title>Adicionar Equipamento</title>
        </head>
        <body>
            <h1>Adicionar Novo Equipamento</h1>
            <form action="/equipamento" method="post">
                <label>Processo:</label><br>
                <input type="number" name="processo" required><br><br>

                <label>Nome:</label><br>
                <input type="text" name="nome" required><br><br>

                <label>Fabricante:</label><br>
                <input type="text" name="fabricante" required><br><br>

                <label>Data de Entrada:</label><br>
                <input type="date" name="data_entrada" required><br><br>

                <label>Tipo:</label><br>
                <input type="text" name="tipo" required><br><br>

                <label>Descrição:</label><br>
                <textarea name="descricao" required></textarea><br><br>

                <button type="submit">Adicionar Equipamento</button>
            </form>
        </body>
    </html>
    """
    return render_template_string(html)

# Rota para adicionar equipamentos ao banco de dados (POST)
@app.route("/equipamento", methods=["POST"])
def add_equipamento():
    try:
        equipamento_id = request.form["processo"]
        nome = request.form["nome"]
        fabricante = request.form["fabricante"]
        data_entrada = request.form["data_entrada"]
        tipo = request.form["tipo"]
        descricao = request.form["descricao"]

        connection = sqlite3.connect("equipamentos.db")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO equipamentos (processo, nome, fabricante, data_entrada,tipo, descricao) VALUES (?, ?, ?, ?, ?, ?)", 
                       (equipamento_id, nome, fabricante, data_entrada,tipo, descricao))
        connection.commit()
        connection.close()

        # Gera o QR Code e salva no servidor temporariamente
        qr_code_path = gerar_qr_code(equipamento_id)

        # Faz download do QRcode no navegador
        return send_file(qr_code_path, as_attachment=True)

    except KeyError as e:
        return jsonify({"erro": f"Campo obrigatório ausente: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Inicia o servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  
