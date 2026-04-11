from flask import Flask, render_template

app = Flask(__name__)

# Homepage
@app.route('/')
def home():
    return render_template('index.html')


# Health check (VERY IMPORTANT for DevOps)
@app.route('/health')
def health():
    return {"status": "running"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)