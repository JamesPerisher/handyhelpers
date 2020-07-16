import json


class Config(dict):
    def __init__(self, file, raw_data="", autoadd=True, create_file=True, readonly=False):
        self.file = file
        self.raw_data = raw_data
        self.autoadd = autoadd
        self.create_file = create_file
        self.readonly = readonly

        self = super().__init__() if self.raw_data.strip() == "" else super().__init__(json.loads(self.raw_data))

    @staticmethod
    def from_file(file, autoadd=True, create_file=True, readonly=False):
        raw_data = ""
        try:
            with open(file, "r") as f:
                raw_data = f.read()
        except FileNotFoundError as e:
            if create_file:
                open(file, "w").close()
            else:
                raise e

        return Config(file, raw_data, autoadd, create_file, readonly)

    @staticmethod
    def from_memory(autoadd=True, create_file=True, readonly=False):
        return Config(vertualfile.VertualFile(doclose=False), "", autoadd, create_file, readonly)


    def __repr__(self):
        self.save()
        return "%s.config(%s, '%s', %s, %s, %s)" %(__name__, "'%s'"%self.file if not isinstance(self.file, vertualfile.VertualFile) else self.file, self.raw_data, self.autoadd, self.create_file, self.readonly)

    def __getitem__(self, key, *args, **kwargs):
        return self.get(key)

    def __setitem__(self, *args, **kwargs):
        super().__setitem__(*args, **kwargs)
        self.save()

    def __delitem__(self, *args, **kwargs):
        super().__delitem__(*args, **kwargs)
        self.save()

    def update(self, key,*args, **kwargs):
        self.get(key)
        super().update(key,*args, **kwargs)
        self.save()

    def get(self, key, default=None):
        data = super().get(key, None)
        if data == None:
            if self.autoadd:
                self[key] = default
                self.save()
            return default
        return data


    def save(self):
        if self.readonly : return
        self.raw_data = json.dumps(self)
        with vertualfile.open(self.file, "w") as f:
            f.write(self.raw_data)

    def close(self):
        self.file.close()
