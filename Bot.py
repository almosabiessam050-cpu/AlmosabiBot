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

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

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
    await generate_image(ctx, "The Al-Aqsa Mosque in Jerusalem, golden dome, beautiful Palestinian landscape, ancient stone walls, olive trees, warm sunset lighting, breathtaking view")

# أمر رسم الدول
@bot.command()
async def country(ctx, *args):
    if not args:
        await ctx.send('الرجاء كتابة اسم الدولة. مثال: !country Egypt')
        return
    country_name = ' '.join(args)
    prompt = f"The most beautiful landmarks and iconic scenery of {country_name}, famous tourist attractions, beautiful view, cultural heritage"
    await generate_image(ctx, prompt)

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
• `!draw [وصف]` : رسم أي شيء تريده (واقعي)
• `!portrait [وصف]` : رسم بورتريه شخصي واقعي
• `!landscape [وصف]` : رسم منظر طبيعي واقعي
• `!animal [وصف]` : رسم حيوان واقعي
• `!city [وصف]` : رسم مدينة واقعية
• `!car [وصف]` : رسم سيارة واقعية
• `!space [وصف]` : رسم الفضاء الخارجي
• `!ping` : اختبار اتصال البوت
    """
    await ctx.send(help_text)

bot.run(TOKEN)
