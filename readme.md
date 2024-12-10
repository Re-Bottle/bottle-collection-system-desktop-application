### Update system software
```sudo apt-get update -y && sudo apt-get upgrade -y```

### Clone the repository
```git clone https://github.com/Re-Bottle/bottle-collection-system-desktop-application.git```

### Change directory into the folder
```cd bottle-collection-system-desktop-application```

#### ImageTK 
```sudo apt-get install -y python3-pil python3-pil.imagetk```

#### Keyring
```sudo apt-get install -y python3-keyring```
```sudo apt-get install -y python3-qrcode```

### Start the application
```python main.py```

## Troubleshooting
### Install Picamera2 if it is not installed
```sudo apt install -y python3-libcamera python3-kms++ libcap-dev```  
```sudo apt install -y python3-prctl libatlas-base-dev ffmpeg python3-pip```  
```sudo apt install -y python3-pyqt5 python3-opengl```  # only if you want GUI features  
```sudo apt install -y python3-numpy```  
```sudo apt install -y python3-picamera2```  
```sudo apt install -y lgpio```

#### install pigpio
```sudo spt install -y pigpio python3-pigpio``` Install pigpio
```sudo pigpiod``` Start the pigpio daemon
or
```sudo systemctl enable pigpiod``` Start the pigpio daemon everytime on boot