#!/usr/bin/python
#Usage Emu_scripts <Emulator_Name> <install(i), unistall (u)> <app_to be installed>
#TODO: Have to execute the bootanim check to prevent errors caused by emulator not being up before installing the apk.
#TODO: Create a bash script that will block till the boot anim returns.

import sys,os,shutil,time
import subprocess

def installation_app(src_path, app_name,abs_abd_path,emulator_path,Emulator_Name):
	print "Installing app"+ app_name +"from path:" + src_path
	start_emulator(emulator_path, Emulator_Name,abs_abd_path)
	print "Will sleep for 30 seconds"
	time.sleep(30)
#first copy to the adb path	
	shutil.copy(os.path.join(src_path,app_name),abs_abd_path)
	if os.path.isfile(os.path.join(abs_abd_path,app_name)):
		print "Copying Successfull from path: " + os.path.join(abs_abd_path,app_name)
	else:
		print "Failure in copying...Check Permissions"
		sys.exit()
	os.chdir(abs_abd_path)
	'''install_code = subprocess.check_call(['./adb', 'install', app_name ])
	if install_code == 0:
		print "Installed " + app_name + "on Emulator"
		return None
	else:
		raise subprocess.CalledProcessError(install_code, stderr)
		sys.exit()
	'''
	#subprocess.Popen(['./adb','wait-for-device','sleep','200000000'])
#	try:
	print "Checking if boot_animation is done"
	p = subprocess.check_output(['./adb','shell','getprop','init.svc.bootanim'],shell=False,stderr=subprocess.STDOUT,universal_newlines=True)
	
#		print emu_boot_flag
#	except subprocess.CalledProcessError as e:
#		ret = e.returncode
#		print e.output 
#		print "Ret"
#	while ( emu_boot_flag.decode('ascii')!="stopped"): 
#		emu_boot_flag =	subprocess.check_output(['./adb','shell','getprop','init.svc.bootanim'],shell=False,stderr=subprocess.STDOUT)
#		print "Here currently: " + emu_boot_flag.decode('ascii') 
#		time.sleep(1)	
#	subprocess.Popen(['./adb','install',app_name])
#	print "Successful!!!"
	return None
def start_emulator(emulator_path,Emulator_Name,abs_abd_path):
	print Emulator_Name
	if  os.path.exists(emulator_path):
        	abs_emulator_path = os.path.abspath(emulator_path)
	else:
        	print "ERROR: Terminating, Cannot find Emulator--- Check path of Emulator"
        	sys.exit()
	os.chdir( abs_emulator_path)
#yy	start_emulator_code = subprocess.check_call(['./emulator','-avd', Emulator_Name ])#,shell=True)

	p = subprocess.call(['./emulator','-avd', Emulator_Name],stdout=subprocess.PIPE)
	print "checking bootanim property"
	time.sleep(15)
	os.chdir(abs_abd_path)	
	p1 = subprocess.check_output(['./adb','shell','getprop','init.svc.bootanim'],shell=False,stderr=subprocess.STDOUT)
	print p1
	
def uninstall_app(app_name, Emulator_Name, abs_abd_path,emulator_path):
	start_emulator(emulator_path,Emulator_Name,abs_abd_path)
	print "Uninstalling app" + app_name + "from Emulator" + Emulator_Name
	print"----------------Data and Cache will also be deleted----------------"

	os.chdir(abs_abd_path)
	subprocess.Popen(['./adb','uninstall',app_name])
'''	uninstall_code = subprocess.check_call(['./adb','uninstall', app_name])
	if uninstall_code == 0:
		print "Un-Installation Successful"
		return None
	else:
		print "Ooops something went wrong :("
		raise subprocess.CalledProcessError(uninstall_code,stderr)
		sys.exit()	
'''

print "This file will install the app on the emulator and run it"
emulator_path = "/usr/share/adt-bundle/sdk/tools/"
adb_tools = "/usr/share/adt-bundle/sdk/platform-tools/"
src_path =  "/home/ameya/Documents/Privacy_Research/Talking_Tom/apk/"
'''
First we check the length of the arguments. 4 means not default Emulator, else we default the emulator to 
McAfee_Emulator
'''
arg_list = len(sys.argv)
if arg_list < 3 :
	print "Incorrect number of arguments"
	sys.exit()
'''
Assigning Variables to the appropriate argument list
'''
if arg_list == 3:
#We are assuming that for arg_list ==3, user wants default Emulator
	Emulator_Name = 'McAfee_Emulator'
	flags = sys.argv[1]
	app_name = sys.argv[2]	
else:
	Emulator_Name = str(sys.argv[1])
	flags = sys.argv[2]
	app_name = sys.argv[3]
'''
Now to start the installation of the APK
'''
'''
Now to make sure app is an .apk file
'''
FileName, FileExtension = os.path.splitext(app_name)
if str(FileExtension) !=".apk":
	print "ERROR:Not an apk file....Terminating"
	sys.exit()
if os.path.exists(adb_tools):
	abs_abd_path = os.path.abspath(adb_tools)
else:
	print "ERROR:Terminating, installation not possible, check adb path"
	sys.exit()
if flags == "i" :
	if ( os.path.exists(os.path.join(src_path,app_name)) and os.path.isfile(os.path.join(src_path,app_name)) ) :
		#continue
		installation_app(src_path,app_name,abs_abd_path,emulator_path,Emulator_Name)
	else:
		print "ERROR:Terminating, cannot find the app"
		sys.exit()
elif flags =="u":
	#Uninstalling the app
	print "Uninstall Initiated"
	uninstall_app(app_name,Emulator_Name,abs_abd_path,emulator_path)
		#continue
else:
	print "ERROR:Cannot understand input argument[2], it should be \"i\"for install OR \"u\" for uninstall.....try again"
	sys.exit()

