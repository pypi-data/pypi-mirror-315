import random
import string
from datetime import date, datetime, timedelta
from dateutil.parser import parse

class Any:

    @staticmethod
    def of(options: list):
        return random.choice(options)

    @staticmethod
    def listOf(min, max, factoryFunction):
        result = []
        amount = Any.positiveNumber(min, max)
        for i in range(0, amount):
            data = factoryFunction()
            result.append(data)

        return result

    @staticmethod
    def subsetOf(min, max, items):
        items_randomized = random.sample(items, len(items))
        if min == None:
            min=1
        if max == None or max > len(items):
            max=len(items)-1

        amount_to_get = Any.positiveNumber(min=min, max=max)
        return items_randomized[:amount_to_get]

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
    def dateTimeInPast() -> datetime:
        now = datetime.now()
        return now - timedelta(days = Any.positiveNumber())

    @staticmethod
    def dateTimeInFuture() -> datetime:
        now = datetime.now()
        return now + timedelta(days=Any.positiveNumber())

    @staticmethod
    def dateTimeBefore(beforeDateTime) -> datetime:
        if isinstance(beforeDateTime, str):
            beforeDateTime = parse(beforeDateTime, fuzzy=True)

        return beforeDateTime - timedelta(days=Any.positiveNumber())

    @staticmethod
    def dateTimeAfter(afterDateTime) -> datetime:
        if isinstance(afterDateTime, str):
            afterDateTime = parse(afterDateTime, fuzzy=True)

        return afterDateTime + timedelta(days=Any.positiveNumber())

    @staticmethod
    def datetimeBetween(from_datetime, to_datetime) -> datetime:
        if isinstance(from_datetime, str):
            from_datetime = parse(from_datetime, fuzzy=True)

        if isinstance(to_datetime, str):
            to_datetime = parse(to_datetime, fuzzy=True)

        from_datetime_ts = from_datetime.timestamp()
        to_datetime_ts = to_datetime.timestamp()

        random_ts_between = Any.positiveNumber(min=from_datetime_ts, max=to_datetime_ts)

        return datetime.fromtimestamp(random_ts_between)

    @staticmethod
    def dateTime() -> datetime:
        return Any.of([Any.dateTimeInPast(), Any.dateTimeInFuture()])

    @staticmethod
    def date() -> date:
        return Any.dateTime().date()

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
