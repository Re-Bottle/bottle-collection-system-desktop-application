### Update system software

`sudo apt-get update -y && sudo apt-get upgrade -y`

### Clone the repository

`git clone https://github.com/Re-Bottle/bottle-collection-system-desktop-application.git`

### Change directory into the folder

`cd bottle-collection-system-desktop-application`

#### ImageTK

`sudo apt-get install -y python3-pil python3-pil.imagetk`

#### Keyring

`sudo apt-get install -y python3-keyring`
`sudo apt-get install -y python3-qrcode`

#### Pi Camera

`sudo apt install build-essential libatlas-base-dev python3-opencv `
`sudo apt install -y python3-picamera2 libcamera-apps libcamera-dev`
`pip3 install tflite-runtime --break-system-packages`

#### Running Tensorflow Model

`sudo apt install build-essential`
`sudo apt install libatlas-base-dev`
`pip3 install numpy`
`pip3 install opencv-python==4.4.0.46`
`pip3 install tflite-runtime`

### Start the application

`python main.py`

## Troubleshooting

### Install Picamera2 if it is not installed

`sudo apt install -y python3-libcamera python3-kms++ libcap-dev`  
`sudo apt install -y python3-prctl libatlas-base-dev ffmpeg python3-pip`  
`sudo apt install -y python3-pyqt5 python3-opengl` # only if you want GUI features  
`sudo apt install -y python3-numpy`  
`sudo apt install -y python3-picamera2`  
`sudo apt install -y lgpio`

#### pigpio is not supported
