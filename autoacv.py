# -*- coding: utf-8 -*-
import subprocess
import time
import os
import signal
import csv
import re
import msvcrt
import sys
import datetime

def start_frida_server():
    
    cmd = ['adb', 'shell', 'su', '0', './data/local/tmp/frida-server-16.2.1-android-x86_64', '&']
    
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    cmd = ['adb', 'shell', 'su', '0', './data/local/tmp/gdbserver', '-l', '0.0.0.0:13099', '&']
    
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    cmd = ['adb', 'shell', 'su', '0', './data/local/tmp/jdb', '-l', '0.0.0.0:13100', '&']
    
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    
def execute_adb_command_vol_down():
    for _ in range(30):
        os.system("adb shell input keyevent 25")
    
def execute_command_instrument(command):
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode('utf-8', errors='replace')
    except subprocess.CalledProcessError as e:
        print("An error occurred:", e)
        return False

def extract_total_percentage(html_file):
    with open(html_file, 'rU') as file:
        html_content = file.read()
    
    pattern = r'<tfoot>\s*<tr>\s*<td>Total</td>\s*<td>\d+ of \d+</td>\s*<td>([0-9.]+%)</td>'
    match = re.search(pattern, html_content)
    
    if match:
        percentage = match.group(1)
        return percentage
    
    return None


def execute_acv_instrument(apk_file):
    command = 'acv instrument {}'.format(apk_file)
    output,err,_ = execute_command(command)
    if "Error: Unable to open" in output or "Error: Unable to open" in err:
        return False
    
    
    
    if output:
        lines = output.split('\n')
        pickle_file = None
        apk_instrumented = None
        package_name = None
        
        for line in lines:
            if line.startswith('pickle file saved:'):
                pickle_file = line.split(': ')[1].strip()
            elif line == 'apk instrumented':
                apk_instrumented = True
            elif line.startswith('apk instrumented:'):
                apk_instrumented = line.split(': ')[1].strip()
            elif line.startswith('package name:'):
                package_name = line.split(': ')[1].strip()
        
        if pickle_file and apk_instrumented and package_name:
            return pickle_file, apk_instrumented, package_name
        else:
            
            output,_,_ = execute_command(command)
            if output:
                lines = output.split('\n')
                for line in lines:
                    if line.startswith('pickle file saved:'):
                        pickle_file = line.split(': ')[1].strip()
                    elif line == 'apk instrumented':
                        apk_instrumented = True
                    elif line.startswith('apk instrumented:'):
                        apk_instrumented = line.split(': ')[1].strip()
                    elif line.startswith('package name:'):
                        package_name = line.split(': ')[1].strip()
                
                if pickle_file and apk_instrumented and package_name:
                    return pickle_file, apk_instrumented, package_name
    
    return False



def acv_install_apk(package_name, apk_file):
    if not os.path.exists(apk_file):
        print "Error: APK file %s not found." % apk_file
        return
    apk_name = os.path.basename(apk_file)
    cmd = "adb shell pm list packages | findstr %s" % package_name
    
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()    
    
    if package_name.encode() in stdout:
        print "INFO: Package %s already exists on device." % package_name
        return
    cmd = "acv install %s" % apk_file
    
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    print("stdout:", stdout.decode('utf-8', errors='replace'))
    print("stderr:", stderr.decode('utf-8', errors='replace'))
    if "device offline" in stderr:
        print("apk_file",apk_file)
        sys.exit()
    if "Failed to extract native libraries" in stderr:
        raise Exception("Dynamic analysis failure")


def execute_command(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    print("output:", output.decode('utf-8', errors='replace'))
    print("error:", error.decode('utf-8', errors='replace'))
    if "device offline" in error or "adb.exe: no devices" in error:
        print("cmd",cmd)
        sys.exit()
    return output.decode('utf-8', errors='replace'), error.decode('utf-8', errors='replace'), process.returncode




def acv_uninstall_apk(package_name):
    cmd = "adb shell pm list packages | findstr {}".format(package_name)
    
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    print("stdout:", stdout.decode('utf-8', errors='replace'))
    print("stderr:", stderr.decode('utf-8', errors='replace'))
    

   
    if package_name.encode() not in stdout:
        return

    cmd = "acv uninstall {}".format(package_name)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    print("stdout:", stdout.decode('utf-8', errors='replace'))
    print("stderr:", stderr.decode('utf-8', errors='replace'))
    if "device offline" in stderr:
        print("package_name",package_name)
        sys.exit()

    if "Success" not in stdout:
        print("Error: Failed to uninstall package {}.\nPlease uninstall {} yourself later".format(package_name, package_name))
        print(stderr)
        return

    print("Package {} uninstalled successfully.".format(package_name))


def acv_runtime_analysis(package_name, pickle_file):

    cmd0 = "adb shell am force-stop " + package_name
    output, err, _ = execute_command(cmd0)
    
    
    
    
    cmd1 = "start /B acv start "+ package_name +" > output.txt 2>&1"
    print "cmd1, ",cmd1
    process1 = subprocess.Popen(cmd1, shell=True)
    process1.wait()  
    i = 0
    while True:
        
        if process1.poll() is None:
            time.sleep(2)  
            continue
        
        with open('output.txt', 'rU') as file:
            try:
               
                
                output = file.read()
                if 'INSTRUMENTATION_CODE: 0' in output or "Lock file exists for some reason" in output:
                    
                    process1.terminate()
                    process1 = subprocess.Popen(cmd1, shell=True)
                    process1.wait()  
                    print("Attempt to reanalyze")
                    i = i+1
                    
                    if i > 3 :
                        return "False"
                    print("i =", i)
                    continue
                

                break
            except Exception as e:
                print("An error occurred:", e)
                
                continue
                
                
        
        
 

    time.sleep(2)
    
    #cmd0 = "adb shell am force-stop com.rngamingstudio.icecream.sundae.maker"
    #output, _, _ = execute_command(cmd0)
    
    
    cmd2 = 'adb shell monkey -p '+ package_name +' --throttle 500 --pct-touch 80 --pct-motion 20  --pct-appswitch 0 -v 500'
    print "cmd2 ",cmd2
    output, std, err= execute_command(cmd2)
    #process2 = subprocess.Popen(cmd2, shell=True)
    #process2.wait()
    #print "err ",err
    #print "output ",output
    #print "std ",std
    if not err:
        time.sleep(300)
    else:
        time.sleep(5)
    
 

    print("Get analysis report")
    cmd3 = "acv report "+ package_name +" -p  "+pickle_file
    
    output, err, returncode= execute_command(cmd3)
    if "No such file or directory" in err:
        raise Exception("Dynamic analysis failure")
    

    if err != 1:
        print "output ",output

    if err == 1:
        return "False"
    
    
    
def write_to_csv(filename, sha256, column, value):
    with open(filename, 'rb') as file:  # 'rb' for reading in binary mode
        csv_reader = csv.reader(file)
        csv_data = list(csv_reader)
        
        
        for row in csv_data:
            if row[0] == sha256.upper():
                row[column] = value
                break

    with open(filename, 'wb') as file:  # 'wb' for writing in binary mode
        writer = csv.writer(file)
        writer.writerows(csv_data)

def clean_repDirectory(target_directory):
    for file_name in os.listdir(target_directory):
        if file_name.endswith('.apk') or file_name.endswith('.idsig'):
            file_path = os.path.join(target_directory, file_name)
            os.remove(file_path)


if __name__ == '__main__':
    
    target_directory = '0424'
    #target_directory = 'test'
    reportPath = "C:\\Users\\dfpp125\\acvtool\\acvtool_working_dir\\report\\"
    apk_files = [file for file in os.listdir(target_directory) if file.endswith('.apk')]
    start_time = time.time()
    num = len(apk_files)
    i = 0
    Falsenum = 0
    package_name = ""
    start_frida_server()
    

    
    for apk_file in apk_files:
        
        i = i +1
        print "A total of "+ str(num) +" apk tapes are analyzed, and " + str(i) + " is in progress......"
        print('Processing:', apk_file)
        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        print(current_time_str)
        apk_file_no_suffix = apk_file[:-4]  
        
        isDo = True
        
        try:
            with open("failInstrumentApk.csv", "rU") as file:
                reader = csv.reader(file)
                for row in reader:
                    if not row:
                        
                        continue
                    if row[0] == apk_file_no_suffix:
                        count = int(row[1])
                        if count >= 2:
                            Falsenum = Falsenum +1
                            isDo = False
                            print('InstrumentFailCount:', count)
                          
                            break
                    
            if not isDo:
                continue
            
            with open("failRuntimeApk.csv", "rU") as file:
                reader = csv.reader(file)
                for row in reader:
                    if not row:
                        continue
                    if row[0] == apk_file_no_suffix:
                        count = int(row[1])
                        if count >= 2:
                            Falsenum = Falsenum +1
                            isDo = False
                            print('RuntimeFailCount:', count)
                           
                            break
                    
            if not isDo:
                continue
            
            with open("0424.csv", "rU") as file:
                reader = csv.reader(file)
                for row in reader:
                    if not row:
                       
                        continue
                    if row[0] == apk_file_no_suffix and row[14]:
                        
                        isDo = False
                        #print('row[8]', row[8])
                        break
            
            if not isDo:
                continue
            result = execute_acv_instrument(target_directory+"/"+apk_file)

            if result:
                pickle_file, apk_instrumented, package_name = result
                print('pickle file saved:', pickle_file)
                #print pickle_file == "/home/suodewen/acvtool/acvtool_working_dir/metadata/0A59F7A87BEDFB59EC8BB3C42884A3FC453430FB0666DFEA8BFDE2EA543D3ED4.pickle"  #OK
                print('apk instrumented:', apk_instrumented)
                #print apk_instrumented == "/home/suodewen/acvtool/acvtool_working_dir/instr_0A59F7A87BEDFB59EC8BB3C42884A3FC453430FB0666DFEA8BFDE2EA543D3ED4.apk"   #OK
                print('package name:', package_name)
                #print package_name == u'com.rngamingstudio.icecream.sundae.maker'   #OK
            else:
                print "Instrumentation failed. This apk will be skipped"
                clean_repDirectory("C:\\Users\\dfpp125\\acvtool\\acvtool_working_dir")
                Falsenum = Falsenum +1
               
                found = False
                with open('failInstrumentApk.csv', 'rb') as file:
                    reader = csv.reader(file)
                    content = list(reader)
                    

                    for row in content:
                        if len(row) > 0 and row[0] == apk_file_no_suffix:
                            found = True
                            row[1] = str(int(row[1])+1)
                            break

                if not found:
                    content.append([apk_file_no_suffix, "1"])

                with open('failInstrumentApk.csv', 'wb') as file:  
                    writer = csv.writer(file)
                    writer.writerows(content)

                continue

            
            acv_install_apk(package_name, apk_instrumented)

            time.sleep(2)
            #package_name = u'com.rngamingstudio.icecream.sundae.maker' 
            #pickle_file = "/home/suodewen/acvtool/acvtool_working_dir/metadata/0A59F7A87BEDFB59EC8BB3C42884A3FC453430FB0666DFEA8BFDE2EA543D3ED4.pickle"

            
            result = acv_runtime_analysis(package_name, pickle_file)
            filename = "0424.csv"
            sha256 = apk_file.rsplit('.', 1)[0]

            #print "result ", result
            if result == "False":
                Falsenum = Falsenum +1
                time.sleep(2)
                try:
                    
                    #write_to_csv(filename,sha256,8,"false")
                    acv_uninstall_apk(package_name)
                except Exception as e:
                    
                    print("An error occurred:", e)
                    

            time.sleep(2)
            
            if result != "False":
                try:
                    print("Fill code coverage")
                    
                   
                    print("Fill code coverage11111")
                    curReportPath = reportPath + package_name + "\\report\\index.html"
                    print("Fill code coverage22222")
                    per = extract_total_percentage(curReportPath)
                    print("percentage",per)
                    write_to_csv(filename,sha256,14,per)
                    #write_to_csv(filename,sha256,8,"true")
                    acv_uninstall_apk(package_name)
                
                except Exception as e:
                    
                    print("An error occurred:", e)
            print("Clean up temporary files")
            clean_repDirectory("C:\\Users\\dfpp125\\acvtool\\acvtool_working_dir")
            if i%5==0 :
                os.system("adb emu avd snapshot load  snap_2024-04-25_23-55-20")
                time.sleep(180)
                start_frida_server()
            if i%10==0 :
                os.system("adb shell reboot")
                time.sleep(180)
                start_frida_server()
            


        except Exception as e:
            
            print('An error occurred:', e)
            found = False
            with open('failRuntimeApk.csv', 'rb') as file:  
                reader = csv.reader(file)
                content = list(reader)
                

                for row in content:
                    if len(row) > 0 and row[0] == apk_file_no_suffix:
                        found = True
                        row[1] = str(int(row[1])+1)
                        break

            if not found:
                content.append([apk_file_no_suffix, "1"])
                
            acv_uninstall_apk(package_name)
            Falsenum = Falsenum +1
            time.sleep(10)
            if "device offline" in e or "adb.exe: no devices" in e:
                print("apk_file",apk_file)
                current_time = datetime.datetime.now()
                current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
                print(current_time_str)
                sys.exit()
            continue
    
    print str(num - Falsenum)+ " APKs were successfully analyzed and "+str(Falsenum)+" failed"
    end_time = time.time()

    
    execution_time = end_time - start_time

    
    print("Execution time: {} seconds".format(execution_time))

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
