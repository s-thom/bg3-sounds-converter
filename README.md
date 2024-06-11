# BG3 sound categoriser

This script is heavily based on (by which I mean copy/pasted from) [/u/NikolayTeslo's comment](https://www.reddit.com/r/BaldursGate3/comments/14eipmt/comment/k16mtq7/) in /r/BaldursGate3. This script will also use vgmstream to do the conversion so you don't need a separate step for that.

## Requirements

This script assumes you are on Windows and are comfortable enough in a terminal to run a command or two.

You will need to download/install a few things to make this work.

- [BG3 Modders Multitool](https://github.com/ShinyHobo/BG3-Modders-Multitool)
  - Used to unpack the audio files and metadata from the game.
  - Download the latest release from [the releases page](https://github.com/ShinyHobo/BG3-Modders-Multitool/releases) and extract somewhere.
- [Python 3](https://www.python.org/)
  - Used to run this script.
  - Install how you would normally install Python, The Windows Installer from [the website](https://www.python.org/downloads/) is a good choice if you don't know what to do.
- [vgmstream](https://github.com/vgmstream/vgmstream)
  - Used to convert the `.wem` files to `.wav` so audio players can play them.
  - Download the latest release from [the builds website](https://vgmstream.org/) and extract the folder somewhere.
  - Double check the release has a bunch of DLLs included.
- [wwiser](https://github.com/bnnm/wwiser)
  - Used to convert the `.bnk` files to XML so they can be read.
  - Download both `wwiser.pyz` and `wwnames.db3` from [the releases page](https://github.com/bnnm/wwiser/releases) and place them in the folder this README resides.

## Usage

1. Ensure you check this project out in a path with *no spaces* in the name
   - This project is currently sensitive to this, and having spaces in any paths will mean it doesn't work.
2. Open the Modders Multitool
   - Make sure you have your game path set correctly. This can be confirmed by opening the Configuration dialog from thetop menu.
3. In the top menu, select `Utilities` > `Game File Operations` > `Unpack Game Files`.
4. Select `SharedSoundBanks.pak` and `SharedSounds.pak` and confirm.
5. Wait for the unpacking to complete.
6. Back in this project, change the constants in `categoriser.py`
   - `wwizer_pyz` should be the path of the `wwiser.pyz` you downloaded.
   - `folder_vgmstream` should be the folder you extracted vgmstream to.
   - `folder_unpacked_data` should be the `UnpackedData` folder in your BG3 Modders Multitool location.
   - `folder_audio_converted` should be the folder where you want your final files to be.
7. If you want the files renamed to more human-friendly names, check the advanced section.
8. Run `python categoriser.py`
   - This will take some time, so go off and enjoy your life while it does its thing.
9. Your audio files will be categorised in the converted folder.
   - The file names will be numbers, not human friendly names. If you are looking for something specific, then you will need to sort through them manually.

## Future plans

- None. I'll only revisit this if I need to mess with more audio files.
