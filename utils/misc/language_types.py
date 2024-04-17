dictionary = {
    "В какой группе вы учитесь? Пример: SI-23-19": "Siz qaysi guruhda o'qiysiz? Misol: SI-23-19",
    "Пожалуйста напишите своё имя с фамилией": "Iltimos, ismingizni familiya bilan yozing",
    "Спасибо, вы успешно прошли регистрацию.": "Rahmat, siz muvaffaqiyatli ro'yxatdan o'tdingiz.",
    "Напишите несколько слов про тему вашего вопроса.\nМаксимум 10 символов.": "Savolingiz mavzusi haqida bir necha so'z yozing.\nMaksimal 10 ta belgi.",
    "Отмена": "bekor qilish",
    "Подтвердить отправку": "Yuborishni tasdiqlang",
    "Написано же, что максимум 10 символов!": "Maksimal 10 ta belgi!",
    "Теперь пришлите сам вопрос.": "Endi savolni o'zini yuboring.",
    "Вы точно хотите задать этот вопрос?": "Siz bu savolni bermoqchimisiz?",
    "Вопрос успешно отправлен.": "Savol muvaffaqiyatli yuborildi.",
    "Получен ответ на вопрос: ": "Savolga javob olindi: "
}


def F_language(answer: str, language='ru'):
    if language == "uz":
        return dictionary[f'{answer}']
    else:
        return answer

