'''
@package irccbot20191208001
irccbot20191208001_gui
'''

from tkinter import *
from irccbot20191208001 import *

class APP_irccbot20191208001_gui(Tk):
    def start(self):

        self.title('Lancer le bot')
        couleur_fond = 'green'
        couleur_texte = 'red'
        couleur_fond_saisie = 'purple'
        couleur_texte_saisie = 'yellow'
        couleur_activebackground = couleur_texte_saisie
        couleur_activeforeground = couleur_fond_saisie
        
        self.panel_001 = Label(self, bg = couleur_fond)
        self.label_001 = Label(self.panel_001, text = 'Serveur ',
                               fg = couleur_texte,
                               bg = couleur_fond)
        self.entry_serveur = Entry(self.panel_001, bg = couleur_fond_saisie,
                               fg = couleur_texte_saisie,
                               relief = 'flat')
        self.label_002 = Label(self.panel_001, text = 'Canal ',
                               fg = couleur_texte,
                               bg = couleur_fond)
        self.entry_canal = Entry(self.panel_001, bg = couleur_fond_saisie,
                               fg = couleur_texte_saisie,
                               relief = 'flat')
        self.label_003 = Label(self.panel_001, text = 'Pseudonyme ',
                               fg = couleur_texte,
                               bg = couleur_fond)
        self.entry_pseudonyme = Entry(self.panel_001, bg = couleur_fond_saisie,
                               fg = couleur_texte_saisie,
                               relief = 'flat')
        self.button_001 = Button(self.panel_001, bg = couleur_fond_saisie,
                                 fg = couleur_texte_saisie,
                                 text = 'Connecter',
                                 command = lambda: self.do_connect(self.entry_serveur.get(),
                                                                   self.entry_canal.get(),
                                                                   self.entry_pseudonyme.get()),
                                 activebackground = couleur_activebackground,
                                 activeforeground = couleur_activeforeground)
        
        self.panel_001.pack(fill = BOTH, expand = True)
        Grid.rowconfigure(self.panel_001, 0, weight=1)
        Grid.columnconfigure(self.panel_001, 0, weight=1)
        Grid.rowconfigure(self.panel_001, 1, weight=1)
        Grid.columnconfigure(self.panel_001, 1, weight=1)
        Grid.rowconfigure(self.panel_001, 2, weight=1)
        Grid.rowconfigure(self.panel_001, 3, weight=1)
        
        self.label_001.grid(column = 0, row = 0)
        self.entry_serveur.grid(column = 1, row = 0, sticky=W+E)
        self.label_002.grid(column = 0, row = 1)
        self.entry_canal.grid(column = 1, row = 1, sticky=W+E)
        self.label_003.grid(column = 0, row = 2)
        self.entry_pseudonyme.grid(column = 1, row = 2, sticky=W+E)
        self.button_001.grid(column = 0, row = 3, sticky=W+E+N+S, columnspan = 2)

        self.mainloop()
        
    def do_connect(self, server, channel, nickname):
        self.wm_state('icon')
        self.bot = IRCBot(channel, nickname, server, 6667)
        self.bot.start()

def main():
    client = APP_irccbot20191208001_gui()
    client.start()

if __name__ == "__main__":
    main()
