import discord
from PIL import Image
import os
import random
from io import BytesIO
from dtoken import TOKEN  # Ensure TOKEN is your bot's token

client = discord.Client(intents=discord.Intents.all())

base_dir = "Images"
layers_order = ["Backgrounds", "Hoodies", "Heads", "Masks", "Eyes"]

def generate_random_color_image(size=(760, 1075)):
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    image = Image.new("RGB", size, color)
    return image

def generate_image():
    final_image = generate_random_color_image()

    for layer in layers_order:
        layer_path = os.path.join(base_dir, layer)
        image_names = os.listdir(layer_path)
        selected_image_name = random.choice(image_names)
        image_path = os.path.join(layer_path, selected_image_name)
        
        layer_image = Image.open(image_path).convert("RGBA")
        if layer_image.size != final_image.size:
            layer_image = layer_image.resize(final_image.size)
        final_image.paste(layer_image, (0, 0), layer_image)
    
    return final_image

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Don't respond to messages sent by the bot itself
    if message.author == client.user:
        return

    if message.content.startswith('!pfp'):
        img = generate_image()
        with BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            await message.channel.send(file=discord.File(fp=image_binary, filename='profile.png'))

client.run(TOKEN)
