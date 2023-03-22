import os
from random import choices

from gtts import gTTS
from english_words import get_english_words_set
from pydub import AudioSegment


OVERLAY_DELAY = 2000  # Сколько мс задержки перед наложением следующего голоса 
SAVE_FILE = "noise.mp3"  # Название файла с результатом

# Конфиг, где определяются голоса
# lang - язык голоса (en | ru)
# slow - медленная скорость (да - True | нет - False)
# words - количество слов, которые должен произнести голос

GENERATE_CONF = [
    {
        "lang": "en",
        "slow": False,
        "words": 50
    },
    {
        "lang": "ru",
        "slow": False,
        "words": 50
    },
    {
        "lang": "ru",
        "slow": True,
        "words": 50
    }
]

def create_russian(slow, words, name):
    ru_text = " ".join(choices(ru, k=words))
    obj = gTTS(text=ru_text, lang="ru", slow=slow)
    obj.save(name)

def create_english(slow, words, name):
    eng = get_english_words_set(['web2'], lower=True)
    eng_text = " ".join([eng.pop() for _ in range(words)])
    obj = gTTS(text=eng_text, lang="en", slow=slow)
    obj.save(name)

FUNCS = {
    "en": create_english,
    "ru": create_russian
}

with open("rus.txt") as ru_file:
    ru = ru_file.read().split()

segments = []

for i in range(len(GENERATE_CONF)):
    name = "file_{0}.mp3".format(i)
    obj = GENERATE_CONF[i]
    FUNCS[obj["lang"]](obj["slow"], obj["words"], name)
    segments.append(AudioSegment.from_mp3(name))

output = segments[0]
for i in range(1, len(segments)):
    output = output.overlay(segments[i], position=OVERLAY_DELAY)
output.export(SAVE_FILE, format="mp3")

for i in range(len(GENERATE_CONF)):
    name = "file_{0}.mp3".format(i)
    if os.path.exists(name):
        os.remove(name)
