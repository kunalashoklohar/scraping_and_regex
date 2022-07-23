import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import csv
import requests
import shutil

class DermnetScraper(webdriver.Chrome): 
    def __init__(self) :
        super(DermnetScraper, self).__init__(ChromeDriverManager().install())
        self.url = "https://dermnetnz.org/image-library/"
        self.all_diseases_details = None
        self.get(self.url)
        time.sleep(5)
    

    def scrape_disease_details(self):
        """
        Save all diseases details in to a list of tuples containg ('name_of_disease','url of disease','url of images')
        """
        all_diseases = self.find_elements(By.CLASS_NAME,"imageList__group__item")
        self.all_diseases_details = [(
                        disease.text.replace(" images","") ,
                        disease.get_attribute("href")      ,                                
                        disease.find_element(By.TAG_NAME,"img").get_attribute("src")                                
                                                                            ) for disease in all_diseases]

    def save_disease_details_to_csv(self):
        """Saves all details file to csv file 'dermnetNZ.csv'
        """
        column_names = ["disease_name","url","image_url"]
        with open('dermnetNZ.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(column_names)
            write.writerows(self.all_diseases_details)
        print("All disease details has been saved succesfully to 'dermnetNZ.csv'.")


    @staticmethod     
    def save_image(url:str,disease_name:str, folder_name)->None:
        image_name = disease_name.replace(" ","_").replace("/","_") +"." + url.split(".")[-1]
        image_file_name = os.path.join(os.getcwd() ,folder_name, image_name)
        image_stream = requests.get(url, stream = True)
        if image_stream.status_code == 200:
            with open(image_file_name,'wb') as f:
                shutil.copyfileobj(image_stream.raw, f)
            print('Image sucessfully Downloaded: ',image_file_name)
        else:
            print('Image Couldn\'t be retrieved')

    def save_images_of_diseases(self, folder_name = "dermnetnz_images"):
        if self.all_diseases_details:
            os.mkdir(folder_name) 
            [ self.save_image(url=disease[-1], disease_name=disease[0], folder_name = folder_name) for disease in self.all_diseases_details ]