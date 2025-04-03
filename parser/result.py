from string import Template


class Result:
    MD_TEMPLATE = Template("""
- [ ] Href: **$url**
    - Name: _${name}_
    - Parent URL: $parent
    - Result: `$result`
"""
    )
    TXT_TEMPLATE = Template("""
URL: $url
Name: $name
Parent URL: $parent
Result: $result
"""
    )

    def __init__(self, url, name, parent, result):
        self.url = url
        self.name = name
        self.parent = parent
        self.result = result

    def __iter__(self):
        for attr in ("url", "name", "parent", "result"):
            yield getattr(self, attr)

    def __substitutions(self, template):
        return template.substitute(
            url=self.url,
            name=self.name,
            parent=self.parent,
            result=self.result
        )

    @property
    def txt(self):
        return self.__substitutions(self.TXT_TEMPLATE)

    @property
    def markdown(self):
        return self.__substitutions(self.MD_TEMPLATE)
