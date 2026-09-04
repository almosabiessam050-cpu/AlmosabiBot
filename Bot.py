import discord
from discord.ext import commands
import urllib.request
import urllib.parse
import os

# قراءة التوكن من متغيرات Railway
TOKEN = os.getenv('DISCORD_TOKEN')
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'تم تشغيل البوت: {bot.user}')

# دالة مساعدة لرسم الصور
async def generate_image(ctx, prompt):
    msg = await ctx.send(f'⏳ جاري رسم: {prompt}...')
    
    try:
        # استخدام خدمة Stability AI
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
        
        with open('generated_image.png', 'wb') as f:
            f.write(image_data)
        
        await msg.delete()
        await ctx.send(file=discord.File('generated_image.png'))
        
    except Exception as e:
        await msg.delete()
        await ctx.send(f'حدث خطأ أثناء توليد الصورة: {e}')

# أمر الرسم العام
@bot.command()
async def draw(ctx, *args):
    if not args:
        await ctx.send('الرجاء كتابة وصف الصورة. مثال: !draw a beautiful woman')
        return
    prompt = ' '.join(args)
    await generate_image(ctx, prompt)

# أمر رسم فلسطين
@bot.command()
async def palestine(ctx):
    await generate_image(ctx, "The Al-Aqsa Mosque in Jerusalem, golden dome, beautiful Palestinian landscape, ancient stone walls, olive trees, warm sunset lighting, breathtaking view")

# أمر رسم الدول
@bot.command()
async def country(ctx, *args):
    if not args:
        await ctx.send('الرجاء كتابة اسم الدولة. مثال: !country Egypt')
        return
    country_name = ' '.join(args).lower()
    
    # إذا كانت الدولة موجودة في القائمة الذكية
    if country_name in country_landmarks:
        await generate_image(ctx, country_landmarks[country_name])
    else:
        await generate_image(ctx, f"The most beautiful landmarks and iconic scenery of {country_name}, famous tourist attractions, beautiful view, cultural heritage")

# أوامر مختصرة واحترافية
@bot.command()
async def portrait(ctx, *args):
    prompt = ' '.join(args) if args else 'a beautiful woman'
    await generate_image(ctx, prompt, "professional portrait")

@bot.command()
async def landscape(ctx, *args):
    prompt = ' '.join(args) if args else 'a breathtaking mountain landscape'
    await generate_image(ctx, prompt, "epic landscape")

@bot.command()
async def animal(ctx, *args):
    prompt = ' '.join(args) if args else 'a majestic lion'
    await generate_image(ctx, prompt, "wildlife photography")

@bot.command()
async def city(ctx, *args):
    prompt = ' '.join(args) if args else 'a futuristic city at night'
    await generate_image(ctx, prompt, "cyberpunk city")

@bot.command()
async def car(ctx, *args):
    prompt = ' '.join(args) if args else 'a luxury sports car'
    await generate_image(ctx, prompt, "automotive photography")

@bot.command()
async def space(ctx, *args):
    prompt = ' '.join(args) if args else 'a stunning galaxy'
    await generate_image(ctx, prompt, "astrophotography")

# أمر المساعدة
@bot.command()
async def commands(ctx):
    help_text = """
**📜 قائمة أوامر البوت:**
• `!palestine` : رسم المسجد الأقصى وفلسطين
• `!country [اسم الدولة]` : رسم معالم أي دولة
• `!draw [وصف]` : رسم أي شيء تريده
• `!portrait [وصف]` : رسم بورتريه شخصي
• `!landscape [وصف]` : رسم منظر طبيعي
• `!animal [وصف]` : رسم حيوان
• `!city [وصف]` : رسم مدينة
• `!car [وصف]` : رسم سيارة
• `!space [وصف]` : رسم الفضاء
• `!ping` : اختبار اتصال البوت
    """
    await ctx.send(help_text)

bot.run(TOKEN)
