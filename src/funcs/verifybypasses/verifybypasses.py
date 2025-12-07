from src import *
from src.utils.console import Console
from src.utils.logging import Logger

class verifybypasses:
    def __init__(self):
        self.console = Console('Verify Bypasses')
    
    def reaction(self):
        Logger.paidonly()

    def button(self):
        Logger.paidonly()

    def rule(self):
        Logger.paidonly()

    def onboarding(self):
        Logger.paidonly()

    def restorecord(self):
        Logger.paidonly()

    def authgg(self):
        Logger.paidonly()

    def menu(self):
        menu = {
            'Reaction Bypass $': self.reaction,
            'Button Bypass $': self.button,
            'Rule Btpass $': self.rule,
            'Onboarding Bypass $': self.onboarding,
            'Restorecord Bypass $': self.restorecord,
            'Authgg Bypass $': self.authgg,
        }

        self.console.createmenu(menu)
        choice = self.console.input('Choice', int)

        if choice == 1:
            self.reaction()

        elif choice == 2:
            self.button()

        elif choice == 3:
            self.rule()

        elif choice == 4:
            self.onboarding()

        elif choice == 5:
            self.restorecord()
        
        elif choice == 6:
            self.authgg()