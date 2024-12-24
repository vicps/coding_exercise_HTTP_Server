# coding_exercise_HTTP_Server
In this repository, I'll be presenting the code to SDET code challenge: create a Http Server to shorten, retrieving, redirecting and couting how many times a shortned url was clicked!

## Running the code

1- Clone or download the files from this repository

2- Install Python 3 (if you have it already, please ignore this step)

Windows: You can install Python 3 downloading the .exe file in [oficial Python site](https://www.python.org/downloads/)
MacOs: You can install Python 3 using Homebrew `$ brew install python`

3- Install Flask (if you have it already, please ignore this step) : on terminal, use `pip install flask`

4- On a new terminal, navigate to the folder where the files are located

5- On the correct folder, execute the .py file. In this case, our .py file is named "revelo_challenge.py": `python revelo_challenge.py`

6- After running the .py file, the HTTP Serve will initialized and you'll see the host name to access it. In our example, the host was `http://127.0.0.1:5000/`

7- In the web page created for this HTTP Server, you can short any URL you want. Just put the inputns in the correct fields.

8- If you want to follow the requests made, keep an eye in the terminal. All the requests and errors will be shown there.


## Features

1. **URL Shortner**: Converts a long URL into a shortened URL, keeping it always the same shortened url
2. **Retrieve URL**: Retrieves the original URL of a shortened URL.
3. **Redirect URL**: Redirects a shortened URL to the original long URL. Just paste the shortned url in a new tab.
4. **Click Counting**: Counts the number of times a shortened URL has been used.


## Notes, comments and explanations

1- Http Server created using Python3 and Flask, to make it simple, easy and quick;

2- Still about Flask: using flask libs to render html page and to facilitate JSON requests

3- On the HTML file, using Ajax to make it possible to submit the inputs and get the responses without reloading the page or redirecting to a less readable page, where you'd have to come back to the previous page to use the input fields again (see the script in the html file); 

4- Using Hashlib to short, encode and store the shortned urls and originals urls, this way we guarantee that the shortned url will remain always the same and that we can retrieve the original url, as well redirect it when needed;

5- The URLs and click counts are stored in dictionaries (`url_mapping` and `click_counts` -  in memory storage, as suggest in the challenge description), to make it simple. In a production environment, again as suggested in the challenge description, a persistent database should be used.

6- Using simple free CSS templates, available at [W3Schools](https://www.w3schools.com/w3css/tryit.asp?filename=tryw3css_templates_cv&stacked=h)

