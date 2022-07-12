# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 13:59:22 2020

@author: Lia
"""

"""
import hashlib 

def Pow(x):
    y = 0  
    # Conversion du résultat (int) de la multiplication en un string
    multiplication_string = f'{x*y}'
        
    # Codage Unicode de la chaine de caractères précédente
    multiplication_unicode = multiplication_string.encode()
        
    # Création d'un object qui hash avec sha256
    hash_SHA256 = hashlib.sha256()
        
    # Hashage du code Unicode du résultat de la multiplication
    hash_SHA256.update(multiplication_unicode)
        
# Sortie de la fonction de hachage cryptographique SHA256 (=digest) sous forme héxadécimale
    hash_hexa = hash_SHA256.hexdigest()
        
    while hash_hexa[-2] != "00" :
        y += 1
        
        # Exactement la même chose qu'au dessus mais en condensé
        hash_hexa = hashlib.sha256(f'{x*y}'.encode()).hexdigest()
    return y

print("y vaut :", Pow(10))"""


import hashlib 

def Pow(x):
    y = 0  
    # Conversion du résultat (int) de la multiplication en un string
    multiplication_string = f'{x*y}'
        
    # Codage Unicode de la chaine de caractères précédente
    multiplication_unicode = multiplication_string.encode()
        
    # Création d'un object qui hash avec sha256
    hash_SHA256 = hashlib.sha256()
        
    # Hashage du code Unicode du résultat de la multiplication
    hash_SHA256.update(multiplication_unicode)
        
# Sortie de la fonction de hachage cryptographique SHA256 (=digest) sous forme héxadécimale
    hash_hexa = hash_SHA256.hexdigest()
        
    while hash_hexa[-2] != "00":
        y += 1
        
        # Exactement la même chose qu'au dessus mais en condensé
        hash_hexa = hashlib.sha256(f'{x*y}'.encode()).hexdigest()
    return y

print("y vaut :", Pow(2))

