from openai import OpenAI

client = OpenAI()

toppings = []
i = 0
get_meat = input("What type of meat? impossible or beef?")



while i < 8:
    get_topping = input("What is your topping? Say DONE when finished. Up to 8 toppings")
    if get_topping.lower() == "done":
        break
    toppings.append(get_topping)
    i += 1

join_top = '\n'.join(toppings)

start_prompt = f"Please generate a beautiful hamburger that has an {get_meat} patty and these toppings: {join_top}\n Only include the listed toppings. Do not add any others. Do not add any condiments unless specifically specified. Generate the burger on a solid green background. Do not include anything else in the image except the burger."


response = client.images.generate(
  model="dall-e-3",
  prompt=start_prompt,
  size="512x512",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
print(image_url)