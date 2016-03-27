import baker
import irc.bot
import irc.strings
import toml

import pyborg.pyborg

class ModIRC(irc.bot.SingleServerIRCBot):
    def __init__(self, my_pyborg, channel, nickname, server, port):
        super(ModIRC, self).__init__([(server, port)], nickname, nickname)
        self.my_pyborg = my_pyborg
        self.channel = channel

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip())
        return
    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection
        c.notice(nick, "Hello {}".format(nick))



@baker.command(default=True)
def start_irc_bot(channel, nickname, server, port=6697):
    pyb = pyborg.pyborg.pyborg()
    bot = ModIRC(pyb, channel, nickname, server, port)
    try:
        bot.start()
    except KeyboardInterrupt:
        pyb.save_all()
        bot.disconnect("Default disconnect message")

if __name__ == '__main__':
    baker.run()