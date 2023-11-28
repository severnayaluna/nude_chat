class Render:
    def __call__(self, *args, text):
        return text % args
