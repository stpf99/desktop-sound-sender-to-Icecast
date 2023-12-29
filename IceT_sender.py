import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import soundcard as sc

class AudioStreamer:
    def __init__(self):
        self.input_device = None
        self.output_device = None
        self.pipeline = None
        self.loop = None

        Gst.init(None)
        self.loop = GLib.MainLoop()

        # Ustawienia dla PipeWire
        self.setup_pipeline()

    def setup_pipeline(self):
        # Ustawienia pipeline dla GStreamer z użyciem PipeWire
        pipeline_description = """
            autoaudiosrc ! lamemp3enc ! shout2send ip=streamlive*.hearthis.at port=**** password=************ mount=/*****.ogg username=*****
        """
        self.pipeline = Gst.parse_launch(pipeline_description)

    def start(self):
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

        # Start pipeline
        self.pipeline.set_state(Gst.State.PLAYING)
        self.loop.run()

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.loop.quit()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("Error: {}, Debug: {}".format(err, debug))
            self.loop.quit()

    def stop(self):
        # Zatrzymaj pipeline
        self.pipeline.set_state(Gst.State.NULL)
        self.loop.quit()

if __name__ == '__main__':
    audio_streamer = AudioStreamer()
    audio_streamer.start()

