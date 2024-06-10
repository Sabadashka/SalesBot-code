from datetime import datetime

last_click_times = {}

warning_phrases = [
    "<blockquote>😅 Не потрібно так натискати на кнопки. Зачекайте трошки перед наступним натисканням</blockquote>",
    "<blockquote>😬 Вибачте, але Ви натискатимете на кнопки швидше за нашого бота! Потрібно трохи зачекати</blockquote>",
    "<blockquote>😱 Нам дуже прикро, але якщо Ви будете так швидко натискати кнопки, бот може захворіти на стрес!</blockquote>",
    "<blockquote>🤖 Ми любимо Ваш ентузіазм, але будь ласка, дайте нашому боту трохи відпочинку від натискання кнопок</blockquote>",
    "<blockquote>💪Ви справжній майстер швидкого натискання кнопок! Іноді потрібно трошки зачекати на результат</blockquote>",
    "<blockquote>🚀 Швидке натискання кнопок - це як швидкий поштовх в зад. Дайте боту трохи простору для дихання!</blockquote>",
    "<blockquote>⏳ Бот також має свої справи. Натискання кнопок не допоможе йому прискорити відповідь</blockquote>",
    "<blockquote>🙏 Дякуємо за ваше натхнення, але потрібно трошки зачекати, перш ніж натискати наступну кнопку</blockquote>",
    "<blockquote>😅 Ой, Ви забагато натискнули на кнопки! Давайте трохи відпочинемо перед наступним натисканням.</blockquote>",
    "<blockquote>😱 Швидкість вашого натискання вражає, але дайте іншим користувачам також шанс взяти участь у взаємодії з ботом</blockquote>",
    "<blockquote>🤖 Ми всі захоплені вашою активністю, але боту теж потрібен час для обробки запитів. Нехай він трошки відпочине</blockquote>",
    "<blockquote>💪 Послідовність натискань - ваше головне бачення! Але іноді варто зачекати, щоб насолодитися результатом</blockquote>",
    "<blockquote>🚀 Швидкість світла може завидувати вашій швидкості натискання! Проте варто трошки відпочити перед новими зверненнями до бота</blockquote>",
    "<blockquote>⏳ Час тече швидко, але не забувайте, що і бот потребує часу на обробку запитів. Нехай він трошки розслабиться перед наступним викликом</blockquote>",
    "<blockquote>😂 Ого, Ви точно не клацали мишкою на роботі! Давайте знайомитися повільніше з нашим ботом.</blockquote>",
    "<blockquote>🤪 Ви, як настільки швидкий Флеш, що боту потрібен відпочинок від вашої світлової швидкості!</blockquote>",
    "<blockquote>😆 Ваші пальці майже згоріли від швидкості! Потрібно розслабитися перед новими натисканнями кнопок</blockquote>",
    "<blockquote>🤭 Натискання кнопок так швидко - це як спроба зламати рекорд Гіннесса. Але нам трошки треба відпочити від цього забавного змагання!</blockquote>",
    "<blockquote>🤓 Ви точно вивчали швидкісне натискання кнопок у своєму попередньому житті! Але давайте трошки зачекаємо перед наступними кліками</blockquote>",
    "<blockquote>😇 Якщо б кожен клік кнопки був доларом, Ви були б мільйонером! Але трошки спокою перед наступними діями не зашкодить</blockquote>",
    "<blockquote>😎 Ну давайте зіграємо в гру - хто перше втомиться: Ви або бот? Я на вашому боці, але давайте дати боту трошки відпочинку</blockquote>",
    "<blockquote>🤣 Це така швидкість, що навіть блискавка не може догнати! Та все-таки, хто знає, що тут може трапитися, давайте трохи зупинимося на мить</blockquote>",
    "<blockquote>😂 Якщо Ви продовжите так швидко натискати кнопки, можливо, ви розгубите нашого бота! Давайте дати йому трохи часу на обробку</blockquote>",
    "<blockquote>🤪 Здається, Ви натискатимете кнопки так швидко, що час буде йти назад! Але трошки спокою завжди буде корисним</blockquote>",
    "<blockquote>🤣 Ці кнопки не тікають, вони ще будуть тут, коли ви зупинитесь! Так давайте відкриємо більше кав'ярню й трошки відпочинемо</blockquote>",
    "<blockquote>😜 На цьому боті немає кнопки турбо! Тож давайте трошки сповільнимося й насолоджуватися подорожжю</blockquote>",
    "<blockquote>🐢 Навіть черепаха швидше зупиниться, ніж ви натискатимете кнопки! Давайте трошки зачекаємо</blockquote>",
    "<blockquote>🐌 Здається, ці кнопки отримали би Вас на Олімпійських іграх! Але для бота краще трошки спокою</blockquote>",
    "<blockquote>🚶‍♂️ Зупиніться на хвилину та подивіться навколо - Ви можете втратити бота! Трохи спокою завжди корисно</blockquote>",
    "<blockquote>👀 Це така швидкість, що й ваша відповідь буде передбачена ботом! Давайте трошки зачекаємо на кращий результат</blockquote>",
    "<blockquote>🏎️ Навіть Феррарі не встигає за вашим натисканням кнопок! Але давайте трошки зачекаємо, щоб бот міг наздогнати</blockquote>",
    "<blockquote>🚀 Вибачте, але бот ще не отримав свій щоденний заряд енергії! Трошки зачекайте, і він буде готовий відповісти</blockquote>",
    "<blockquote>🤖 Ой, вибачте! Якщо ви так швидко натискатимете кнопки, бот може подумати, що його переслідують</blockquote>",
    "<blockquote>😄 Ви так швидко натискатимете кнопки, що ваше око може не вловити, як швидко бот відповідає!</blockquote>",
    "<blockquote>🔨 Натискання кнопок так швидко - це як кувати молотом! Подумайте про дрібниці і трошки зачекайте</blockquote>",
    "<blockquote>🐰 Ви ще краще за кролика з забігу! Але навіть він іноді потребує трошки відпочинку.</blockquote>"
]


def check_message_interval(acc_id, button_text, interval_seconds=3):
    current_time = datetime.now()
    last_click_time = last_click_times.get(acc_id, {}).get(button_text)
    if last_click_time is not None:
        time_diff = current_time - last_click_time
        if time_diff.total_seconds() < interval_seconds:
            return False

    if acc_id not in last_click_times:
        last_click_times[acc_id] = {}
    last_click_times[acc_id][button_text] = current_time
    return True