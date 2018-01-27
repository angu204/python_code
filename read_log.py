import xml.etree.ElementTree as ET
import subprocess
import os
import time
svnPath = "/opt/cproject/techoism"
fileName = "/opt/svnlog/log.log"
errLog  = "/opt/svnlog/err.log"
b_version = 0
e_version = 0
init = 0
def check_syn(): 
	status = 0
        #要读取的SVN日志的文件名
	sql_command = "mysql -uroot -proot -Dtest <"
        #当发生语法错误使，对数据进行回滚操作，防止有锁
	sql_rollback = 'mysql -uroot -proot -Dtest -e "rollback" '
	tree = ET.parse(fileName)
	root = tree.getroot()
	for path in root.iter("path"):
		a = path.attrib.get("action")#只处理新增和修改SVN的记录
		b = path.text
		full_Name = svnPath + b
		#print(a,':',b)
		if (a == 'M' or a == 'A'):
			#os.system('more '+svnPath+""+b)
			try:
				status = os.system(sql_command+full_Name)
				if (status != 0):
					with open(errLog,'a') as f:
						f.write('error:'+  full_Name + '\n')
				else:
					with open(errLog,'a') as f:
						f.write('success:'+  full_Name + '\n')
					#print(sql_command + full_Name)
			except(e):
				with open(errLog,'a') as f:
					f.write(e)
				#print("self_erro: " + e)
			finally:
				os.system(sql_rollback)
		else:
			pass
def  get_max_reversion():
	command = "svn info | grep 'Revision' | awk '{print $2}'"
	os.chdir(svnPath)
	result = subprocess.check_output(command,shell=True);
	result = int(str(result,'utf-8'))
	#print(result + 1)
	return result
#check_syn()
#max_version = get_max_reversion()
def create_log():
	global b_version
	global e_version
	log_command = "svn log -v --xml -r"
	os.chdir(svnPath)
	e_version = get_max_reversion()
	#print(log_command+str(b_version)+":"+str(e_version));
	os.system(log_command+str(b_version)+":"+str(e_version) + ">" + fileName)

#create_log()
def main():
	global init
	global b_version
	global e_version
	while(True):
		time.sleep(2)
		create_log()
		print("b_verion:" + str(b_version) + " e_version:" + str(e_version))
		if (init == 0 or b_version != e_version):
			check_syn()  
			b_version = e_version
			init = 1
if __name__=="__main__":
   b_version = get_max_reversion()
   main()
