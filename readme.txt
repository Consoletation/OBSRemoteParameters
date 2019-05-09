OBS STUDIO REMOTE CONTROL PARAMETER SCRIPT FOR STREAMLABS CHATBOT
###############################################################################

To use the OBS Remote Parameters you first need to have OBS Websocket plugin installed to use in OBS.

Download and install the latest version of the plugin here from GitHub;
> https://github.com/Palakis/obs-websocket/releases

After installing start OBS Studio, then a new option is available under 'Tools' in the menu bar.
Open 'Websocket Server Settings' and check the Enable box and hit OK. Optionally you can set a password.

Then go to Streamlabs Chatbot Connections (the avatar icon) > OBS Remote > Setup the same port and
password (if any is set in the OBS plugin) and hit connect.

# Few pointers;

Streamlabs Chatbot will attemt to auto-connect to the OBS websocket on startup if OBS Studio
is started and running before you start the bot. If you start OBS Studio after starting the
bot you have to manually connect again.

If the used parameter (see available parameters in ParameterHelp directory) is spit back out in
the chat, that means the scripts parameter parser is not hooked/loaded in correctly. One can
resolive this, by making sure it is enabled, then reload scripts and/or restart the bot. Or you
have used the parameter incorrectly, make sure you check carefully over the use of the parameter!


CHANGE TO SCENE WITH OPTIONAL DELAY
===============================================================================

$OBSscene("<scene>")
$OBSscene("<scene>", "<delay>")

  # Swap to a scene instantly or after a delay.
  
  <scene>

    The scene name to swap to.
    This is a required argument and cannot be empty. The name has to match the
    scene name in SLOBS and is therefore case sensitive. All characters can be
    used except names containing single (') or double (") quotes for this
    parameter.

  <delay>

    The delay in seconds before changing to the targeted scene.
    This is an optional argument but if given it needs to contain a valid
    number in seconds.


SET VISIBILITY OF SOURCE IN ACTIVE OR TARGET SCENE
===============================================================================

$OBSsource("<source>", "<visible>")
$OBSsource("<source>", "<visible>", "<scene>")

  # Set the visibilty of a source in the current active or target scene.
  
  <source>

    Name of the targeted source to set the visibility of.
    This is a required argument and cannot be empty. The name has to match the
    source name in OBS and is therefore case sensitive. All characters can be
    used except names containing single (') or double (") quotes for this
    parameter.

  <visible>

    Sets the visibility state of the targeted source [true|false].
    This is a required argument and the targeted source will be set to *not*
    visible if this argument is set to `false`. Anything else, or `true` will
    set the targeted source to visible.

  <scene>

    Name of the targeted scene to set the targeted source visibility in.
    This is an optional argument but if given it needs to match the scene name
    in SLOBS and is case sensitive. All characters can be used execept names
    containing containing single (') or double (") quotes for this parameter.

CHANGE TO SCENE THEN TO ANOTHER SCENE AFTER A SET DELAY
===============================================================================

$OBStimedScene("<scene_one>", "<scene_two>", "<delay>")

  # Swap from one scene and back or another scene after a set time.
  
  <scene_one>

    The scene name to change to.
    This is a required argument and cannot be empty. The name has to match the
    scene name in SLOBS and is therefore case sensitive. All characters can be
    used except names containing single (') or double (") quotes for this
    parameter.

  <scene_two>

    The scene name to swap to after the delay elapsed.
    This is a required argument and cannot be empty. The name has to match the
    scene name in SLOBS and is therefore case sensitive. All characters can be
    used except names containing single (') or double (") quotes for this
    parameter.

  <delay>

    Time in seconds how long the targeted scene needs to be visible.
    This is a required argument and cannot be empty and needs to be a valid
    number to be used.


SET VISIBILITY OF SOURCE IN ACTIVE OR TARGET SCENE TIMED ONOFF OR OFFON
===============================================================================

$OBStimedSource("<source>", "<mode>", "<delay>")
$OBStimedSource("<source>", "<mode>", "<delay>", "<scene>")

  # Set the visibilty of a source in the current active or target scene for a
  # set amount of time (delay) and then turns it to another state (mode).

  <source>

    Name of the targeted source to set the visibility of.
    This is a required argument and cannot be empty. The name has to match the
    source name in OBS and is therefore case sensitive. All characters can be
    used except names containing single (') or double (") quotes for this
    parameter.

  <mode>

    Sets mode to use visible/hidden or hidden/visible. [onoff|offon]
    This is a required argument and the targeted source will turn on and then
    off after a delay (mode: onoff) or will turn off and then on again after a
    delay (mode: offon).

  <delay>

    Set the delay in seconds before hiding or showing the targeted source.
    This is a required argument and cannot be empty and needs to be a valid
    number to be used.

  <scene>

    Name of the targeted scene to set the targeted source visibility in.
    This is an optional argument but if given it needs to match the scene name
    in SLOBS and is case sensitive. All characters can be used execept names
    containing containing single (') or double (") quotes for this parameter.


STOP STREAMING
===============================================================================

$OBSstop

  No arugments required. Can be used for example for a trusted moderator to
  stop streaming in case of an emergency.