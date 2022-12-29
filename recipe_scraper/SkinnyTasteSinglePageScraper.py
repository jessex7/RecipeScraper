import scrapy
import json

class SkinnyTasteSinglePageScraper(scrapy.Spider):
    name:str = "recipescraper"
    start_urls: list[str] = ["https://www.skinnytaste.com/air-fryer-whole-chicken/"]
        

    def parse(self, response):
        title:str = response.css('.wprm-recipe-name::text').get()
        prep_time_num:str = response.css(".wprm-recipe-prep_time::text").get()
        prep_time_unit:str = response.css(".wprm-recipe-prep_time-unit::text").get()
        prep_time:str = f"{prep_time_num} {prep_time_unit}"
        cook_time_num = response.css(".wprm-recipe-cook_time::text").get()
        cook_time_unit = response.css(".wprm-recipe-cook_time-unit::text").get()
        cook_time = f"{cook_time_num} {cook_time_unit}"
        ingredients:list[tuple] = []
        ingredients_raw = response.css(".wprm-recipe-ingredient")
        for item in ingredients_raw:
            name = item.css(".wprm-recipe-ingredient-name::text").get()
            amount = item.css(".wprm-recipe-ingredient-amount::text").get()
            unit = item.css(".wprm-recipe-ingredient-unit::text").get()
            notes = item.css(".wprm-recipe-ingredient-notes::text").get()
            ingredient = (name,amount,unit,notes)
            ingredients.append(ingredient)
        instructions_raw:list[scrapy.Selector] = response.css(".wprm-recipe-instruction")
        instructions: list[str] = []
        for item in instructions_raw:
            instruction = item.css("div::text")
            if instruction is None or len(instruction) == 0:
                instruction = item.css("div>span::text")
            txt = instruction.get()
            instructions.append(txt)
        recipe = {
            "original_url":response.url,
            "title":title,
            "prep_time":prep_time,
            "cook_time":cook_time,
            "ingredients": ingredients,
            "instructions": instructions
        }
        page = response.url.split("/")[-2]
        filename = f"recipes-{page}.json"
        data = json.dumps(recipe)
        with open(filename, "a") as f:
            f.write(data)
        self.log(f"Saved file {filename}")
