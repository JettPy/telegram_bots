def func(a: int, b: int):
    print(f"Sum of {a} and {b} is {a + b}") 


var = func
# print(var)
# var(1, 1)

# def some_func(f, a, b):
#     print("Сделай что то до функции")
#     f(a, b)
#     print("Сделай что то после функции")



# some_func(func, 2, 2)


def decorator(f):
    def wrapper(a, b):
        print("Сделай что то до функции")
        f(a, b)
        print("Сделай что то после функции")
    return wrapper


# var = decorator(func)
# var(3, 3)
# func(3, 3)

# Вывод:
# /---------\
# #помидоры#
# --ветчина--
# ~~~салат~~~
# \--------/

def meat():
    print('--ветчина--')


def ingredints(f):
    def wrapper():
        print("#помидоры#")
        f()
        print("~~~салат~~~")
    return wrapper


def bread(f):
    def wrapper():
        print("/---------\\")
        f()
        print("\--------/")
    return wrapper

# bread(ingredints(meat))()

@bread
@ingredints
def sandwich():
    print('--ветчина--')


sandwich()

# Но есть одна проблема - мы не сможем передавать аргументы в такой декоратор.
# Что бы сделать такую возможность нужно добавить такие аргументы как *args, **kwargs:
def bread_args(func):
    def wrapper(*args, **kwargs):  # args - аргументы функции по типу: f(1, 2)
        print("/---------\\")      # kwargs - именованные аргументы по типу: f(a=1, b=2)
        func(*args, **kwargs)
        print("\\--------/")
    return wrapper


def ingredients_args(func):
    def wrapper(*args, **kwargs):
        print("#помидоры#")
        func(*args, **kwargs)
        print("~~~салат~~~")
    return wrapper

@bread_args
@ingredients_args
def sandwich_args(food='--ветчина--'):
    print(food)


sandwich_args('**курица**')
# Вывод:
# /---------\
# #помидоры#
# **курица**
# ~~~салат~~~
# \--------/


# nums = [1, 2, 3, 4, 5, 6, 7]
# a, *b, c = nums
# print(a, b, c)

# nums = {"q": 1, "w": 2, "e": 3}
# **b = nums.items()
# print(a, b, c)

def wrapper(*args, **kwargs):
    print(args)
    print(kwargs)

wrapper(1, 2, True, a =4, v = "Hello")