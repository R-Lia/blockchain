# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 14:47:47 2020

@author: Lia
"""


# utile pour le chiffrement
import hashlib

#utile pour le formatage des blocs
import json

# Utile pour les timestamps des blocs
import time

class Blockchain(object):
    
    def __init__(self):
        
        # Initialisation de la blockchain sous forme de liste
        self.chain = []
        
        # Initialisation de la liste des transaction en cours (pas encore approuvées)
        self.transaction_en_cours = []
        
        # Création et ajout du bloc genèse
        self.nouveau_bloc(100, hashlib.sha256("Hello".encode()).hexdigest())
             
        
        
    # méthode qui permet de créer un bloc et de l'ajouter à la blockchain
    def nouveau_bloc(self, proof, hash_precedent=None):
        # bloc sous la forme d'un dictionnaire
        bloc = {
            'index': len(self.chain), # place du bloc dans la chaine (commence à 0)
            'timestamp' : time.time(),
            'transaction': self.transaction_en_cours, # Toutes les transactions en cours sont ajoutées dans le bloc
            'preuve': proof,
            'hash_précédent': hash_precedent or self.hash(self.chain[-1]), # le hash du bloc précédent
            }
        
        # On vide la liste des transactions en cours car elles ont toutes été ajoutées au nouveau bloc
        self.transaction_en_cours =[] 
        
        # On ajoute le bloc à la chaine
        self.chain.append(bloc)
        
        return bloc
    
    
    
    # méthode qui retourne le dernier bloc de la blockchain
    @property
    def dernier_bloc(self):
        return self.chain[-1]
    
    
    # méthode qui crée une nouvelle transaction et l'ajoute à la liste des transaction_en_cours
    def nouvelle_transaction(self, celui_qui_paie, celui_qui_est_paye, montant):
        # transaction sous la forme d'un dictionnaire
        transaction = {
            'émetteur' : celui_qui_paie,
            'récepteur' : celui_qui_est_paye,
            'montant': montant,
            }
        # Ajout de la transaction à la liste des transactions en cours
        self.transaction_en_cours.append(transaction)
        
        return self.dernier_bloc['index'] +1
    
    
    # méthode qui hash un bloc
    def hash(self, bloc):
        # Conversion du bloc sous forme de dictionnaire en format JSON
        bloc_json = json.dumps(bloc, sort_keys=True)
        
        return sha256_hexa(bloc_json)
    
        """
    Méthode pour trouver un nombre p' tel que le hash de (pp') contiennent quatre 0, avec p la preuve du bloc précédent
    """
    def Pow(self, proof_precedente):
    
    # Initialisation de la preuve
        proof = 0
    
    # Conversion des preuves en un string
        proof_string = f'{proof_precedente}{proof}'

        # Tant que le hash de (proof_precedente proof) ne finit pas par 0000 on incrémente proof de 1
        while sha256_hexa(proof_string)[:4] != '0000' :
            
            proof +=1
            proof_string = f'{proof_precedente}{proof}'
            
        return proof
    

def sha256_hexa(chaine):
        # Codage Unicode du format JSON du bloc précédent 
    bloc_unicode = chaine.encode()
        
        # Création d'un object qui hash avec sha256
    hash_SHA256 = hashlib.sha256()
        
        # Hashage du code Unicode du résultat de la multiplication
    hash_SHA256.update(bloc_unicode)
        
        # Sortie de la fonction de hachage cryptographique SHA256 (=digest) sous forme héxadécimale
    hash_hexa = hash_SHA256.hexdigest()
        
    return hash_hexa


blockchain = Blockchain ()

t1 = blockchain.nouvelle_transaction("Satoshi", "Mike", '5 BTC')
t2 = blockchain.nouvelle_transaction("Mike", "Satoshi", '1 BTC')
t3 = blockchain.nouvelle_transaction("Satoshi", "Hal Finney", '5 BTC')
blockchain.nouveau_bloc(12345)

t4 = blockchain.nouvelle_transaction("Mike", "Alice", '1 BTC')
t5 = blockchain.nouvelle_transaction("Alice", "Bob", '0.5 BTC')
t6 = blockchain.nouvelle_transaction("Bob", "Mike", '0.5 BTC')
blockchain.nouveau_bloc(6789)

print("blockchain: ", blockchain.chain)

