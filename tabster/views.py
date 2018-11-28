from tabster import app, db
from tabster.forms import LoginForm, SearchForm
from tabster.utilities import Finder
from tabster.models import Tabs
from werkzeug.utils import secure_filename
import sys
import os
from flask import render_template, flash, redirect, abort, url_for, request
from flask import send_from_directory


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/index', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])  # This maps the main part of our application (/) to the home() function. By default, Flask accepts GET requests for all routes, so here we're telling it to allow GET and POST requests.
def index():
    if request.form:  # check if someone just submitted the form. If they did, we can access the data that they submitted through the request.form variable. We’ll just print it out for now to see that our form is working.
        tab_temp = Finder(request.form.get("title"))

        tab = Tabs(url=request.form.get("title"), author=tab_temp.artist, typology=tab_temp.typology, title=tab_temp.title, tuning=tab_temp.tuning)  # grab the input from the form and we use it to initialize a new tab object
        db.session.add(tab)
        db.session.commit()
    result = Tabs.query.order_by(Tabs.title)
    intestation = "Lista Completa Ordinata Per Titolo!"

    return render_template('index.html', intestation=intestation, tab=result, search=search)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))

    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('login.html', title='Sign In', form=form, search=search)


@app.route('/search')
def search():
    query = request.args.get("query")
    tuning = request.args.get("tuning")
    if tuning == "All":
        tab = Tabs.query.filter((Tabs.author.like("%"+query+"%")) | (Tabs.title.like("%"+query+"%"))).all()
    else:
        tab = Tabs.query.filter((Tabs.author.like("%"+query+"%")) | (Tabs.title.like("%"+query+"%"))).filter(Tabs.tuning == tuning).all()

    return render_template('search.html', intestation="Risultati per: " + query, tab=tab)


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/files', methods=["GET", "POST"])
def files():
    if request.method == 'POST':
        title = request.form.get("title")
        artist = request.form.get("artist")
        capo = request.form.get("capo")
        youtube = request.form.get("youtube")
        tuning = request.form.get("tuning")
        metadata = ""
        newname = ""
        if(title):
            newname = newname + title + "_"
            metadata = metadata + "Title: " + title + "\n"
        if(artist):
            newname = newname + artist + "_"
            metadata = metadata + "Artist: " + artist + "\n"
        if(capo):
            newname = newname + capo
            metadata = metadata + "Capo: " + capo + "\n"
        if(tuning):
            metadata = metadata + "Tuning: " + tuning + "\n"
        if(youtube):
            metadata = metadata + "Youtube: " + youtube + "\n"

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            txtfile = newname + "_meta.txt"
            newname = newname + "." + filename.split(".")[-1]
            print('Metadata: ' + metadata, file=sys.stderr)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], newname))
            f = open(os.path.join(app.config['UPLOAD_FOLDER'], txtfile), "w+")
            f.write("Metadata:\n%s\r\n" % (metadata))
            f.close()
            return redirect(url_for('uploaded_file',
                                    filename=newname))
    # return redirect(url_for('uploaded_file', filename=filename))

    '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/fileslist')
def fileslist():
    return render_template('files.html')


'''The form.validate_on_submit() method does all the form processing work.
When the browser sends the GET request to receive the web page with the form, this method is going to return False,
so in that case the function skips the if statement and goes directly to render the template in the last line of the function.

When the browser sends the POST request as a result of the user pressing the submit button,
form.validate_on_submit() is going to gather all the data, run all the validators attached to fields,
and if everything is all right it will return True, indicating that the data is valid and can be processed by the application.
But if at least one field fails validation, then the function will return False, and that will cause the form to be rendered
back to the user, like in the GET request case. Later I'm going to add an error message when validation fails.

When form.validate_on_submit() returns True, the login view function calls two new functions, imported from Flask.
The flash() function is a useful way to show a message to the user. A lot of applications use this technique to let the user
know if some action has been successful or not. In this case, I'm going to use this mechanism as a temporary solution,
because I don't have all the infrastructure necessary to log users in for real yet. The best I can do for now is show a message
that confirms that the application received the credentials.

The second new function used in the login view function is redirect(). This function instructs the client web browser to
automatically navigate to a different page, given as an argument. This view function uses it to redirect the user to the index
page of the application.

When you call the flash() function, Flask stores the message




Flask provides a function called url_for(), which generates URLs using its internal mapping of URLs to view functions.
For example, url_for('login') returns /login, and url_for('index') return '/index. The argument to url_for() is the endpoint name,
which is the name of the view function.

You may ask why is it better to use the function names instead of URLs.
The fact is that URLs are much more likely to change than view function names, which are completely internal.
A secondary reason is that as you will learn later, some URLs have dynamic components in them, so generating those URLs by
hand would require concatenating multiple elements, which is tedious and error prone.
The url_for() is also able to generate these complex URLs.

'''
