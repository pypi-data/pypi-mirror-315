import sys

def helloworld(message=None):
    if message is None and len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    elif message is None:
        message = "Hello, World!"

    print(message)

if __name__ == "__main__":
    helloworld()
