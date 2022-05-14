from flask import Flask, render_template, url_for, request, redirect
from combined import allTogether, Y_TIT, rowAttrributes
global priceFilter,buyFilter

#priceFilter="20"
#buyFilter="All"
app = Flask(__name__)


@app.route('/handle_data', methods=['POST'])
def handle_data():
    searchterm = request.form['q']
    
    # priceFilter = request.form['pFilter']
    # buyFilter = request.form['buyFilter']
    # print(buyFilter)
    # print(priceFilter)
    if(len(searchterm) == 0):
        return render_template('noResults.html')
    imdb = allTogether().getIMDB_WithTitle(searchterm)
    if not imdb:
        return render_template('noResults.html')
    else:
        return render_template('modal.html',option_table = imdb) #, pf=priceFilter,bf = buyFilter

@app.route('/handle_data2', methods=['POST'])
def handle_data2():
    allTogetherObject = allTogether()
    searchterm = request.form['choice2']
    # print(searchterm)
    searchterm = searchterm.split("<*")
    imdb_id = searchterm[1]
    searchType = searchterm[2]
    # if(searchType == "s"):
    #     searchType = "show"
    # else:
    #     searchType = "movie"
    # priceFilter = request.form['priceFilter']
    # buyFilter = request.form['buyFilter']
    # print(buyFilter)
    # print(priceFilter)
    try:
        tmdb_id = allTogetherObject.getTMDBID(imdb_id)
        rec = ""
        if(searchType == "movie"):
            rec = allTogetherObject.movieRec(tmdb_id)
        elif(searchType == "show"):
            rec = allTogetherObject.showRec(tmdb_id)
        


        table = allTogetherObject.getResults(searchType, tmdb_id, True)
        if(len(table) == 0):
            return render_template('noResults.html')
        return render_template('table.html', table_value = table, recomendations = rec[:5])
    except: 
        return render_template('noResults.html')


@app.route('/handle_data3', methods=['POST'])
def handle_data3():
    try:
        searchterm = request.form['choice2']
        # print(searchterm)
        searchterm = searchterm.split("<*")
        tmdb_id = searchterm[1]
        searchType = searchterm[2]
        rec = ""
        if(searchType == "movie"):
            rec = allTogether().movieRec(tmdb_id)
        elif(searchType == "show"):
            rec = allTogether().showRec(tmdb_id)


        table = allTogether().getResults(searchType, tmdb_id, True)
        if(len(table) == 0):
            return render_template('noResults.html')
        return render_template('table.html', table_value = table, recomendations = rec[:5])
    except:
        return render_template('noResults.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/modal')
def modal():
    return render_template('modal.html')


@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == "__main__":
    app.run(debug=True)

