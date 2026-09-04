import discord
from discord.ext import commands
import urllib.request
import urllib.parse
import os
import random
import json
from datetime import datetime

# قراءة التوكن من متغيرات Railway
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

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

# الرد الذكي
async def ai_reply(prompt):
    try:
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode()
    except Exception:
        return "عذراً، لم أستطع الإجابة على هذا السؤال."

# الترحيب بالأعضاء الجدد
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    if channel:
        await channel.send(f"🎉 مرحباً بك يا {member.mention} في السيرفر! نتمنى لك وقتاً ممتعاً!")

# حذف الرسائل المسيئة
bad_words = ["سب", "شتم"]

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if any(word in message.content.lower() for word in bad_words):
        await message.delete()
        await message.channel.send(f"⚠️ {message.author.mention}, تم حذف رسالتك لأنها تحتوي على كلمات مسيئة!")

    await bot.process_commands(message)

# أوامر الرسم
@bot.command()
async def draw(ctx, *args):
    if not args:
        await ctx.send('الرجاء كتابة وصف الصورة. مثال: !draw a beautiful woman')
        return
    prompt = ' '.join(args)
    await generate_image(ctx, prompt)

@bot.command()
async def palestine(ctx):
    await generate_image(ctx, country_landmarks["palestine"])

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

# أوامر الذكاء الاصطناعي
@bot.command()
async def ask(ctx, *args):
    if not args:
        await ctx.send('الرجاء كتابة سؤالك. مثال: !ask ما هي عاصمة فرنسا؟')
        return
    prompt = ' '.join(args)
    reply = await ai_reply(prompt)
    await ctx.send(reply)

# أوامر النكات والاقتباسات
@bot.command()
async def joke(ctx):
    jokes = [
        "لماذا لا يذهب الدجاج إلى المدرسة؟ لأن لديه الكثير من الكتاكيت! 😂",
        "قال المبرمج لصديقه: حياتي كلها صفر وواحد! 😂",
        "ماذا قال الكمبيوتر للجوال؟ أنت ذكي جداً! 😂",
        "لماذا لم يذهب الضوء إلى الحفلة؟ لأنه كان مشغولاً! 😂"
    ]
    await ctx.send(random.choice(jokes))

@bot.command()
async def quote(ctx):
    quotes = [
        "النجاح هو مجموع جهود صغيرة تتكرر كل يوم. - روبرت كولير",
        "العقل السليم في الجسم السليم. - المثل اليوناني",
        "من جدّ وجد، ومن زرع حصد. - مثل عربي",
        "القراءة غذاء العقل والروح. - مجهول"
    ]
    await ctx.send(random.choice(quotes))

# أمر الطقس
@bot.command()
async def weather(ctx, *args):
    if not args:
        await ctx.send('الرجاء كتابة اسم المدينة باللغة الإنجليزية. مثال: !weather Dubai')
        return
    city = ' '.join(args)
    try:
        # استخدام خدمة Open-Meteo للطقس (أكثر دقة وموثوقية)
        # أولاً: البحث عن إحداثيات المدينة
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1&language=ar&format=json"
        geo_req = urllib.request.Request(geo_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(geo_req, timeout=15) as response:
            geo_data = json.loads(response.read())
        
        if not geo_data['results']:
            await ctx.send(f"عذراً، لم أجد مدينة باسم {city}")
            return
        
        latitude = geo_data['results'][0]['latitude']
        longitude = geo_data['results'][0]['longitude']
        
        # ثانياً: الحصول على الطقس
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        weather_req = urllib.request.Request(weather_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(weather_req, timeout=15) as response:
            weather_data = json.loads(response.read())
        
        temperature = weather_data['current_weather']['temperature']
        wind_speed = weather_data['current_weather']['windspeed']
        
        await ctx.send(f"🌤️ الطقس في {city}:\n🌡️ درجة الحرارة: {temperature} درجة مئوية\n💨 سرعة الرياح: {wind_speed} كم/ساعة")
        
    except Exception as e:
        await ctx.send(f"عذراً، لم أستطع معرفة الطقس في {city}")

# أوامر إضافية
@bot.command()
async def gif(ctx, *args):
    if not args:
        await ctx.send('الرجاء كتابة وصف الصورة المتحركة. مثال: !gif happy')
        return
    prompt = ' '.join(args)
    try:
        url = f"https://api.tenor.com/v1/search?q={urllib.parse.quote(prompt)}&key=LIVDSRZULELA&limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read())
            if data['results']:
                gif_url = data['results'][0]['media'][0]['gif']['url']
                await ctx.send(gif_url)
            else:
                await ctx.send("لم أجد صورة متحركة مناسبة")
    except Exception:
        await ctx.send("حدث خطأ أثناء البحث عن الصورة المتحركة")

@bot.command()
async def calc(ctx, *args):
    if not args:
        await ctx.send('الرجاء كتابة العملية الحسابية. مثال: !calc 5+5')
        return
    try:
        expression = ' '.join(args)
        result = eval(expression)
        await ctx.send(f"🧮 {expression} = {result}")
    except Exception:
        await ctx.send("عذراً، لم أستطع حساب هذه العملية")

@bot.command()
async def time(ctx):
    now = datetime.now()
    await ctx.send(f"🕐 الوقت الحالي هو: {now.strftime('%H:%M:%S')}")

@bot.command()
async def meme(ctx):
    try:
        url = "https://api.imgflip.com/get_memes"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read())
            memes = data['data']['memes']
            meme = random.choice(memes)
            meme_url = meme['url']
            await ctx.send(meme_url)
    except Exception:
        await ctx.send("حدث خطأ أثناء البحث عن ميم")

# أمر المساعدة
@bot.command()
async def commands(ctx):
    help_text = """
**📜 قائمة أوامر البوت:**
• `!ask [سؤال]` : الرد الذكي على الأسئلة
• `!weather [مدينة]` : معرفة حالة الطقس (بالإنجليزية)
• `!gif [وصف]` : إرسال صورة متحركة
• `!calc [عملية]` : آلة حاسبة
• `!time` : معرفة الوقت الحالي
• `!meme` : إرسال ميم عشوائي
• `!joke` : إرسال نكتة عشوائية
• `!quote` : إرسال اقتباس عشوائي
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
