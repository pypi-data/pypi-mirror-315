from remotemanager.connection.url import URL
from remotemanager.script.script import Script


class Computer(Script, URL):
    """
    Combo class that allows for connection to a machine and generating jobscripts
    """

    def __init__(self, template, **kwargs):
        # super() behaves strangely with multiple inheritance
        # explicitly call the __init__ with self
        Script.__init__(self, template=template, **kwargs)
        URL.__init__(self, **kwargs)

    def pack(self, *args, **kwargs) -> dict:
        url_data = URL.pack(self, *args, **kwargs)
        template = Script.pack(self)

        url_data["template"] = template
        url_data["_empty_treatment"] = self._empty_treatment
        url_data["_init_args"] = self._init_args
        url_data["_temporary_args"] = {}

        return url_data

    @classmethod
    def unpack(cls, data: dict):
        return super(Script, cls).unpack(data=data)
