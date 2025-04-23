import { Client, GatewayIntentBits } from 'discord.js';
import natural from 'natural';

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

// Contoh pengetahuan sederhana
const knowledgeBase = [
 `Selamat pagi,\nSaya adalah Nanami, asisten cerdas dan dapat memberikan informasi seputar akademik. \n`,
  "Alamat UPM berada di blablabla",
  "halo, selamat datang di server kami!",
  "irfan adalah pengembang saya.",
  "Saya adalah Nanami, asisten cerdas yang dikembangkan oleh Irfan.",
  "Kunjungi situs irfanks.site untuk info lebih lanjut.",
  "Saya suka diskusi tentang coding, AI, dan teknologi masa depan.",
  "Irfan adalah mahasiswa di UPI YPTK PADANG.",
];
    
const tfidf = new natural.TfIdf();
knowledgeBase.forEach((text) => tfidf.addDocument(text));

client.once('ready', () => {
  console.log(`✅ ${client.user.tag} siap membantu!`);
});

client.on('messageCreate', (message) => {
  if (message.author.bot) return;

  let maxScore = 0;
  let bestReply = "Maaf, saya belum bisa menjawab itu.";

  tfidf.tfidfs(message.content, (i, score) => {
      if (score > maxScore) {
        maxScore = score;
        bestReply = knowledgeBase[i];
        console.log(score, bestReply);
    }
  });

  message.reply(bestReply);
});

client.login(process.env.DISCORD_TOKEN);
