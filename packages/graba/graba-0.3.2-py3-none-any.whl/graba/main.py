import random
import string
from datetime import date, datetime, timedelta

class Any:

    @staticmethod
    def of(options: list):
        return random.choice(options)

    @staticmethod
    def listOf(min, max, factoryFunction):
        amount = Any.positiveNumber(min, max)
        return [factoryFunction()] * amount

    @staticmethod
    def subsetOf(amount, items):
        pass

    @staticmethod
    def positiveNumber(min: int = 0, max=9999) -> int:
        return random.randrange(min, max)

    @staticmethod
    def negativeNumber(min: int = -9999, max=0) -> int:
        return random.randrange(min, max)

    @staticmethod
    def anyNumber() -> int:
        return Any.of([Any.positiveNumber(), Any.negativeNumber()])

    @staticmethod
    def rating() -> int:
        return Any.positiveNumber(min=0, max=5)

    @staticmethod
    def anyLetter() -> str:
        return Any.of(list(string.ascii_lowercase))

    @staticmethod
    def word(min = 1, max = 30) -> str:
        length = Any.positiveNumber(min, max)
        alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]

        return ''.join(random.choice(alphabet) for i in range(length))

    @staticmethod
    def sentence(min_words: int = 1, max_words: int = 5) -> str:
        amount_words = Any.positiveNumber(min=min_words, max=max_words)
        words=[]
        for i in range(amount_words):
            words.append(Any.word())

        return ' '.join(words)

    @staticmethod
    def bytes(min=1, max=30) -> bytes:
        word = Any.word(min, max)
        return word.encode('UTF-8')

    @staticmethod
    def url(min=1, max=4) -> str:
        length = Any.positiveNumber(min, max)
        words = []
        for i in range(length):
            words.append(Any.word())

        return "http://www/"+'.'.join(words)

    @staticmethod
    def bool() -> bool:
        return Any.of([True, False])

    @staticmethod
    def email()->str:
        return f"{Any.word(max = 5)}@{Any.word(max=5)}.{Any.of(['com', 'net', 'co.uk', 'es', 'io'])}"

    @staticmethod
    def dateTimeInPast() -> datetime:
        now = datetime.now()
        return now - timedelta(days = Any.positiveNumber())

    @staticmethod
    def dateTimeInFuture() -> datetime:
        now = datetime.now()
        return now + timedelta(days=Any.positiveNumber())

    @staticmethod
    def dateTimeBefore(beforeDateTime: datetime) -> datetime:
        return beforeDateTime - timedelta(days=Any.positiveNumber())

    @staticmethod
    def dateTimeAfter(afterDateTime: datetime) -> datetime:
        return afterDateTime + timedelta(days=Any.positiveNumber())

    @staticmethod
    def dateTime() -> datetime:
        return Any.of([Any.dateTimeInPast(), Any.dateTimeInFuture()])

    @staticmethod
    def date() -> date:
        return Any.dateTime().date()

    @staticmethod
    def country() -> str:
        return Any.of(["España", "Reino Unido", "Francia", "Italia", "Alemania"])

    @staticmethod
    def street_via() -> str:
        return Any.of(["calle", "Avda", "plaza", "corredera", "carretera"])

    @staticmethod
    def postcode() -> str:
        return Any.of(["28015", "23400", "23700", "N153TS", "carretera"])

    @staticmethod
    def city():
        return Any.of(["London", "Madrid", "Buenos Aires", "Vikingolandia", "Coventry"])

    @staticmethod
    def country() -> str:
        return Any.of(["Spain", "United Kingdom", "France", "Ghana", "Argentine", "Italy"])

    @staticmethod
    def streetVia() -> str:
        return Any.of(["street", "road", "square", "avenue"])

    @staticmethod
    def address() -> str:
        return f"{Any.streetVia()} {Any.word()}, {Any.city()}, {Any.country()}"

    @staticmethod
    def latitude(min: int = None, max: int = None) -> str:
        min=-90 if min == None else min
        max=90  if max == None else max
        decimal_places = 4
        random_lat = random.uniform(min, max)

        return f"{round(random_lat, decimal_places)}"

    @staticmethod
    def longitude(min: int = None, max: int = None) -> str:
        min = -180 if min == None else min
        max =  180 if max == None else max
        decimal_places = 4
        random_lat = random.uniform(min, max)

        return f"{round(random_lat, decimal_places)}"

    @staticmethod
    def point() -> str:
        return f"Point({Any.longitude()} {Any.latitude()} )"