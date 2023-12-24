def sleeping_time(func):
    def wrapper():
        print("Проснулся")
        func()
        print("Лег спать")
    return wrapper


def eating_time(func):
    def wrapper():
        print("Позавтракал")
        func()
        print("Поужинал")
    return wrapper


def school_trip(func):
    def wrapper():
        print("Иду в школу")
        func()
        print("Иду со школы")
    return wrapper


@sleeping_time
@eating_time
@school_trip
def regular_school_day():
    print("Учусь")


regular_school_day()