from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
import os

# index view function suppressed for brevity

@app.route('/POST', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #return os.getcwd()
        import TideCoordination as tc
        js = tc.loadJSON(filePath='app/data/StationLookup.json')
        outJSON = tc.TideCoordination(form.lat.data,form.lon.data,js,dtg=form.dtg.data,data_dir='app/data/')
        return outJSON
    return render_template('POST.html', 
                           title='POST',
                           form=form)
