from flask import Flask, render_template, request, redirect, jsonify
import hashlib

app = Flask(__name__)

# In-memory storage for URLs and click counts
url_mapping = {}
click_counts = {}


#index page, the main one, where we are going to insert the inputs
@app.route('/')
def index():
    return render_template('htmlPage.html')

#function to shorten url, using hash lib. Also saves the original url on the hash map, which allows us to always generate as the same shortned url
def shorten_url(original_url):
    #enconding the url, turning into a different string
    short_hash = hashlib.md5(original_url.encode()).hexdigest()[:6]
    short_url = request.host_url + short_hash
    #mapping everything, so we can retrieve it later
    url_mapping[short_hash] = original_url
    #setting counting to 0
    click_counts[short_hash] = 0
    return short_url

#request to shorten url, /shorten is a page/endpoint
@app.route('/shorten', methods=['POST'])
def shorten():
    #usinh id=original_url from html file
    original_url = request.form['original_url']
    short_url = shorten_url(original_url)
    return jsonify({'short_url': short_url})

#request to retrieve the original url, looking at the hash mapping to find the original url of the respective shortned url
@app.route('/retrieve', methods=['POST'])
def retrieve():
    short_url = request.form['shorten_url']
    #getting only yhe shortned part at the end
    short_hash = short_url.split('/')[-1]
    original_url = url_mapping.get(short_hash)
    if original_url:
        return jsonify({'original_url': original_url})
    else:        
        return jsonify({'error': 'Short URL not found'}), 404
        #adding an error handling for non existent urls
        #note about this error handling: since we are using Ajax to see the results in the page without reloading
        #or redirecting to a page showing the JSON repsonse, this error is not shown

    

#if any of our shortned urls are used, it redirects to the original one. And so, if this redirection happens,
#it means that our url was used and its counter must show it adding plus 1 click
@app.route('/<short_hash>')
def redirect_to_original(short_hash):
    original_url = url_mapping.get(short_hash)
    if original_url:
        click_counts[short_hash] += 1
        return redirect(original_url)
    else:
        return jsonify({'error': 'Short URL not found'}), 404


#getting how many times a shortned url was clicked. Remeber we stored this info in memory, making reference to the shortned url
@app.route('/count', methods=['POST'])
def count():
    short_url = request.form['count_url']
    short_hash = short_url.split('/')[-1]
    count = click_counts.get(short_hash)
    if count is not None:
        return jsonify({'click_count': count})
    else:
        return jsonify({'error': 'Short URL not found'}), 404


#just the standart main
if __name__ == '__main__':
    app.run(debug=True)
