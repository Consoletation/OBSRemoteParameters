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