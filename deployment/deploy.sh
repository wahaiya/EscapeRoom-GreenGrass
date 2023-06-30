sudo /greengrass/v2/bin/greengrass-cli deployment create \
  --recipeDir recipes \
  --artifactDir artifacts \
  --merge "com.escape.switch=1.0.0"


sudo tail -f /greengrass/v2/logs/greengrass.log 
sudo tail -f /greengrass/v2/logs/com.escape.switch.log


sudo /greengrass/v2/bin/greengrass-cli deployment create --remove="com.escape.switch"



sudo /greengrass/v2/bin/greengrass-cli deployment create \
  --recipeDir recipes \
  --artifactDir artifacts \
  --merge "com.escape.relay=1.0.0"


sudo tail -f /greengrass/v2/logs/greengrass.log 
sudo tail -f /greengrass/v2/logs/com.escape.relay.log


sudo /greengrass/v2/bin/greengrass-cli component restart  --names com.escape.relay 



sudo /greengrass/v2/bin/greengrass-cli deployment create --remove="com.escape.relay"




sudo /greengrass/v2/bin/greengrass-cli deployment create \
  --recipeDir recipes \
  --artifactDir artifacts \
  --merge "com.escape.camera=1.0.0"


sudo tail -f /greengrass/v2/logs/greengrass.log 
sudo tail -f /greengrass/v2/logs/com.escape.camera.log

sudo /greengrass/v2/bin/greengrass-cli component restart  --names com.escape.camera 


sudo /greengrass/v2/bin/greengrass-cli deployment create --remove="com.escape.camera"


usb 摄像头权限的设置 

sudo gpasswd --add ggc_user dialout

# 查看摄像头0设备信息
udevadm info /dev/video0
# 查看摄像头0设备信息
udevadm info /dev/video0
# 设定udev规则
sudo vim /etc/udev/rules.d/99-video.rules
# 输入下面一行后保存
SUBSYSTEMS=="video4linux", GROUP="video", MODE="0666"
# 重载udev规则
sudo udevadm control --reload
# 现在可以在普通用户模式使用usb摄像头了





sudo pip3 install rpi_ws281x
sudo apt install rpi.gpio-common
sudo adduser ggc_user dialout
sudo reboot



sudo /greengrass/v2/bin/greengrass-cli deployment create \
  --recipeDir recipes \
  --artifactDir artifacts \
  --merge "com.escape.PixelStrip=1.0.0"


sudo tail -f /greengrass/v2/logs/greengrass.log 
sudo tail -f /greengrass/v2/logs/com.escape.camera.log

sudo /greengrass/v2/bin/greengrass-cli component restart  --names com.escape.PixelStrip 


sudo /greengrass/v2/bin/greengrass-cli deployment create --remove="com.escape.PixelStrip"

