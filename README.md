# Computer vision system for Defect Recognition

## **General description**
Communication and image processing system for the automation of industrial processes. This application recognizes manufacturing defects automatically. The defects detected in the produced pieces can also be of small dimensions.

The images are captured by a 4K video camera placed at the end of the production so that they can be detected automatically, saving a lot of time for industrial operators.

<br>

## 🟢 droplets recognition
![](./docs/foto_54.png)

## 🟢 holes recognition
![](./docs/foto_11_2.png)

## **Software**
Learn to use OpenCV and Depthai, they are the libraries on which the application is based.
- Course **OpenCV** https://courses.opencv.org/
- **OpenCV** official documentation https://docs.opencv.org/4.5.5/
- **Depthai** Official Documentation https://docs.luxonis.com/projects/api/en/latest/

## **Object Detection**
- https://onnx.ai/

## **Hardware**
Ideal computers and processors for the project
- https://www.lattepanda.com/products

## **Build machine learning models**
Create neural network models with free online tools.
- https://teachablemachine.withgoogle.com/
- https://www.makesense.ai/



## **Application Workflow**
This Computer Vision application allows you to:

1. It communicates through the socket with the PLC microcontroller connected to a sensor which warns of the arrival of a product. A string message arrives from a PLC socket client.

2. When a message is sent from the PLC, the app activates and takes a picture of one or more cameras connected locally.

3. Process the photo to check for errors in the finished product:

      1. background removal
    
      2. the detection of contours
    
      3. the detection of errors
    
      4. classification of errors

4. report system results :
      1. Load the original image and the processed image on the frontend in the PLC panel (or in a local pop-up frame for debugging use).
      2. return a message to the PLC containing a booleno indicating the presence or absence of the error, and the type of error.



## **Installation**

1. install pip, the python package manager <br>
```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```
```python3 get-pip.py```
```rm .\get-pip.py```

2. update the pip package manager <br>
```pip install -U pip```

2. create and install the development environment with _venv_<br>
```python3 -m venv venv```

3. Activating the development environment
      (Mac OS / Linux)<br>
```source venv/bin/activate```

      (Windows) <br>
```venv\Scripts\activate```

```python -m pip install --upgrade pip```

4. Install required libraries <br>
``` pip install -r ./requirements.txt```


### **Alternate installation with Anaconda**
If you use the Anaconda environment (conda), you can also use this way to install the development environment.
1. ```conda create -n env``` <br>
2. ```conda activate env``` <br>
3. ```conda config --env --add conda-forge channels```<br>
4. ```conda install --file requirements.txt```<br>

<br>

## **Launch the application**
   The app only works with a socket that connects to the server and sends data.
   These socket messages are triggers on having to take a picture.
 
   To start the application, either the PLC socket is connected which sends messages every time a picture needs to be taken, or for debugging it is possible to launch a test socket called plc_client_test.py, where random messages will be sent every few seconds to the server . In this way it is possible to activate the artificial vision system.


### **Debug (test) mode**
In two separate terminals
```
python3 plc_test_client.py
python3 app.py
```

### **Live mode (in real)**
Activate the PLC that connects with a socket to the server (app.py) and run the following command:
```
nohup python3 app.py 1> logs.out 2> logs.err &
```


# **Tech Stack**

## **Open CV**
OpenCV (Open Source Computer Vision Library) is a library of programming functions aimed primarily at real-time computer vision. The library is cross-platform and free to use under the Apache 2 open source license. As of 2011, OpenCV offers GPU acceleration for real-time operations. OpenCV is written in C++ and its main interface is in C++, but still retains a less complete though extensive C interface. All new developments and algorithms appear in the C++ interface. There are bindings in Python, Java and MATLAB/OCTAVE. I have been
