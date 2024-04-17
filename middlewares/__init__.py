# from .Big_brother import BigBrother УБРАТЬ ЭТОТ СЛЭШ
from loader import dp
from .throttling import ThrottlingMiddleware

if __name__ == "middlewares":
    # dp.middleware.setup(BigBrother()) убрать этот слэш чтобы вернуть видение апдейтов
    dp.middleware.setup(ThrottlingMiddleware())