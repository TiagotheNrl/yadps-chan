from handler.config.data import Data
from handler.logging.log import Log
import os


class CommandController:
    data = Data()
    command_log = Log().create(__name__, data.config["commandLog"])
    total_loaded = 0

    def __init__(self, bot):
        self.bot = bot
        self.command_log.info("Initing commands")

    def load(self):
        if self.data.config["enableDevCommands"]:
            self.set_command_state(self.data.config["devCog"], 'load')
        if self.data.config["enableAdminCommands"]:
            self.set_command_state(self.data.config["adminCog"], 'load')
        if self.data.config["enableModCommands"]:
            self.set_command_state(self.data.config["modCog"], 'load')
        if self.data.config["enableUserCommands"]:
            self.set_command_state(self.data.config["userCog"], 'load')
        self.command_log.info(f"Total commands loaded: {self.total_loaded}")

    def set_command_state(self, module, state, command=None):
        path_string = self.data.config["cogPath"] + '.' + module
        if command and isinstance(command, str):
            arg = {path_string + '.' + command}
            getattr(self.bot, "%s_extension" % state)(*arg)
        else:
            for cmd in os.listdir(self.data.config["cogPath"].replace('.', '/') + '/' + module):
                if cmd.endswith('.py'):
                    arg = {path_string + '.' + cmd[:-3]}
                    getattr(self.bot, "%s_extension" % state)(*arg)
                    self.total_loaded += 1

    def get_command_ranks(self) -> list:
        path = self.data.config["cogPath"].replace(".", "/")
        ranks = []
        for dir in os.listdir(path):
            ranks.append(dir)
        return ranks

    def get_command_list(self, rank=None) -> list:
        path = self.data.config["cogPath"].replace(".", "/")
        commands = []
        if rank:
            for file in os.listdir(path + "/" + rank):
                if file.endswith(".py"):
                    commands.append(file.replace(".py", ""))
            return commands
        if rank is None:
            for dir in os.listdir(path):
                for file in os.listdir(path + "/" + dir):
                    if file.endswith(".py"):
                        commands.append(file.replace(".py", ""))
            return commands
