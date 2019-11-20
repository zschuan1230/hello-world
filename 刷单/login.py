#coding=utf-8


def out1(func):
    def inner():
        print("装饰器")
        return func()
    return inner

def out2(level):
    def out(func):
        def inner():
            print("装饰器:{}".format(level))
            return func()
        return inner
    return out



@out2(2)
def a():
    print("方法a")

@out1
def b():
    print("方法b")


if __name__ == "__main__":
    a()
    b()