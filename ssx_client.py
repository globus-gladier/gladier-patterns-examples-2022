#!/usr/bin/env python

# Enable Gladier Logging
# import gladier.tests

import argparse
import os

from gladier import GladierBaseClient, generate_flow_definition

from tools.ssx_create_phil import CreatePhil

@generate_flow_definition()
class SSXFlow(GladierBaseClient):
    gladier_tools = [
        "gladier_tools.globus.transfer.Transfer:FromStorage",
        # CreatePhil,
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
    dials_path = '~/dials/dials-v3-10-3'

    # Your Globus Transfer endpoint UUID where data processing will be done
    # destination_endpoint_id = "<UUID Value>"
    destination_endpoint_id = "08925f04-569f-11e7-bef8-22000b9a448b"

    # Your FuncX endpoint UUID where the processing function can run. It must be
    # able to access the data as stored on the Globus Transfer endpoint set by
    # destination_endpoint_id
    # funcx_endpoint_compute = "<UUID Value"
    funcx_endpoint_compute = "6951024f-06fb-4547-ade7-51e3515a5a05"

    # Your FuncX endpoint UUID where the non-compute intensive processing will
    # run. It also must be able to access the data as stored on the Globus
    # Transfer endpoint set by destination_endpoint_id
    # funcx_endpoint_non_compute = "<UUID Value"
    funcx_endpoint_non_compute = "6951024f-06fb-4547-ade7-51e3515a5a05"


    # Base input for the flow
    flow_input = {
        "input": {
            # processing variables
            "sample_name": sample_name,
            "data_dir": data_dir,  # relative to endpoint
            "proc_dir": data_dir,  # relative to funcx
            # REMOTE DEMO ENDPOINT FOR SSX DATA
            "from_storage_transfer_source_endpoint_id": "a17d7fac-ce06-4ede-8318-ad8dc98edd69",
            "from_storage_transfer_source_path": "/SSX/data1",
            # Value from settings above
            "from_storage_transfer_destination_endpoint_id": destination_endpoint_id,
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
            # Values from settings above
             "funcx_endpoint_non_compute": funcx_endpoint_non_compute,
             "funcx_endpoint_compute": funcx_endpoint_compute,
        }
    }

    ssx_flow = SSXFlow()
    run = ssx_flow.run_flow(flow_input=flow_input, label=run_label)

    print(
        f"Run started, you can also track the progress at: \n"
        f"https://app.globus.org/runs/{run['run_id']}"
    )
