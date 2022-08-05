#!/usr/bin/env python

# Enable Gladier Logging
# import gladier.tests

import argparse
import os

from gladier import GladierBaseClient, generate_flow_definition, GladierBaseTool

from tools.ssx_create_phil import CreatePhil
from gladier_tools.posix.shell_cmd import shell_cmd as shell_cmd_fn


def stills_shell_cmd(*args, **kwargs):
    return shell_cmd_fn(*args, **kwargs)


@generate_flow_definition(
    modifiers={
        "stills_shell_cmd": {
            "payload": {
                "args.$": "$.input.stills_args",
                "cwd.$": "$.input.stills_cwd",
            }
        }
    }
)
class StillsShellCmd(GladierBaseTool):
    funcx_functions = [stills_shell_cmd]


def plot_hist_shell_cmd(*args, **kwargs):
    return shell_cmd_fn(*args, **kwargs)


@generate_flow_definition(
    modifiers={
        "plot_hist_shell_cmd": {
            "payload": {
                "args.$": "$.input.plot_hist_args",
                "cwd.$": "$.input.plot_hist_cwd",
            }
        }
    }
)
class PlotHistShellCmd(GladierBaseTool):
    funcx_functions = [plot_hist_shell_cmd]


@generate_flow_definition
class SSXFlow(GladierBaseClient):
    gladier_tools = [
        "gladier_tools.globus.transfer.Transfer:FromStorage",
        CreatePhil,
        StillsShellCmd,
        PlotHistShellCmd,
    ]


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--datadir", help="input file pathname", default="~/gladier_demo/ssx/"
    )
    parser.add_argument("--samplename", help="input file pathname", default="demo1")
    return parser.parse_args()


if __name__ == "__main__":

    args = arg_parse()

    sample_name = args.samplename
    data_dir = os.path.join(args.datadir, sample_name)
    run_label = "DEMO SSX: " + sample_name

    # The predefined Globus collection UUID for test data
    instrument_computer_collection_id = "a17d7fac-ce06-4ede-8318-ad8dc98edd69"

    # TODO: Set the following values for your environment

    # A) Your DIALS installation path:
    dials_path = "~/dials-v3-10-2"

    # B) The Globus collection UUID on the computer where data processing will be done
    analysis_computer_collection_id = "<UUID Value>"

    # C) Your FuncX endpoint UUID where the processing function can run. It must be
    # able to access the data as stored on the Globus collection identified by analysis_computer_collection_id
    analysis_computer_funcx_id = "<UUID Value>"

    # Base input for the flow
    flow_input = {
        "input": {
            # processing variables
            "sample_name": sample_name,
            "data_dir": data_dir,  # relative to endpoint
            "proc_dir": data_dir,  # relative to funcx
            # Source location for SSX data
            "from_storage_transfer_source_endpoint_id": instrument_computer_collection_id,
            "from_storage_transfer_source_path": "/SSX/data1",
            "from_storage_transfer_destination_endpoint_id": analysis_computer_collection_id,
            "from_storage_transfer_destination_path": str(data_dir),
            "from_storage_transfer_recursive": True,
            # shell cmd inputs
            "stills_args": f"source {dials_path}/dials_env.sh && dials.stills_process {data_dir}/process.phil {data_dir}",
            "stills_cwd": f"{data_dir}_proc",
            "stills_timeout": 180,
            # shell cmd inputs
            "plot_hist_args": f"source {dials_path}/dials_env.sh && dials.unit_cell_histogram {data_dir}_proc/*integrated.expt",
            "plot_hist_cwd": f"{data_dir}_proc",
            "plot_hist_timeout": 180,
            "funcx_endpoint_compute": analysis_computer_funcx_id,
            "funcx_endpoint_non_compute": analysis_computer_funcx_id,
        }
    }

    ssx_flow = SSXFlow()
    run = ssx_flow.run_flow(flow_input=flow_input, label=run_label)

    print(
        f"Run started, you can also track the progress at: \n"
        f"https://app.globus.org/runs/{run['run_id']}"
    )
