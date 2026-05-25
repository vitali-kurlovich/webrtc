class TemplateBuilder:
    def __init__(self, templatePath: str):
        self.templatePath = templatePath
        self.mappings = {}

    def append(self, key: str, value: str):
        self.mappings[key] = value
        return self

    def build(self) -> str:
        with open(self.templatePath, "r") as f:
            result = f.read()

        for key, value in self.mappings.items():
            result = result.replace(f"%{{{key}}}%", value)
        return result

    def write(self, outputPath: str):
        with open(outputPath, "w") as f:
            f.write(self.build())
