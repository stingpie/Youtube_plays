# Hi it's Whomobile and welcome to newbie programmer hour, theres gonna be A LOT of comments on this. 
#---------------------------------------------------------
# I used these Twitch plays examples of code for reference:
# https://www.wituz.com/make-your-own-twitch-plays-stream.html
# https://www.dougdougw.com/twitch-plays-code/twitchplays-py

# I also looked at Pimanrules's code for YouTube Plays Super Mario Odyssey for reference too,
# mosty for the system that allows commands to be queued:
# https://gist.github.com/jsettlem/ca3274927f872f14fc8eae821a76e0cf

# I use the pytchat module to find and read the Youtube livechat, it seems to work well.
# I should probably look at the Youtube API for Python at some point but this is more easy.

# Asyncio does, something? I'm still not too sure I understand it but it seems to be better
# for reading the chat comment by comment

# pyvjoy interacts with vjoy to emulate a gamepad output

# time is for time stuff (huurr), most notibly the delay between actions

from pytchat import LiveChatAsync
from concurrent.futures import CancelledError
import pyvjoy
import asyncio
import time

# The nosense string is the Youtube stream url, might have to find
# a more neater way of replacing it in the future
chat = "HKheeRCfeyU"

# Inputs I want filtered (do I need this? I might keep for reference anyway...)
validCommands = ["up", "down", "left", "right", "u", "d", "l", "r",
                 "upleft", "upright" "downleft", "downright", "ul", "dl", "ur",
                 "mouse1", "mouse2", "m1", "m2"]

# Empty string of commands, used to make a list and go through them 1 by 1
commands = []
# The ammount of delay I want between commands, will probably try to make this
# detect how many commands and adjust it's self in the future
inputDelay = 0.3
# Setting up the controller for pyjoy
gamepad = pyvjoy.VJoyDevice(1)
# This does something I don't understand
nxt = time.time()

#Getting the Youtubechat and turning 
async def main():
  livechat = LiveChatAsync(chat, callback = func)
  while livechat.is_alive():
    #Still don't really get asyncio but it does what I want
    await asyncio.sleep(3)

# Turning chat data into a string to read
async def func(chatdata):
#idk what c is, but it works
  for c in chatdata.items:
    # This prints the timestamp, name of commenter, and the message they wrote in console
    # it also sets the message as the "msg" value  
    #print(f"{c.datetime} [{c.author.name}]-{c.message} {c.amountString}")
    msg = c.message
    
    # Ignore messages with a ! in them, makes it so you can posts scripts in chat
    if "!" in msg:
        # This also makes the message blank, probably don't need to do this but eh
        msg = ""
        continue
    # If the message contains a comma, count it as a new input after the last
    # This line finds commas and splits commands in msgParts along them. 
    msgParts = msg.split(",")
        
    # Make a list with the author and their command, we don't need the author
    # (unless I make a ban system...).
    # It also counts the number of commands in the comment
    commands.append(["", msgParts[0]])        
    #print(len(msgParts))
    
    if validCommands not in msgParts:
        continue
    
    if len(msgParts) > 1:
    # Limit number of commands (currently 1 to 10 commands are allowed, might bump
    # this up or change it to filter repeat/spam commands
    # This dosn't seem to work the way I want it too, but I can use it for something else later I guess
        for cmdnum in msgParts[1:10]:
            # Still don't need the author lol
            commands.append(["", cmdnum])
            #print(cmdnum)
            
    # I don't fully understand this part, I think it has something to do with the command limiter
#     if len(commands) and nxt < time.time():
#         msg = commands.pop(0)
#         msg = msg[1]
    
    #This part controls how fast the script will process the chat
    msgLoopCount = 0
    #Toggle states for Mouse buttons, they only seem to work here for some reason
    cmdDelay = 0.05
    
    #keyboard = Controller()
    #remember these start as False when the script is loaded
    togglem1 = False
    togglem2 = False
    
    while msgLoopCount < len(msgParts):
        # These are all the controls and the keys they are bind to
        # For "UP" 
        if msgParts[msgLoopCount] == "up" or msgParts[msgLoopCount] == "u":
            # For some reason this counts as a button push
            gamepad.set_button(1,1)
            time.sleep(cmdDelay)
            gamepad.set_button(1,0)
            print("up");
        # For "DOWN" 
        if msgParts[msgLoopCount] == "down" or msgParts[msgLoopCount] == "d":
            gamepad.set_button(2,1)
            time.sleep(cmdDelay)
            gamepad.set_button(2,0)
            print("down");
        # For "LEFT" 
        if msgParts[msgLoopCount] == "left" or msgParts[msgLoopCount] == "l":
            gamepad.set_button(3,1)
            time.sleep(cmdDelay)
            gamepad.set_button(3,0)
            print("left");
        # For "RIGHT"
        if msgParts[msgLoopCount] == "right" or msgParts[msgLoopCount] == "r":
            gamepad.set_button(4,1)
            time.sleep(cmdDelay)
            gamepad.set_button(4,0)
            print("right");
            
        # Next is the diagonals, only gonna allow verical/horizonal formatting eg: downleft not leftdown
        # For "UPLEFT"
        if msgParts[msgLoopCount] == "upleft" or msgParts[msgLoopCount] == "ul":
            gamepad.set_button(1,1)
            gamepad.set_button(3,1)
            time.sleep(cmdDelay)
            gamepad.set_button(1,0)
            gamepad.set_button(3,0) 
            print("upleft");
        # For "DOWNLEFT" 
        if msgParts[msgLoopCount] == "downleft" or msgParts[msgLoopCount] == "dl":
            gamepad.set_button(2,1)
            gamepad.set_button(3,1)
            time.sleep(cmdDelay)
            gamepad.set_button(2,0)
            gamepad.set_button(3,0)
            print("downleft");
        # For "UPRIGHT" 
        if msgParts[msgLoopCount] == "upright" or msgParts[msgLoopCount] == "ur":
            gamepad.set_button(1,1)
            gamepad.set_button(4,1)
            time.sleep(cmdDelay)
            gamepad.set_button(1,0)
            gamepad.set_button(4,0)
            print("upright");
        # For "DOWNRIGHT"
        if msgParts[msgLoopCount] == "downright" or msgParts[msgLoopCount] == "dr":
            gamepad.set_button(2,1)
            gamepad.set_button(4,1)
            time.sleep(cmdDelay)
            gamepad.set_button(2,0)
            gamepad.set_button(4,0)
            print("downright");
            
        # Now for the Mouse, I want it to toggle when m1 or m2 is detected
        
        # For "MOUSE1"
        if msgParts[msgLoopCount] == "mouse1" or msgParts[msgLoopCount] == "m1":
            togglem1 = not togglem1
            if togglem1 == True:
                gamepad.set_button(5,1)
                print("m1 on");
                time.sleep(cmdDelay + 0.05)
            if togglem1 == False:
                gamepad.set_button(5,0)
                print("m1 off");
                time.sleep(cmdDelay + 0.05)
                
        # For "MOUSE2"
        if msgParts[msgLoopCount] == "mouse2" or msgParts[msgLoopCount] == "m2":
            togglem2 = not togglem2
            if togglem2 == True:
                gamepad.set_button(6,1)
                print("m2 on");
                time.sleep(cmdDelay + 0.05)
            if togglem2 == False:
                gamepad.set_button(6,0)
                print("m2 off");
                time.sleep(cmdDelay + 0.05)
            
        # Add +1 to the loop count and add a slight delay before processing the next command in the queue
        msgLoopCount += 1
        time.sleep(inputDelay)
        
    # Now a quick rest between executing commands, might get rid of this later if needed. 
    time.sleep(0.5)
    
    # This does something with asyncio I don't understand yet.
    await chatdata.tick_async()

# This does something I don't fully understand yet, but it seems important
# Looks like it takes the program back to the main fuction to make loop?
if __name__ == '__main__':
  try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
  except CancelledError:
      pass
    
#TODO(DOO)
# - Take photo of game every so often (every 15, 30 minutes? 10 seems like too much)
# - PRIORITY: work out a way to filter spam inputs so long strings of commands can be
# rolled out, I think a limit of 10 of the same command in a row is fair and should stop spammers
# - Remove case sensitivty
# - 
# - Display outputted commands alongside gameplay in OBS (don't know how 2 yet)
    