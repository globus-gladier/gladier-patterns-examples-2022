import argparse
import os

from gladier import GladierBaseClient, generate_flow_definition
from tools.xpcs_boost_corr import BoostCorr
from tools.xpcs_plot import MakeCorrPlots


@generate_flow_definition
class XPCSBoost(GladierBaseClient):
    gladier_tools = [
        "gladier_tools.globus.transfer.Transfer:FromStorage",
        BoostCorr,
        MakeCorrPlots,
    ]


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--datadir", help="input file pathname", default="~/gladier_demo/xpcs/"
    )
    parser.add_argument("--samplename", help="input file pathname", default="demo1")
    parser.add_argument(
        "--gpu_flag",
        type=int,
        default=-1,
        help="""Choose which GPU to use. if the input is -1, then CPU is used""",
    )
    return parser.parse_args()


def main():
    args = arg_parse()

    sample_name = args.samplename
    data_dir = os.path.join(args.datadir, sample_name)
    run_label = "DEMO XPCS: " + sample_name

    raw_name = "A001_Aerogel_1mm_att6_Lq0_001_00001-01000.imm"
    hdf_name = "A001_Aerogel_1mm_att6_Lq0_001_0001-1000.hdf"
    qmap_name = "comm201901_qmap_aerogel_Lq0.h5"

    dataset_dir = data_dir

    # # Generate Destination Pathnames.
    raw_file = os.path.join(dataset_dir, raw_name)
    qmap_file = os.path.join(dataset_dir, qmap_name)
    # do need to transfer the metadata file because corr will look for it
    # internally even though it is not specified as an argument
    input_hdf_file = os.path.join(dataset_dir, hdf_name)
    output_hdf_file = os.path.join(dataset_dir, "output", hdf_name)
    # Required by boost_corr to know where to stick the output HDF
    output_dir = os.path.join(dataset_dir, "output")
    # This tells the corr state where to place version specific info
    execution_metadata_file = os.path.join(dataset_dir, "execution_metadata.json")
    
    instrument_computer_collection_id = "a17d7fac-ce06-4ede-8318-ad8dc98edd69"

    # TODO: Set the following values for your environment

    # The Globus collection UUID on the computer where data processing will be done
    analysis_computer_collection_id = "<UUID Value>"

    # Your FuncX endpoint UUID where the processing function can run. It must be
    # able to access the data as stored on the Globus collection identified by analysis_computer_collection_id
    analysis_computer_funcx_id = "<UUID Value>"



    flow_input = {
        "input": {
            # processing variables
            "sample_name": sample_name,
            "data_dir": data_dir,  # relative to endpoint
            "proc_dir": data_dir,  # relative to funcx
            # REMOTE DEMO ENDPOINT FOR PTYCHO DATA
            "from_storage_transfer_source_endpoint_id": instrument_computer_collection_id,
            "from_storage_transfer_source_path": "/XPCS/A001_Aerogel_1mm_att6_Lq0_001_0001-1000/",
            "from_storage_transfer_destination_endpoint_id": analysis_computer_collection_id,
            "from_storage_transfer_destination_path": str(data_dir),
            "from_storage_transfer_recursive": True,
            "metadata_file": input_hdf_file,
            "hdf_file": output_hdf_file,
            "execution_metadata_file": execution_metadata_file,
            "funcx_endpoint_compute": analysis_computer_funcx_id,
            "boost_corr": {
                "atype": "TwoTime",
                "qmap": qmap_file,
                "raw": raw_file,
                "output": output_dir,
                "batch_size": 8,
                "gpu_id": args.gpu_flag,
                "verbose": False,
                "masked_ratio_threshold": 0.75,
                "use_loader": True,
                "begin_frame": 1,
                "end_frame": -1,
                "avg_frame": 1,
                "stride_frame": 1,
                "overwrite": True,
            },
        }
    }

    corr_flow = XPCSBoost()
    run = corr_flow.run_flow(
        flow_input=flow_input, label=run_label, tags=["gladier", "demo", "simple_xpcs"]
    )

    print(
        f"Run started, you can also track the progress at: \n"
        f"https://app.globus.org/runs/{run['run_id']}"
    )


if __name__ == "__main__":
    main()
