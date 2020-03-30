from flask import Flask, render_template, request
import string
import nltk
import pandas as pd
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import date
import pickle

app = Flask(__name__)

    
@app.route("/", methods=['get', 'post'])
def game_picker(): 
  # Step 1, display form to choose a semester
  if "step" not in request.form:
    return render_template("template.html", step="choose_title", )

  # Step 2, accept semester from form, output form to choose class
  elif request.form["step"] == "choose_desc":
    title = request.form["title"]
    return render_template("template.html", step="choose_desc", title=title)

  # Step 2, accept semester from form, output form to choose class
  elif request.form["step"] == "choose_mature":
    title = request.form["title"]
    desc = request.form['desc']
    return render_template("template.html", step="choose_mature", title=title, desc=desc)

  # Step 3, accept semester from form, output form to choose class
  elif request.form["step"] == "choose_type":
    title = request.form["title"]
    desc = request.form['desc']
    mature = request.form['mature']
    return render_template("template.html", step="choose_type", title=title, desc=desc, mature=mature)

  # Step 4, accept semester from form, output form to choose class
  elif request.form["step"] == "choose_genre":
    title = request.form["title"]
    desc = request.form['desc']
    mature = request.form['mature']
    game_type = request.form["game_type"]
    return render_template("template.html", step="choose_genre", title=title, desc=desc, mature=mature, game_type=game_type)


  # Step 5, accept semester from form, output form to choose class
  elif request.form["step"] == "choose_category":
    title = request.form["title"]
    desc = request.form['desc']
    mature = request.form['mature']
    game_type = request.form["game_type"]
    genre = request.form.getlist('genre')
    return render_template("template.html", step="choose_category", title=title, desc=desc, mature=mature, game_type=game_type, \
      genre=genre)

  # Step 6, accept semester from form, output form to choose class
  elif request.form["step"] == "choose_tags":
    title = request.form["title"]
    desc = request.form['desc']
    mature = request.form['mature']
    game_type = request.form["game_type"]
    genre = request.form.getlist('genre')
    category = request.form.getlist('category')
    return render_template("template.html", step="choose_tags", title=title, desc=desc, mature=mature, game_type=game_type, \
      genre=genre, category=category)


  # Step 7
  elif request.form["step"] == "langs":
    title = request.form["title"]
    desc = request.form['desc']
    mature = request.form['mature']
    game_type = request.form["game_type"]
    genre = request.form.getlist('genre')
    category = request.form.getlist('category')
    tag_tag = request.form.getlist('tag_tag')
    return render_template("template.html", step="langs", title=title, desc=desc, mature=mature, game_type=game_type, \
      genre=genre, category=category, tag_tag=tag_tag)

  # Step 8
  elif request.form["step"] == "do_registration":
    # real world registration code goes here...
    lang = request.form.getlist('lang')
    tag_tag = request.form.getlist('tag_tag')
    category = request.form.getlist('category')
    genre = request.form.getlist('genre')
    game_type = request.form['game_type']
    mature = request.form['mature']
    desc = request.form['desc']
    title = request.form["title"]
    courses = tag_tag + category + genre + lang
    courses.append(mature) 
    courses.append(game_type)
    courses.append(desc) 
    output = rec(courses, title)

    return render_template("template.html", step="do_registration", output=output)



def clean_string(string_list):
    soup_list = []
    for i in string_list:
        res = i.strip('""').strip('][').split(', ') 
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in res]
        for j in stripped:
            soup_list.append(j)
    soup = ''
    return (soup.join(soup_list))


def get_similarity(df):
    stopwords = nltk.corpus.stopwords.words('english')
    newStopWords = ['description', 'developers', 'describe']
    stopwords.extend(newStopWords)
    count = CountVectorizer(stop_words=newStopWords)
    count_matrix = count.fit_transform(df['soup'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    df = df.reset_index()
    indices = pd.Series(df.index, index = df['name'])
    return cosine_sim, indices


def get_recommendations(name, df):
    cosine_sim, indices = get_similarity(df)
    idx = indices[name]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    recs_df = pd.DataFrame() 
    sim_scores = sim_scores[1:6]
    recs_df['score'] = [i[1] for i in sim_scores]
    game_indices = [i[0] for i in sim_scores]
    games = []
    est_revenues = []
    seasons = []
    years = []
    for i in game_indices:
        game = df['name'].iloc[i]
        games.append(game)
        est_rev = df['est_revenue'].iloc[i]
        est_revenues.append(est_rev)
        season = df['season'].iloc[i]
        seasons.append(season)
        year = df['year'].iloc[i]
        years.append(year)
    recs_df['game'] = games
    recs_df['est_revenue'] = est_revenues
    recs_df['season'] = seasons
    recs_df['year'] = years
    recs_df = recs_df.reset_index()
    
    return recs_df

def get_season(name, df):
    df = get_recommendations(name, df)
    season = 'none'
    year_ = date.today().year
    oldest = year_ - 20 
    df = df[df.year >= oldest]
    if df.est_revenue.idxmax() == 0:
        season = df.loc[[0], 'season'].iloc[0]
    else: 
        df = df.sort_values(by=['est_revenue', 'score'], ascending=False)
        df = df.reset_index(drop=True)
        season = df.loc[[0], 'season'].iloc[0]
    return season 

def rec(soup, name):
  soup = clean_string(soup)
  name = name
  df = pd.read_pickle("simple.pkl")
  new_game = {'name': name, 'owners': 0, 'price': 0, 'est_revenue': 0, 'season': 'none', 'soup': soup}
  df = df.append(new_game, True)
  season = get_season(name, df)
  return season



app.run(debug=True)



