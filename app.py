from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Variáveis que serão enviadas para o template
    
    # Renderiza o template e passa as variáveis
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
