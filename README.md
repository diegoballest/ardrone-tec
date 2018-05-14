# Python3 - ArDrone
## Demo
([PyARdrone + Tensorflow object recognition](https://drive.google.com/open?id=15-YeUDQg23QysssecI_6iY1-p89EAxBu))

## Ubuntu Installation guide:

Be sure to have already installed Python’s package manager
```
sudo apt install python3-pip
```

Install the following packages:
```
sudo pip3 install pyardrone
sudo pip3 install numpy
sudo pip3 install tensorflow
sudo pip3 install Cython
sudo pip3 install pillow
sudo pip3 install lxml
sudo pip3 install jupyter
sudo pip3 install matplotlib
```

Download or clone tensorflow models repository from here:
```
https://github.com/tensorflow/models
```
Extract the zip file if downloaded.

If you don’t have protobuf already installed, download the latest version for your corresponding python version from here:
```
https://github.com/google/protobuf/releases
```
Extract the zip file and go to the protobuf folder to execute the following commands:
```
sudo ./configure
sudo make check
sudo make install
```

If you get the following error:
```
"protoc: error while loading shared libraries: libprotoc.so.15: cannot open shared object file: No such file or directory"
```
Just execute the following command:
```
sudo ldconfig
```
If you already had/have profobuf then go to “tensorflow/models/research/” from the downloaded repo folder and launch the following commands:
```
protoc object_detection/protos/*.proto --python_out=.
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
```

You’re ready to start using tensorflow.
For more information:
```
https://www.tensorflow.org/install/install_linux
https://github.com/tensorflow/models/tree/master/research/object_detection
```

## How to make it work:

After correctly installing tensorflow and all the libraries, go to the object detection folder, "models-master/research/object_detection" and create your new file in this path, or simply download the code file from:
```
https://github.com/diegoballest/ardrone-tec
```
Copy the "drone.py" file to the path and run it with the following command:
```
sudo python3 drone.py
```

Make sure that your first execution is in a local wifi network, this will download the model file to make the object detection work.

After the first execution, connect to the drones network and also you can comment the following lines from the "drone.py" file:
```
opener = urllib.request.URLopener()
opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
```
This is because every time you execute the file, this tries to download the model file and takes more time to execute it.
