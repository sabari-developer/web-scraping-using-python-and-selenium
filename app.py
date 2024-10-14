from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

# Set up a route for the API
@app.route('/scrape', methods=['POST'])
def scrape():
    # Get the URL from the POST request
    url = request.json.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Open the webpage
        driver.get(url)

        # Optional: wait for the page to fully load
        time.sleep(3)  # Adjust based on the website's load speed

        # Get the full HTML content
        html_content = driver.page_source

        # Optionally, save to a file (uncomment if needed)
        # with open('scraped_page.html', 'w', encoding='utf-8') as file:
        #     file.write(html_content)

        # Return the HTML content as a response
        return jsonify({'html': html_content}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Close the WebDriver session
        driver.quit()

# Main function to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
