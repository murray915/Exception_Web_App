from flask import Flask, render_template, request, url_for, flash, redirect
import database as db
import json
from icecream import ic

def ic_print_setting(setting:bool):
    """ setting on debug/printing for icecream"""    
    if setting:        
        ic.enable()
        ic.configureOutput(includeContext=True)
    elif not setting:
        ic.disable()

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/settings", methods=['GET', 'POST'])
def settings():

    with open(".\data\console_settings.json", mode="r", encoding="utf-8") as read_file:
        settings_data = json.load(read_file)
        settings_data

    if request.method == 'POST':
        # Get submitted form data
        updated_data = {}
        for key in settings_data.keys():
            new_value = request.form.get(key)
            updated_data[key] = [settings_data[key][0], new_value]  # Keep description, update value

        settings_data = updated_data

        with open(".\data\console_settings.json", "w") as jsonFile:
            json.dump(updated_data, jsonFile)

        # Return updated data back to template
        return render_template('settings.html', title="Settings", settings_data=settings_data, message="Settings saved!")

    return render_template('settings.html', title="Settings", settings_data=settings_data)


if __name__ == '__main__':
    ic_print_setting(True)
    app.run(debug=True)
    ic("test")