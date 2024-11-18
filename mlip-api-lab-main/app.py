from flask import Flask, request, jsonify, render_template
from analyze import read_image
import requests  # Added to handle API call from frontend

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template('index.html')

# API at /api/v1/analysis/
@app.route("/api/v1/analysis/", methods=['GET'])
def analysis():
    try:
        get_json = request.get_json()
        image_uri = get_json['uri']
    except:
        return jsonify({'error': 'Missing URI in JSON'}), 400
    
    try:
        res = read_image(image_uri)
        
        response_data = {
            "text": res
        }
    
        return jsonify(response_data), 200
    except:
        return jsonify({'error': 'Error in processing'}), 500

# Route to handle form submission from the homepage
@app.route("/submit", methods=['POST'])
def submit_image():
    image_uri = request.form['image_uri']
    
    # Call the API to analyze the image
    try:
        response = requests.get(
            "http://localhost:3000/api/v1/analysis/", 
            json={"uri": image_uri}
        )
        result = response.json()
        # Pass the result to the homepage to display
        return render_template('index.html', result=result)
    except Exception as e:
        print(f"Error during API call: {e}")
        return render_template('index.html', error="Failed to analyze image.")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
