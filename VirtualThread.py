class ThreadTranslate:
    def __init__(self):
        self.convert_file = True

    def stop(self):
        self.convert_file = False

    def get_convert(self):
        return self.convert_file
