@app.route('/')
def home():
    session['basket'] = []
    return render_template('home.html')