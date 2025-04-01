from flask import Flask,render_template,request,jsonify
from recommendations import recommended_books
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend',methods=['POST'])
def get_recommendations():
    data = request.json
    book_name = data.get('book_name')
    recommendations = recommended_books(book_name)
    return jsonify({'recommendations': recommendations})
if __name__ == '__main__':
    app.run(debug=True)