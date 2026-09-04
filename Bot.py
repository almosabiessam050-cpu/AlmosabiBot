import discord
from discord.ext import commands
import urllib.request
import urllib.parse
import os
import json

# قراءة التوكن من متغيرات Railway
TOKEN = os.getenv('DISCORD_TOKEN')
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'تم تشغيل البوت: {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def draw(ctx, *args):
    if not args:
        await ctx.send('الرجاء كتابة وصف الصورة. مثال: !draw a realistic portrait')
        return

    prompt = ' '.join(args)
    msg = await ctx.send(f'⏳ جاري رسم: {prompt}...')

    try:
        # استخدام Stability AI API
        url = "https://api.stability.ai/v2beta/stable-image/generate/core"
        data = urllib.parse.urlencode({
            "prompt": prompt,
            "aspect_ratio": "3:2"
        }).encode()
        
        req = urllib.request.Request(url, data=data, headers={
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "image/*"
        })
        
        with urllib.request.urlopen(req, timeout=180) as response:
            image_data = response.read()
        
        # حفظ الصورة وإرسالها
        with open('generated_image.png', 'wb') as f:
            f.write(image_data)
        
        await msg.delete()
        await ctx.send(file=discord.File('generated_image.png'))
        
    except Exception as e:
        await msg.delete()
        await ctx.send(f'حدث خطأ أثناء توليد الصورة: {e}')

bot.run(TOKEN)
