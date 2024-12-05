### Update system software
```sudo apt-get update -y && sudo apt-get upgrade -y```

### Clone the repository
```git clone https://github.com/Re-Bottle/bottle-collection-system-desktop-application.git```

### Change directory into the folder
```cd bottle-collection-system-desktop-application```

### install the dependencies
```pip install -r requirements.txt```

### Start the application
```python main.py```

## Troubleshooting
### Install Picamera2 if it is not installed
```sudo apt install -y python3-libcamera python3-kms++ libcap-dev```  
```sudo apt install -y python3-prctl libatlas-base-dev ffmpeg python3-pip```  
```sudo apt install -y python3-pyqt5 python3-opengl```  # only if you want GUI features  
```pip install numpy --upgrade```  
```sudo apt install -y python3-picamera2```  


```pip install picamera2```