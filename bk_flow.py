import requests
import json
import time


class bk():
    bk_endpoints = {
        "init" : "https://mdw.bk.com/api/whopper/initialize",
        "validate" : "https://mdw.bk.com/api/ingredients/validate",
        "generate" : "https://mdw.bk.com/api/whopper/generate"
    }
    bk_headers = {
        "Content-Type": "application/json",
        "User-Agent"  : "69/4.2.0",
        "Referer" : "https://mdw.bk.com/create/"
    }
    def __init__(self):
        curr_req = requests.post(bk.bk_endpoints["init"], headers=bk.bk_headers, data="{}")
        if curr_req.status_code == 200:
            self.uuid = curr_req.json()["id"]
            self.img_url = f"https://mdw.bk.com/assets/whopper/images/{self.uuid}.png"
        else:
            print(curr_req.status_code)
            print(curr_req.text)
    
    def validate(self, topping, ignore_fail=False) -> bool:
        json_body = {
            "ingredient" : topping,
            "whopperId"  : self.uuid
        }
        curr_req = requests.post(bk.bk_endpoints["validate"], headers=bk.bk_headers, json=json_body)
        if curr_req.status_code == 200:
            return curr_req.json()["isValid"]
        else:
            if not ignore_fail:
                raise Exception(f"Failed to validate {curr_req.status_code}. \n {curr_req.text}")
            print(f"{curr_req.status_code} : {topping}")
            return False
        
    def generate(self, toppings, impossible=False, validate_here=False) -> bool:
        '''the toppings is a list and set impossible to True if you want an impossible burger (yes the default is meat. You're welcome PETA)'''
        if validate_here:
            for topping in toppings:
                if not self.validate(topping):
                    print("You can't use {topping}. BK only allows validated toppings")
                    return False
        json_body = {
            "patty" : "flameGrilledBeefPatty" if not impossible else "impossiblePatty",
            "ingredients" : toppings,
            "whopperId"  : self.uuid
        }
        curr_req = requests.post(bk.bk_endpoints["generate"], headers=bk.bk_headers, json=json_body)
        if curr_req.status_code == 200:
            return curr_req.json()["status"].lower() == "success"
        else:
            raise Exception(f"Failed to generate {curr_req.status_code}. \n {curr_req.text}")

class food_validations():
    def check_all_foods_foundation(foundationFoodsFile, out_file):
        my_bk = bk()
        out_data = {"valid" : [], "invalid" : []}
        with open(foundationFoodsFile, "r") as foods_fp:
            food_json = json.load(foods_fp)
            if not my_bk.validate("oil", ignore_fail=False):
                print("Failed to validate oil")
            else:
                print("Validated oil")
            print("Waiting...")
            time.sleep(10)
            print("Starting...")
            for curr_food_group in food_json["FoundationFoods"]:
                food_splits = (curr_food_group["description"].lower().replace(" ", "").split(","))
                print(food_splits)
                for curr_food in food_splits:
                    if curr_food not in out_data["valid"] and curr_food not in out_data["invalid"]:
                        if my_bk.validate(curr_food, ignore_fail=True):
                            out_data["valid"].append(curr_food)
                            print(curr_food, "valid")
                        else:
                            out_data["invalid"].append(curr_food)
                            print(curr_food, "invalid")
                        time.sleep(0.1)
        print("Finished. Loading file...")
        with open(out_file, "w") as valid_fp:
            json.dump(out_data, valid_fp, indent=4)
