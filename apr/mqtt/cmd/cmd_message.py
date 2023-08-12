import time
import uuid


class CmdMessage:
    def __init__(self, command_type="default", cmd_message_inner=None):
        self.command_id = str(uuid.uuid4())
        self.command_type = command_type
        self.timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
        self.cmd_message_inner = cmd_message_inner
        self.response = None

    def get_command_id(self):
        return self.command_id

    def get_command_type(self):
        return self.command_type

    def get_timestamp(self):
        return self.timestamp

    def get_cmd_message_inner(self):
        return self.cmd_message_inner

    def set_cmd_message_inner(self, cmd_message_inner):
        self.cmd_message_inner = cmd_message_inner

    def get_response(self):
        return self.response

    def set_response(self, response):
        self.response = response

    def __str__(self):
        return (
            f"CmdMessage{{commandId='{self.command_id}', commandType='{self.command_type}', "
            f"timestamp={self.timestamp}, mCmdMessageInner='{self.cmd_message_inner}', "
            f"response='{self.response}'}}"
        )
        
    def to_dict(self):
        return {
            "commandId": self.command_id,
            "commandType": self.command_type,
            "timestamp": self.timestamp,
            "mCmdMessageInner": self.cmd_message_inner,
            "response": self.response
        }


# 示例用法
# cmd_message = CmdMessage(command_type="doRSA", cmd_message_inner="pwd")
# print(cmd_message)
