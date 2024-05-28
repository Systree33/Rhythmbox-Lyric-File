from gi.repository import GObject, Gtk, Peas, RB, Gdk
import os
import urllib

class LyricFile(GObject.Object, Peas.Activatable):
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        super(LyricFile, self).__init__()
        GObject.threads_init()
        Gdk.threads_init()

    def do_activate(self):
        self.Shell = self.object
        self.Player = self.object.props.shell_player

        # Make the panel
        self.Box = Gtk.VBox()

        # View only textview and buffer for lyrics
        self.TextView = Gtk.TextView()
        
        self.TextView.set_editable(False)
        self.TextView.set_cursor_visible(False)
        self.TextView.set_wrap_mode(Gtk.WrapMode.WORD)
        
        self.TextView.set_left_margin(10)
        self.TextView.set_right_margin(10)

        # Spacing between lines
        self.TextView.set_pixels_above_lines(5)
        self.TextView.set_pixels_below_lines(5)
        
        self.TextBuffer = Gtk.TextBuffer()
        self.TextBuffer.set_text("No song")
        self.TextView.set_buffer(self.TextBuffer)

        # Place the textview in a GtkScrolledWindow in the case that the lyrics are
        # longer than the window
        self.Scroll = Gtk.ScrolledWindow(child=self.TextView)
        self.Box.pack_start(self.Scroll, expand=True, fill=True, padding=0)
        
        self.Box.show_all()

        # Add the panel the the right side of the rythmbox shell
        self.Shell.add_widget(self.Box, RB.ShellUILocation.RIGHT_SIDEBAR, expand=True, fill=True)
        self.Change_Connection = self.Player.connect('playing-song-changed', self.Update_Lyrics)
        
    def do_deactivate(self):
        self.Shell.remove_widget(self.Box, RB.ShellUILocation.RIGHT_SIDEBAR)
        self.Player.disconnect(self.Change_Connection)

    def Update_Lyrics(self, Player, _):
        Song = self.Player.get_playing_entry()
        SongFile = Song.get_playback_uri()
        SongFile = SongFile.removeprefix("file://")

        # Replace the extension with .lrc, and remove the url encoding
        LyricFile = SongFile.split(".")[0] + ".lrc"
        LyricFile = urllib.parse.unquote(LyricFile, 'utf-8')

        if os.path.isfile(LyricFile):
            # load and show the lyrics
            with open(LyricFile,"r") as File:
                LyricLines = File.readlines()

##            for Count, Line in enumerate(LyricLines):
##                LyricLines[Count] = "".join(Line.split("]")[1:]).lstrip(" ")

            Lyrics = "".join(LyricLines)
            self.TextBuffer.set_text(Lyrics)
        else:
            self.TextBuffer.set_text(f"No lyric file found for this song.\nCould not find '{LyricFile}'")
