from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage for survey submissions
surveys = []

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    # Required fields from the frontend
    required_fields = [
        'fullname', 'email', 'contact', 'date', 'age',
        'food', 'eatout', 'movies', 'tv', 'radio'
    ]
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing field: {field}'}), 400

    # Validate age
    try:
        age = int(data['age'])
        if age < 5 or age > 120:
            return jsonify({'message': 'Age must be between 5 and 120.'}), 400
    except ValueError:
        return jsonify({'message': 'Invalid age format.'}), 400

    # Validate food selection
    if not isinstance(data['food'], list) or len(data['food']) == 0:
        return jsonify({'message': 'At least one favorite food must be selected.'}), 400

    # Append survey data
    surveys.append(data)
    return jsonify({'message': 'Survey submitted successfully!'}), 200

@app.route('/results', methods=['GET'])
def results():
    if not surveys:
        return jsonify({'message': 'No Surveys Available', 'total': 0}), 200

    total = len(surveys)
    ages = [int(s['age']) for s in surveys]
    avg_age = round(sum(ages) / total, 1)
    oldest = max(ages)
    youngest = min(ages)

    # Percentage who selected 'Pizza'
    pizza_count = sum(1 for s in surveys if 'Pizza' in s['food'])
    pizza_percent = round((pizza_count / total) * 100, 1)

    # Average rating for 'eatout'
    eatout_avg = round(sum(int(s['eatout']) for s in surveys) / total, 2)

    return jsonify({
        'total': total,
        'avg_age': avg_age,
        'oldest': oldest,
        'youngest': youngest,
        'pizza_percent': pizza_percent,
        'eatout_avg': eatout_avg
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
