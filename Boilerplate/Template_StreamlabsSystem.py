#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
import random
from random import randint 
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from Settings_Module import MySettings
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "All or nothing"
Website = "https://www.streamlabs.com"
Description = "!allornothing"
Creator = "Olga"
Version = "1.0.0.0"

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = MySettings()
#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():

    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    ScriptSettings = MySettings(SettingsFile)
    ScriptSettings.Response = "Overwritten pong! ^_^"
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------

def Execute(data):
    #   Check if the propper command is used, the command is not on cooldown and the user has permission to use the command
    if '!allornothing' in data.Message and not Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User) and Parent.HasPermission(data.User,ScriptSettings.Permission,ScriptSettings.Info):
        Parent.BroadcastWsEvent("EVENT_MINE","{'show':false}")
        winningCondition = random.randint(0,4) % 4 == 0
        playersPoints = Parent.GetPoints(data.UserName)

        Parent.SendStreamMessage(str(winningCondition))
        Parent.SendStreamMessage(str(playersPoints))
        if winningCondition and Parent.GetPoints(data.UserName) >= 1:
            reward = playersPoints * 2

            Parent.AddPoints(data.User,data.UserName,reward)
            Parent.SendStreamMessage('Well done, you get EVERYTHING')

        elif Parent.GetPoints(data.UserName) < 1 :
            Parent.SendStreamMessage('Sorry, you need at least 500 points to play')

        elif winningCondition == False :
            Parent.RemovePoints(data.User,data.UserName,playersPoints)
            Parent.SendStreamMessage('Sorry you lose EVERYTHING')        
    return

   
#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    
    if "$myparameter" in parseString:
        return parseString.replace("$myparameter","I am a cat!")
    
    return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return
