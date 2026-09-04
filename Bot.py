import discord, os, json, urllib.request

TOKEN = os.getenv('DISCORD_TOKEN') # التوكن الخاص ببوتك
STABILITY_KEY = os.getenv('STABILITY_API_KEY') # المفتاح الجديد
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'تم تشغيل البوت: {bot.user}')

@bot.command()
async def draw(ctx, *args):
    prompt = ' '.join(args)
    msg = await ctx.send(f'⏳ جاري رسم: {prompt}...')
    
    data = json.dumps({
        "prompt": prompt, 
        "aspect_ratio": "3:2"
    }).encode()

    req = urllib.request.Request(
        "https://api.stability.ai/v2beta/stable-image/generate/core",
        data=data,
        headers={"Authorization": f"Bearer {STABILITY_KEY}", "Content-Type": "application/json"}
    )
    # ... كود حماية لإرسال الصورة الناتجة لـ Discord
    bot.run(TOKEN)
