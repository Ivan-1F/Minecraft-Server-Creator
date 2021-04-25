class Properties:
    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}

        with open(self.file_name, 'r') as f:
            for line in f:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    parsed = line.split('=')
                    self.properties[parsed[0].strip()] = parsed[1].strip()
            f.close()

    def has_key(self, key):
        return key in self.properties

    def get(self, key, default_value=''):
        if key in self.properties:
            return self.properties[key]
        return default_value

    def put(self, key, value):
        self.properties[key] = value

    def save(self):
        with open(self.file_name, 'w') as f:
            content = ''
            for p in self.properties.items():
                content += f'{p[0]}={p[1]}\n'
            f.write(content)
            f.close()