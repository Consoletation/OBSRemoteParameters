#!/usr/bin/python
# -*- coding: utf-8 -*-

""" OBS REMOTE PARAMETERS

Parameter library to control OBS within current existing commands!

Version

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
ScriptName = "OBS Remote Parameters"
Website = "http://www.twitch.tv/ocgineer"
Description = "Parameter Library to control OBS Studio with the regular command system."
Creator = "Ocgineer"
Version = "1.2.0.0"

#---------------------------------------
# Global Vars
#---------------------------------------
RegObsScene = None
RegObsSource = None
RegObsTmdSrc = None
RegObsTmdScn = None

#---------------------------------------
# Functions
#---------------------------------------
def CallbackLogger(response):
	""" Logs callback error response in scripts logger. """
	parsedresponse = json.loads(response)
	if parsedresponse["status"] == "error":
		Parent.Log("OBS Remote", parsedresponse["error"])
	return

def DisableSourceTimer(source, seconds, scene):
	""" Disables a given source in optional scene after given amount of seconds. """
	counter = 0
	while counter < seconds:
		time.sleep(1)
		counter += 1
	Parent.SetOBSSourceRender(source, False, scene, CallbackLogger)
	return

def SwapSceneTimer(scene, seconds):
	""" Swaps to a given secene after given amount of seconds. """
	counter = 0
	while counter < seconds:
		time.sleep(1)
		counter += 1
	Parent.SetOBSCurrentScene(scene, CallbackLogger)
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
	RegObsScene = re.compile(r"(?:\$OBSscene\([\ ]*[\"\'](?P<scene>[^\"\']+)[\"\'][\ ]*\))", re.U)
	RegObsSource = re.compile(r"(?P<full>\$OBSsource\([\ ]*[\"\'](?P<source>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<enabled>[^\"\']*)[\"\'][\ ]*(?:\,[\ ]*[\"\'](?P<scene>[^\"\']*)[\"\'][\ ]*)?\))", re.U)
	RegObsTmdSrc = re.compile(r"(?P<full>\$OBStimedSource\([\ ]*[\"\'](?P<source>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<seconds>\d+)[\"\'][\ ]*(?:\,[\ ]*[\"\'](?P<scene>[^\"\']*)[\"\'][\ ]*)?\))", re.U)
	RegObsTmdScn = re.compile(r"(?P<full>\$OBStimedScene\([\ ]*[\"\'](?P<s1>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<s2>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<seconds>\d+)[\"\'][\ ]*\))", re.U)

	# End of Init
	return

#---------------------------------------
# Parse parameters
#---------------------------------------
def Parse(parseString, user, target, message):
	""" Custom Parameter Parser. """

	# $OBSscene("scene") parameter
	if "$OBSscene" in parseString:

		# Apply regex to verify correct parameter use
		result = RegObsScene.search(parseString)
		if result:		

			# Get results from regex match
			fullParameterMatch = result.group(0)
			scene = result.group("scene")

			# Call OBS Current Scene
			Parent.SetOBSCurrentScene(scene, CallbackLogger)

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
			enabled = result.group("enabled")
			scene = result.group("scene")

			# Set enabled, scene target, and call OBS Source Renderer
			setEnabled = True if enabled.lower() == "true" else False
			sceneTarget = scene if scene else None
			Parent.SetOBSSourceRender(source, setEnabled, sceneTarget, CallbackLogger)

			# Replace the whole parameter with an empty string
			return parseString.replace(fullParameterMatch, "")

	# $OBStimedSource("source", "seconds")
	# $OBStimedSource("source", "seconds", "scene")
	if "$OBStimedSource" in parseString:

		# Apply regex to verify correct parameter use
		result = RegObsTmdSrc.search(parseString)
		if result:

			# Get match groups from regex
			fullParameterMatch = result.group(0)
			source = result.group("source")
			seconds = int(result.group("seconds"))
			scene = result.group("scene")

			# Set scene target and call OBS Source Renderer
			sceneTarget = scene if scene else None
			Parent.SetOBSSourceRender(source, True, sceneTarget, CallbackLogger)

			# A valid time given?
			if seconds > 0:

				# Start a new thread to disable the source again after amount of given seconds
				threading.Thread(target=DisableSourceTimer, args=(source, seconds, sceneTarget)).start()

			# Replace the whole parameter with an empty string
			return parseString.replace(fullParameterMatch, "")

	# #OBStimedScene("scene1", "scene2", "seconds")
	if "$OBStimedScene" in parseString:

		# Apply regext to verify correct parameter use
		result = RegObsTmdScn.search(parseString)
		if result:

			# Get match groups from regex
			fullParameterMatch = result.group(0)
			scene1 = result.group("s1")
			scene2 = result.group("s2")
			seconds = int(result.group("seconds"))

			# call OBS Current Scene to swap to scene1
			Parent.SetOBSCurrentScene(scene1, CallbackLogger)

			# A vailid time given?
			if seconds > 0:

				# Start a new thread to swap to scene2 after amount of given seconds
				threading.Thread(target=SwapSceneTimer, args=(scene2, seconds)).start()

			return parseString.replace(fullParameterMatch, "")

	# $OBSstop parameter
	if "$OBSstop" in parseString:

		# Call Stop streaming
		Parent.StopOBSStreaming(CallbackLogger)

		# Replace the whole parameter with an empty string
		return parseString.replace("$OBSstop", "")

	# Return unaltered parseString
	return parseString
