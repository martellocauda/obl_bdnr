import requests, json, math, random, codesearch, feed, time
from flask import Flask,render_template, request

app = Flask(__name__)

def calculate_navigation_pages(feed_actions_per_page, feed_of_logged_user, activepage):
    cant_feed_actions=len(feed_of_logged_user)
    pages=math.ceil(cant_feed_actions/feed_actions_per_page)
    pages_arr=range(1, pages+1, 1)
    cont=1
    put_page=1
    for feed_action in feed_of_logged_user:
        if cont > feed_actions_per_page:
            cont=1
            put_page+=1
        feed_action['page']=put_page
        cont+=1
    return pages_arr

@app.route('/', methods=['GET'])
def index():
    licences=codesearch.get_distinct_licence_types()
    languages=codesearch.get_distinct_languages()
    return render_template('index.html', licences=licences, languages=languages)
    
@app.route('/feed', methods=['GET', 'POST'])
def feed_get():
    actions=['pull','push','fetch','clone']
    branches=['master','develop','awesomeBranch','integration','feature1','newFeature']
    repos=['AwesomeRepo','SuperRepo','BDNRRepo','ExonerationRepo']
    if request.method == 'POST':
        feed.post_feed_action(1, "Covid Perez", "%s on %s"%(random.choice(actions),random.choice(branches)), "%s"%random.choice(repos))
    activepage=request.args.get('pag')
    if activepage:
        activepage=int(activepage)
    feed_of_logged_user=feed.get_feed_by_user(11, 0) #11 representa el usuario logueado
    pages=calculate_navigation_pages(5, feed_of_logged_user, activepage)
    licences=codesearch.get_distinct_licence_types()
    languages=codesearch.get_distinct_languages()
    return render_template('feed.html', feed_of_logged_user=feed_of_logged_user, pages=pages, activepage=activepage, licences=languages, languages=languages)

@app.route('/codesearch', methods=['POST'])
def search():
    if request.form['hasadvancedsearch'] == "yes":
        data_to_search=request.form['data_to_search']
        licence_to_search=request.form['licence_to_search']
        language_to_search=request.form['language_to_search']
        startDate_to_search=request.form['startDate_to_search']
        endDate_to_search=request.form['endDate_to_search']
        search_result=codesearch.make_es_search(data_to_search, licence_to_search, language_to_search, startDate_to_search, endDate_to_search)
    else:
        data_to_search=request.form['data_to_search']
        endDate_to_search=request.form['endDate_to_search']
        search_result=codesearch.make_es_search(data_to_search, "*", "*", "", endDate_to_search)
    return render_template('results.html', search_result=search_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
