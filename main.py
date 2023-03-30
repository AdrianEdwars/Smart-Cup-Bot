import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

session = vk_api.VkApi(
    token="vk1.a.BkFKcSk0gZ-nEN9Q6Sbc0rzb7etqmDHNOeIkHuHxgOjKYQk0Zd7IIg9N5dtnAWSgFAm5c-eXOv8zS2ya33PzwYKrbcUK6o_0eVtZWGgaeT1A19Rx5UhqgJBedXMdcvEHTDBBm61IvX7Qe1ahfK4eKmEnHABp0b8hGCUb5YxYfzWAYKijfbMQAappnb8p2Mu65B4z9MOoiCuoQC3PdZbr7Q")

# Global variables
status = 2
ANSWERS = []
i, k, lang = 0, 0, 0
# Russian and English questions for first story!
RU_QUESTIONS1 = [
    "Название твоего города.", "Существо мужского рода.", "Куда? (без предлога)", "Из чего? (без предлога в Родительном падеже)",
    "Какая твоя самая любимая вещь? (В женском роде, 1 склонение.)", "К чему? (без предлога)", "Ваша история готова!"
]
ENG_QUESTIONS1 = [
    "Which city are you from?", "Creature", "To where? (Without pretext)", "Your favourite material",
    "What's your favourite object?", "Any place", "Your history is done."
]
# Russian and English questions for second story!
RU_QUESTIONS2 = [
    "Где бы ты мечтал побывать? (без предлога в мужском роде)", "Что ты собираешься делать?",
    "Как зовут вашего монстра?", "Куда? (без предлога в винительном падеже)", "Любой предмет (в винительном падеже)", "Любое оружие (в мужском роде)", "Ваша история готова!"
]
ENG_QUESTIONS2 = [
    "Where would you like to go?", "What would you gonna do?",
    "Name of monster, who you very afraid of.", "To where?  (Without pretext)", "Any object", "Any gun", "Your history is done."
]

def send_message(user_id, message, keyboard=None):
    post = {
        "user_id": user_id,
        "message": message,
        "random_id": 0,
    }

    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    else:
        post = post
    session.method("messages.send", post)


for event in VkLongPoll(session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower()
        user_id = event.user_id

        if lang == 0:
            if text == 'история' or text == 'change language 🇷🇺' and status != 1:
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("Поиски затерянного артефакта 🏺", VkKeyboardColor.PRIMARY)
                keyboard.add_button("Путешествие к загадочному зданию 🧙‍", VkKeyboardColor.PRIMARY)
                keyboard.add_button("Сменить язык 🇬🇧", VkKeyboardColor.PRIMARY)
                send_message(user_id, "Выберите сценарий истории. Или смените язык.", keyboard)
                status = 0
            if text == 'сменить язык 🇬🇧' and status == 0:
                lang = 1
                send_message(user_id, "Вы успешно изменили язык на английский (You succesfully changed language to English)")
            if text == 'поиски затерянного артефакта 🏺' and status == 0:
                status = 1
                ANSWERS = []
                i = 0
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("Хватит ❌", VkKeyboardColor.NEGATIVE)
                send_message(user_id,
                             "Отлично! Сейчас я вам задам несколько вопросов. Отвечайте на них одним словом в нужной форме.\nИтак, первый вопрос. Как зовут вашего отца?",
                             keyboard)
            if text == "путешествие к загадочному зданию 🧙‍" and status == 0:
                status = 3
                ANSWERS = []
                k = 0
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("Хватит ❌", VkKeyboardColor.NEGATIVE)
                send_message(user_id,
                             "Отлично! Сейчас я вам задам несколько вопросов. Отвечайте на них одним словом в нужной форме.\nИтак, первый вопрос. Как зовут вашего друга?",
                             keyboard)

            if text == 'хватит ❌' and status > 0:
                send_message(user_id, "Окей, если захотите играть скажите - история.")
                status = 0
            if text is not None and status == 3 and not text in ["поиски затерянного артефакта 🏺", "путешествие к загадочному зданию 🧙‍"]:
                ANSWERS.append(text)
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("Хватит ❌", VkKeyboardColor.NEGATIVE)
                send_message(user_id, RU_QUESTIONS2[k], keyboard)
                k += 1
            if text is not None and status == 1 and not text in ["поиски затерянного артефакта 🏺", "путешествие к загадочному зданию 🧙‍"]:
                ANSWERS.append(text)
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("Хватит ❌", VkKeyboardColor.NEGATIVE)
                send_message(user_id, RU_QUESTIONS1[i], keyboard)
                i += 1
            if k == 7 and status == 3:
                ANSWERS.append(text)
                ANSWERS[0] = ANSWERS[0].capitalize()
                print(ANSWERS)
                send_message(user_id,
f"""Однажды {ANSWERS[0]} отправился в долгое путешествие по миру фэнтези. Первой остановкой был {ANSWERS[1]}. В это место, люди приходили в поисках невероятного оружия под названием "{ANSWERS[6]}", который даровал своему обладателю неограниченную власть. {ANSWERS[0]} также присоединился к поиску и отправился в {ANSWERS[4]}.
Вскоре он обнаружил {ANSWERS[6]} в таинственной пещере, но что-то пошло не так. Когда он схватил {ANSWERS[5]}, произошло что-то невероятное. Внезапно перед ним появился {ANSWERS[3]}, готовый атаковать. {ANSWERS[0]} выхватил {ANSWERS[7]} и встал на защиту. Но оружие оказалось не таким уж и эффективным. Тогда {ANSWERS[0]} решил {ANSWERS[2]}, и это помогло ему победить монстра и вернуться назад в {ANSWERS[1]}.""")
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("История", VkKeyboardColor.PRIMARY)
                keyboard.add_button("Хватит ❌", VkKeyboardColor.NEGATIVE)
                send_message(user_id, "Выбирайте, что будем делать дальше?", keyboard)
                status = 2
            if i == 7 and status == 1:
                ANSWERS.append(text)
                ANSWERS[0] = ANSWERS[0].capitalize()
                ANSWERS[2] = ANSWERS[2].capitalize()
                print(ANSWERS)
                send_message(user_id,
f"""Жил-был молодой герой по имени {ANSWERS[0]}. Он жил в маленькой деревушке на окраине королевства "{ANSWERS[1].capitalize()}". Однажды {ANSWERS[0]} отправился на прогулку в лес и наткнулся на существо по имени - "{ANSWERS[2]}". {ANSWERS[2]} смотрел на нашего героя странным взглядом и спросил: "Ты готов совершить путешествие в "{ANSWERS[3]}"?" {ANSWERS[0]} не знал, что делать, но решился и ответил "Да, я готов!".
{ANSWERS[0].capitalize()} и {ANSWERS[2]} отправились в путешествие через темный лес, который казался бесконечным. Вскоре они пришли к {ANSWERS[6]}, которое было полностью построено из {ANSWERS[4]}. {ANSWERS[2]} сказал: "Мы пришли за артефактом под названием "{ANSWERS[5]}", который был спрятан внутри этого здания много лет назад". {ANSWERS[0]} почувствовал себя немного напуганным, но его любопытство взяло верх, и он решил идти внутрь здания вместе с {ANSWERS[2]}.
Они преодолели множество опасностей, прежде чем нашли {ANSWERS[5][:-1]}у. Но внезапно {ANSWERS[0]} услышал странный звук, и {ANSWERS[2]} исчез. {ANSWERS[0]} остался один в здании, но он знал, что должен вернуться домой и рассказать всем свою историю.""")
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("История", VkKeyboardColor.PRIMARY)
                keyboard.add_button("Хватит ❌", VkKeyboardColor.NEGATIVE)
                send_message(user_id, "Выбирайте, что будем делать дальше?", keyboard)
                status = 2
        else:
            if text == 'history' or text == 'сменить язык 🇬🇧' and status != 1:
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("Finding a Lost Artifact 🏺", VkKeyboardColor.PRIMARY)
                keyboard.add_button("Journey to the Mysterious Building 🧙‍", VkKeyboardColor.PRIMARY)
                keyboard.add_button("Change language 🇷🇺", VkKeyboardColor.PRIMARY)
                send_message(user_id, "Choose script or change language.", keyboard)
                status = 0
            if text == 'change language 🇷🇺' and status == 0:
                lang = 0
                send_message(user_id, "Вы успешно изменили язык на русский (You succesfully changed language to Russian)")
            if text == 'finding a lost artifact 🏺' and status == 0:
                status = 1
                ANSWERS = []
                i = 0
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("Stop ❌", VkKeyboardColor.NEGATIVE)
                send_message(user_id, "Great! Now I will ask you a few questions. Answer them with one word in the right form.\nFirst question: What's your name?",
                             keyboard)
            if text == "journey to the mysterious building 🧙‍" and status == 0:
                status = 3
                ANSWERS = []
                k = 0
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("Stop ❌", VkKeyboardColor.NEGATIVE)
                send_message(user_id, "Great! Now I will ask you a few questions. Answer them with one word in the right form.\nFirst question: What's your name?",
                             keyboard)

            if text == 'stop ❌' and status > 0:
                send_message(user_id, "Okey, if you want to start - enter 'history'")
                status = 0
            if text is not None and status == 3 and not text in ["finding a lost artifact 🏺", "journey to the mysterious building 🧙‍"]:
                ANSWERS.append(text)
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("Хватит ❌", VkKeyboardColor.NEGATIVE)
                send_message(user_id, ENG_QUESTIONS2[k], keyboard)
                k += 1
            if text is not None and status == 1 and not text in ["finding a lost artifact 🏺", "journey to the mysterious building 🧙‍"]:
                ANSWERS.append(text)
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("Хватит ❌", VkKeyboardColor.NEGATIVE)
                send_message(user_id, ENG_QUESTIONS1[i], keyboard)
                i += 1
            if k == 7 and status == 3:
                ANSWERS.append(text)
                ANSWERS[0] = ANSWERS[0].capitalize()
                print(ANSWERS)
                send_message(user_id,
f"""Once upon a time, {ANSWERS[0]} embarked on a long journey through the fantasy world. The first stop was {ANSWERS[1]}. People came to this place in search of the {ANSWERS[6]}, which bestowed unlimited power upon its owner. {ANSWERS[0]} also joined the search and set off in the direction of {ANSWERS[4]}. Soon he discovered the {ANSWERS[6]} in a mysterious cave, but something went wrong.
When he grabbed the object, something incredible happened. Suddenly, a {ANSWERS[3]} appeared before him, ready to attack. {ANSWERS[0]} grabbed {ANSWERS[7]} and stood up for himself. But the weapon turned out to be not so effective. Then {ANSWERS[0]} decided to {ANSWERS[2]}, and it helped him defeat the monster and return with the object back to {ANSWERS[1]}.""")
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("History", VkKeyboardColor.PRIMARY)
                keyboard.add_button("Stop ❌", VkKeyboardColor.NEGATIVE)
                send_message(user_id, "Choose what to do next?", keyboard)
                status = 2
            if i == 7 and status == 1:
                ANSWERS.append(text)
                ANSWERS[0] = ANSWERS[0].capitalize()
                ANSWERS[2] = ANSWERS[2].capitalize()
                send_message(user_id,
f"""Once upon a time, there was a young hero named {ANSWERS[0]}. He lived in a small village on the outskirts of the "{ANSWERS[1]}" kingdom. One day, {ANSWERS[0]} went for a walk in the forest and stumbled upon a {ANSWERS[2]}. {ANSWERS[2]} looked at {ANSWERS[0]} with a strange gaze and asked, "Are you ready to embark on a journey to "{ANSWERS[3]}"?" {ANSWERS[0]} didn't know what to do, but he gathered his courage and replied, "Yes, I am ready!"
 {ANSWERS[0]} and {ANSWERS[2]} set off on a journey through the dark forest, which seemed endless. Soon, they arrived at a {ANSWERS[6]} that was entirely built from {ANSWERS[4]}. {ANSWERS[2]} said, "We have come for the {ANSWERS[5]} that was hidden inside this building many years ago." {ANSWERS[0]} felt a little scared, but his curiosity took over, and he decided to enter the building together with {ANSWERS[2]}.
 They overcame many dangers before they found the {ANSWERS[5]}. But suddenly, {ANSWERS[0]} heard a strange sound, and {ANSWERS[2]} disappeared. {ANSWERS[0]} was left alone in the building, but he knew that he had to return home and tell everyone his story.""")
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("History", VkKeyboardColor.PRIMARY)
                keyboard.add_button("Stop ❌", VkKeyboardColor.NEGATIVE)
                send_message(user_id, "Choose what to do next?", keyboard)
                status = 2
