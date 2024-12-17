
def hello_world():
    print("Hello World!")

def hello1() -> str:
    return "hello world"

class MyClass:
    def __init__(self, name: str):
        self.name = name
    def __repr__(self):
        repr(self.name)