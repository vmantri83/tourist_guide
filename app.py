from flask import Flask, request, jsonify, send_from_directory
import requests
import flickrapi
import logging

app = Flask(__name__, static_url_path='')

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Flickr API credentials (replace with your own)
FLICKR_API_KEY = 'aab885bd72de41b4f5f4d59c41389e37'
FLICKR_API_SECRET = '626308b3d28af17b'

flickr = flickrapi.FlickrAPI(FLICKR_API_KEY, FLICKR_API_SECRET, format='parsed-json')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    data = request.json  # Get JSON data from the request body
    location = data.get('location')
    tags = data.get('tags')

    # Validate input
    if not location or not tags:
        return jsonify({"error": "Location and tags are required"}), 400

    # Call Nominatim API to get recommendations
    recommendations = fetch_recommendations(location, tags)

    # Fetch photos for each recommendation
    for rec in recommendations:
        rec['photos'] = fetch_photos(rec['name'])

    # Log the recommendations
    logging.debug(f"Recommendations: {recommendations}")

    return jsonify(recommendations)

def fetch_recommendations(location, tags):
    # Use Nominatim API to get coordinates for the location
    nominatim_url = f'https://nominatim.openstreetmap.org/search?q={location}&format=json'
    nominatim_response = requests.get(nominatim_url)
    nominatim_data = nominatim_response.json()

    if not nominatim_data:
        return {"error": "Location not found"}

    # Get the first result's coordinates
    lat = nominatim_data[0]['lat']
    lon = nominatim_data[0]['lon']

    # Use Overpass API to search for places with the given tags near the coordinates
    overpass_url = 'http://overpass-api.de/api/interpreter'
    query = f'''
    [out:json];
    (
      node["tourism"~"{'|'.join(tags)}"](around:5000,{lat},{lon});
      way["tourism"~"{'|'.join(tags)}"](around:5000,{lat},{lon});
      relation["tourism"~"{'|'.join(tags)}"](around:5000,{lat},{lon});
    );
    out body;
    >;
    out skel qt;
    '''
    logging.debug(f"Overpass query: {query}")
    overpass_response = requests.post(overpass_url, data={'data': query})
    overpass_data = overpass_response.json()

    recommendations = []
    for element in overpass_data['elements']:
        if 'tags' in element:
            recommendations.append({
                'name': element['tags'].get('name', 'Unnamed'),
                'type': element['tags'].get('tourism'),
                'latitude': element.get('lat', element['center']['lat'] if 'center' in element else None),
                'longitude': element.get('lon', element['center']['lon'] if 'center' in element else None),
                'address': element['tags'].get('addr:full', 'No address available')
            })

    return recommendations

def fetch_photos(place_name):
    photos = []
    try:
        response = flickr.photos.search(text=place_name, per_page=5, extras='url_m')
        for photo in response['photos']['photo']:
            if 'url_m' in photo:
                photos.append(photo['url_m'])
    except Exception as e:
        logging.error(f"Error fetching photos for {place_name}: {e}")
    return photos

if __name__ == '__main__':
    app.run(debug=True)
