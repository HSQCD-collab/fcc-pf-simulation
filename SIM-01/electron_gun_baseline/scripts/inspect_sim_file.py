#!/usr/bin/env python3

"""
inspect_sim_file.py

Purpose:
    Inspect an EDM4hep ROOT simulation file produced by ddsim.

This script is intended for Week 1 SIM validation.

It does three things:
    1. Lists all top-level ROOT objects in the file.
    2. Lists all branches inside each TTree.
    3. Loops over all events and counts how many events have non-empty
       collections such as MCParticles, ECalBarrelCollection, HCalBarrelCollection, etc.

Example usage:
    python scripts/inspect_sim_file.py electrons_10GeV_uniform_CLD_o2_v07.edm4hep.root \
      --output logs/inspect_uniform.txt
"""

import argparse
import sys
import ROOT


class Report:
    """
    Small helper class.

    It stores all output lines in memory.
    At the end, it can:
        - print them to terminal
        - save them to a text file
    """

    def __init__(self):
        self.lines = []

    def add(self, text=""):
        """Add one line to the report."""
        self.lines.append(str(text))

    def print_to_terminal(self):
        """Print all stored lines to the terminal."""
        print("\n".join(self.lines))

    def save_to_file(self, output_path):
        """Save all stored lines to a text file."""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines))
            f.write("\n")


def get_branch_size(tree, branch_name):
    """
    Return the size of a branch for the current event.

    Many EDM4hep collections behave like arrays/vectors in PyROOT.
    For example:
        len(events.ECalBarrelCollection)

    Some technical branches may not support len().
    In that case, this function returns None.
    """

    try:
        branch_object = getattr(tree, branch_name)
    except Exception:
        return None

    try:
        return len(branch_object)
    except Exception:
        return None


def print_file_structure(root_file, report):
    """
    Print the top-level ROOT objects and their branches.

    In EDM4hep ROOT files, the most important tree is usually:
        events

    Other trees such as:
        runs
        meta
        metadata
        podio_metadata

    contain run-level and metadata information.
    """

    report.add("=" * 100)
    report.add("ROOT FILE STRUCTURE")
    report.add("=" * 100)

    keys = root_file.GetListOfKeys()

    for key in keys:
        object_name = key.GetName()
        root_object = root_file.Get(object_name)
        class_name = root_object.ClassName()

        report.add("")
        report.add(f"Top-level object: {object_name}")
        report.add(f"Class: {class_name}")

        if root_object.InheritsFrom("TTree"):
            report.add(f"Entries: {root_object.GetEntries()}")
            report.add("Branches:")

            for branch in root_object.GetListOfBranches():
                report.add(f"  - {branch.GetName()}")


def inspect_event_collections(root_file, report):
    """
    Inspect all branches in the events tree.

    For every readable branch, this function calculates:
        - number of non-empty events
        - total number of objects across all events
        - maximum number of objects in one event

    This is useful because podio-dump usually shows only one event by default.
    """

    events = root_file.Get("events")

    if not events:
        report.add("")
        report.add("ERROR: No 'events' tree found.")
        return

    number_of_events = events.GetEntries()
    branch_names = [branch.GetName() for branch in events.GetListOfBranches()]

    summary = {}

    for branch_name in branch_names:
        summary[branch_name] = {
            "readable": False,
            "non_empty_events": 0,
            "total_size": 0,
            "max_size": 0,
        }

    for event_index in range(number_of_events):
        events.GetEntry(event_index)

        for branch_name in branch_names:
            size = get_branch_size(events, branch_name)

            if size is None:
                continue

            summary[branch_name]["readable"] = True
            summary[branch_name]["total_size"] += size
            summary[branch_name]["max_size"] = max(
                summary[branch_name]["max_size"],
                size,
            )

            if size > 0:
                summary[branch_name]["non_empty_events"] += 1

    report.add("")
    report.add("=" * 100)
    report.add("EVENT COLLECTION OCCUPANCY SUMMARY")
    report.add("=" * 100)
    report.add(f"Number of events: {number_of_events}")
    report.add("")

    report.add(
        f"{'Branch / Collection':45s} "
        f"{'Readable':>10s} "
        f"{'Non-empty events':>18s} "
        f"{'Total size':>12s} "
        f"{'Max/event':>10s}"
    )
    report.add("-" * 100)

    for branch_name in branch_names:
        info = summary[branch_name]
        readable_text = "yes" if info["readable"] else "no"

        report.add(
            f"{branch_name:45s} "
            f"{readable_text:>10s} "
            f"{info['non_empty_events']:18d} "
            f"{info['total_size']:12d} "
            f"{info['max_size']:10d}"
        )


def print_week1_summary(root_file, report):
    """
    Print a short summary focused only on the Week 1 SIM acceptance criteria.

    Required checks:
        - MCParticles exists and is non-empty
        - ECalBarrelCollection exists and is checked
        - HCalBarrelCollection exists and is checked

    I also include ECalEndcapCollection and HCalEndcapCollection because the
    uniform angular sample naturally sends some particles into the endcaps.
    """

    events = root_file.Get("events")

    if not events:
        return

    number_of_events = events.GetEntries()

    important_collections = [
        "MCParticles",
        "ECalBarrelCollection",
        "ECalEndcapCollection",
        "HCalBarrelCollection",
        "HCalEndcapCollection",
    ]

    report.add("")
    report.add("=" * 100)
    report.add("WEEK 1 SIM CHECKS")
    report.add("=" * 100)

    for collection_name in important_collections:
        branch_exists = bool(events.GetBranch(collection_name))

        if not branch_exists:
            report.add(f"{collection_name:35s} : MISSING")
            continue

        non_empty_events = 0
        total_objects = 0
        max_objects = 0

        for event_index in range(number_of_events):
            events.GetEntry(event_index)

            size = get_branch_size(events, collection_name)

            if size is None:
                size = 0

            total_objects += size
            max_objects = max(max_objects, size)

            if size > 0:
                non_empty_events += 1

        report.add(
            f"{collection_name:35s} : "
            f"exists, non-empty events = {non_empty_events}/{number_of_events}, "
            f"total objects = {total_objects}, "
            f"max/event = {max_objects}"
        )


def main():
    """
    Main program.

    Steps:
        1. Read command-line arguments.
        2. Open the ROOT file.
        3. Build the inspection report.
        4. Print the report.
        5. Optionally save the report to a text file.
    """

    parser = argparse.ArgumentParser(
        description="Inspect an EDM4hep ROOT simulation file."
    )

    parser.add_argument(
        "input_file",
        help="Input EDM4hep ROOT file, for example electrons_10GeV_uniform_CLD_o2_v07.edm4hep.root",
    )

    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Optional text file where the inspection report will be saved.",
    )

    args = parser.parse_args()

    root_file = ROOT.TFile.Open(args.input_file)

    if not root_file or root_file.IsZombie():
        print(f"ERROR: Could not open ROOT file: {args.input_file}")
        sys.exit(1)

    report = Report()

    report.add(f"Input file: {args.input_file}")

    print_file_structure(root_file, report)
    inspect_event_collections(root_file, report)
    print_week1_summary(root_file, report)

    root_file.Close()

    report.print_to_terminal()

    if args.output:
        report.save_to_file(args.output)
        print("")
        print(f"Saved report to: {args.output}")


if __name__ == "__main__":
    main()