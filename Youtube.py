# This is for capturing the Youtube chat as a string
# ------------------------------------------------------
# I use a module called [pytchat] to get the chat, Using the Youtube API is probably a
# better choice for this but it works fine for what I want.
import pytchat
# Don't know what this is yet
from concurrent.futures import CancelledError
# Asynchronous I/O, Allows different parts of code to run at different times
import asyncio
# Regular Expressions, used to filter chat of any unwanted symbols
import re
import pyvjoy
import time

# button push time, how long you want all buttons held down for
btnPushTime = 0.05

# Setting up the controller for pyjoy
gamepad = pyvjoy.VJoyDevice(1)
# Empty string of commands, used to make a list and go through them 1 by 1
commands = []
# List  of valid commands, use to see if any valid inputs are use and if they are to
# be counted towards the time spent processing them
  # It seems m1 & m2 both correspond to the same joystick key. 
  # It would probably be simpler if you just had m1 & maybe an extra command
  # to turn off m1. 
validCommands = ["up", "down", "left", "right", "u", "d", "l", "r",
                 "upleft", "upright" "downleft", "downright", "ul", "dl", "ur",
                 "mouse1", "mouse2", "m1", "m2"]





async def main():
    livechat = pytchat.LiveChatAsync("JmnxpJLikB8", callback=readchat)
    while livechat.is_alive():
        await asyncio.sleep(0)


# This is the part that reads the chat and cleans it up
async def readchat(chatdata, togglem1=False, togglem2=False):
    # I don't understand what c is, it's a value of some sort? how is it counted?
    for c in chatdata.items:
        # prints incoming messages to console
        print(f"{c.datetime} [{c.author.name}]-{c.message} {c.amountString}")
        # sets only the chat message as a string value
        msg = c.message
        # Ignores message if a ! is read, makes it loop to the top
        if "!" in msg:
            continue
        # This removes unwanted punctuation and makes the text lowercase, allowing for
        # non-case sensitivity
        msg = re.sub(r'[.;@#?!&$]+ *', " ", msg.lower())
        # print end result
        print(msg)

        # If the message contains a comma, count it as a new input after the last
        # This line finds commas and splits commands in into a list
        msgCmdList = msg.split(',')
        # Print how many commands as a number and the list
        print(len(msgCmdList))
        print(msgCmdList)

        # now compare the input commands with the list valid commands and remove invalids
        temp = set(validCommands)
        # Don't quite get the logic for this, but it seems to work! I think it mashes
        # lists together and ignores things that don't match with the first list.
        # This method is not perfect and tends to ignore messages with unwanted outputs at the start
        # Still better than registering too many commands in a list
          # So, what this simplifies down to is:
          #
          # for value in msgcmdlist:
          #   if value in temp:
          #     return value
          #
        sortedCmdList = [value for value in msgCmdList if value in temp]
        # And print the result!
        print(len(sortedCmdList))
        print(sortedCmdList)

        # Limit number of commands (currently 1 to 10 commands are allowed, might bump
        # this up or change it to filter repeat/spam commands
        if len(sortedCmdList) > 1:
            for cmd in sortedCmdList[0:10]:
                # Take the commands and process them one by one in order
                print(cmd)

        # This part controls how fast the script will process the chat
        msgLoopCount = 0

        while msgLoopCount < len(sortedCmdList[0:10]):
            # These are all the controls and the keys they are bind to

            # For "UP"
            if sortedCmdList[msgLoopCount] == "up" or sortedCmdList[msgLoopCount] == "u":
                # For some reason this counts as a button push
                gamepad.set_button(1, 1)
                time.sleep(btnPushTime)
                gamepad.set_button(1, 0)
                print("up")
            # For "DOWN"
            if sortedCmdList[msgLoopCount] == "down" or sortedCmdList[msgLoopCount] == "d":
                gamepad.set_button(2, 1)
                time.sleep(btnPushTime)
                gamepad.set_button(2, 0)
                print("down")
            # For "LEFT"
            if sortedCmdList[msgLoopCount] == "left" or sortedCmdList[msgLoopCount] == "l":
                gamepad.set_button(3, 1)
                time.sleep(btnPushTime)
                gamepad.set_button(3, 0)
                print("left")
            # For "RIGHT"
            if sortedCmdList[msgLoopCount] == "right" or sortedCmdList[msgLoopCount] == "r":
                gamepad.set_button(4, 1)
                time.sleep(btnPushTime)
                gamepad.set_button(4, 0)
                print("right")

            # Next is the diagonals, only gonna allow vertical/horizontal formatting eg: downleft not leftdown
            # For "UPLEFT"
            if sortedCmdList[msgLoopCount] == "upleft" or sortedCmdList[msgLoopCount] == "ul":
                gamepad.set_button(1, 1)
                gamepad.set_button(3, 1)
                time.sleep(btnPushTime)
                gamepad.set_button(1, 0)
                gamepad.set_button(3, 0)
                print("upleft")
            # For "DOWNLEFT"
            if sortedCmdList[msgLoopCount] == "downleft" or sortedCmdList[msgLoopCount] == "dl":
                gamepad.set_button(2, 1)
                gamepad.set_button(3, 1)
                time.sleep(btnPushTime)
                gamepad.set_button(2, 0)
                gamepad.set_button(3, 0)
                print("downleft")
            # For "UPRIGHT"
            if sortedCmdList[msgLoopCount] == "upright" or sortedCmdList[msgLoopCount] == "ur":
                gamepad.set_button(1, 1)
                gamepad.set_button(4, 1)
                time.sleep(btnPushTime)
                gamepad.set_button(1, 0)
                gamepad.set_button(4, 0)
                print("upright")
            # For "DOWNRIGHT"
            if sortedCmdList[msgLoopCount] == "downright" or sortedCmdList[msgLoopCount] == "dr":
                gamepad.set_button(2, 1)
                gamepad.set_button(4, 1)
                time.sleep(btnPushTime)
                gamepad.set_button(2, 0)
                gamepad.set_button(4, 0)
                print("downright")

            # Now for the Mouse, I want it to toggle when m1 or m2 is detected

            
            
            # For "MOUSE1"
            if sortedCmdList[msgLoopCount] == "mouse1" or sortedCmdList[msgLoopCount] == "m1":
                # Here, since togglem1 can only be true or false, we can simply 
                # invert the value of it. 
                # Not True --> False
                # Not False --> True
                togglem1= not togglem1
                
                # Here, I removed the "is true", because
                # that is asking if togglem1 == True,
                # but in that case, togglem1 would just be true,
                # so we can just ask if togglem1. 
                if togglem1:
                    gamepad.set_button(5, 0)
                    print("m1 off")
                else:
                    gamepad.set_button(5, 1)
                    print("m1 on")

            # For "MOUSE2"
            if sortedCmdList[msgLoopCount] == "mouse2" or sortedCmdList[msgLoopCount] == "m2":
                
                togglem2 = not togglem2
                if togglem2 :
                    togglem2 = False
                    gamepad.set_button(5, 0)
                    print("m1 off")
                else:
                    gamepad.set_button(5, 1)
                    print("m1 on")
                    
                    
            # As far As I can tell, msgloopcount +=1 does not actually delay anything.
            # Add +1 to the loop count then process the next command in the queue
            msgLoopCount += 1
            
            # This extra sleep command makes sure a frame has passed in between two button presses. 
            # Otherwise, the mousebuttons could be activated and deactivated in the same frame. 
            time.sleep(btnPushTime)

        await chatdata.tick_async()


# todo: Take a screenshot every 15 minutes!

# todo: take a savestate every half hour

# todo: make a visual output for button presses

  #   I'm not sure of the set-up your doing here, but if you are streaming your display,
  #   you might want to try pygame. Depending on how you want the controls to show up, 
  #   pygame would probably be the easiest.

# todo: fix mouse output stickiness

# todo: fix filter killing messages that don't fit the filter, instead of allowing them but ingoring unvalid inputs

# This does something I don't fully understand yet, but it seems important
# Looks like it takes the program back to the main fuction to make loop?
  # What I think this does, is that it is the code that first runs when
  # you load the program, and then it activates the other asyncrhonous loops. 
if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except CancelledError:
        pass
