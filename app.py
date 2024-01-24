from flask import Flask, render_template, request, redirect, url_for
from cs50 import SQL
import random
from datetime import datetime

app = Flask(__name__)

db = SQL('sqlite:///data.db')

# Create a class
class Period:
    def __init__(self) -> None:
        start_time = 0;
        end_time = 0;

# Initiate a period instance
user_session = Period()

# Number of images that will be presented to the user
FOTO_NUMBER = 3

# Allowed response values
ALLOWED_RESPONSES = ['1', '2', '3', '4']

# Legal countries to select from
COUNTRIES = ['germany', 'moldova', 'romania']

# Legal positions to choose from
POSITIONS = ['student', 'resident', 'doctor']

# Dictionary that will contain all the relevant info about the user
# Eventually it will be added into a database
user_data = {}

@app.route('/', methods=['get', 'post'])
def index():
    if request.method == 'GET':
        return render_template('index.html', lang="eng")
    else:
        return render_template('index.html', lang=request.form.get('lang'))

@app.route('/personal', methods=['get','post'])
def personal():
    if request.method == 'GET':
        user_session.start_time = datetime.now()
        return render_template('personal.html', lang = request.args.get('lang'))
    else:
        # Should do user input check
        # Check existance of name
        if not request.form.get('name'):
            return render_template('personal.html', message='Name is a required field', lang = request.form.get('lang'))
        
        # Check existance of surname
        if not request.form.get('surname'):
            return render_template('personal.html', message='Surname is a required field', lang = request.form.get('lang'))
        
        # Check existance of position
        if not request.form.get('position'):
            return render_template('personal.html', message='Position is a required field', lang = request.form.get('lang'))
        
        # Check position to be one of the legal options
        if request.form.get('position') not in POSITIONS:
            return render_template('personal.html', message='Should select only the available position options!', lang = request.form.get('lang'))
        
        # Check existance of country
        if not request.form.get('country'):
            return render_template('personal.html', message='Country is a required field', lang = request.form.get('lang'))

        # Check country to be one of the legal options
        if request.form.get('country') not in COUNTRIES:
            return render_template('personal.html', message='Should select only the available country options!', lang = request.form.get('lang'))
        
        # Save the values to the user dictionary
        user_data['name'] = request.form.get('name')
        user_data['surname'] = request.form.get('surname')
        user_data['position'] = request.form.get('position')
        user_data['country'] = request.form.get('country')

        # Redirect user to questions form
        return redirect(url_for('form', lang = request.form.get('lang')))


@app.route('/form', methods=['post','get'])
def form():
    # Page represented right at the beginning
    if request.method == 'GET':
        # 50 percent chance to be in either group
        AI_group = random.choice(["True", "False"])

        # Adding category info to user dict
        user_data["category"] = AI_group

        return render_template('form.html', number = 1, category = AI_group, lang=request.args.get('lang'))
    
    # Next pages
    else:
        # Get the value for the cateogry
        AI_group = request.form.get('category')

        # To do when we arrived at the last image
        if int(request.form.get('question')) >= FOTO_NUMBER:
            #Check for existence of user input
            if not request.form.get('q' + request.form.get('question')):
                return render_template('form.html', number = int(request.form.get('question')), message = "You should select an option!", category = AI_group, lang = request.form.get('lang'))
            
            #Check for valid user input
            if request.form.get('q' + request.form.get('question')) not in ALLOWED_RESPONSES:
                return render_template('form.html', number = int(request.form.get('question')), message = "Not an eligible option!", category = AI_group, lang = request.form.get('lang'))
            
            # Adding response to the dictionary containing all the user input
            user_data['q' + request.form.get('question')] = request.form.get('q' + request.form.get('question'))
            
            # Time when the user ended the survey
            user_session.end_time = datetime.now()

            # Now request he goodbye page
            return redirect(url_for('goodbye', lang = request.form.get('lang')))
        
        # To do when we still haven't arrived at the last page
        else:
            # Checking user input as above
            if not request.form.get('q' + request.form.get('question')):
                return render_template('form.html', number = int(request.form.get('question')), message = "You should select an option!", category = AI_group, lang = request.form.get('lang'))
            if request.form.get('q' + request.form.get('question')) not in ALLOWED_RESPONSES:
                return render_template('form.html', number = int(request.form.get('question')), message = "Not an eligible option!", category = AI_group, lang = request.form.get('lang'))
            
            # Adding info to dict as above
            user_data['q' + request.form.get('question')] = request.form.get('q' + request.form.get('question'))
            return render_template('form.html', number = int(request.form.get('question')) + 1, category = AI_group, lang = request.form.get('lang'))

@app.route('/goodbye', methods=['get'])
def goodbye():
    # Total elapsed time since the start of the survey
    elapsed_time = user_session.end_time - user_session.start_time
    # Add it to the user dict
    user_data['elapsed_time'] = str(elapsed_time.seconds)
    # Adding data to database
    db.execute('INSERT INTO answers (name, surname, position, country, category, q1, q2, q3, elapsed_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', user_data["name"], user_data["surname"], user_data["position"], user_data["country"], user_data["category"], user_data['q1'], user_data['q2'], user_data['q3'], user_data['elapsed_time'])

    return render_template('goodbye.html', elapsed_time = elapsed_time.seconds, lang = request.args.get('lang'))