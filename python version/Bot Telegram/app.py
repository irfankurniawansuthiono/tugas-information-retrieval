import os
import dotenv
import telebot
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load .env file supaya aman
dotenv.load_dotenv()

# Inisialisasi bot dengan token dari environment variable
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))  

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

# Buat vektor TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(knowledge_base)

# Handler untuk perintah /start dan /hello
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "👋 Halo! Saya Nanami, siap membantu Anda seputar UPI YPTK Padang. Silakan ketik pertanyaan Anda!")

# Handler untuk semua pesan teks biasa
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = [message.text]
    user_vector = vectorizer.transform(user_input)

    similarities = cosine_similarity(user_vector, tfidf_matrix)
    max_score_index = similarities.argmax()
    max_score_value = similarities[0][max_score_index]

    if max_score_value > 0.1:
        best_reply = knowledge_base[max_score_index]
    else:
        best_reply = "Maaf, saya belum memiliki jawaban untuk pertanyaan itu."

    print(f"[Log Similarity] {similarities}")  # buat debugging santai
    bot.reply_to(message, best_reply)

# Menjaga bot tetap hidup
if __name__ == "__main__":
    print("✅ Nanami siap melayani di Telegram!")
    bot.infinity_polling()
