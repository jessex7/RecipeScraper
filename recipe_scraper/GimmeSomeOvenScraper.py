import scrapy

class GimmeSomeOvenScraper(scrapy.Spider):
    name:str = "gimmesomeovenscraper"
    start_urls: list[str] = ["https://www.gimmesomeoven.com/cacio-e-pepe"]

    def parse(self, response):
        title = response.css("h2.tasty-recipes-title::text").get()
        prep_time = response.css("span.tasty-recipes-prep-time::text").get()
        cook_time = response.css("span.tasty-recipes-cook-time::text").get()
        ingredients = response.css("div.tasty-recipes-ingredients-body ul li")s