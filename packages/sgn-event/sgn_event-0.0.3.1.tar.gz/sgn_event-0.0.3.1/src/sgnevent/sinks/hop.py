from dataclasses import dataclass

from hop.robust_publisher import RobustProducer
from sgn.base import SinkElement


@dataclass
class HOPSink(SinkElement):
    hostname: str = "prod.hop.scimma.org"
    port: int = 9092
    topic: str = "amon.amon.chad"
    verbose: bool = False

    def pull(self, pad, frame):
        if frame.EOS:
            self.mark_eos(pad)
        if frame.data is not None:
            with RobustProducer(
                f"kafka://{self.hostname}:{self.port}/{self.topic}"
            ) as s:
                s.write(frame.data)
        if self.verbose:
            print("No data" if not frame.data else frame.data)
