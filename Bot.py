import discord
from discord.ext import commands
import urllib.request
import urllib.parse
import os

# قراءة التوكن من متغيرات Railway
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'تم تشغيل البوت: {bot.user}')

# قائمة ذكية بالمعالم السياحية للدول
country_landmarks = {
    "egypt": "The Great Pyramids of Giza and the Sphinx, ancient Egyptian architecture, golden sand dunes, dramatic sunset lighting",
    "turkey": "The Hagia Sophia and Blue Mosque in Istanbul, Ottoman architecture, beautiful Bosphorus view",
    "japan": "Mount Fuji, cherry blossom trees, traditional Japanese temples, spring season",
    "france": "The Eiffel Tower in Paris, beautiful cityscape, romantic atmosphere",
    "saudi arabia": "The Kaaba in Mecca, beautiful Islamic architecture, desert landscapes",
    "usa": "The Statue of Liberty in New York, cityscape, skyscrapers",
    "uk": "Big Ben and the Tower of London, beautiful historic architecture",
    "italy": "The Colosseum in Rome, beautiful historic architecture, Mediterranean atmosphere",
    "china": "The Great Wall of China, beautiful mountains, ancient architecture",
    "qatar": "The skyline of Doha, modern architecture, stunning sunset",
    "uae": "The Burj Khalifa in Dubai, modern cityscape, desert landscape",
    "germany": "The Brandenburg Gate, historic architecture, beautiful cityscape",
    "india": "The Taj Mahal, beautiful marble architecture, warm sunset",
    "jordan": "The ancient city of Petra, carved rock architecture, desert canyon",
    "palestine": "The Al-Aqsa Mosque in Jerusalem, golden dome, beautiful Palestinian landscape, olive trees, warm sunset"
}

# دالة مساعدة لرسم الصور
async def generate_image(ctx, prompt, extra_style=""):
    msg = await ctx.send(f'⏳ جاري رسم: {prompt}...')
    
    try:
        full_prompt = f"{prompt}, {extra_style}, photorealistic, ultra realistic, 8k resolution, highly detailed, sharp focus, cinematic lighting, professional photography, depth of field, dramatic shadows"
        
        url = f'https://image.pollinations.ai/prompt/{urllib.parse.quote(full_prompt)}?width=1024&height=1024&nologo=true'
        
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
    await generate_image(ctx, country_landmarks["palestine"])

# أمر رسم الدول
@bot.command()
async def country(ctx, *args):
    if not args:
        await ctx.send('الرجاء كتابة اسم الدولة. مثال: !country Egypt')
        return
    country_name = ' '.join(args).lower()
    
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

@bot.command()
async def cat(ctx):
    await generate_image(ctx, "a cute fluffy cat, realistic")

@bot.command()
async def dog(ctx):
    await generate_image(ctx, "a cute golden retriever dog, realistic")

@bot.command()
async def robot(ctx):
    await generate_image(ctx, "a futuristic robot, high tech, realistic")

@bot.command()
async def food(ctx, *args):
    prompt = ' '.join(args) if args else 'a delicious burger'
    await generate_image(ctx, prompt, "food photography")

@bot.command()
async def house(ctx, *args):
    prompt = ' '.join(args) if args else 'a beautiful modern house'
    await generate_image(ctx, prompt, "architectural photography")

@bot.command()
async def nature(ctx, *args):
    prompt = ' '.join(args) if args else 'a beautiful forest with sunlight'
    await generate_image(ctx, prompt, "nature photography")

@bot.command()
async def ocean(ctx, *args):
    prompt = ' '.join(args) if args else 'a beautiful tropical ocean'
    await generate_image(ctx, prompt, "underwater photography")

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
• `!cat` : رسم قطة
• `!dog` : رسم كلب
• `!robot` : رسم روبوت
• `!food [وصف]` : رسم طعام
• `!house [وصف]` : رسم منزل
• `!nature [وصف]` : رسم طبيعة
• `!ocean [وصف]` : رسم محيط
• `!ping` : اختبار اتصال البوت
    """
    await ctx.send(help_text)

bot.run(TOKEN)
