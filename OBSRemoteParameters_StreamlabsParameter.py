#!/usr/bin/python
# -*- coding: utf-8 -*-

""" OBS REMOTE PARAMETERS

Parameter library to control OBS within current existing commands!

Version

	1.3.0
		$OBStimedSource now has an onoff or offon mode and $OBSscene now can accept an optional delay.
		All parameters now use threading in Python to execute actions.
	1.2.0
		Added $OBStimedScene swap to a given scene for a set period of time, then swap to another given scene.
		Changed script name to _StreamlabsSystem to accomedate the change in the bot name.
	1.1.0
		Added $OBStimedSource enabled a given source for a set period of time
	1.0.0
		Initial release containing $OBSsource, $OBSscene and $OBSstop

"""

#---------------------------------------
# Import Libraries
#---------------------------------------
import clr
clr.AddReference("IronPython.Modules.dll")

import os
import json
import re
import time
import threading

#---------------------------------------
# Script Information
#---------------------------------------
ScriptName = "OBS Studio Remote Parameters"
Website = "http://www.twitch.tv/ocgineer"
Description = "Parameter Library to control OBS Studio with the regular command system."
Creator = "Ocgineer"
Version = "1.3.0"

#---------------------------------------
# Global Vars
#---------------------------------------
ReadMeFile = os.path.join(os.path.dirname(__file__), "ReadMe.txt")
RegObsScene = None
RegObsSource = None
RegObsTmdSrc = None
RegObsTmdScn = None

#---------------------------------------
# Functions
#---------------------------------------
def OpenReadMe():
	""" Open the script readme file in users default .txt application. """
	os.startfile(ReadMeFile)
	return

def CallbackLogger(response):
	""" Logs callback error response in scripts logger. """
	parsedresponse = json.loads(response)
	if parsedresponse["status"] == "error":
		Parent.Log("OBS Remote", parsedresponse["error"])
	return

def ChangeToScene(scene, delay=None):
	""" Swaps to a given scene, optionally after given amount of seconds. """
	if delay:
		time.sleep(delay)
	Parent.SetOBSCurrentScene(scene, CallbackLogger)
	return

def SetSourceVisibility(source, enabled, scene=None):
	""" Set the targeted source visibility optionally in a scene. """
	Parent.SetOBSSourceRender(source, enabled, scene, CallbackLogger)
	return

def ChangeScenesTimed(scene_one, scene_two, delay):
	""" Swap to one scene then to another scene after a set delay. """
	Parent.SetOBSCurrentScene(scene_one, CallbackLogger)
	if delay:
		time.sleep(delay)
	Parent.SetOBSCurrentScene(scene_two, CallbackLogger)
	return

def VisibilitySourceTimed(source, mode, delay, scene):
	""" Disables a given source in optional scene after given amount of seconds. """
	# off - delay - off
	if mode == "offon":
		Parent.SetOBSSourceRender(source, False, scene, CallbackLogger)
		if delay:
			time.sleep(delay)
		Parent.SetOBSSourceRender(source, True, scene, CallbackLogger)
	# on - delay - off
	else:
		Parent.SetOBSSourceRender(source, True, scene, CallbackLogger)
		if delay:
			time.sleep(delay)
		Parent.SetOBSSourceRender(source, False, scene, CallbackLogger)
	# done
	return

#---------------------------------------
# Initialize data on load
#---------------------------------------
def Init():
	""" Initialize Script. """

	# Globals
	global RegObsScene
	global RegObsSource
	global RegObsTmdSrc
	global RegObsTmdScn

	# Compile regexes in init
	RegObsScene = re.compile(r"(?:\$OBSscene\([\ ]*[\"\'](?P<scene>[^\"\']+)[\"\'][\ ]*(?:\,[\ ]*[\"\'](?P<delay>\d*)[\"\'][\ ]*)?\))", re.U)
	RegObsSource = re.compile(r"(?P<full>\$OBSsource\([\ ]*[\"\'](?P<source>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<enabled>[^\"\']*)[\"\'][\ ]*(?:\,[\ ]*[\"\'](?P<scene>[^\"\']*)[\"\'][\ ]*)?\))", re.U)
	RegObsTmdScn = re.compile(r"(?P<full>\$OBStimedScene\([\ ]*[\"\'](?P<s1>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<s2>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<delay>\d+)[\"\'][\ ]*\))", re.U)
	RegObsTmdSrc = re.compile(r"(?P<full>\$OBStimedSource\([\ ]*[\"\'](?P<source>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<mode>onoff|offon)[\"\'][\ ]*\,[\ ]*[\"\'](?P<delay>\d+)[\"\'][\ ]*(?:\,[\ ]*[\"\'](?P<scene>[^\"\']*)[\"\'][\ ]*)?\))", re.U)

	# End of Init
	return

#---------------------------------------
# Parse parameters
#---------------------------------------
def Parse(parseString, user, target, message):
	""" Custom Parameter Parser. """

	# $OBSscene("scene") parameter
	# $OBSscene("scene", "delay") parameter
	if "$OBSscene" in parseString:

		# Apply regex to verify correct parameter use
		result = RegObsScene.search(parseString)
		if result:		

			# Get results from regex match
			fullParameterMatch = result.group(0)
			scene = result.group("scene")
			delay = int(result.group("delay")) if result.group("delay") else None

			# Change to another scene, using threading
			threading.Thread(target=ChangeToScene, args=(scene, delay)).start()

			# Replace the whole parameter with an empty string
			return parseString.replace(fullParameterMatch, "")

	# $OBSsource("source", "enabled")
	# $OBSsource("source", "enabled", "scene")
	if "$OBSsource" in parseString:

		# Apply regex to verify correct parameter use
		result = RegObsSource.search(parseString)
		if result:

			# Get match groups from regex
			fullParameterMatch = result.group(0)
			source = result.group("source")
			enabled = False if result.group("enabled").lower() == "false" else True
			scene = result.group("scene") if result.group("scene") else None

			# Set source visibility, using threading
			threading.Thread(target=SetSourceVisibility, args=(source, enabled, scene)).start()		

			# Replace the whole parameter with an empty string
			return parseString.replace(fullParameterMatch, "")

	# #OBStimedScene("scene_one", "scene_two", "delay")
	if "$OBStimedScene" in parseString:

		# Apply regext to verify correct parameter use
		result = RegObsTmdScn.search(parseString)
		if result:

			# Get match groups from regex
			fullParameterMatch = result.group(0)
			scene1 = result.group("s1")
			scene2 = result.group("s2")
			delay = int(result.group("delay")) if result.group("delay") else None

			# Change to scene one, then to two after set delay, using threading
			threading.Thread(target=ChangeScenesTimed, args=(scene1, scene2, delay)).start()

			# Replace the whole parameter with an empty string
			return parseString.replace(fullParameterMatch, "")

	# $OBStimedSource("source", "mode", "delay")
	# $OBStimedSource("source", "mode", "delay", "scene")
	if "$OBStimedSource" in parseString:

		# Apply regex to verify correct parameter use
		result = RegObsTmdSrc.search(parseString)
		if result:

			# Get match groups from regex
			fullParameterMatch = result.group(0)
			source = result.group("source")
			mode = result.group("mode")
			delay = int(result.group("delay")) if result.group("delay") else None
			scene = result.group("scene") if result.group("scene") else None

			# Start a new thread to disable the source again after amount of given seconds
			threading.Thread(target=VisibilitySourceTimed, args=(source, mode, delay, scene)).start()

			# Replace the whole parameter with an empty string
			return parseString.replace(fullParameterMatch, "")

	# $OBSstop parameter
	if "$OBSstop" in parseString:

		# Call Stop streaming
		Parent.StopOBSStreaming(CallbackLogger)

		# Replace the whole parameter with an empty string
		return parseString.replace("$OBSstop", "")

	# Return unaltered parseString
	return parseString
