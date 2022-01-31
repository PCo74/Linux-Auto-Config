"""
get keys/values from init file (*.ini)
"""


class InitFile:

    def __init__(self, filepath, sep='=', comment_char='#'):
        """
        :param filepath:
        :param sep:
        :param comment_char:

        >>> ini.IDFIC
        '=--='
        """
        self.filepath = filepath
        self.props = self.get_key_value_pairs(sep, comment_char)
        for key, value in self.props.items():
            setattr(self, key, value)

    def get_key_value_pairs(self, sep='=', comment_char='#'):
        """
        Read the file passed as parameter as a properties file.
        REF : https://stackoverflow.com/questions/3595363/properties-file-in-python-similar-to-java-properties
        """
        props = {}
        with open(self.filepath, "rt") as f:
            for line in f:
                l = line.strip()
                if l and not l.startswith(comment_char):
                    key_value = l.split(sep)
                    key = key_value[0].strip()
                    value = sep.join(key_value[1:]).strip().strip('"')
                    props[key] = value
        return props


if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'ini': InitFile("../../config.ini")})
