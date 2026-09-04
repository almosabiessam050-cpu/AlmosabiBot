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
async def draw(ctx, *args):
    if not args:
        await ctx.send('الرجاء كتابة وصف الصورة. مثال: !draw a realistic portrait')
        return

    prompt = ' '.join(args)
    msg = await ctx.send(f'⏳ جاري رسم: {prompt}...')

    try:
        # استخدام Stability AI API
        url = "https://api.stability.ai/v2beta/stable-image/generate/core"
        headers = {
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Accept": "image/*"
        }
        # إرسال الطلب بصيغة Form-Data
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        body = f'--{boundary}\r\nContent-Disposition: form-data; name="prompt"\r\n\r\n{prompt}\r\n--{boundary}\r\nContent-Disposition: form-data; name="aspect_ratio"\r\n\r\n3:2\r\n--{boundary}--\r\n'
        
        req = urllib.request.Request(url, data=body.encode(), headers={
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "image/*"
        })
        
        with urllib.request.urlopen(req, timeout=120) as response:
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
