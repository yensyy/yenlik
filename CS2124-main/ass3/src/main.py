

from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy

import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/python'
app.config['SQLALCHEMY TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)    



class Nft:
    nft_id = db.Column(db.Integer, primary_key=True)
    nft_mint = db.Column(db.String, nullable=False)
    nft_name = db.Column(db.String, nullable=False)
    def __init__(self,name,mint):
        self.nft_mint=mint
        self.nft_name=name

        
        
    def saveDb(self):
        db.session.add(self)
        db.session.commit()
    
    
with app.app_context():
    db.create_all()
    
    
@app.route("/", methods=['GET'])
def nftSearch():
    return render_template('index.html')

@app.route("/nft", methods=['GET'])
def nft():
    q = request.args['q']
    
    url = f"https://solana-gateway.moralis.io/nft/mainnet/{q}/metadata"
    
    headers = {

        "accept": "application/json",

        "X-API-Key": "10jftiyaAgczYG5YPUbRLEfaUI6uZIXFsquIdlPvkslIcExce1hIXxGyjczsGafC"

    }
    
    response = requests.get(url, headers=headers)
    
    payload = response.json()
    print(payload)
    nft_mint = payload["mint"]
    nft_name = payload["name"]
    nft = Nft(name=payload["name"], mint=payload["mint"])
    # nft.saveDb()
    return render_template("nft.html", name=nft_name, mint=nft_mint)


if __name__ == '__main__':
    app.run(debug=True)
