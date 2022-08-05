# Gladier Application Examples

The paper **Linking Scientific Instruments and Computation** describes five example Gladier applications. We provide code pointers and information on how to run simple versions of each application at the following links:

* [XPCS](https://github.com/globus-gladier/gladier-patterns-examples-2022/blob/main/xpcs_client.py): X-ray Photon Correlation Spectroscopy application.
* [SSX](https://github.com/globus-gladier/gladier-patterns-examples-2022/blob/main/ssx_client.py): Serial Synchrotron Crystallography application 
* [HEDM](): High-energy Diffraction Microscopy
* [BRAGGNN](https://github.com/globus-gladier/gladier-patterns-examples-2022/blob/main/braggnn_client.py): Bragg
* [PTYCHOGRAPHY](https://github.com/globus-gladier/gladier-patterns-examples-2022/blob/main/ptychodus_client.py): Ptychography application.

We also provide below information on how to set up to run these applications.


## The common pattern implemented by all five applications

Although each of the five applications has its own particular set of tools, they all implement a common pattern, shown in the following figure, in which the a Gladier application (the **client**), running somewhere, makes a `Transfer` request to transfer data from an **instrument computer** to an **analysis computer** and then makes one or more `Compute` requests to the analysis computer to manipulate the data. Note the Globus collections (Globus terminology for a storage endpoint) on the analysis and instrument computers and the funcX endpoint on the analysis computer.

<img src=Fig4Web.jpg width=800>

Of course, many Gladier applications (including the production applications described in the paper) are more complex than that, but this pattern captures important concepts.

We describe in the following how to realize the common pattern using your own computer as the analysis computer.

### Synopsis of the infrastructure services needed to realize the common pattern

The common pattern requires that three distinct endpoints be running:

* On the **instrument computer**, a first Globus collection, which we refer to here as *instrument-transfer*, so that files can be transferred *from* the instrument.
* On the **analysis computer**, a second Globus collection (*analysis-transfer*), so that files can be transferred *to* the analysis computer.
* Also on the  **analysis computer**, a funcX endpoint (*analysis-compute*), so that tasks can be sent to the analysis computer for execution. 

The client application is configured with the addresses of these three endpoints, as we describe below.

### Configuring the instrument computer

In a real deployment, the *instrument-transfer* Globus collection will typically be a Globus Connect Server instance running on a storage system at the instrument where data are being produced.

To facilitate experimentation, we make test data available for the XPCS, SSX, BraggNN, and Ptychography applications at this [Globus collection](https://app.globus.org/file-manager?origin_id=a17d7fac-ce06-4ede-8318-ad8dc98edd69&origin_path=%2F~%2F). Thus there is nothing for you to do to configure the instrument computer for those applications.


### Configuring the analysis computer 

In a real deployment, the **analysis computer** will typically be a high-performance computing (HPC) system that is likely to have Globus collection(s) and funcX endpoint(s) deployed. 

When experimenting, you may instead want to use a PC or laptop, in which case you will need to install the Globus Connect Personel and funcX endpoint software on that machine.

**Note**: There are currently issues using Macs as FuncX endpoints when using Python 3.8 or later. We recommend using Linux instead.

1. Install some basic software on your computer
  * Install [Anaconda](https://www.anaconda.com/products/distribution#Downloads), which we will use to install other software.
2. Install Globus Connect Personal 
  * To retrieve example datasets you will need a Globus collection on your **analyis computer**: see [how to deploy Globus Connnect Personal](https://docs.globus.org/how-to/globus-connect-personal-linux/).
3. Install funcX endpoint software
  * A FuncX endpoint is a long-lived Python process for queuing and running work on your compute machine. It can be installed from PyPi under the name `funcx-endpoint`. Once installed, an endpoint can be deployed using the following commands.

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


## Configuring the Gladier client applications

Before running each application, you will need to configure its Gladier script with identifiers for the three endpoints just listed.

The test client, unlike the scientific tools, requires no additional external dependencies.
You will need to edit the `test_client.py` script to include your
FuncX endpoints, along with a Globus collection. 

You may install and run the Gladier scripts in a separate Python environment or on a separate machine
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

### Ptychography

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
the values in the script.

```bash

python ptychodus_client.py --datadir <data path>
```

### XPCS flow

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


### SSX flow

The SSX flow uses the [DIALS Package][https://dials.github.io/], and requires the following dependencies
for its compute endpoint:

```bash

#SSX flow
git clone https://github.com/dials/dials
python installer/bootstrap.py --conda
```

Remember to restart your compute endpoint and add the values to the `ssx_client.py` script.

```bash

python ssx_client.py --datadir <data path>
```

For more information on how to install DIALS please visit [dials.github.io](dials.github.io)


### BraggNN flow

The BraggNN flow uses pyTorch for training the network, and requires the following dependencies
for its compute endpoint:

```bash
#BRAGGNN flow
conda install -c nvidia cudatoolkit
conda install -c pytorch pytorch
git clone https://github.com/lzhengchun/BraggNN.git
```

Remember to restart your compute endpoint and add the values to the `braggnn_client.py` script.

```bash

python bragnn_client.py --datadir <data path>
```

## Production Workflows

The simplfied examples described above are intended to be an introduction to the production clients.
In particular, they not publish the results into a Globus catalog, and do not have an associated portal.

Globus-Search and portals can be studied by following the tutorials. A good video tutorial can be found [here](https://www.youtube.com/watch?v=IEQtI8VVT3s&ab_channel=Globus)
