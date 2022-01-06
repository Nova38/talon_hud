from talon import app, actions, Module
import os

mod = Module()

class HeadUpDocumentation:
    order = None
    files = None
    descriptions = None
    
    def __init__(self):
        self.files = {}
        self.descriptions = {}
        self.order = []
    
    def add_file(self, title: str, description: str, filename: str):
        if os.path.isfile(filename):
            self.files[title] = filename
            if description:
                self.descriptions[title] = description
                
            if title not in self.order:
                self.order.append(title)
        else:
            app.notify(filename + " could not be found")

    def load_documentation(self, title: str):
        if title in self.files:
            text_file = open(self.files[title], "r")
            documentation = text_file.read()
            text_file.close()
            actions.user.hud_publish_content(documentation, "documentation", title)

    def show_overview(self):
        documentation = "Say any of the bolded titles below to open the documentation\n\n"
        for index, order in enumerate(self.order):
            documentation += "<* " + str(index + 1) + " - " + order + "/>"
            if order in self.descriptions:
                documentation += ": " + self.descriptions[order]
            documentation += "\n"

        voice_commands = {}
        for title in self.order:
            voice_commands[title] = lambda self=self, title=title: self.load_documentation(title)
        actions.user.hud_publish_content(documentation, "documentation", "Documentation panel", True, [], voice_commands)

hud_documentation = HeadUpDocumentation()

@mod.action_class
class Actions:

    def hud_add_documentation(title: str, description: str, filename: str):
        """Add a file to the documentation panel of the Talon HUD"""
        global hud_documentation
        hud_documentation.add_file(title, description, filename)
        
    def hud_show_documentation(title: str = ""):
        """Show the general documentation"""
        global hud_documentation
        if title == "":
            hud_documentation.show_overview()
        else:
            hud_documentation.load_documentation(title)
        