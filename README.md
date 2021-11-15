Pi-Top DS

Based on the work of others.  Seriously, I borrowed most of this.

The robot.service needs to be installed via systemctl/systemd. The file should end up in /etc/systemd/system/robot.service.

The OLED stuff for the pitop needs editing.  I commented out a lot of the menu items because I didn't need them.

The PageManager.py file needs to be placed into: /usr/lib/pt-sys-oled/components/

The ment_page_actions.py file needs to be placed into: /usr/lib/pt-sys-oled/components/helpers/

The robot.png file needs to be placed into: /usr/share/pt-sys-oled/images/settings/status_icons/

The sys_info.py file needs to go into /usr/lib/python3/dist-packages/pitopcommon/ to add the robot service bits

That should be all that is required outside of setting up the udev rules for the USB to the RoboRIO/RoboRIIO.

I've probably forgotten something so let me know if you try it.

YouTube Demo Video here: https://youtu.be/Dxmqwbp8v48
