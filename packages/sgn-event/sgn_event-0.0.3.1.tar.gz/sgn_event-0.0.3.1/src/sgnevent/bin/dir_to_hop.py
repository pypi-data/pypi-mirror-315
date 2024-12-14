#!/usr/bin/env python3

import argparse
import json
from sgn.apps import Pipeline
from sgn.sources import SignalEOS
from sgnevent.sources import DirectorySource
from sgnevent.sinks import HOPSink
from hop.models import VOEvent


def parse_command_line():
    parser = argparse.ArgumentParser(
        prog="sgn-amon",
        description="poll a directory, send a json or vo event xml file and then post it to a scimma hop client",
        epilog="I really hope you enjoy this program.",
    )
    parser.add_argument(
        "--input-directory",
        help="Input directory. Required",
    )
    parser.add_argument(
        "--output-directory",
        help="Output directory. Required",
    )
    parser.add_argument(
        "--hostname",
        help="kafka host name. Default prod.hop.scimma.org",
        default="prod.hop.scimma.org",
    )
    parser.add_argument(
        "--topic",
        help="kafka topic. Required",
    )
    parser.add_argument("--port", type=int, help="port. Default 9092", default=9092)
    parser.add_argument("--verbose", action="store_true", help="Be verbose")
    args = parser.parse_args()
    assert (
        args.input_directory
        and args.output_directory
        and args.hostname
        and args.topic
        and args.port
    )
    return args

def main():
    args = parse_command_line()

    src = DirectorySource(
        source_pad_names=[
            "file",
        ],
        inputdir=args.input_directory,
        outputdir=args.output_directory,
        handlers={
            ".json": lambda x: json.load(open(x, "r")),
            ".xml": VOEvent.load_file,
        },
    )
    snk = HOPSink(
        sink_pad_names=[
            "file",
        ],
        hostname=args.hostname,
        port=args.port,
        topic=args.topic,
        verbose=args.verbose,
    )

    p = Pipeline()

    p.insert(
        src,
        snk,
        link_map={
            snk.snks["file"]: src.srcs["file"],
        },
    )
    with SignalEOS() as signal_eos:
        p.run()


if __name__ == "__main__":
    main()
