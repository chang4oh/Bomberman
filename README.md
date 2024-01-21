# Bomberman
Created from ChatGPT
Bomberman is a classic video game franchise that was first introduced by Hudson Soft (now
part of Konami) in the 1980s. The game series is known for its action-packed gameplay and 
maze-like levels where players control a character who must strategically place bombs to 
defeat enemies and solve puzzles.

The basic premise of the game involves a character named Bomberman, who navigates 
through grid-based levels, trying to eliminate enemies by strategically placing and 
detonating bombs while avoiding being caught in the blast radius of their own bombs. The 
game typically features both single-player and multiplayer modes, making it a popular 
choice for multiplayer gaming.

Bomberman has seen numerous iterations and adaptations across various gaming 
platforms, including the NES, Super Nintendo, and modern consoles. It has become a 
beloved and enduring franchise in the gaming world and has been released in various forms, 
including 2D and 3D versions, as well as spin-off titles.

The multiplayer aspect of Bomberman is particularly well-known, as it allows for exciting and 
competitive gameplay, with players trying to outwit and outmaneuver their opponents while 
avoiding the destructive power of the bombs.

Bomberman has also made appearances in various crossover games and has a strong 
presence in the gaming community. It remains a favorite among gamers for its classic, 
addictive gameplay and has contributed significantly to the history of video games.
//Created from ChatGPT


### Tools and Resources
      PyCharm - Coding
      ChatGPT - Coding and guide
      iCon8 - Sprites
      Link:  https://icons8.com/icons/set/bomberman
      My Brain :  Making sure it's Bomberman game
      Music - Bomberman Music
      Link:  https://downloads.khinsider.com/game-soundtracks/album/bomberman-turbografx-16-1990
      Bomb Explosion Sound - 
      Link:  https://www.101soundboards.com/boards/44154-sound-effects-super-bomberman-2-miscellaneous-snes

      TO PLAY, download dist (is the latest version)
      Click the main.exe and the software will automatically work
      Will need Python IDE downloaded

### HOW TO PLAY
      CONTROLS  Arrow keys (character movement, choice selection)
                ENTER (select)
                ESC (current menu such as Menu screen, end screen, level screen)
                SPACE (drop bomb, 1 bomb per second)
                
### Incase you have run into the problem and can't get it resolved
*This is for interested developers and if you want to try the game,
please check for .exe or .html to play instantly.
This instruction is very very important! Or else you will go into
loops of errors and will take many hours just to have the same error
stuck forever.

1. uninstall python
2. uninstall ubuntu/linux (if used)

*Basic settings on VSCode, Ubuntu, Bash, and JS are recommended to look
for tutorial videos.

*when there is warning on pathing issue, go to window, edit environment variable
	double click PATH, copy&paste the location installed to PATH

1. install VSCode
2. install from official Python website
	Make sure install python with PATH added
	With checkmarks just about everything (look tutorial downloading)
	Get it from official website
3. install Ubuntu 22.0 on microsoft store
	any LTE versions are good

3. Open VSCode
	open terminal using 'shift'+'`' keys
	Bash: pip install pygame // pip install is equivalent to import in Ubuntu
				// make sure right interpretor is selected or error will pop up

4. Create an .exe file
	Bash: pip install pipinstaller // app that makes into .exe
	Bash: python -m PyInstaller myscript.py	// no depublicates; takes a while to install .exe
	
5. Create an HTML
	asyncio based program used coroutine which is on top of single thread 
	as compared to multithreading

	Bash: pip install asyncio 
	Bash: pip install pygbag
	*follow tutorial where to place asyncio to make it work
	pygbag folder_name	// must do outside the folder_name
	http://localhost:8000#debug	// HTML debug

## ChangeLogs
### Version 2.0
      Branch created in works of seperating files in organized manner
      In works of creating working .exe and .html version                
### Version 1.4  
      Button clicking is reponsive, in pace, and no flicking screen
      Added theme menu image  
      End Menu [Retry] and [Menu] buttons added with appropriate function
      Fixed end game screen screen flickers when any button is selected 
      *Added exe. file inside dist for easy access to game play
      Keyword for creating exe. : pyinstaller main.py  --onefile --noconsole in Local Terminal
      Will need to install pyinstaller (only when creating exe.)
      Process:  https://chat.openai.com/share/837969f0-6921-43fb-b280-05acc8bd1918
### Version 1.3 
      Credits button function added
      Options button funciton added (Music On/Off, Difficulty Normal/Hard, Change Skin)
      Multiple error fixes including screen transition between menu and buttons
      Process:  https://chat.openai.com/share/6fa990e8-069e-4c92-b570-d19b361867e9
      Process:  https://chat.openai.com/share/6fa990e8-069e-4c92-b570-d19b361867e9
      Note: With just near 500 lines code on version 1.3, using ChatGPT is difficult
      Will need backup because game will not work especially when requesting 
      multiple changes at the same time.
### Version 1.2 
      Game background music added
      Bomb explosion sound added
      Menu Screen added with four button (Start Game) (Options) (Credits) (Quit)
      Quit button function added
      Menu screen music added
      Start button function added
      Note: adding menu screen and connecting to start game is very difficult process
      Everything is rendered now, adjusted every objects (another difficult process)
      Start button function added
      Automatic leveling, and scoring 
      Process:  https://chat.openai.com/share/837969f0-6921-43fb-b280-05acc8bd1918
      Process:  https://chat.openai.com/share/6fa990e8-069e-4c92-b570-d19b361867e9
### Version 1.1
      Player now be able to drop one bomb at a time (not an easy task)
      Bomb will remove enemy after exploding in close proximity
      Process:  https://chat.openai.com/share/837969f0-6921-43fb-b280-05acc8bd1918
### Version 1.0 
      Bomb (Bomb sprite) explode and with short animation. 
      Player (Bomberman sprite) with control and screen follow the player . 
      Random Enemy spawn (Ghost sprite) with random movement. Player removed upon collision AKA lose game.
      Random Wall spawn (Wall sprite) with collision
      Process:  https://chat.openai.com/share/837969f0-6921-43fb-b280-05acc8bd1918




