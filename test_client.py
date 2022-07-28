from gladier import GladierBaseClient, generate_flow_definition


@generate_flow_definition
class GladierTestClient(GladierBaseClient):
    gladier_tools = [
        # Transfer a file from Tutorial Storage
        "gladier_tools.globus.transfer.Transfer:FromStorage",
        # Run a shell command on the file
        "gladier_tools.posix.shell_cmd.ShellCmdTool",
    ]


def main():

    # Parameters setup for the demonstration environment
    source_endpoint_id = "a17d7fac-ce06-4ede-8318-ad8dc98edd69"

    source_path = "/TEST/gladier_test_file.txt"

    # TODO: Set the following values for your environment
    # The input data will be copied to this location for processing
    destination_path = "~/gladier_demo/gladier_test_file.txt"

    # Your Globus Transfer endpoint UUID where data processing will be done
    # destination_endpoint_id = "<UUID Value>"

    # Your FuncX endpoint UUID where the processing function can run. It must be
    # able to access the data as stored on the Globus Transfer endpoint set by
    # destination_endpoint_id
    # funcx_endpoint_compute = "<UUID Value>"

    # Base input for the flow
    flow_input = {
        "input": {
            # The Test data sourced from a public location.
            "from_storage_transfer_source_endpoint_id": source_endpoint_id,
            "from_storage_transfer_source_path": source_path,
            "from_storage_transfer_destination_endpoint_id": destination_endpoint_id,
            "from_storage_transfer_destination_path": destination_path,
            "from_storage_transfer_recursive": False,
            # shell cmd inputs. Run the 'cat' command on the file
            "args": f"cat {destination_path}",
            "capture_output": True,
            # TODO: Uncomment and add your FuncX endpoint here.
            "funcx_endpoint_compute": funcx_endpoint_compute,
        }
    }

    # Run the flow. If running this for the first time, it will prompt a login flow.
    gladier_test_client = GladierTestClient()
    run = gladier_test_client.run_flow(flow_input=flow_input, label=f"Gladier Test")
    print(
        f"Run started, you can also track the progress at: \n"
        f"https://app.globus.org/runs/{run['run_id']}"
    )

    # Track the progress of the flow until completion
    gladier_test_client.progress(run["run_id"])

    # Report the result
    status = gladier_test_client.get_status(run["run_id"])
    print(f"The flow completed with the status: {status.get('status')}")
    if status.get("status") == "SUCCEEDED":
        print(
            f"Output: {status['details']['output']['ShellCmd']['details']['result'][0]}"
        )
    else:
        print(
            f"Check the logs for details: https://app.globus.org/runs/{run['run_id']}"
        )


if __name__ == "__main__":
    main()
