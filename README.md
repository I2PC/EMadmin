## See Scipion Usage site
> http://calm-shelf-73264.herokuapp.com

## Activate
 Add the following two lines to Config ($HOME/.config/scipion/scipion.conf), section VARIABLES:

> SCIPION_NOTIFY = True<br>

## Shortcut to this page
 > http://tinyurl.com/scipion-readme

## Test: Query from command line:

> curl http://calm-shelf-73264.herokuapp.com/report_protocols/api/workflow/protocol/?name=ProtMonitorSystem<br>
> curl http://calm-shelf-73264.herokuapp.com/report_protocols/api/workflow/workflow/?project_uuid=b9a2d873-53d2-42fb-aa69-a5002f2f08e9

##Admin interface (requires password)

> http://calm-shelf-73264.herokuapp.com/admin/

## Details of usage data collection
You can find them here https://github.com/I2PC/scipion/wiki/Collecting-Usage-Statistics-for-Scipion

--

## Testing EMadmin in Éinstein
- open a vnc conection with Einstein
     - connect to Einstein using ssh as scipionuser
     - start the server:    killall Xvnc4; rm -rf /tmp/.X*-lock; vncserver -geometry 1280x960
- in your computer opena vnc client; vncviewer einstein:PORTNUMBER (portnumber usually 1)
- cd /home/scipionuser/webservices/EMadmin/src
- Start a virtual environment: source ../virEMadmin/bin/activate
- launch django server: python manage.py runserver
- open browser and connect to server at URL http://127.0.0.1:8000
- create new project and lunch scipion
- execute scipion protocols
- check html report
