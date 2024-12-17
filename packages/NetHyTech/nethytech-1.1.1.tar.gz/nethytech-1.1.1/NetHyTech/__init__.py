import time
from selenium import webdriver  # pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # Correct import for ChromeDriverManager
from os import getcwd

#--------
import subprocess
import time
from colorama import Fore, Back, Style, init
from tqdm import tqdm

options = Options()
options.add_argument('--use-fake-ui-for-media-stream')
options.add_argument('--headless')


# Initialize colorama
init(autoreset=True)

def install_all_and_add(modules):
    modules_list = modules.split(" ")

    # Create a progress bar
    with tqdm(total=len(modules_list), desc="Installing modules", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [Elapsed: {elapsed}]", dynamic_ncols=True) as pbar:
        
        for module in modules_list:
            print(Fore.YELLOW + f"\nStarting installation of {module}...")
            result = subprocess.run(f'pip install {module}', capture_output=True, text=True)

            if result.returncode == 0:
                # Successful installation
                print(Fore.GREEN + Style.BRIGHT + f"✔ {module} installed successfully!")
                pbar.update(1)
                # Add to requirements.txt
                with open("requirements.txt", 'a+') as file:
                    file.seek(0)
                    lines = file.readlines()
                    if f"{module}\n" not in lines:
                        file.write(f"{module}\n")
                        print(Fore.CYAN + f"Added {module} to requirements.txt")
                    else:
                        print(Fore.GREEN + f"{module} is already in requirements.txt")
            else:
                # Installation failed
                print(Fore.RED + Style.BRIGHT + f"✖ Failed to install {module}: {result.stderr}")
                pbar.update(1)

            # Adding some animation effect for visual appeal
            print(Fore.CYAN + "Checking if module exists in 'requirements.txt'...")
            time.sleep(1)  # Simulating some delay for checking/adding
            print(Fore.MAGENTA + "Done checking!")

            # You can add animations or effects here, such as loading dots
            time.sleep(0.1)  # Short delay to simulate action for better visual effect.



def SpeechToText():
    # Create a Service instance with ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get('https://aquamarine-llama-e17401.netlify.app/')
        txt_box = driver.find_element(By.ID, "textbox")
        last_txt = txt_box.get_attribute('value')

        while True:
            current_txt = txt_box.get_attribute('value')
            if current_txt != last_txt:
                print(current_txt)
                # Only write to file if there is a change
                with open(f'{getcwd()}\\input_cmd.txt', 'w') as file:
                    file.write(current_txt)
                last_txt = current_txt
            time.sleep(0.1)  # Adjust sleep duration if needed

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()


import subprocess

def weather(area):
    subprocess.run(f'curl wttr.in/{area}')

import time
import sys

def printA(text, delay=0.0085):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # For newline after the animation


def calculate(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {e}"