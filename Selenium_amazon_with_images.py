import os
import requests
from pprint import pprint 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def Write_image(id_element,image_response):

    image_folder = os.getcwd() + "\Amazon_result_image"

    if os.path.exists(image_folder) == False:
        os.mkdir(image_folder)
                    
    if image_response.status_code == 200:
        with open(f'{image_folder}\\{id_element}.png', 'wb') as image_file:
            image_file.write(image_response.content)
                        
    else:
        print(f'Failed to download image-{id_element}')

def Web_scraping():
    try:
        options = Options() 
        options.add_argument("-headless") 
        driver = webdriver.Firefox(options=options)
        print("webdriver is open")

        with open("Amazon_result.txt", "w", encoding="utf-8") as file:
            print("Started to the file")

            file.write("""--------------------------------------Selenium Amazon Search Result--------------------------------------""")

            driver.get("https://www.amazon.in/s?k=gaming+monitor&crid=3MHDYZB2OO82H&sprefix=gaming+monitor%2Caps%2C298 &ref=nb_sb_noss_1")
            content = driver.find_elements(By.CSS_SELECTOR, "div.sg-col-20-of-24")

            file.write("\n\n")

            id_element = 0
            
            for ele in content:

                try:
            
                    name_element = ele.find_element(By.XPATH, ".//span[@class='a-size-medium a-color-base a-text-normal']").text
                    file.write(f"Product Name({id_element}) : "+ name_element+"\n")
                    
                    image_element = ele.find_element(By.XPATH, ".//img[@class='s-image']").get_attribute("src")
                    file.write("Image url: "+image_element+"\n")

                    price_element = ele.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
                    file.write("Product Price: "+ price_element+"\n")

                    image_response = requests.get(image_element)
                    Write_image(id_element,image_response)                   
                        
                    id_element += 1

                except:
                    continue


            print("Completed the writing file.")
            print("File located at ", os.path.realpath(file.name))

    except:
         print("Error Occurred.....")


    finally:
        driver.quit()
        print("webdriver is close")


if __name__ == "__main__":

    try:
        while True:
            title = "Selenium Amazon Search Result"
            print(f"--------------------------------------{title}--------------------------------------")

            var = input("To run or stop program : ").lower()

            match var:
                case "run":
                    Web_scraping()
                case "stop":
                    raise KeyboardInterrupt
                case _:
                    print("Invalid input.The available input Run or Stop.")
                    continue

    except KeyboardInterrupt:
        print(" End of Program.")
