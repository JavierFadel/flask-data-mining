from flask import Blueprint, render_template, request, jsonify
from app.utils.data_loader import load_dataset
from app.utils.recommender import recommend_songs, data

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Get the song name and year from the form (or request data)
        song_name = request.form['song_name']
        song_year = int(request.form['song_year'])

        # Call the recommend_songs function from recommend.py
        recommendations = recommend_songs([{'name': song_name, 'year': song_year}], data)

        return jsonify(recommendations)
    
    except Exception as e:
        return jsonify({'error': str(e)})