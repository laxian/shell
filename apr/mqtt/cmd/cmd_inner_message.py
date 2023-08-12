class CmdMessageInner:
    def __init__(self, command=None, download_key=None):
        self.un_signed_string = None
        self.signed_string = None
        self.command = command
        self.download_key = download_key

    def get_signed_string(self):
        return self.signed_string

    def set_signed_string(self, signed_string):
        self.signed_string = signed_string

    def get_un_signed_string(self):
        return self.un_signed_string

    def set_un_signed_string(self, un_signed_string):
        self.un_signed_string = un_signed_string

    def get_command(self):
        return self.command

    def set_command(self, command):
        self.command = command

    def get_download_key(self):
        return self.download_key

    def set_download_key(self, download_key):
        self.download_key = download_key

    def __str__(self):
        return (
            f"CmdMessageInner{{unSignedString='{self.un_signed_string}', signedString='{self.signed_string}', "
            f"command='{self.command}', downloadKey='{self.download_key}'}}"
        )

    def to_dict(self):
        return {
            "unSignedString": self.un_signed_string,
            "signedString": self.signed_string,
            "command": self.command,
            "downloadKey": self.download_key,
        }
