# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from os import getcwd


# Set up Chrome options
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Allow microphone access
#chrome_options.add_argument("--headless=new")  # Run in headless mode

# Initialize the Chrome driver
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Load the local HTML file
#website = f"{getcwd()}\\index.html"
#driver.get(website)

# Path to the input file
#rec_file = f"{getcwd()}\\input.txt"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Allow microphone access
chrome_options.add_argument("--headless=new")  # Run in headless mode

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Load the local HTML file
website = "https://allorizenproject1.netlify.app/"
driver.get(website)

# Path to the input file
rec_file = f"{getcwd()}\\input.txt"


def listen():
    try:
        # Wait for the start button to be clickable and click it
        start_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'startButton')))
        start_button.click()
        print("Listening...")
        output_text = ""

        while True:
            # Wait for the output element to be present
            output_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'output')))
            current_text = output_element.text.strip()

            # If the current text is different from the last saved text, update the file
            if current_text != output_text:
                output_text = current_text
                with open(rec_file, "w") as file:
                    file.write(output_text.lower())  # Save the text in lowercase
                    print("Sunil: " + output_text)  # Print the recognized text to console

            # Optional: Add a break condition if needed
    except KeyboardInterrupt:
        print("Listening stopped.")
    except Exception as e:
        print(e)


# Start listening
listen()