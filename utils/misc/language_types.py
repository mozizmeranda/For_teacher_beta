dictionary = {
    "В какой группе вы учитесь? Пример: SI-23-19": "Siz qaysi guruhda o'qiysiz? Masalan: SI-23-19",
    "Пожалуйста напишите своё имя с фамилией": "Iltimos, ismingiz va familiyangizni yozing",
    "Спасибо, вы успешно прошли регистрацию.": "Rahmat, siz muvaffaqiyatli ro'yxatdan o'tdingiz.",
    "Напишите несколько слов про тему вашего вопроса.\nМаксимум 15 символов.": "Savolingiz mavzusi haqida yozing.\nMaksimal 15 ta belgi.",
    "Отмена": "bekor qilish",
    "Подтвердить отправку": "Yuborishni tasdiqlang",
    "Написано же, что максимум 15 символов!": "Maksimal 15 ta belgi!",
    "Теперь пришлите сам вопрос.": "Endi savolni o'zini yuboring.",
    "Вы точно хотите задать этот вопрос?": "Siz haqiqatdan ham, bu savolni bermoqchimisiz?",
    "Вопрос успешно отправлен.": "Savol muvaffaqiyatli yuborildi.",
    "Получен ответ на вопрос: ": "Savolga javob olindi: ",
    "Вы вызвали команду для замены ваших данных. Вам придется заново зарегистрироваться.": "Ma'lumotlaringizni o`zgartirish uchun buyruqni chaqirdingiz. Siz qayta ro'yxatdan o'tishingiz kerak bo'ladi.",
    "Задать вопрос": "Savol berish",
    "Вы можете задать вопрос с помощью кнопки ниже.": "Quyidagi tugma yordamida savol qoldirishingiz mumkin.",
    "Вы отменили отправку вопроса. Чтобы отправить вопрос, вам надо заново задать его, нажав другую кнопку.": "Siz savol yuborishni bekor qildingiz. Savolni qayta yuborish uchun quyidagi tugmani bosing.",
    "Код вашего вопроса: ": "Sizni savolingizni codi: ",
    " ": " "
}


def F_language(answer: str, language='ru'):
    if language == "uz":
        return dictionary[f'{answer}']
    else:
        return answer

