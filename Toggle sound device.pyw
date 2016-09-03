import os, tkinter, myPrint, subprocess, traceback

# What if one of the devices names doesn't exist (unplugged/renamed)? Can subprocess return an error from NirCmd?
# Replace myPrint.error() with something else (no console if using .pyw file)

def currentDevice():
  with open(configFile) as file:                                                    # Open config file in read mode
    return file.read()                                                              # Return the text in the config file

def getNewDevice():
  if currentDevice() == 'Speakers':                                                 # Check if current device is speakers
    return 'Headphones'                                                             # Return headphones
  elif currentDevice() == 'Headphones':                                             # Current device is headphones
    return 'Speakers'                                                               # Return speakers
  else:
    myPrint.error('Wrong text in configuration file')

def updateFile(device):
  with open(configFile, 'w') as file:                                               # Open config file in write mode
    file.write(device)                                                              # Write new device to config file

def showText(message):
  label = tkinter.Label(text=message,                                               # Create a label with the specified text
          font=('Verdana','28'),                                                    # Set font type and size
          fg='black', bg='gray1',                                                   # Set foreground and background color
          justify=tkinter.LEFT)                                                     # Align text to the left
  label.master.overrideredirect(True)                                               # Turn off window border
  label.master.geometry('+50+50')                                                   # X-Y coordinates for text
  label.master.lift()                                                               # Move widget to the top of the window stack
  label.master.wm_attributes('-topmost', True)                                      # Make sure that window stays on top of all other windows
  label.master.wm_attributes('-disabled', True)                                     # Make sure that the window can't be interacted with
  label.master.wm_attributes('-transparentcolor', 'gray1')                          # Make color transparent
  label.after(1000, lambda: label.master.destroy())                                 # Destroy object after 1 second
  label.pack()                                                                      # Fit the size of the window to the widget
  label.mainloop()                                                                  # Show window

try:
  currentDir = os.path.dirname(__file__)                                            # Get directory path to this file
  configFile = currentDir + '\\currentDevice.ini'                                   # Path to config file
  nirCmdPath = currentDir + '\\nircmd.exe'                                          # Path to NirCmd

  devices = {'Speakers':'Speakers',                                                 # Variable to hold name of speakers
             'Headphones':'Realtek HD Audio 2nd output'}                            # Variable to hold name of headphones

  newDevice = getNewDevice()                                                        # Get the device to switch to
  subprocess.call([nirCmdPath, 'setdefaultsounddevice', devices[newDevice], '0'])   # Set new device to default sound device
  subprocess.call([nirCmdPath, 'setdefaultsounddevice', devices[newDevice], '2'])   # Set new device to default communications device
  showText('Current audio device:\n' + newDevice)                                   # Show new device as text on screen
  updateFile(newDevice)                                                             # Write new device output to config file
except:
  traceback.print_exc()                                                             # Print error
  input()                                                                           # Pause program
