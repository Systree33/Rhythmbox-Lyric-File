# Rhythmbox-Lyric-File
A Rhythmbox plugin that shows local .lrc files

All this does is load the file and display it. It does not display lyrics synchronously.

### Installation
Move or copy ```LyricFile.py``` and ```LyricFile.plugin``` into ```~/.local/share/rhythmbox/plugins.

You may have to create the ```plugins``` directory.

### Usage
The plugin looks for ```.lrc``` files in the same directory as the audio files.

For example, if your song was in this directory: ```~/Music/Downloaded/Song.mp4```, then the plugin will look for ```~/Music/Downloaded/Song.lrc```

I use this with spot dl, with ```spotdl <url> --lyrics genius --generate-lrc```, which downloads lyrics from genius and saves them as ```.lrc``` files in the same directory.
