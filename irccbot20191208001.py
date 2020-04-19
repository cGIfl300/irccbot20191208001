''''
@package irccbot20191208001
irccbot20191208001
'''
import irc.bot
import requests
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

secure_nick = "cGIfl300" # The one who can kill the bot

class IRCBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(
            self.connection.get_nickname()
        ):
            self.do_command(e, a[1].strip())
        return

    def on_dccmsg(self, c, e):
        # non-chat DCC messages are raw bytes; decode as text
        text = e.arguments[0].decode('utf-8')
        c.privmsg("You said: " + text)

    def on_dccchat(self, c, e):
        if len(e.arguments) != 2:
            return
        args = e.arguments[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)

    def do_verset(self, versets, version, supprime):
        versets = versets.replace(supprime,"")
        versets = versets.replace(" ","")
        url = "https://www.biblegateway.com/passage/?search="+versets+"&version="+version+"&interface=print"
        try:
            pagecontent = requests.get(url)
            pagecontent.liste = pagecontent.text.split("\n")
            for ligne in pagecontent.liste :
                if ligne.find("<meta property=\"og:description\" content=\"") == 0:
                    ligne = ligne.replace("<meta property=\"og:description\" content=\"","")
                    ligne = ligne.replace("\"/>","")
                    ligne = ligne.replace("&amp;#39;","\'")
                    return ligne
        except:
            return "Verse not found."
    
    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection

        if cmd == "disconnect":
            if nick == secure_nick:
                self.disconnect()
        elif cmd == "die":
            if nick == secure_nick:
                self.die()
        elif cmd == "stats":
            for chname, chobj in self.channels.items():
                c.notice(nick, "--- Channel statistics ---")
                c.notice(nick, "Channel: " + chname)
                users = sorted(chobj.users())
                c.notice(nick, "Users: " + ", ".join(users))
                opers = sorted(chobj.opers())
                c.notice(nick, "Opers: " + ", ".join(opers))
                voiced = sorted(chobj.voiced())
                c.notice(nick, "Voiced: " + ", ".join(voiced))
        elif cmd == "join":
            c.join(self.channel)
        elif cmd.find(".bible ") == 0:
            verset = self.do_verset(cmd, "NIV", ".bible ")
            try:
                c.notice(nick, verset)
            except:
                c.notice(nick, "Verse not found.")
        elif cmd.find(".biblefr ") == 0:
            verset = self.do_verset(cmd, "SG21", ".biblefr ")
            try:
                c.notice(nick, verset)
            except:
                c.notice(nick, "Verse not found.")
        elif cmd.find(".biblede ") == 0:
            verset = self.do_verset(cmd, "SCH1951", ".biblede ")
            try:
                c.notice(nick, verset)
            except:
                c.notice(nick, "Verse not found.")
        else:
            c.notice(nick, "Not understood: " + cmd)

def main():
    import sys

    if len(sys.argv) != 4:
        print("Usage: testbot <server[:port]> <channel> <nickname>")
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print("Error: Erroneous port.")
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    nickname = sys.argv[3]

    bot = IRCBot(channel, nickname, server, port)
    bot.start()


if __name__ == "__main__":
    main()
