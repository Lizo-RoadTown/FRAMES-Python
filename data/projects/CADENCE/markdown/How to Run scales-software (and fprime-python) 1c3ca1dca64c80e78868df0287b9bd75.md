# How to Run scales-software (and fprime-python)

happy fsw-ing! - alex 🎉🛰️

Make sure you have at least Python 3.8. Python 3.11 has worked best for me

You can check which versions of python you have

```bash
$ which python
/usr/bin/python

$ ls /usr/bin | grep python
python
python2
python2.7
python2.7-config
python2-config
python3
python3.11
python3.11-config
python3.13
python3.13-config
python3.13-nogil
python3.13-nogil-config
python3.13t
python3.13t-config
python3.8
python3.8-config
python3-config
python-config
```

To install python, it should look something similar to this

```bash
sudo apt-get install python3.11 python3.11-venv python3.11-dev
```

Clone the repository

```bash
git clone git@github.com:BroncoSpace-Lab/scales-software.git
cd scales-software
git checkout lex-ari-ML-Component
git submodule init && git submodule update
```

Create a fprime-venv for development

```bash
python3.11 -m venv fprime-venv
source fprime-venv
pip install -r fprime/requirements.txt
```

Additionally, if you want to run ML models, make sure you install these requirements:

```bash
pip install torch transformers datasets pillow
```

If you would like to utilize your nvidia GPU for ML processing, make sure you install Cuda.

I recommend CUDA 12.6 https://developer.nvidia.com/cuda-12-6-0-download-archive

And follow the pytorch documentation for this installation https://pytorch.org/get-started/locally/

Make sure to go into fprime-python and init the pybind11 submodule

```bash
## from ~/scales-software
cd fprime-python
git submodule init && git submodule update
```

IMPORTANT FIX:

the fprime-python library does not yet correctly establish itself within the Fprime cmake system. Running fprime-util generate will break, and you’d likely get an error along the lines of

```bash
	CMake Error at Components/PythonComponent/CMakeLists.txt:39
  (register_python_component):

    Unknown CMake command "register_python_component".
```

To fix this, open fprime/cmake/API.cmake and comment out this “if” loop check

![image.png](image%20377.png)

if you already fprime-util generate, make sure you purge before you try again!

```bash
# in ~/scales-software
fprime-util purge
fprime-util generate && fprime-util build -j20
```

# TROUBLESHOOTING

If you get an error along the lines of

```bash
import <Python.h>
no such file or directory
```

make sure you install these dependencies:

```bash
sudo apt-get install python3.11-dev
```

# Running the flight software:

I made a “hacky” bash script that should copy over python files into a new build-python-fprime directory, which would host your python interpreter calls.

```bash
# in ~/scales-software
fprime-util generate
fprime-util build -j20
./fsw.sh
```

To run the flight software, initialize a python interpreter and import the software binary shared object.

```bash
# in ~/scales-software
cd build-python-fprime
python
```

```python
import python_extension
python_extension.main()
```

To run GDS, make sure you source the dev environment and run these following commands in a NEW terminal

```bash
# in ~/scales-software
source fprime-venv/bin/activate
fprime-gds -n --dictionary build-artifacts/Linux/TestDeployment/dict/TestDeploymentTopologyDictionary.json --ip-client
```

Please note: You will NOT see a constant green circle in the GDS. This is expected behavior.

There are several commands:

**TestDeployment.mLManager.SET_ML_PATH:** Sets the model to inference / train with

**TestDeployment.mLManager.SET_INFERENCE_PATH:** Sets the path of files / imagery in which the selected ML model will inference on.

**TestDeployment.mLManager.CLEAR_INFERENCE_PATH**: Clears the path set by …SET_INFERNECE_PATH (this will work for resnet_cifar100)

**TestDeployment.mLManager.MULTI_INFERENCE:** This will run the main function of the model, and will inference either on its own dataset (resnet_cifar100) or on a path specified (resnet_inference).

To run an inference on the test-imagery folder:

Send a command **TestDeployment.mLManager.SET_ML_PATH** with arguments **resnet_inference**

Send a command **TestDeployment.mLManager.SET_INFERENCE_PATH** with argument **../test-imagery**

Verify in the “events” tab that these commands completed successfully.

![image.png](image%20378.png)

Finally, send a command

**TestDeployment.mLManager.MULTI_INFERNECE**

Wait a little bit for the ML model to finish its inferences. The output should look something similar to this

![image.png](image%20379.png)

🎉 Congratulations 🎉

You have just ran machine learning models in Fprime, utilizing a special experimental utility called fprime-python!

# Additional Tests:

Clear the inference path by sending a CLEAR_INFERENCE_PATH command, and then set the ML model to resnet_cifar100. Send a command to MULTI_INFERENCE and check the output on the **terminal** where the FSW is hosted.

![image.png](image%20380.png)