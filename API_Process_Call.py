#!/bin/usr/python
'''
#	File Name : API_Process_Call.py

#	Purpose:

#	Creation Date : 08-08-2014

#	Last Modified: Mon 11 Aug 2014 03:30:14 PM PDT


#	Created By : Ameya Sanzgiri

#	Organization : McAfee Inc.

'''
import sys, time, os, subprocess, re, csv,ConfigParser,inspect

#iFile_path = '/home/ameya/Documents/McAfee_Research/Scripts/API_call/' --This is for my santoku at home.
iFile_path = '/home/ameya/Documents/Privacy_Research/Scripts/'

#-------------------------------------------------------------------------------------------------------Constants

CON_ManifestFile = 'AndroidManifest.xml'
CON_APIFILE = '/home/ameya/Documents/Privacy_Research/Scripts/a.txt'
sharefolder = ''
zip_input = ''
unzip_output = ''
passwd=''
apkfolder = ''
decompileAPK = ''


#----------------------------------------------------------------------------------------------------------------------------------
def DEBUG1 ( String1):
	print "DEBUG INFO:" + String1

def ERROR1 (String1):
	print "ERROr: " + String1
	exit()

def exit():
	sys.exit()

def Check_Path(filepath):
	if (os.path.isdir(os.path.abspath(filepath))):
		DEBUG1( "Path is TRUE")
		return True
	else:
		DEBUG1("Path does not exist")
		return False


def Check_File(filename):
	if(os.path.isfile(filename)):
		DEBUG1( "File exists") 
		return True
	else:
		DEBUG1("File does not exist")
		return False


def FindAFile(path, name,flag):
	for root,dirs,files in os.walk(path):
		if flag == 0:
			if name in files:
				return os.path.join(root,name)
			else:
				ERROR1 ("No Manifest File Found....Call Script from correct location")
		elif flag == 1:
			if name in dirs:
				return os.path.join(root,name)
			else:
				ERROR1("Directory" +str( name) + " not found")
		else:
			ERROR1("Wrong flag can only find file (0) or directory(1)")
'''The following two modules do the string match
   AMS COmment: Python Search Match is AWESOME!!!!
'''
#-----Process Manifest for package name
def Process_Manifest_Package(ManifestFilePath):
	Man_File = open(ManifestFilePath, 'r+')
	pat = re.compile(r'.*android:installLocation=(.*).* package="(.*)".*')
	for line in Man_File:
		searchObj = re.search(pat,line)
		if searchObj:
			#TODO: Write to a file or string and keep for csv preparation
			print searchObj.group(1) #Gets the install location
			print searchObj.group(2) #gets Package name
	Man_File.close()	

#---------------Process Manifest for Permission List

def Process_Manifest_Permission(MFpath):
	MAN_PERM_STR = ""
	Man_file = open(MFpath, 'r+')
	print Man_file
	pat = re.compile(r'.*permission.*android:name="(.*)".*')
	for line in Man_file:
		searchPermObj = re.search(pat, line)
		if searchPermObj:
			print searchPermObj.group(1)
			MAN_PERM_STR = MAN_PERM_STR + searchPermObj.group(1) + '\n'
	Man_file.close()
	print MAN_PERM_STR

def Copy_API_Calls_and_Transform_to_SMALI(APICallFile):
	#To get dir, change to working dir create copy and work on the copy
	os.chdir(os.getcwd())  #change to dir of decompiled apk
	subprocess.call(['cp',APICallFile, 'copy-a.txt']) #Create a dummy file to use as input
	APIcallFileObj= open ( 'copy-a.txt','r+') 
	pat = re.compile("(.*)\((.+)\)") #we are searching for paranthesis
	APICall = open('APICall.txt','w+') 
	for line in APIcallFileObj:
		searchAPIcallObj = re.search(pat,line) 
		if searchAPIcallObj:
			APICall.write(str(searchAPIcallObj.group(1))+'\n') 
	APIcallFileObj.close() 
	subprocess.call(['rm','copy-a.txt'])
	DEBUG1("Removed shadow API calls")
	APICall.close() 
        APICall = open('APICall.txt','r') #create a file to write teh new api calls
        API_CALL_STR = APICall.read()
        #This is the sub/replace logic
        API_CALL_NEW_STR = re.sub('\.',"/",API_CALL_STR)
        APICall.close()
        APICall = open('APICall.txt','w')
        APICall.write(API_CALL_NEW_STR) #rewrite to file (we dont have to take care of the \n this way
        APICall.close() #close file.

#creating a csv file for now.
#-----------------------------------------------
def Write_CSV_File (data, path):
	with open(path,"wb") as csv_file:
		writer = csv.writer(csv_file,delimiter = ',',quoting=csv.QUOTE_ALL)
		for line in data:
			writer.writerow(line)

  

def ProcessMan():
	print str( os.getcwd() )
	if( Check_Path( os.getcwd() ) ):
		ManifestFilePath = FindAFile(os.path.abspath(os.getcwd()),CON_ManifestFile,0)
		if ( Check_File (ManifestFilePath)):
			#search for the package name
			print "Manifest File at : " + str(ManifestFilePath)
			#To get Package name and add it to the File name
			Process_Manifest_Package(ManifestFilePath) #Gets Package Name
			Process_Manifest_Permission(ManifestFilePath) #Gets Permission List
		else:
			ERROR1("File not found")
	else:
		ERROR1("Directory not found")

def ProcessAPICalls(CON_APIFILE, iFilePath):
	print str(CON_APIFILE)
	if (Check_Path(iFile_path)):
		if (Check_File(os.path.abspath(CON_APIFILE))):
			CopyTransform(os.path.abspath(CON_APIFILE))
		else:
	       		ERROR1("File not found")
	else:
		ERROR1("directory not found")

def ProcessConstants():
	configreader = ConfigParser.RawConfigParser()
	if Check_File('/home/ameya/Documents/Privacy_Research/Scripts/Config_API_call.txt'):
		configreader.read('/home/ameya/Documents/Privacy_Research/Scripts/Config_API_call.txt')
		Sharefolder = configreader.get('UNZIP','CONST_SHARE')
		if Check_Path( Sharefolder ):
			dirs = os.listdir( Sharefolder )
			print len(dirs)
			if ( len (dirs) ) != 0 :
				print len(dirs)
				zip_input = configreader.get('UNZIP','CONST_ZIP_INPUT')
				print zip_input
				unzip_output = configreader.get('UNZIP', 'CONST_OUTPUT_DIR')
				passwd = configreader.get('UNZIP', 'CONST_PASSWD')
			else:
				ERROR1("Mount ShareFolder")
			if not( Check_Path(zip_input) and Check_Path(unzip_output) ):
				ERROR1( "Check UNZIP configs")
		else:
			ERROR1( "Shrefolder does not exst")
		#This is for the renaming and decompiling
		unzip_output = configreader.get('UNZIP','CONST_OUTPUT_DIR')
		apkfolder = configreader.get('DECOMPILE', 'CONST_APK')
		print apkfolder 
		decompileAPK = configreader.get( 'DECOMPILE', 'CONST_DECOMPILE')
		if not( Check_Path(apkfolder) and Check_Path(decompileAPK) ):
			ERROR1("Issues with either APKFolder or DEcompile folder - Check if they exist")
		#This is for the rest of stuff like the grep	
		iFile_path = configreader.get( 'PROCESS', 'CON_FILEPATH')
		CON_APIFILE = configreader.get('PROCESS', 'CON_APIFILE')
		DEBUG1("ALL constants have been processed\n")
		CON_ManifestFile = configreader.get('PROCESS', 'CON_MANFILE')
		if(PerformUnzip(zip_input,unzip_output,passwd)):
			DEBUG1("Unzip worked well")
		else:
			DEBUG1("Unzip already performed\n")
		if (bin2apk(unzip_output,apkfolder)):
			DEBUG1("Bin2apk executed successfully...files have been moved and renamed\n")
		else:
			DEBUG1("Files were already moved and converted possibly")
		#Decompile
		if (decompileAPK1(apkfolder,decompileAPK) ):
			DEBUG1("decompiled successfully")
		else:
			DEBUG1("Already decompiled\n")
		if (ProcessAPICalls(CON_APIFILE , iFilePath) ):
			DEBUG1( "The File has been copied and exists in " + str(os.getcwd()) )
		else:
			DEBUG1("File has been processed\n")
		curr_dir = os.getcwd()
		decompiled_apk_folders = os.listdir(os.path.relpath (decompileAPK) )
		for decAPK in decompiled_apk_folders:
			print decAPK
		
		#Goto each folder of the decompiled files and do in the following sequence:
			#1. Call ProcessAPICalls():Copy the transformed file to the folder
			#2. Call ProcessMan():Processes Man and writes file to a folder
			#3. Call CollectAPIStat(): Runs the Grep command on each folder and stores the result in a file in the foldera
			#4. Call ConcatenateFile(): Concatenates a result of all the files into a single file
			#5. Call AnalyzeFile(): Gets the Analysis of the file.
	else:
		ERROR1( "Config file not found The folder of the script also should have the file a.txt and the config file\n")

#def getAPICall( decompileFolder):
	# First open a file to write or we can just put results into it using the '>>' command
	# For each decompiled folder grep exact API call run grep on the files
	# 

def PerformUnzip(inpDir,OutDir,Passwd):
	if (Check_Path(inpDir)):
			if (Check_Path(OutDir)):
				DEBUG1("Both directories seem to be fine")
				zipfiles = os.listdir(os.path.relpath(inpDir))
				count_zip = len(zipfiles )
				binfiles=os.listdir( OutDir ) 
				count_bin = len( binfiles )
				os.chdir(inpDir)
				if ( count_bin != count_zip ) :
					for zips in zipfiles:
						try:
							subprocess.call ( ['unzip','-o', '-P',"infected",'-d',OutDir,zips ] )
						except OSError:
							ERROR1( "Some Problem in the unzip command...check the arguments" )
					return True
				else:
					return False
			else:
				ERROR1("Output Directory does not exist")
	else:
		ERROR1(" Check where the zip files are")
		
def bin2apk(unzipDir,APKs):
	os.chdir(unzipDir)
	if( len (os.listdir( unzipDir)) !=   len (os.listdir ( APKs)) ):
		for f in os.listdir(unzipDir):
			files,ext = os.path.splitext( os.path.basename (f) )
			apk_command = APKs+files+'.apk'
			try:
				subprocess.call( [ 'mv' , f , apk_command])
			except OSError:
				Error1("Error in module ")
		return True
	else:
		return False

def decompileAPK1 ( APKs, Decompile_Folder):
	os.chdir(APKs)
	DEBUG1(str(os.getcwd()))
	if (len (os.listdir(APKs)) != len( os.listdir(Decompile_Folder))):
		for f in os.listdir(APKs):
			os.chdir( APKs)
			files,ext = os.path.splitext( os.path.basename (f) )
			apk_dec_folder = Decompile_Folder+'/'+files
			try:
				subprocess.call( [ 'apktool', '-q','d','-r', f ,apk_dec_folder])
			except OSError:
				ERROR1( "Decompile unknown for Unknnown Reasons!!!")
			if ( Check_Path (os.path.join(apk_dec_folder,'res') ) ):
					os.chdir(apk_dec_folder)
					try:
						subprocess.call( ['rm', '-rf', 'res'])
					except OSError:
						ERROR1( " Could not remove the res file")
			if ( Check_Path ( os.path.join(apk_dec_folder,'assets') )):
				os.chdir(apk_dec_folder)
				try:
					subprocess.call(['rm','-rf','assets'])
				except OSError:
					ERROR1("Failed in removing the assets folder")
			if ( Check_Path (os.path.join( apk_dec_folder, 'lib') )):
				os.chdir(apk_dec_folder)
				try:
					subprocess.call( [ 'rm' ,'-rf', 'lib' ])
				except OSError:
					ERROR1 ( "Failed to remove the lib folder")

		return True
	else:
		return False

 
#-------------------
#grep and plot files
#--------------------
''''
	-	open file first
	- 	for each line in the file
	-	grep from root directory
	-		-go to smali directory
			-print out the API calls
'''
DEBUG1(str(os.getcwd()))

'''
Main starts here
'''
ProcessConstants() #ProcessConstants calls PerformUnzip, bin2apk,decompileAPK1 and also process_things
#UnzipApk() #UnzipAPk should actually rename all the bins, move them to a separate folder and call apktool on it.
#bin2apk(unzip_output,apkfolder)
#apkdecompile(apkfolder,decompileAPK)
#ProcessMan()
#ProcessAPICalls(CON_APIFILE,iFile_path)

