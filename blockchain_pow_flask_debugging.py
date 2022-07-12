# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 01:23:30 2020

@author: Lia
"""
# utile pour le chiffrement
import hashlib

#utile pour le formatage des blocs
import json

# Utile pour les timestamps des blocs
import time

# utile pour 
import flask

# Classe bloc qui va constituer les éléments chainés de la class blockchain
class Block:
    def __init__(self, index, transactions, timestamp, hash_precedent, nonce=0):
            self.index= index # place du bloc dans la chaine (commence à 0)
            self.timestamp = timestamp
            self.transactions = transactions # Toutes les transactions en cours sont ajoutées dans le bloc
            self.nonce = nonce # nombre que l'on va incrémenter dans le Pow afin de trouver le hash du bloc qui correspond à la contrainte
            self.hash_precedent = hash_precedent # le hash du bloc précédent
      
        
    # méthode qui hash un bloc
    def bloc_hash(self):
        # Conversion du bloc sous forme de dictionnaire en format JSON
        # self.__dict___ donne les attributs de la classe sous forme de dictionnaire
        bloc_json = json.dumps(self.__dict__, sort_keys=True)
        
        return sha256_hexa(bloc_json)
        



class Blockchain:
  
    # Correspond  à la difficulté de l'algo de PoW
    nb_0 = 4
    
    
    def __init__(self):
        
        # Initialisation de la blockchain sous forme de liste
        self.chain = []
        
        # Initialisation de la liste des transaction en cours (pas encore approuvées)
        self.transaction_en_cours = []
                     

    # méthode qui crée le bloc de genèse et l'ajoute à la blockchain
    def creation_bloc_genese(self):
        # création du bloc de genèse qui ne contient aucune transaction et un hash choisi au hasard
        bloc_genese = Block(index=0, transactions=[], timestamp=time.time(), hash_precedent=sha256_hexa("Hello"))
        
        # Calcul du hash du bloc de genèse
        bloc_genese.hash = bloc_genese.bloc_hash()
        
        # Ajout du bloc de genèse à la blockchain
        self.chain.append(bloc_genese)
        
        
    # méthode qui retourne le dernier bloc de la blockchain
    # Le décorateur @propr
    @property
    def dernier_bloc(self):
        return self.chain[-1]
    
        
    # méthode qui permet de créer un bloc et de l'ajouter à la blockchain
    def ajouter_bloc(self, bloc, preuve):
        # Calcul du hash du dernier bloc
        hash_precedent = self.dernier_bloc.hash
        
        # Si le champ hash du dernier bloc de la chaine ne correspond pas au champ hash_precedent du bloc courant alors on renvoit faux
        if hash_precedent != bloc.hash_precedent:
            return False
        
        # On vérifie si la preuve répond bien à la contrainte du pow et si la preuve correspond bien au hash du bloc courant (=vérifie que le mineur a le bon nonce)
        if (preuve[:self.nb_0] != (self.nb_0 * '0') and preuve == bloc.bloc_hash()):
            # le hash du bloc courant vaut la preuve
            bloc.hash = preuve
            
            # On ajoute le bloc à la chaine
            self.chain.append(bloc)
            
            return True
        
        else :
            return False
     
        
        """
    Méthode pour trouver un nombre p' tel que le hash de (pp') contiennent quatre 0, avec p la preuve du bloc précédent
   A nonce is a number that we can keep on changing until we get a hash that satisfies our constraint. The nonce satisfying the constraint serves as proof that some computation has been performed. This technique is a simplified version of the Hashcash algorithm used in Bitcoin. The number of zeroes specified in the constraint determines the difficulty of our proof of work algorithm (the greater the number of zeroes, the harder it is to figure out the nonce).
   Return : la preuve (=le hash du bloc courant une fois que le nonce a été trouvé )
   """
    def Pow(self, bloc):
    
    # Initialisation de la preuve
        bloc.nonce = 0
    
    # Calcul du hash du bloc courant
        hash_bloc_courant = bloc.bloc_hash()

        # Tant que le hash du bloc courant ne finit pas par 0000 on incrémente le nonce de 1
        while hash_bloc_courant[:self.nb_0] != (self.nb_0 * '0') :
            
            bloc.nonce +=1
            hash_bloc_courant = bloc.bloc_hash()
            
        return hash_bloc_courant

    
    # méthode qui crée une nouvelle transaction et l'ajoute à la liste des transaction_en_cours
    def ajouter_nouvelle_transaction(self, transaction):
        self.transaction_en_cours.append(transaction)
        
    
    # méthode qui sert à "miner" un bloc ie créer un bloc avec toutes les transactions en cours, trouver son nonce et l'ajouter à la chaine.
    def miner(self):
        # Vérifier que la liste des transactiosn en cours n'est pas vide
        if self.transaction_en_cours == []:
            return False
        
        # Récupération du dernier bloc
        dernier_bloc = self.dernier_bloc
        
        # Création d'un bloc avec toutes les transactions en cours
        nouveau_bloc = Block(index=dernier_bloc.index + 1, transactions=self.transactions_en_cours, timestamp=time.time(), hash_precedent=dernier_bloc.hash)
        
        # Calcul de la preuve du nouveau_bloc à l'aide de l'algorithme de consensus
        preuve = self.Pow(nouveau_bloc)
        
        # Ajout du nouveau_bloc à la blockchain
        self.ajouter_bloc(nouveau_bloc, preuve)
        
        # Remise à 0 de la liste des transactiosn en cours 
        self.transaction_en_cours = []
        
        return True
    
    
    
class Transaction:
    def __init__(self, envoyeur, receveur, montant):
        self.sender = envoyeur
        self.recipient = receveur
        self.amount = montant
    

def sha256_hexa(chaine):
        # Codage Unicode  
    bloc_unicode = chaine.encode()
        
        # Création d'un object qui hash avec sha256
    hash_SHA256 = hashlib.sha256()
        
        # Hashage du code Unicode du résultat de la multiplication
    hash_SHA256.update(bloc_unicode)
        
        # Sortie de la fonction de hachage cryptographique SHA256 (=digest) sous forme héxadécimale
    hash_hexa = hash_SHA256.hexdigest()
        
    return hash_hexa



# Création d'une application Flask
app = flask.Flask(__name__)

# Création d'une instance de la classe Blockchain
blockchain = Blockchain ()

blockchain.creation_bloc_genese()

@app.route('/')
def index():
    return "Welcome to my blockchain that uses PoW !"


""" Endpoint flask pour miner qui ne répond qu'aux requêtes GET
"""

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    dernier_bloc = blockchain.dernier_bloc
        
        # Création d'un bloc avec toutes les transactions en cours
    nouveau_bloc = Block(index=dernier_bloc.index + 1, transactions=blockchain.transactions_en_cours, timestamp=time.time(), hash_precedent=dernier_bloc.hash)
        
        # Calcul de la preuve du nouveau_bloc à l'aide de l'algorithme de consensus
    preuve = blockchain.Pow(nouveau_bloc)
        
        # Ajout du nouveau_bloc à la blockchain
    blockchain.ajouter_bloc(nouveau_bloc, preuve)
        
        # Remise à 0 de la liste des transactiosn en cours 
    blockchain.transaction_en_cours = []


    response = {
        'mok'
    }
    return flask.jsonify(response), 200



""" Endpoint flask pour soumettre de nouvelles transactions à la blockchain qui ne répond qu'aux requêtes POST
"""

@app.route('/nouvelles_transactions', methods=['POST'])
def nouvelle_transaction():
 # Récupère les données JSON des requêtes POST et les transforme en dictionnaire python grâce à la méthode get_json
    json_data = flask.request.get_json()
    
    # Verification que la requête POST  contient les 3 attributs nécéssaires à une transaction
    champs_obligatoires = ["sender", "recipient", "amount"]

    for k in champs_obligatoires:
        if not json_data.get(k):
            return "Invalid transaction data", 404

    # Création d'une transaction avec les infos de la requête POST
    transaction = Transaction(json_data["sender"], json_data["recipient"], json_data["amount"])
    
    # Ajout de cette nouvelle transaction à la liste des transactions en cours de la blockchain
    blockchain.ajouter_nouvelle_transaction(transaction)

    return ("Succès, la transaction est ajoutée dans la liste des transactions en cours", 201)



""" Endpoint flask qui renvoie la blockchain complète qui ne répond qu'aux requêtes GET
"""
@app.route("/blockchain", methods=['GET'])
def blockchain_complete() :
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return flask.jsonify({
        "longueur_de_la_chaine": len(chain_data),
        "chaine": chain_data
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    