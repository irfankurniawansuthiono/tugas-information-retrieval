import os
import discord
from discord.ext import commands
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import dotenv

dotenv.load_dotenv()

knowledge_base = [
    "Selamat pagi,\nSaya adalah Nanami, asisten cerdas dan dapat memberikan informasi seputar akademik.\n",
    "UPI YPTK Padang adalah singkatan dari Universitas Putra Indonesia YPTK Padang, sebuah perguruan tinggi swasta di Sumatera Barat.",
    "Alamat UPI YPTK Padang adalah Jl. Raya Lubuk Begalung, Padang, Sumatera Barat, Indonesia.",
    "UPI YPTK Padang memiliki berbagai fakultas seperti Teknik, Ekonomi, Ilmu Komputer, Sastra, dan lainnya.",
    "Universitas ini dikenal dengan program studi di bidang teknologi dan informasi, serta pendekatan pendidikan berbasis praktik.",
    "UPI YPTK Padang berdiri sejak tahun 1985 dan telah menghasilkan ribuan alumni yang tersebar di berbagai sektor.",
    "Moto dari UPI YPTK Padang adalah 'Smart, Creative, and Innovative'.",
    "UPI YPTK Padang memiliki fasilitas lengkap seperti laboratorium komputer, perpustakaan digital, dan koneksi internet kampus.",
    "Salah satu fakultas unggulan di UPI YPTK Padang adalah Fakultas Ilmu Komputer yang memiliki jurusan Teknik Informatika dan Sistem Informasi.",
    "Untuk informasi lebih lanjut, kunjungi situs resmi UPI YPTK Padang di https://www.upiyptk.ac.id/",
    "UPI YPTK Padang juga aktif di media sosial dan sering mengadakan webinar, workshop, serta seminar nasional.",
]


vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(knowledge_base)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} siap membantu!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_input = [message.content]
    user_vector = vectorizer.transform(user_input)

    similarities = cosine_similarity(user_vector, tfidf_matrix)
    max_score_index = similarities.argmax()
    max_score_value = similarities[0][max_score_index]

    if max_score_value > 0.1: 
        best_reply = knowledge_base[max_score_index]
    else:
        best_reply = "Maaf, saya belum bisa menjawab itu."
    print(similarities)
    await message.reply(best_reply)

    await bot.process_commands(message)  

bot.run(os.getenv("DISCORD_TOKEN"))
