from flask import Flask, render_template, request, redirect, jsonify 
import hashlib, logging, validators, csv


# Custom CSV formatter
class CSVFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self._fmt = '%(asctime)s,%(levelname)s,%(message)s'

    def format(self, record):
        record.message = record.getMessage()
        return self._fmt % record.__dict__

# Configure logging to save to a CSV file
log_file = 'revelo_challenge_logs.csv'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s,%(levelname)s,%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler(log_file, mode='w'),
                              logging.StreamHandler()])

app = Flask(__name__)

# In-memory storage for URLs and click counts
url_mapping = {}
click_counts = {}

# Index page, the main one, where we are going to insert the inputs
@app.route('/')
def index():
    logging.debug("Rendering index page.")
    return render_template('htmlPage.html')

# Function to shorten url, using hash lib. Also saves the original url on the hash map,
# which allows us to always generate the same shortened url
def shorten_url(original_url):
    logging.debug(f"Shortening URL: {original_url}")
    # Encoding the url, turning into a different string
    short_hash = hashlib.md5(original_url.encode()).hexdigest()[:6]
    short_url = request.host_url + short_hash
    # Mapping everything, so we can retrieve it later
    url_mapping[short_hash] = original_url
    # Setting counting to 0
    click_counts[short_hash] = 0
    logging.debug(f"Generated short URL: {short_url}")
    return short_url

# Request to shorten url, /shorten is a page/endpoint
@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['original_url']
    logging.debug(f"Received URL to shorten: {original_url}")
    if not validators.url(original_url):        
        logging.error("Invalid URL provided.")
        return jsonify({'error': 'Invalid URL'}), 400        
    short_url = shorten_url(original_url)
    logging.debug(f"Returning shortened URL: {short_url}")
    return jsonify({'short_url': short_url})

# Request to retrieve the original url, looking at the hash mapping to find the original url of the respective shortened url
@app.route('/retrieve', methods=['POST'])
def retrieve():
    short_url = request.form['shorten_url']
    logging.debug(f"Retrieving original URL for shortened URL: {short_url}")
    # Getting only the shortened part at the end
    short_hash = short_url.split('/')[-1]
    original_url = url_mapping.get(short_hash)
    if original_url:
        logging.debug(f"Found original URL: {original_url}")
        return jsonify({'original_url': original_url})
    else:        
        logging.error("Short URL not found.")
        return jsonify({'error': 'Short URL not found'}), 404

# If any of our shortened URLs are used, it redirects to the original one.
# And so, if this redirection happens, it means that our URL was used and its counter must show it adding plus 1 click
@app.route('/<short_hash>')
def redirect_to_original(short_hash):
    logging.debug(f"Redirecting to original URL for short hash: {short_hash}")
    original_url = url_mapping.get(short_hash)
    if original_url:
        click_counts[short_hash] += 1
        logging.debug(f"Redirecting to: {original_url}, click count is now {click_counts[short_hash]}")
        return redirect(original_url)
    else:
        logging.error("Short URL not found.")
        return jsonify({'error': 'Short URL not found'}), 404

# Getting how many times a shortened URL was clicked. Remember we stored this info in memory,
# making reference to the shortened URL
@app.route('/count', methods=['POST'])
def count():
    short_url = request.form['count_url']
    logging.debug(f"Getting click count for shortened URL: {short_url}")
    short_hash = short_url.split('/')[-1]
    count = click_counts.get(short_hash)
    if count is not None:
        logging.debug(f"Click count for {short_url} is {count}")
        return jsonify({'click_count': count})
    else:
        logging.error("Short URL not found.")
        return jsonify({'error': 'Short URL not found'}), 404

# Just the standard main
if __name__ == '__main__':
    logging.debug("Starting Flask application.")
    app.run(debug=True)