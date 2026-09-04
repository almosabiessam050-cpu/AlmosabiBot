import discord
from discord.ext import commands
import urllib.request
import urllib.parse
import os
import base64

# ضع التوكن هنا
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'تم تشغيل البوت: {bot.user}')

@bot.command()
async def draw(ctx, *args):
    if not args:
        await ctx.send('الرجاء كتابة وصف الصورة. مثال: !draw a realistic portrait')
        return

    prompt = ' '.join(args) + ', photorealistic, ultra realistic, 8k resolution, highly detailed, sharp focus, cinematic lighting'
    encoded_prompt = urllib.parse.quote(prompt)

    msg = await ctx.send(f'⏳ جاري رسم: {prompt}...')

    try:
        # استخدام خدمة رسوم مجانية بديلة
        url = f'https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&model=flux'
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=120) as response:
            data = response.read()
        
        with open('generated_image.png', 'wb') as f:
            f.write(data)
        
        await msg.delete()
        await ctx.send(file=discord.File('generated_image.png'))
        
    except Exception as e:
        await msg.delete()
        await ctx.send(f'حدث خطأ أثناء توليد الصورة: {e}')

bot.run(TOKEN)
