from scraper.dermnetnz import DermnetScraper

def main():
    dermnetnz = DermnetScraper()
    dermnetnz.scrape_disease_details()
    dermnetnz.save_disease_details_to_csv()
    dermnetnz.save_images_of_diseases()

    print("Scraped sucessfully !")

if __name__ == "__main__":
    main()    