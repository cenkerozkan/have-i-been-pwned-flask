def singleton(class_):
    instances: dict = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


if __name__ == "__main__":
    # To see if it works.
    @singleton
    class MyClass:
        pass

    obj1 = MyClass()
    obj2 = MyClass()
    print(obj1 is obj2)
