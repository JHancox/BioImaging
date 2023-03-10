# BioImaging
Whole Slide Imaging with RAPIDS

Prerequisites:
See on ngc.nvidia.com/catalog/containers/nvidia:rapidsai:rapidsai for details

* Notebook_1.ipynb - the first notebook to run uses cuCim to load the patient_100_node_0.tif
* Notebook_2.ipynb - the second notebook, which uses dask to load foreground tiles and run them through an autoencoder
* Notebook_3.ipynb - final notebook to build and visualize a graph from the embeddings generated
* docker_build - folder containing a docker container build script
  * Dockerfile - file used to build a local Docker container that has all the dependencies needed

Steps to run the pipeline:

Launch a terminal in the root of the repo folder
 
Copy the following files into the data subfolder
* M2_WEIGHTS.PT - model weights for the VAE. Provided so that training it is optional 
https://drive.google.com/file/d/1OJzBs5nCnMtvtnFp9EAt345dF8DfTl7L/view?usp=sharing
* patient_100_node_0.tif - WSI from the Camelyon 16 dataset
https://drive.google.com/file/d/10IUHPUPlU4FcKLU9pUO9UEdTG30zigk0/view?usp=sharing
* wsi_dfx - a dataframe containing tile features.
https://drive.google.com/file/d/1ILpogNHhWjraYAZMalAx11MXy5D8h7W7/view?usp=sharing

`cd docker_build`

`docker build -f Docker_Build -t dli/gtc23:v1 .`
 
You can then run the container that this builds after returning to the root folder:

`cd ..`

`docker run –gpus all –rm -it –ipc=host -p 8808:8888 -v [absolute path to current folder]:notebooks dli/gtc23:v1`

The host folder should appear as 'notebooks' in the container, which means you can load and save things easily from the container.
create a symlink: 

`ln -s /notebooks notebooks`

This should make the folder appear in Jupyter

Once this is done, you should be able to simply browse to the jupyter lab using localhost:8808/lab
