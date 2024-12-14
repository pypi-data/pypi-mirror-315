#!/usr/bin/env python3
"""iox - Check input and output to conditionally execute commands in parallel

Usage:
======
Single job:
$ iox -i input1 input2 -o output1 output2 --exec "command {input} {output}"

Single job rerun if inputs are newer than outputs:
$ iox -u -i input1 input2 -o output1 output2 --exec "command {input} {output}"

Parallel jobs:
$ iox -i input1/{d}.csv -o output/{d}.csv -d 2020 2021 2022 \\
    --exec "command {input} {output} && echo {d} > {output}"

Parallel jobs with wildcards from a file:
$ iox -i input1/{f}.csv -o output/{f}.csv --date file.txt \\
    --exec "echo {date} > {output}"

Parallel jobs with combinations of wildcards:
$ iox -i input_{a}/{d}.csv -o output/{a}_{d}.csv \\
    --combinations -a type1 type2 type2 -d 2020 2021 2022 \\
    --exec "command --year {d} -t {a} {input} {output}"

Jobs in a pipeline, input/output paths are passed through:
$ echo f1 f2 f3 \\
    | iox -o f4 -x "echo {input} > {output}" \\
    | iox -o summary -x "cat {input} > {output}"
"""
import subprocess
from shutil import rmtree
import sys
import itertools
import string
from pathlib import Path
import os
from typing import List, Dict, Any
from functools import partial
from collections import defaultdict
import logging

# will be replaced by the git commit hash during setup.py
__version__ = "0.4.0"

INCOMPLETE_EXT = "iox_incomplete"


class Paths(list):
    def __init__(self, *paths):
        args = [Path(i) for i in paths]
        super().__init__(args)

    def __getattr__(self, name):
        """Return method if attr is callable else just the attribute."""
        attributes = [getattr(item, name) for item in self]
        if all(callable(i) for i in attributes):

            def method(*args, **kwargs):
                out = [item(*args, **kwargs) for item in attributes]
                # coerce to Paths if all elements are Paths
                if all(isinstance(i, Path) for i in out):
                    return Paths(*out)
                return out

            return method
        else:
            # coerce to Paths if all elements are Paths
            if all(isinstance(i, Path) for i in attributes):
                return Paths(*attributes)
            return attributes

    def __str__(self):
        return " ".join(map(str, self))

    def non_existing(self):
        return Paths(*[p for p in self if not p.exists()])

    def existing(self):
        return Paths(*[p for p in self if p.exists()])

    def remove(self):
        for path in self:
            if path.is_dir():
                rmtree(path)
            elif path.is_file():
                path.unlink()
        return

    def modification_time(self):
        return [p.stat().st_mtime for p in self]


def safe_format(s: str, kwargs) -> str:
    class SafeFormatter(dict):
        def __missing__(self, key):
            return "{" + key + "}"

    return s.format_map(SafeFormatter(**kwargs))


def format_wildcards(
    wildcards: Dict[str, List[str]],
    paths: List[str],
    combinations: bool = False,
) -> List[str]:
    # expand wildcards
    if combinations:
        combos = list(itertools.product(*wildcards.values()))
        expand_dict = [dict(zip(wildcards.keys(), c)) for c in combos]
    else:
        # group wildcards by length
        lens = defaultdict(list)
        for k, v in wildcards.items():
            lens[len(v)].append(k)
        wildcard_combos = {}
        for cw in lens.values():
            wildcard_combos[tuple(cw)] = list(zip(*[wildcards[v] for v in cw]))
        # take combinations of wildcards with the same length
        expand = list(itertools.product(*wildcard_combos.values()))
        expand_dict = [{kk: vv for k, v in zip(wildcard_combos.keys(), e) for kk, vv in zip(k, v)} for e in expand]

    out = [[safe_format(str(i), wc) for i in paths] for wc in expand_dict]
    return out


def check_output(
    input: Paths,
    output: Paths,
    update: bool = False,
    dry_run: bool = False,
    force: bool = False,
) -> bool:
    # check if outputs need to be updated
    eout = output.existing()
    needs_update = False
    if eout and update and input:
        needs_update = min(eout.modification_time()) < max(input.modification_time())
        if needs_update:
            logging.info(f"Updating: {eout}")
    # Check if all output paths exist
    if output and all(output.exists()) and not needs_update and not force:
        return True

    if dry_run:
        if eout:
            logging.info(f"Would clean and recreate: {eout}")
        return False
    # Clean output and make sure all directories exist
    eout.remove()
    output.parent.mkdir(parents=True, exist_ok=True)
    return False


def handle_incomplete_output(output: Paths) -> None:
    # move any existing output to a iox_incomplete dir
    incomplete = output.existing()
    incompletes = {}
    if incomplete:
        for p in incomplete:
            incomplete_name = p.parent / f"{p.stem}_{INCOMPLETE_EXT}{p.suffix}"
            p.rename(incomplete_name)
            logging.warning(f"Moved incomplete output to {incomplete_name}")
            incompletes[p] = incomplete_name
    return incompletes


def check_io(
    input: Paths = Paths(),
    output: Paths = Paths(),
    exec: List[str] = [],
    force: bool = False,
    dry_run: bool = False,
    quiet: bool = False,
    update: bool = True,
    **kwargs,
) -> None:
    # make sure all Paths and convert lists to space-separated strings
    input = Paths(*input)
    output = Paths(*output)
    exec = safe_format(" ".join(exec), {"input": input, "output": output})

    # Print for debugging
    logging.debug(f"Input: {input}")
    logging.debug(f"Output: {output}")
    logging.debug(f"Exec: {exec}")

    # Check if all input paths exist
    iein = input.non_existing()
    if len(iein) > 0:
        raise FileNotFoundError(f"Input paths do not exist: {iein} - exiting.")

    output_uptodate = check_output(input, output, update, dry_run, force)

    # job info to return
    job_info = {"input": str(input), "output": str(output), "exec": exec, "uptodate": output_uptodate}

    if output_uptodate and not force:
        logging.info("All output paths exist, nothing to be done. Exiting.")
        return job_info

    if dry_run:
        logging.info(f"Would execute: {exec}")
        logging.info("Dry run. Exiting.")
        return job_info

    # Execute the command
    stdout = open(os.devnull, "w") if quiet else sys.stdout
    try:
        run = subprocess.run(exec, shell=True, check=True, stdout=stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running {exec}: {e}")
        handle_incomplete_output(output)
        raise e

    # Exit if not all output paths exist
    ieout = output.non_existing()
    if len(ieout) > 0:
        errmsg = f"Not all outputs exist after running {exec}.\n{ieout}\nExiting."
        raise FileNotFoundError(errmsg)

    return job_info


def check_io_parallel(
    wildcards: Dict[str, str],
    input: List[Path],
    output: List[Path],
    exec: List[str],
    jobs: int = 1,
    combinations: bool = False,
    **kwargs,
) -> None:
    import multiprocessing as mp

    logging.debug(f"Input: {input}")
    logging.debug(f"Output: {output}")
    logging.debug(f"Wildcards: {wildcards}")

    inputs = format_wildcards(wildcards, input, combinations)
    outputs = format_wildcards(wildcards, output, combinations)
    execs = format_wildcards(wildcards, exec, combinations)

    logging.debug("Parallel jobs:")
    for i, o, e in zip(inputs, outputs, execs):
        logging.debug(f"-i {i} -o {o} --exec {e}")

    def update_progress():
        nonlocal completed_jobs, total_jobs
        completed_jobs += 1
        prec = len(str(total_jobs))
        pct = f"{(completed_jobs / total_jobs) * 100:03.{prec-1}f}".zfill(prec + 2)
        return f"[{completed_jobs:0{prec}d}/{total_jobs} ({pct}%)] "

    def report_complete(result):
        progress = update_progress()
        if result["uptodate"]:
            logging.warning(progress + "Up-to-date: " + result["output"])
        else:
            logging.warning(progress + result["exec"])

    def report_error(error):
        progress = update_progress()
        logging.error(progress + str(error))

    total_jobs = len(outputs)
    completed_jobs = -1
    worker_func = partial(check_io, **kwargs)

    # initialise progress
    logging.warning(update_progress())
    pool = mp.Pool(jobs)
    res = []
    for i, o, e in zip(inputs, outputs, execs):
        r = pool.apply_async(
            worker_func,
            args=(i, o, e),
            callback=report_complete,
            error_callback=report_error,
        )
        res.append(r)
    pool.close()
    pool.join()
    # get results
    out = [r.get() for r in res]
    return out


def parse_wildcards(unknown_args: List[str]) -> Dict[str, str]:
    # Convert unknown arguments to a dictionary
    extra_args = {}
    for arg in unknown_args:
        if arg.startswith("--") or arg.startswith("-"):
            key = arg.lstrip("--").lstrip("-")
            extra_args[key] = []
        else:
            extra_args[key].append(arg)
    # if any argument only has one value, try to treat it as a file and open it
    # and replace the argument with the lines of the file
    for key, value in extra_args.items():
        if len(value) == 1:
            with open(value[0]) as f:
                extra_args[key] = f.read().splitlines()
    return extra_args


def __main__() -> None:
    """Command line interface for iox."""
    import argparse

    arguments = [
        {
            "names": ("-i", "--input"),
            "args": {"nargs": "+", "required": False, "type": Path, "default": Paths()},
            "help": "Input path/pattern",
        },
        {
            "names": ("-o", "--output"),
            "args": {"nargs": "+", "required": True, "type": Path},
            "help": "Output path/pattern",
        },
        {
            "names": ("-x", "--exec"),
            "args": {"nargs": argparse.REMAINDER, "required": True},
            "help": "Command to execute",
        },
        {
            "names": ("-f", "--force"),
            "args": {"action": "store_true"},
            "help": "Force execution even if output paths exist",
        },
        {
            "names": ("-n", "--dry-run"),
            "args": {"action": "store_true"},
            "help": "Perform a dry run without executing the command",
        },
        {
            "names": ("-j", "--jobs"),
            "args": {"type": int, "default": 1},
            "help": "Number of parallel jobs",
        },
        {
            "names": ("-c", "--combinations"),
            "args": {"action": "store_true"},
            "help": "Create all combinations of wildcards",
        },
        {
            "names": ("--no-update",),
            "args": {"action": "store_false", "dest": "update"},
            "help": "Don't update existing output files even if input files are newer",
        },
        {
            "names": ("-q", "--quiet"),
            "args": {"action": "store_true"},
            "help": "Suppress output from the command",
        },
        {
            "names": ("-v", "--verbose"),
            "args": {"action": "store_true"},
            "help": "Enable verbose output",
        },
        {
            "names": ("-h", "--help"),
            "args": {"action": "help"},
            "help": "Show help message and exit",
        },
        {
            "names": ("--version",),
            "args": {"action": "version", "version": __version__},
            "help": "Show version and exit",
        }
    ]

    parser = argparse.ArgumentParser(
        description=__doc__,
        add_help=False,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    for arg in arguments:
        parser.add_argument(*arg["names"], help=arg["help"], **arg["args"])

    args, wildcard_args = parser.parse_known_args()
    args = vars(args)
    # add stdin if given
    if not sys.stdin.isatty():
        std_input = sys.stdin.read().split()
        args["input"] = Paths(*args["input"] + std_input)

    # set up logging
    loglevel = "DEBUG" if args["verbose"] else ("WARNING" if args["quiet"] else "INFO")
    logging.basicConfig(level=getattr(logging, loglevel), format="%(message)s")

    if wildcard_args:
        wildcards = parse_wildcards(wildcard_args)
        result = check_io_parallel(wildcards, **args)
    else:
        result = [check_io(**args)]

    # if piping/redirecting, print the output files to stdout
    if not sys.stdout.isatty():
        print(' '.join([r["output"] for r in result]))
    return


if __name__ == "__main__":
    __main__()
