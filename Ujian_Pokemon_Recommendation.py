from flask import Flask, render_template, request, jsonify

import requests
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

def find_pokemon_recommendation(name):

    poke = name
    poke = poke.capitalize()
    pokemon_index = pokelist[pokelist['Name'] == poke].index[0]
    recom = list(enumerate(score[pokemon_index]))
    pokemon_index_list = sorted(recom, key=lambda x:x[1], reverse=True)[0:6]
    idx = [i[0] for i in pokemon_index_list]
    pokelist_recomm=pokelist.iloc[idx][['Name', 'Type 1', 'Generation', 'Legendary']]
    
    lst = []

    url='https://pokeapi.co/api/v2/pokemon'
    for i in range(pokelist_recomm.shape[0]):
        adc={}
        adc['Name'] = pokelist_recomm.iloc[i]['Name']
        api=requests.get(url+'/'+adc['Name'].lower())
        data_pokemon = api.json()
        gambar = data_pokemon['sprites']['front_default']
        adc['Gambar'] = gambar
        adc['Type 1'] = pokelist_recomm.iloc[i]['Type 1']
        adc['Generation'] = pokelist_recomm.iloc[i]['Generation']
        adc['Legendary'] = pokelist_recomm.iloc[i]['Legendary']
        
        lst.append(adc)
    
    return lst[1:]

@app.route('/', methods=['POST', 'GET'])
def func1():
    return render_template("home.html")

@app.route("/hasil", methods=['POST'])
def func2():
    
    try:
        data = request.form
        data=data
        url='https://pokeapi.co/api/v2/pokemon'
        api=requests.get(url+'/'+data['pokemon'])
        recommendation = find_pokemon_recommendation(data['pokemon'])
        print(recommendation)
        data_pokemon = api.json()
        gambar = data_pokemon['sprites']['front_default']
        pokemon_favorit=recommendation[0]
        final_data = {
            'Name': pokemon_favorit['Name'],
            'Gambar': gambar,
            'Type 1': pokemon_favorit['Type 1'],
            'Generation': pokemon_favorit['Generation'],
            'Legendary': pokemon_favorit['Legendary']

        return render_template("result.html", data=final_data, pokelist=recommendation)
    
    except:
        return render_template('not_found.html')

if __name__ == "__main__":
    
    pokelist = pd.read_csv('Pokemon.csv')
    pokelist.shape
    arr = []

    for i in range(pokelist.shape[0]):
        val = str(pokelist.loc[i]['Type 1'])+' '+str(pokelist.loc[i]['Generation'])+' '+str(pokelist.loc[i]['Legendary'])
        arr.append(val)

    pokelist['feature'] = np.array(arr)
    c_vect = CountVectorizer(tokenizer = lambda x : x.split(' '))
    matrix = c_vect.fit_transform(pokelist['feature'])
    score = cosine_similarity(matrix)
    makan="makan nasi"

    app.run(debug=True)