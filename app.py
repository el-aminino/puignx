from flask import Flask , render_template
app = Flask(__name__, template_folder='.')


@app.route('/')
def home_page():
    return "Hello World!"

if __name__== '__main__':
    app.run(debug=True)