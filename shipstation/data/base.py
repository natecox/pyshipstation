class ShipStationBase(object):
    @classmethod
    def to_camel_case(cls, name):
        tokens = name.lower().split('_')
        first_word = tokens.pop(0)
        return first_word + ''.join(x.title() for x in tokens)

    def as_dict(self):
        d = dict()

        for key, value in self.__dict__.items():
            key = self.to_camel_case(key)
            if value is None:
                d[key] = None
            else:
                d[key] = str(value)

        return d
