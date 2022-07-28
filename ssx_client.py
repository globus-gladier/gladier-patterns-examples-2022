#!/usr/bin/env python

# Enable Gladier Logging
# import gladier.tests

import argparse
import os

from gladier import GladierBaseClient, generate_flow_definition


@generate_flow_definition()
class SSXFlow(GladierBaseClient):
    gladier_tools = [
        "gladier_tools.globus.transfer.Transfer:FromStorage",
        "gladier_tools.posix.shell_cmd.ShellCmdTool:Stills",
        "gladier_tools.posix.shell_cmd.ShellCmdTool:PlotHist",
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

    # TODO: Uncomment and add your dials installation here
    # dials_path = ''


    # Base input for the flow
    flow_input = {
        "input": {
            # processing variables
            "sample_name": sample_name,
            "data_dir": data_dir,  # relative to endpoint
            "proc_dir": data_dir,  # relative to funcx
            # REMOTE DEMO ENDPOINT FOR SSX DATA
            "from_storage_transfer_source_endpoint_id": "a17d7fac-ce06-4ede-8318-ad8dc98edd69",
            "from_storage_transfer_source_path": "/SSX/clean_data",
            # TODO: Uncomment and add your Globus Collection here
            # "from_storage_transfer_destination_endpoint_id": "6d3275c0-e5d3-11ec-9bd1-2d2219dcc1fa",
            "from_storage_transfer_destination_path": str(data_dir),
            "from_storage_transfer_recursive": True,
            # shell cmd inputs
            "stills_args": f"",
            "stills_cwd": f"source {dials_path}/dials && dials.stills_process {phil_name} {data_dir} > {logname}.txt",
            "stills_timeout": 180,
            # shell cmd inputs
            "plot_hist_args": f"",
            "plot_hist_cwd": f"{data_dir}",
            "plot_hist_timeout": 180,
            # TODO: Uncomment and add your funcX endpoints here
            # "funcx_endpoint_non_compute": "",
            # "funcx_endpoint_compute": "",
        }
    }

    ssx_flow = SSXFlow()
    run = ssx_flow.run_flow(flow_input=flow_input, label=run_label)

    print(
        f"Run started, you can also track the progress at: \n"
        f"https://app.globus.org/runs/{run['run_id']}"
    )
