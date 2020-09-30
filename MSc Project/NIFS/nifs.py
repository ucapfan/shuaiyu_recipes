import time,json,random,os
from selenium import webdriver

def do_search(search_one):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver2.exe',chrome_options=chrome_options)#C:/Users/kzb/Desktop/
    driver.get("https://dbshino.nifs.ac.jp/nifsdb")

    #选择CHART
    # driver.find_element_by_xpath("//a[@href='/nifsdb/chart/top']").click()
    #选择COML
    driver.find_element_by_xpath("//a[@href='/nifsdb/cmol/top']").click()
    
    #输入搜索内容
    driver.find_element_by_xpath("//input[@name='basic[element_a1]']").send_keys(search_one)

    #勾选Cross Section
    # driver.find_element_by_xpath("//input[@id='basic_data_type_cs']").click()
    #勾选Rate coefficient
    driver.find_element_by_xpath("//input[@id='basic_data_type_rc']").click()

    #进行搜索
    driver.find_element_by_xpath("//input[@id='btn_search']").click()
    
    get_custom_content(search_one,driver)
    # get_numerical_content(search_one,driver)
    # time.sleep(3)
 
def get_custom_content(search_one,driver):
    
    #勾选Custom及其相关系数
    driver.find_element_by_xpath("//input[@id='display_format_custom']").click()

    driver.find_element_by_xpath("//input[@id='custom_record_no']").click()
    driver.find_element_by_xpath("//input[@id='custom_element_a']").click()
    driver.find_element_by_xpath("//input[@id='custom_authors']").click()
    driver.find_element_by_xpath("//input[@id='custom_page_numbers']").click()
    driver.find_element_by_xpath("//input[@id='custom_process']").click()
    driver.find_element_by_xpath("//input[@id='custom_initial_charge_state_a']").click()
    driver.find_element_by_xpath("//input[@id='custom_initial_charge_state_b']").click()
    driver.find_element_by_xpath("//input[@id='custom_original_x_unit']").click()
    driver.find_element_by_xpath("//input[@id='custom_title_of_record']").click()
    driver.find_element_by_xpath("//input[@id='custom_date_of_publication']").click()
    driver.find_element_by_xpath("//input[@id='custom_theory_or_experiment']").click()
    driver.find_element_by_xpath("//input[@id='custom_initial_excited_state_b']").click()
    driver.find_element_by_xpath("//input[@id='custom_original_y_unit']").click()
    driver.find_element_by_xpath("//input[@id='custom_journal_name']").click()
    driver.find_element_by_xpath("//input[@id='custom_process_title']").click()
    driver.find_element_by_xpath("//input[@id='custom_data_type']").click()
    driver.find_element_by_xpath("//input[@id='custom_element_b']").click()
    driver.find_element_by_xpath("//input[@id='custom_final_products']").click()
    driver.find_element_by_xpath("//input[@id='custom_reference_no']").click()
    driver.find_element_by_xpath("//input[@id='custom_volume_and_issue_no']").click()

    # time.sleep(10)
    
    #进入数据页面
    driver.find_element_by_xpath("//input[@id='btn_find_display']").click()
    
    uls = driver.find_elements_by_xpath("//ul")
    
    # print(uls[0].text)
    
    pre_process_title = []
    print(len(uls))

    for ul in uls:
        #反应方程式
        process_title = ul.text.split("Process Title = ")[1]
        #记录编号
        Id_Number = ul.text.split(" = ")[1].split("\n")[0]
        # print(process_title)

        if process_title not in pre_process_title:
            
            f = open("data/{}/{}.txt".format(search_one,Id_Number),"w",errors="ignore")
            f.write(ul.text)
            f.close()
        else:
            print(process_title)

        pre_process_title.append(process_title)
    
def get_numerical_content(search_one,driver):

    driver.find_element_by_xpath("//input[@id='display_format_numeric']").click()

    #进入二级页面
    driver.find_element_by_xpath("//input[@id='btn_find_display']").click()

    driver.find_element_by_xpath("//input[@id='display_write_vertical']").click()

    #进入数据页面
    driver.find_element_by_xpath("//input[@id='btn_num_display']").click()

    uls = driver.find_elements_by_xpath("//ul")
    # print(uls[0].text)
    pre_process_title = []

    for ul in uls:
        #反应方程式
        process_title = ul.text.split("\n")[1]
        #记录编号
        Id_Number = ul.text.split("=")[1].split("\n")[0]
  
        if process_title not in pre_process_title and Id_Number.isdigit():
            
            f = open("data/{}/{}.csv".format(search_one,Id_Number),"a",errors="ignore")  

            f.write("{}\n".format(process_title))
            f.write("X = Electron energy (eV),Y = Cross section (cm2),Y Error Plus (cm2),Y Error Minus (cm2)\n")

            for x in ul.text.split("\n")[10:]:
                # print(x)
                f.write("{}\n".format(x.replace(" ",",")))

            f.close()

        # if process_title in pre_process_title and Id_Number.isdigit():
        #     print(process_title)

        pre_process_title.append(process_title)


if __name__ == '__main__':

    with open("species.txt") as f:
        QDB = f.readlines()

    for search_one in QDB:
        #去掉多余的换行符
        search_one = search_one.replace("\n","")
        print("开始搜索：",search_one)

        # 检查文件夹是否存在，不存在则创建
        path = "data/{}".format(search_one)
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            # do_search(search_one)
            do_search(search_one)
        except:
            print("无记录元素有：",search_one)
            f = open("data/log.txt","a",errors="ignore")
            f.write("无记录元素有：{}\n".format(search_one))
            f.close()

        # do_search(search_one)