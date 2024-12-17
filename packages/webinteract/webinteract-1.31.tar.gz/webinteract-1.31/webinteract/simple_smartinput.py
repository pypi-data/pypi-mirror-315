#
# This is a dumb re-implementation of the `smartinput` module (no
# suggestions and no smart input).  A plugin replacement used in the
# `webinteract` module to make the module work on Windows computers.
#
# Extraxted bits and pieces from:
# https://github.com/shivamsn97/smartinput/blob/master/smartinput/_smartinput.py
# (see license: https://github.com/shivamsn97/smartinput/blob/master/LICENSE)
#

from colorama import Fore, Style, Back

class History:
    
    def __init__(self, default=[]):
        pass

    def add(self, string):
        pass
    
    def find(self, what):
        return []

    def aslist(self):
        return []

def suggestion(query, history, hints):
    return ""

def sinput(
        what = "", history = None, hints = None, historyAsHint = True,
        autohistory = True, eof = None, whatcolor = None, color = None,
        hintcolor = Fore.MAGENTA):
    return (
        input(
            (whatcolor if whatcolor else "") + what + \
            (Style.RESET_ALL if whatcolor else "") + (color if color else "")))

class _exitShell(Exception):
    pass

class _interact:
    
    def __init__(self, intitle, outtitle, inputcolor, outputcolor, alertcolor):
        self.intitle = intitle
        self.outtitle = outtitle
        self.inputcolor = inputcolor
        self.outputcolor = outputcolor
        self.alertcolor = alertcolor
        self.alertmsg = None
        self.message = None

    def exit(self):
        raise _exitShell

    def getmessage():
        return str(self.message)

    def out(self, x):
        if self.alertmsg:
            print(
                '\r'+ ' '*(len(self.alertmsg)+ len(self.outtitle)) + '\r',
                end="", flush=True)
            self.alertmsg = None
        print(
            self.outtitle + (self.outputcolor if self.outputcolor else "") + \
            x + (Style.RESET_ALL if self.outputcolor else ""))

    def alert(self, x):
        print(
            '\r' +  ' '*len(self.outtitle) + \
            (self.alertcolor if self.alertcolor else "" ) + x + \
            (Style.RESET_ALL if self.alertcolor else ""), end="", flush=True)
        self.alertmsg = x

class Shell:
    
    def __init__(
            self, callback = None, exiton = "exit", intitle = "> ",
            outtitle = "< ", inputcolor = None, outputcolor = None,
            alertcolor = None):
        self.intitle=intitle
        self.outtitle=outtitle
        self.history=History()
        self.instancerunning = False
        self.call = callback
        self.inputcolor = inputcolor
        self.outputcolor = outputcolor
        self.alertcolor = alertcolor
        self.exiton = exiton

    def setexiton(self, x):
        self.exiton = x

    def setintitle(self, x):
        self.intitle = x

    def setouttitle(self,x):
        self.outtitle = x

    def setinputcolor(self,x):
        self.inputcolor = x

    def setoutputcolor(self,x):
        self.outputcolor = x

    def setalertcolor(self, x):
        self.alertcolor = x

    def setcallback(self,x):
        self.call = x

    def start(self):
        if(self.instancerunning):
            raise Exception("Instance of shell is already running.")
        if not(self.call):
            raise Exception(
                "No callback function defined. Set a callback function " + \
                "using Shell.setcallback(Function). Function should " + \
                "accept a string and a _interact object as a parameter.")
        self.instancerunning = True
        self.instance = _interact(
            self.intitle, self.outtitle, self.inputcolor, self.outputcolor,
            self.alertcolor)
        while True:
            a = sinput(
                what = self.intitle, hints = [self.exiton],
                color = self.inputcolor, history = self.history,
                eof = self.exiton)
            if a == self.exiton:
                break
            try:
                self.call(a, self.instance)
            except _exitShell:
                break
        self.instancerunning = False

