
from selenium import webdriver
from selenium.webdriver.common.by import By
from collections import Counter
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import time
import csv


job_info_url='https://employers.indeed.com/j#cdjobs'
job_info_sum=5
job_info_roop_start=2

options = webdriver.ChromeOptions()

#chrome://version/で検索するとプロフィールパスが分かる
profile_path='C:/Users/montecampo/AppData/Local/Google/Chrome/User'

options.add_argument('--user-data-dir='+profile_path)

driver = webdriver.Chrome(options=options)


driver.get(job_info_url)
print('ログイン')
driver.implicitly_wait(30)

#上記コードでセッションの保持ができたため自動ログインなし、コメントアウト（一回目のみ手動ログイン）
# login_email=driver.find_element_by_name("__email")
# login_email.send_keys("kato.takako@montecampo.co.jp")
# login_password=driver.find_element_by_name("__password")
# login_password.send_keys("n9F+e$p_")
# login_subumit=driver.find_element_by_id("login-submit-button")
# login_subumit.click()

candidate_names=[]
candidate_links=[]
candidate_types=[]

for i in range(job_info_roop_start , job_info_sum+job_info_roop_start):
    print(str(i)+'個目の求人票')
    # if(i==4):
    #     break
    #     print('飛ばします！！')

    driver.implicitly_wait(30)
    job_info_link_elem=driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div[3]/div/table/tbody/tr['+str(i)+']/td[6]/a[1]')
    job_info_link=job_info_link_elem.get_attribute('href')
    driver.get(job_info_link)
    print('応募者一覧ページ突入')

    #応募者の合計を取得
    driver.implicitly_wait(30)
    candidates_all_sum_elem = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div[2]/div/div/div/div/div[2]/div/div[2]/div/div/button[1]/span[2]/div/span[1]')
    candidates_all_sum = candidates_all_sum_elem.text
    candidates_all_sum = int(candidates_all_sum)
    print('上タブの応募者合計取得')

    #ページネーションする回数
    count_pagenation=candidates_all_sum//20
    page_sum=count_pagenation+1
    print('ページネーション回数：'+str(count_pagenation))
    print('ページ数：'+str(page_sum))
    #職種名の取得
    
    candidate_type_elem=driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/span/div/div/div/button/span/div/div[1]')
    candidate_type=candidate_type_elem.text
    print('職種名取得！！'+candidate_type)

    page=1
    print('1から'+str(page_sum)+'ページ目まで巡回するよ～')
    for j in range(1,page_sum+1):
        print(str(j)+'ページ目')
        #ページの応募者数を取得
        driver.implicitly_wait(30)
        candidates_sum=len(driver.find_elements_by_class_name('cpqap-CandidateRow'))
        print('ページ内の人数:'+str(candidates_sum))

        #応募者ページへ移動、スクレイピングして戻る
        for k in range(1,candidates_sum+1):
            print(str(k)+'人目')

            driver.implicitly_wait(30)
            candidate_link_elem=driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div[2]/div/div/div/div/div[3]/div/div[3]/div[1]/div/fieldset/table/tbody/tr['+str(k)+']/td[2]/a')
            print('k1')
            candidate_link=candidate_link_elem.get_attribute('href')
            print('k2')
            driver.get(candidate_link)
            print('k3　loading now.')

            #配列に応募者名、応募者リンク、職種名を格納
            driver.implicitly_wait(30)
            candidate_name_elem=driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/h1')

            print('k4')
            candidate_name=candidate_name_elem.text
            print('k5')
            candidate_names.append(candidate_name)
            print('k6')
            
            if (candidate_names.count(candidate_name)>1):# candidate_namesで重複で抽出できるデータがあれば・・・
                #重複を削除して・・・
                candidate_names=list(set(candidate_names))
                print('k7　重複削除'+candidate_name)
                print('k8はパスします')
            else:#以降2つのappendをパス。
                candidate_links.append(candidate_link)
                print('k8')
                driver.implicitly_wait(30)

                candidate_types.append(candidate_type)
                print('k9')
                driver.implicitly_wait(30)

                #取得した配列をcsvに出力
                csv_file=open("./candidates.csv","a")
                w=csv.writer(csv_file)
                w.writerow([str(candidate_name),str(candidate_type),str(candidate_link)])
                csv_file.close()
                print('k10　append'+candidate_name)

            #今いるページの応募者一覧へ戻る
            driver.get(job_info_link+'&p='+str(page))
            print('k11')

        #ページネーション
        page+=1
        driver.get(job_info_link+'&p='+str(page))
        print('page nation')

    driver.get(job_info_url)
    driver.implicitly_wait(30)

driver.quit()
print('driver quit')

#Gドライブにcsvをアップロード
# 認証を行う --- (*2)
gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)
print("OAuth login")

folder_id='1XPdgzlRgr9mlCod6LrSf9ij4Mrh_Sr19'


file_metadata = {
    'title': "new_candidates.csv",
    'minetype':"text/csv",
    'parents':[{
        'id':folder_id,
        'kind':'drive#fileLink',
    }]
}
f = drive.CreateFile(file_metadata)
f.SetContentFile('candidates.csv')

f.Upload()
print("ok")

#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/h1
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/h1
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/h1
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[2]/div[3]/h3
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[2]/div[4]/h3
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[2]/div[12]/h3
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/h3
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[2]/div[20]
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[2]/div[12]/h3
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[2]/div[3]/h3
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[2]/div[13]/h3
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/h1
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div[2]/div/div/div/div/div[3]/div/div[2]/fieldset/table/tbody/tr[1]/td[2]/a
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div[2]/div/div/div/div/div[3]/div/div[3]/fieldset/table/tbody/tr[1]/td[2]/a

#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div[3]/div/table/tbody/tr[4]/td[6]/a[1]
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div[3]/div/table/tbody/tr[6]/td[6]/a[1]

#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div[2]/div/div/div/div/div[3]/div/div[3]/div[1]/div/fieldset/table/tbody/tr['+str(k)+']/td[2]/a
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div[2]/div/div/div/div/div[3]/div/div[3]/fieldset/table/tbody/tr['+str(k)+']/td[2]/a

#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/h1
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/h1

#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div[2]/div/div/div/div/div[3]/div/div[3]/div[1]/div/fieldset/table/tbody/tr[4]/td[2]/a
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div[2]/div/div/div/div/div[3]/div/div[3]/div[1]/div/fieldset/table/tbody/tr[5]/td[2]/a

#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/h1
#/html/body/div[2]/div[3]/div[1]/div[3]/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/h1