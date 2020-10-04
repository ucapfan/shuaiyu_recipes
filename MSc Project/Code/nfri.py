import time,json,random,os,requests
from selenium import webdriver
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

def do_search(search_one):
	'''
	进行搜索，并返回driver
	'''
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--headless')
	driver = webdriver.Chrome(executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe',chrome_options=chrome_options)#C:/Users/kzb/Desktop/
	driver.get("https://dcpp.nfri.re.kr/index.do")
	# time.sleep(3)
	
	#清空搜索框中的内容
	driver.find_element_by_xpath("//input[@name='keyword']").clear()
	print("搜索框清空完成")
	#填入搜索内容
	driver.find_element_by_xpath("//input[@name='keyword']").send_keys(search_one)
	print("搜索内容输入完成")

	time.sleep(3)
	#点击搜索
	driver.find_element_by_xpath("//input[@class='b']").click()

	return driver

def get_id(driver):
	'''
	获取搜索内容
	'''
	id_list = []

	one = driver.find_elements_by_xpath("//a[@class='btnGetPlBiSubProc']")
	for i in one:
		id_ = i.get_attribute('id')
		print(id_)
		id_list.append(id_)

	return id_list

def get_search_value(driver):
	"""
	"""
	search_value = driver.find_element_by_xpath("//input[@id='plCpbiEleNum']").get_attribute('value')
	return search_value

def write_content(id_list,search_value,search_one):
	"""
	"""
	for id_ in id_list:
		id_ = id_.replace("btnGetPlBiSubProc","plBiDataBranch=")
		# print(str(id_))
		url_id = id_.split(":")
		# print(url_id)
		#Electron Impact类型数据不需要
		if len(url_id)==3 and url_id[2] != "IC_01":
			url = "https://dcpp.nfri.re.kr/search/list.do?plBiTopBranch=TB_01&"+url_id[0]+"&plBiMainProc="+url_id[1]+"&plCpbiEleNum="+str(search_value)+"&keyword="+search_one+"&seltab=0&plBiImpClass="+url_id[2]
			
			chrome_options = webdriver.ChromeOptions()
			chrome_options.add_argument('--headless')
			driver = webdriver.Chrome(executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe',chrome_options=chrome_options)#C:/Users/kzb/Desktop/
			driver.get(url)
			#a[@id='btnShowCheckedData']
			# time.sleep(1)
			js="var q=document.documentElement.scrollTop=100000"
			driver.execute_script(js)
			# time.sleep(1)
			driver.find_element_by_xpath("//a[@id='btnShowCheckedData']").click()

			print("点击成功")
			all_handles = driver.window_handles
			print('all_handles：', all_handles)
			# time.sleep(1)
			driver.switch_to.window(all_handles[1])
			get_content(driver,search_one)

def get_content(driver,search_one):
	"""
	"""
	Reaction_Formula = ""
	Categorize = ""
	Collision_data_categorize = ""
	Collision_process = ""
	Sub_process = ""
	Collision_type = ""
	TER = ""

	content_list = []

	tbodys_list = driver.find_elements_by_xpath("//tbody")
	fileNames = driver.find_elements_by_xpath("//p")

	for fileName,tbody in zip(fileNames,tbodys_list):
		# print(tbody.get_attribute("innerHTML"))
		trs_list = tbody.find_elements_by_xpath("tr")

		#提取第一个表单的内容
		id_number = fileName.text.split(" ")[2]
		Reaction_formula = trs_list[0].find_element_by_xpath("td").text
		Categorize = trs_list[1].find_element_by_xpath("td").text
		Collision_data_categorize = trs_list[2].find_element_by_xpath("td").text
		Collision_process = trs_list[3].find_element_by_xpath("td").text
		Sub_process = trs_list[4].find_element_by_xpath("td").text
		Collision_type = trs_list[5].find_element_by_xpath("td").text
		TER = trs_list[13].find_element_by_xpath("td").text

		fileName = fileName.text.split(" ")[2]

		# print("文件名为：",fileName)
		f = open("data/{}/{}.csv".format(search_one,fileName),"w",errors="ignore")

		#这是第一个表单的内容
		f.write("id_number,"+id_number+"\n")
		f.write("categorize,"+Categorize+"\n")
		f.write("collision_data_categorize,"+Collision_data_categorize+"\n")
		f.write("collision_process,"+Collision_process+"\n")
		f.write("sub_process,"+Sub_process+"\n")
		f.write("collision_type,"+Collision_type+"\n")
		f.write("Theory_Experiment_Recommendation,"+TER+"\n")
		f.write("reaction_formula,"+Reaction_formula+"\n")
		#这是第二个表单的内容
		get_plBiDataNum_content(f,id_number)
		f.close()


		f = open("data/{}/{}-XY-data.csv".format(search_one,fileName),"w",errors="ignore")
		f.write("X,Y\n")
		for tr_XY in trs_list[15:]:
			X = tr_XY.find_elements_by_xpath("td")[0].text
			Y = tr_XY.find_elements_by_xpath("td")[1].text
			f.write(X+","+Y+"\n")
		f.close()

	return content_list

def get_plBiDataNum_content(f,id_number):
	headers = {
				"User-Agent": str(UserAgent().random)#,
				}
	url = "https://dcpp.nfri.re.kr/search/popupViewBasic.do?plBiDataNum={}".format(id_number)
	req = requests.get(url,headers=headers)
	#校正页面编码
	req.encoding = req.apparent_encoding
	#第二步：解析网页
	soup = BeautifulSoup(req.text, 'lxml')
	Referece_Link = soup.find("span").text


	url = "https://dcpp.nfri.re.kr/search/popupViewArticle.do?plRaiArtclNum={}".format(Referece_Link)
	req = requests.get(url,headers=headers)
	#校正页面编码
	req.encoding = req.apparent_encoding
	
	#第二步：解析网页
	soup = BeautifulSoup(req.text, 'lxml')

	trs_list = soup.find_all("tr")

	author = trs_list[2].find("td").text.replace(",","###")
	title_of_record = trs_list[1].find("td").text
	journal_name = trs_list[3].find("td").text
	volume_and_issue_No = trs_list[9].find("td").text
	page_number = trs_list[11].find("td").text
	date_of_publication = trs_list[13].find("td").text

	f.write("reference_number,"+str(Referece_Link)+"\n")
	f.write("author,"+author+"\n")
	f.write("title_of_record,"+title_of_record+"\n")
	f.write("journal_name,"+journal_name+"\n")
	f.write("volume_and_issue_No,"+str(volume_and_issue_No)+"\n")
	f.write("page_number,"+str(page_number)+"\n")
	f.write("date_of_publication,"+str(date_of_publication)+"\n")

	return

def get_plBiDataNum_content_old(f,id_number):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--headless')
	driver_plBiDataNum = webdriver.Chrome(executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe',chrome_options=chrome_options)#C:/Users/kzb/Desktop/
	driver_plBiDataNum.get("https://dcpp.nfri.re.kr/search/popupViewBasic.do?plBiDataNum="+str(id_number))


	driver_plBiDataNum.find_element_by_xpath("//span").click()

	reference_number = driver_plBiDataNum.find_element_by_xpath("//span").text

	all_handles_driver_plBiDataNum = driver_plBiDataNum.window_handles
	# print('all_handles_driver_plBiDataNum：', all_handles_driver_plBiDataNum)
	# time.sleep(1)
	driver_plBiDataNum.switch_to.window(all_handles_driver_plBiDataNum[1])

	trs_plBiDataNu = driver_plBiDataNum.find_elements_by_xpath("//tbody/tr")


	author = trs_plBiDataNu[2].find_element_by_xpath("td").text.replace(",","###")
	title_of_record = trs_plBiDataNu[1].find_element_by_xpath("td").text
	journal_name = trs_plBiDataNu[3].find_element_by_xpath("td").text
	volume_and_issue_No = trs_plBiDataNu[9].find_element_by_xpath("td").text
	page_number = trs_plBiDataNu[11].find_element_by_xpath("td").text
	date_of_publication = trs_plBiDataNu[13].find_element_by_xpath("td").text

	f.write("reference_number,"+str(reference_number)+"\n")
	f.write("author,"+author+"\n")
	f.write("title_of_record,"+title_of_record+"\n")
	f.write("journal_name,"+journal_name+"\n")
	f.write("volume_and_issue_No,"+str(volume_and_issue_No)+"\n")
	f.write("page_number,"+str(page_number)+"\n")
	f.write("date_of_publication,"+str(date_of_publication)+"\n")

	return

if __name__ == '__main__':

	with open("specie_.txt") as f:
		QDB = f.readlines()

	# #去掉重复元素
	# QDB_list = []
	# for search_one in QDB:
	# 	search_one = search_one.replace("+\n","")
	# 	search_one = search_one.replace("-\n","")
	# 	search_one = search_one.replace("\n","")
	# 	QDB_list.append(search_one)

	# QDB = list(set(QDB_list))
	# for one in QDB:
	# 	with open("specie_.txt","a") as f:
	# 		f.write("{}\n".format(one))

	for search_one in QDB:
		#去掉多余的换行符
		search_one = search_one.replace("\n","")
		print("开始搜索：",search_one)

		#检查文件夹是否存在，不存在则创建
		path = "data/{}".format(search_one)
		if not os.path.exists(path):
			os.makedirs(path)

		#进行搜索
		driver = do_search(search_one)
		#获取信息ID
		id_list = get_id(driver)
		#获取搜索值
		search_value = get_search_value(driver)
		print("获取到的搜索值为："+str(search_value))
		#将数据写入文件
		write_content(id_list,search_value,search_one)