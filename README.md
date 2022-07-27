# Gladier Application Examples

The paper **Linking Scientific Instruments and Computation** describes five example Gladier applications. We provide code pointers and information on how to run simple versions of each application at the following links:

* [XPCS](https://github.com/globus-gladier/gladier-patterns-examples-2022/blob/main/xpcs_client.py): X-ray Photon Correlation Spectroscopy application.
* [SSX](https://github.com/globus-gladier/gladier-patterns-examples-2022/blob/main/ssx_client.py): Serial Synchrotron Crystallography application 
* [HEDM](): High-energy Diffraction Microscopy
* [BRAGGNN](https://github.com/globus-gladier/gladier-patterns-examples-2022/blob/main/braggnn_client.py): Bragg
* [PTYCHOGRAPHY](https://github.com/globus-gladier/gladier-patterns-examples-2022/blob/main/ptychodus_client.py): Ptychography application.

We also provide below information on how to set up to run these applications.


## The common pattern implemented by all five applications

Although each of the five applications has its own particular set of tools, they all implement a common pattern, in which the Gladier application (the **client**) first makes a `Transfer` request to transfer data from an **instrument** to an **analysis computer**, and then makes one or more `Compute` requests to the analysis computer to analyze the data. Of course, many Gladier applications (including the production applications described in the paper) are more complex than that, but this pattern captures important concepts.

We describe in the following how to realize the common pattern using your own computer as the analysis computer.

### Synopsis of the infrastructure services needed to realize the common pattern

The common patternr requires that three distinct endpoints be running:

* On the **instrument**, a first Globus Connect endpoint (or "Collection" in Globus parlance), which we refer to here as *instrument-transfer*, so that files can be transferred *from* the instrumentl
* On the **analysis computer**, a second Globus Connect endpoint (*analysis-transfer*), so that files can be transferred *to* the analysis computer, plus a funcX endpoint (*analysis-compute*), so that tasks can be sent to the analysis computer for execution. 

### Configuring the instrument

In a real deployment, the *instrument-transfer* endpoint will typically be a Globus Connect service running on a storage system at the instrument where data are being produced.

To facilitate experimentation, we make test data available for the XPCS, SSX, and Ptychography applications at this [Globus endpoint](https://app.globus.org/file-manager?origin_id=a17d7fac-ce06-4ede-8318-ad8dc98edd69&origin_path=%2F~%2F). 

### Configuring the analysis computer 

In a real deployment, the **analysis computer** will typically be a high-performance computing (HPC) systen that is likely to have Globus Connect and funcX endpoints deployed. 

When experimenting, you may instead want to use a PC or laptop, in which case you will need to install the Globus Connect and funcX agent software on that machine, which will have the following software installed:

1. Install some basic software on your computer
  * XX
  * XX
1. Install Globus Connect Personal 
1. Install funcX 

* Preferably Linux (Ubuntu works best)
* [Anaconda](https://www.anaconda.com/products/distribution#Downloads)
* [Globus Connnect Personal](https://docs.globus.org/how-to/globus-connect-personal-linux/)

You will also want 

A FuncX endpoint is a long-lived Python process for queuing and running work on your compute machine. It can be installed from PyPi under the name `funcx-endpoint`.

**Note**: There are currently issues using Macs as FuncX Endpoints when using Python 3.8 or later. We highly recommend using Linux instead.

```bash

# Install the necessary components
conda create -n gladier_demo_remote python=3.9
conda activate gladier_demo_remote
pip install funcx-endpoint


# Set up your FuncX "compute" endpoint
# Use the generated UUID for "funcx_endpoint_compute" states
funcx-endpoint configure compute
funcx-endpoint start compute
```

Ensure you have a Globus Collection UUID and that your funcX endpoint is set up. For example:

```
funcx-endpoint list
+----------------+--------------+--------------------------------------+
| Endpoint Name  |    Status    |             Endpoint ID              |
+================+==============+======================================+
+----------------+--------------+--------------------------------------+
| compute        | Running      | abcdefgh-0454-4af1-97ec-012771c869f9 |
+----------------+--------------+--------------------------------------+
```


## Configuring the Gladier client application

Before running each application, you will need to configure its Gladier script with identifiers for the three endpoints just listed.


Gladier is used for registering FuncX functions and deploying flows. Below are steps to
set up funcX endpoints and a Globus Collection. After this, running the test client below
will be possible. The test client, unlike the scientific tools, requires no additional external dependencies.

You will need to edit the `test_client.py` script to include your
FuncX endpoints, along with a Globus Collection. Note: Your
FuncX endpoints _must_ have access to the Globus Collection that you use.

You may install these in a separate Python environment or on a separate machine
if you wish:

```
pip install gladier gladier-tools
```

Test your basic setup by running the test_client.py:

```bash

python test_client.py
```

Running the test client will prompt you to login and will direct you to the running flow in the Globus Web app. Ensure that you see output similar to the following:

```
python test_client.py
Run started, you can also track the progress at:
https://app.globus.org/runs/1742ee41-3e14-4e5e-a191-149857f2ccea
[ACTIVE]: The Flow is starting execution
[ACTIVE]: State TransferFromStorage of type Action started
...
[ACTIVE]: State ShellCmd of type Action started
...
The flow completed with the status: SUCCEEDED
Output: [0, 'Success! You environment has been setup correctly!\n', '']
```

Now you're ready to run the other science flows.

## Ptychography

The ptychography flow uses a shell command tool to execute the `ptychodus` tool on the example data.

Refer to the python environment used for your FuncX Endpoint above:

```
| compute        | Running      | abcdefgh-0454-4af1-97ec-012771c869f9 |
```

Your compute endpoint will require the following dependencies:

```
#Ptycho tools
git clone https://github.com/AdvancedPhotonSource/ptychodus
cd ptychodus
conda install -c conda-forge --file requirements-dev.txt
conda install -c conda-forge tike
pip install -e . 
```

Before you run `ptychodus_client.py`, remember to restart your FuncX compute endpoint and set
the values in the script below.

```bash

python ptychodus_client.py --datadir <data path>
```

## XPCS flow

The XPCS flow uses the boost_corr Python SDK for execution, and requires the following dependencies
for its compute endpoint:

```bash
#XPCS flow
conda install -c nvidia cudatoolkit
conda install -c pytorch pytorch
pip install -e git+https://github.com/AZjk/boost_corr#egg=boost_corr
```


Remember to restart your compute endpoint and add the values to the `xpcs_client.py` script.

```bash

python xpcs_client.py --datadir <data path>
```
