import os
import subprocess
import sys
import wx
import time
 
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Easy Pip Install')
        panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetBackgroundColour(wx.BLACK)
        self.font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.small_font = wx.Font(10, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
        self.original_size = self.GetSize()
 
        self.module_name = ""
        self.python_location = ""
        self.python_program_name = ""
        self.py_path = sys.path
        self.exe_list = []
        self.came_from = []
        self.result = ""
        self.i = 0
 
        #this section finds the location of Python on the computer to use to run pip
        #print(self.py_path)
        for path in self.py_path:
            if not path.endswith(".zip"): #THIS COULD BE EXPANDED, MIGHT BE MORE FILE EXTENSIONS TO IGNORE ON CERTAIN DEVICES
                ##print("This path "+ self.py_path[self.i] + ":")
                self.i += 1
                for files in os.listdir(path):
                    ##print(files)
                    if(files.endswith(".exe")):
                        self.exe_list.append(files)
                        self.came_from.append(path)
            '''else:
                #print("skipped a path")'''
        self.i = 0
        #to use later: C:\Program Files\Gom\2019\python>python.exe -m pip install module_name
        #will be different on every computer but the code above should adapt to the computer
        for choice in self.exe_list:
            if(choice == "python.exe" or choice == "Python.exe"):
                #print("Element "+ str(self.i) + " wanted element!")
                #print(self.exe_list[self.i])
                #print(self.came_from[self.i])
                self.python_location = self.came_from[self.i]
                self.python_program_name = self.exe_list[self.i]
                self.i += 1
            else:
                #print("Element "+ str(self.i) + " not wanted element!")
                #print(self.exe_list[self.i])
                #print(self.came_from[self.i])
                self.i += 1
        self.i = 0
        
        self.text = wx.StaticText(panel, label="Type name of module to install")
        self.text.SetForegroundColour(wx.RED)
        self.text.SetFont(self.font)
        self.sizer.Add(self.text, 0, wx.ALL, 5)

        self.text2 = wx.StaticText(panel, label="")
        self.text2.SetForegroundColour(wx.RED)
        self.text2.SetFont(self.small_font)
        self.sizer.Add(self.text2, 0, wx.ALL, 5)
        self.text2.Show(False)
 
        #text entry here
        self.text_entry = wx.TextCtrl(panel)
        self.text_entry.SetBackgroundColour(wx.RED)
        self.sizer.Add(self.text_entry, 0, wx.ALL | wx.EXPAND, 5)
 
        self.installButton = wx.Button(panel, label='Install Module')
        self.installButton.Bind(wx.EVT_BUTTON, self.install_module)
        self.sizer.Add(self.installButton, 0, wx.ALL | wx.CENTER, 5)

        self.upgradeButton = wx.Button(panel, label='Upgrade Pip')
        self.upgradeButton.Bind(wx.EVT_BUTTON, self.upgrade_pip)
        self.sizer.Add(self.upgradeButton, 0, wx.ALL | wx.CENTER, 5)
 
        self.backButton = wx.Button(panel, label='BACK')
        self.backButton.Bind(wx.EVT_BUTTON, self.back_function)
        self.sizer.Add(self.backButton, 0, wx.ALL | wx.CENTER, 5)
        self.backButton.Show(False)
 
        panel.SetSizer(self.sizer)
        self.sizer.Layout()
        self.Show()
 
    def install_module(self, event):
        self.module_name = self.text_entry.GetValue()
        self.text_entry.Show(False)
        self.installButton.Show(False)
        self.upgradeButton.Show(False)
        self.text.SetLabel("Installing Module...\nPlease Wait")
        self.sizer.Layout()
        time.sleep(0.25)
        wx.Yield()
 
        cmd = [self.python_program_name,
            "-m", 
            "pip", 
            "install",
            self.module_name,
            "--user"]
 
        check = subprocess.run(args = cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
 
        if(check.returncode == 0):
            self.text.SetLabel("Installation Successful!")
            self.text2.SetLabel(check.stderr + check.stdout)
            self.text2.Show()
            self.backButton.Show()
            self.text_entry.Show(False)
            self.installButton.Show(False)
            self.SetSize(wx.Size(800,250))
            self.sizer.Layout()
        else:
            self.text.SetLabel("Installation Failed!")
            self.text2.SetLabel(check.stderr + check.stdout)
            self.text2.Show()
            self.backButton.Show()
            self.text_entry.Show(False)
            self.installButton.Show(False)
            self.SetSize(wx.Size(800,250))
            self.sizer.Layout()
 
    def back_function(self, event):
        self.SetSize(self.original_size)
        self.text.SetLabel("Type name of module to install")
        self.installButton.Show()
        self.upgradeButton.Show()
        self.text_entry.Show()
        self.text_entry.Clear()
        self.backButton.Show(False)
        self.text2.Show(False)
        self.module_name = ""
        self.result = ""

    def upgrade_pip(self, *args):
        self.text_entry.Show(False)
        self.installButton.Show(False)
        self.upgradeButton.Show(False)
        self.text.SetLabel("Upgrading Pip...\nPlease Wait")
        self.sizer.Layout()
        time.sleep(0.25)
        wx.Yield()

        cmd = [self.python_program_name,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
            "--user"]

        check = subprocess.run(args = cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        if(check.returncode == 0):
            self.text.SetLabel("Pip Upgraded Successful!")
            self.text2.SetLabel(check.stderr + check.stdout)
            self.text2.Show()
            self.backButton.Show()
            self.text_entry.Show(False)
            self.installButton.Show(False)
            self.SetSize(wx.Size(800,250))
            self.sizer.Layout()
        else:
            self.text.SetLabel("Pip Upgrade Failed!")
            self.text2.SetLabel(check.stderr + check.stdout)
            self.text2.Show()
            self.backButton.Show()
            self.text_entry.Show(False)
            self.installButton.Show(False)
            self.SetSize(wx.Size(800,250))
            self.sizer.Layout()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()