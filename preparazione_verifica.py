from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)
db_config = {
    'host': 'localhost',      
    'user': 'root',     
    'password': '', 
    'database': 'Animali'  
}


@app.route('/dati', methods=['GET'])
@app.route('/dati/<filtro>/<valore>', methods=['GET'])
@app.route('/dati/<filtro>/<valore_min>/<valore_max>', methods=['GET'])
def get_data(filtro=None, valore=None, valore_min=None, valore_max=None):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM Mammiferi"
        params = ()

        if filtro and valore and not valore_min and not valore_max:
            if filtro in ['Nome_Proprio', 'Eta', 'Razza', 'Peso', 'Id']:
                query += f" WHERE {filtro} = %s"
                params = (valore,)

        elif filtro and valore_min and valore_max:
            if filtro in ['Eta', 'Peso', 'Id']:  
                query += f" WHERE {filtro} BETWEEN %s AND %s"
                params = (valore_min, valore_max)
        
        cursor.execute(query, params)
        result = cursor.fetchall()
        return jsonify(result)
    
    except Error as e:
        print("Errore nella connessione al database:", e)
        return jsonify({"errore": "Impossibile connettersi al database"}), 500
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/dati/crea', methods=['POST'])
def create_animal():
    data = request.get_json()

    
    nome_proprio = data.get('Nome_Proprio')
    eta = data.get('Eta')
    razza = data.get('Razza')
    peso = data.get('Peso')

    if not nome_proprio or not eta or not razza or not peso:
        return jsonify({"errore": "Tutti i campi (Nome_Proprio, Eta, Razza, Peso) sono obbligatori"}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

       
        query = "INSERT INTO Mammiferi (Nome_Proprio, Eta, Razza, Peso) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nome_proprio, eta, razza, peso))
        conn.commit()

        return jsonify({"successo": "Nuovo animale creato", "id": cursor.lastrowid}), 201
    
    except Error as e:
        print("Errore nella connessione al database:", e)
        return jsonify({"errore": "Impossibile inserire l'animale nel database"}), 500
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    app.run()
