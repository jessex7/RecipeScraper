
import scrapy
import json
from os.path import exists, join
from os import mkdir, getcwd

class SkinnyTasteScraper(scrapy.Spider):
    name:str = "SkinnyTasteScraper"
    credit_to:str = "SkinnyTaste"
    start_urls: list[str] = ["https://www.skinnytaste.com/recipes/"]
    custom_settings = {
        "feed_export_encoding": "utf-8"
    }
    limit = 200
    pages_crawled = 0
        
    def parse(self, response):
        for link_selector in response.css(".ast-archive-post"):
            recipe_page_link = link_selector.css("a::attr(href)").get()
            if "7-day-healthy-meal-plan" in recipe_page_link:
                pass
            else:
                self.pages_crawled += 1
                yield response.follow(recipe_page_link, callback=self.parse_recipe)
        next_page = response.css("a.next::attr(href)").get()
        if next_page is not None and self.pages_crawled < self.limit:
            yield response.follow(next_page, callback=self.parse)

    def parse_recipe(self, response:scrapy.http.Response):
        name:str = response.css('.wprm-recipe-name::text').get()
        prep_time_num = float(response.css(".wprm-recipe-prep_time::text").get())
        prep_time_unit:str = response.css(".wprm-recipe-prep_time-unit::text").get().lower()
        if prep_time_unit == "hr" or prep_time_unit== "hours" or prep_time_unit == "hrs" or prep_time_unit == "hour":
            prep_time_num = prep_time_num * 60
        cook_time_num = float(response.css(".wprm-recipe-cook_time::text").get())
        cook_time_unit = response.css(".wprm-recipe-cook_time-unit::text").get()
        if cook_time_unit == "hr" or cook_time_unit== "hours" or cook_time_unit == "hrs" or cook_time_unit == "hour":
            cook_time_num = cook_time_num * 60
        ingredients:list[tuple] = []
        ingredients_raw = response.css(".wprm-recipe-ingredient")
        for item in ingredients_raw:
            ingredient = {
                "ingred_name": item.css(".wprm-recipe-ingredient-name::text").get(),
                "amount": item.css(".wprm-recipe-ingredient-amount::text").get(),
                "unit":  item.css(".wprm-recipe-ingredient-unit::text").get(),
                "notes": item.css(".wprm-recipe-ingredient-notes::text").get()
            }
            if ingredient["ingred_name"] is None:
                ingredient["ingred_name"] = item.css("a.wprm-recipe-ingredient-link::text").get()
            ingredients.append(ingredient)
        instructions_raw:list[scrapy.Selector] = response.css(".wprm-recipe-instruction")
        instructions: list[str] = []
        for item in instructions_raw:
            instruction:list[scrapy.Selector] = item.css("div::text")
            if instruction is None or len(instruction) == 0:
                instruction = item.css("div>span::text")
            txt = instruction.get()
            instructions.append(txt)
        recipe = {
            "original_url":response.url,
            "credit_to":self.credit_to,
            "author":self.credit_to,
            "name":name,
            "prep_time":prep_time_num,
            "cook_time":cook_time_num,
            "ingredients": ingredients,
            "instructions": " ".join(instructions)
        }
        page = response.url.split("/")[-2]

        working_dir = getcwd()
        recipe_data_dir = join(working_dir, "recipe_data2")
        if exists(recipe_data_dir):
            pass
        else:
            mkdir(recipe_data_dir)
        filename = f"{page}.json"
        full_file_path = join(recipe_data_dir, filename)
        data = json.dumps(recipe)
        with open(full_file_path, "w") as f:
            f.write(data)
        self.log(f"Saved file {filename}")
