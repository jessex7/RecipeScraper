import json
from os.path import exists, join
from os import mkdir, scandir
from sys import argv

def translate_dir(input_dir: str, output_dir: str):
    with scandir(input_dir) as dir_entries:
        if not exists(output_dir):
            mkdir(output_dir)
        consolidated_translated_entries = []
        for entry in dir_entries:
            if entry.is_file():
                consolidated_translated_entries.append(translate(entry.name, input_dir, output_dir))
        
        consolidated_file = join(output_dir, "all-entries.json")
        with open(consolidated_file, "w") as f:
            json.dump(consolidated_translated_entries, f, ensure_ascii=False)


def translate(filename: str, input_dir: str, output_dir: str):
    print(f"input file: {filename}")
    print(f"input dir: {input_dir}")
    print(f"output dir: {output_dir}")
    input_file = join(input_dir, filename)
    if not exists(input_file):
        raise Exception(f"{input_file} does not exist.")
    
    with open(input_file, "r") as fi:
        json_data = json.load(fi)
        json_data["name"] = json_data.pop("title")
        ingredients = []
        for ingredient in json_data["ingredients"]:
            ingred_dict = {"ingred_name": ingredient[0], "amount": ingredient[1], "unit": ingredient[2]}
            ingredients.append(ingred_dict)
        json_data["ingredients"] = ingredients
        combined_instructions = " ".join(json_data["instructions"])
        json_data["instructions"] = combined_instructions
        json_data["author"] = json_data.pop("credit_to")

        output_file = join(output_dir, filename)
        print(output_file)
        with open(output_file, "w") as fo:
            json.dump(json_data, fo)
        return json_data

translate_dir(argv[1], argv[2])




        # working_dir = getcwd()
        # recipe_data_dir = join(working_dir, "recipe_data")
        # if exists(recipe_data_dir):
        #     pass
        # else:
        #     mkdir(recipe_data_dir)
        # filename = f"{page}.json"
        # full_file_path = join(recipe_data_dir, filename)
        # data = json.dumps(recipe)
        # with open(full_file_path, "w") as f:
        #     f.write(data)
        # self.log(f"Saved file {filename}")
