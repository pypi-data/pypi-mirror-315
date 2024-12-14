import os
import time
from dataclasses import dataclass

from sgn.base import Frame, SourceElement
from sgn.sources import SignalEOS


@dataclass
class DirectorySource(SourceElement, SignalEOS):
    """A source element that reads files from an input directory and puts them
    into SGN Frames.  The files are moved to the output directory on the next loop
    iteration.  Custom handlers that provide a dictionary of file loading functions
    based on extension determine files are processed"""

    inputdir: str = None
    outputdir: str = None
    wait: int = 1
    handlers: dict = None
    read_unhandled: bool = False

    def __post_init__(self):
        self.last_file = None
        self.output = None
        if self.handlers is None:
            self.handlers = {}
        super().__post_init__()
        assert len(self.source_pad_names) == 1
        assert os.path.exists(self.inputdir)
        assert os.path.exists(self.outputdir)

    def internal(self):
        time.sleep(self.wait)
        if self.last_file:
            os.rename(
                self.last_file,
                os.path.join(self.outputdir, os.path.split(self.last_file)[1]),
            )
        files = [
            f
            for f in os.listdir(self.inputdir)
            if os.path.isfile(os.path.join(self.inputdir, f))
        ]
        if files:
            infile = os.path.join(self.inputdir, files[0])
            outfile = os.path.join(self.outputdir, files[0])
            _, ext = os.path.splitext(infile)
            if ext in self.handlers:
                self.output = self.handlers[ext](infile)
            elif self.read_unhandled:
                with open(infile, "r") as f:
                    self.output = f.read()
            else:
                print(f"Not parsing {infile}, but moving to {self.inputdir}")
            self.last_file = infile
        else:
            self.last_file = None
            self.output = None

    def new(self, pad):
        return Frame(data=self.output, EOS=self.signaled_eos())
