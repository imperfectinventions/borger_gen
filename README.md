![Borger logo](repo_logo.png)
# BK API Reference

POST https://mdw.bk.com/api/whopper/initialize
Gets back a uuid
id : 

POST https://mdw.bk.com/api/ingredients/validate
{ingredient: "cheesepizza", whopperId: "40e250cd-1a5b-4c23-8c3e-223f75b8685a"}

gets back isValid as true or false

POST https://mdw.bk.com/api/whopper/generate
{patty: "flameGrilledBeefPatty", ingredients: ["cheesepizza", "pepperoni pizza", "sausage pizza"], whopperId : ""}

gets back "status" if "Success" then can access the whopper image at:
https://mdw.bk.com/assets/whopper/images/{uuid}.png

# Where to Pull Food Databases

For check_all_foods_foundation: https://fdc.nal.usda.gov/download-datasets.html
