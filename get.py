from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import datetime
import time
import json
import traceback
import os



#Headless Chrome Setting
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36")
options.add_argument("lang=ko_KR")
driver = webdriver.Chrome('C:\dev\python\hackerone\chromedriver', options=options)

#crawl.json read
file_directory = "C:\dev\python\hackerone\crawl.json"
#file_directory = "C:/dev/python/hackerone/result/fail.log"
json_data=open(file_directory).read()
json_data = json.loads(json_data)

f = open("result/work.log", 'w')
#repeat_count = 0
#max = 5
def getReport(report_id):
    #if repeat_count > 5:
    #    return

    print("Start Crawl:"+report_id)
    f.write("Start Crawl:"+report_id+"\n")
    #driver.implicitly_wait(5)
    #driver.set_page_load_timeout(10)
    driver.get('https://hackerone.com/reports/'+report_id)
    #driver.set_page_load_timeout(5)
    #driver.set_page_load_timeout(25)
    #driver.get_screenshot_as_file('C:\dev\python\hackerone\result\'+report_id+'_screen.png')

    try:

        inner = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.spec-report-title'))
        )

    except TimeoutException:
        print("Crawl Fail Time:"+report_id)
        fail = open("result/fail.log", 'a')
        fail.write(report_id+",\n")
        fail.close()



    #driver.get_screenshot_as_file('C:\dev\python\hackerone\result\'+report_id+'_screen.png')

    #Avoid Headless Detection
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
    driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")


    html = driver.page_source
    #html = inner.page_source
    #print(html)

    #soup = BeautifulSoup(open("./test.html"), 'html.parser')
    soup = BeautifulSoup(html, 'html.parser')

    data = {
        "report_id":report_id,
        "author":"",
        "reputation":0,
        "rank":"",
        "signal":"",
        "signal_percent":"",
        "impact":"",
        "percent":"",
        "title":"",
        "state":"",
        "disclosed_date":"",
        "company":"",
        "asset":"",
        "asset_type":"",
        "vuln":"",
        "bounty":0,
        "severity_rating":"",
        "severity_score":"",
        "visibility":"",
        "comment":[]
    }
    try:
        author = soup.select_one('div.content-wrapper > div.spec-researcher-context > div.mini-profile--wide > div.mini-profile__title > span')
        if author is None:
            author = ""
        else:
            author = author.text

        reputation = soup.select_one('div.content-wrapper > div.spec-researcher-context > div.mini-profile--wide > div.spec-data > div.mini-profile__meta > span.mini-profile__meta-group > div.spec-reputation > div.profile-stats-amount > span')
        if reputation is None:
            reputation = ""
        else:
            reputation = reputation.text
            

        rank = soup.select_one('div.content-wrapper > div.spec-researcher-context > div.mini-profile--wide > div.spec-data > div.mini-profile__meta > span.mini-profile__meta-group > div.spec-rank > div.profile-stats-amount > span')
        if rank is None:
            rank = ""
        else:
            rank = rank.text
            
        
        signal = soup.select_one('div.content-wrapper > div.spec-researcher-context > div.mini-profile--wide > div.spec-data > div.mini-profile__meta > span.mini-profile__meta-group > div.spec-signal > div.profile-stats-amount > span')
        if signal is None:
            signal = ""
        else:
            signal = signal.text
            

        signal_percent = soup.select_one('div.content-wrapper > div.spec-researcher-context > div.mini-profile--wide > div.spec-data > div.mini-profile__meta > span.mini-profile__meta-group > div.spec-signal-percentile > div.profile-stats-amount > span')
        if signal_percent is None:
            signal_percent = ""
        else:
            signal_percent = signal_percent.text
        

        impact = soup.select_one('div.content-wrapper > div.spec-researcher-context > div.mini-profile--wide > div.spec-data > div.mini-profile__meta > span.mini-profile__meta-group > div.spec-impact > div.profile-stats-amount > span')
        if impact is None:
            impact = ""
        else:
            impact = impact.text
            
        
        percent = soup.select_one('div.content-wrapper > div.spec-researcher-context > div.mini-profile--wide > div.spec-data > div.mini-profile__meta > span.mini-profile__meta-group > div.spec-impact-percentile > div.profile-stats-amount > span')
        if percent is None:
            percent = ""
        else:
            percent = percent.text
            
        

        title = soup.find_all('div', class_='spec-report-title')
        if len(title) > 0:
            if title[0] is not None:
                title = title[0].text
            else:
                title = ""
        else:
            title = ""

        state = soup.find_all("span", class_="spec-substate-indicator")
        if len(state) > 0:
            if state[0] is not None:
                state = state[0].text
            else:
                state = ""
        else:
            state = ""

        disclosed_date = soup.select_one('div.report-meta > table.report-meta__table > tbody > tr.spec-disclosure-information > td.spec-meta-item-contents > strong')
        if disclosed_date is not None:
            disclosed_date = disclosed_date.text 
            disclosed_date = datetime.datetime.strptime(disclosed_date, "%B %d, %Y %I:%M%p %z") 
            disclosed_date = ("{:%Y-%m-%d %H:%M:%S}".format(disclosed_date))
        else:
            disclosed_date = ""

        #company = soup.select('div.report-meta > table.report-meta__table > tbody > tr.spec-reported-to-meta-item > td.spec-meta-item-contents')
        data['reputation'] = reputation 
        data['author'] = author
        data['rank'] = rank 
        data['signal'] = signal 
        data['signal_percent'] =  signal_percent
        data['impact'] =  impact
        data['percent'] = percent 
        data['title'] = title
        data['state'] = state
        data['disclosed_date'] = disclosed_date

        #공격대상 및 종류
        asset = soup.select_one('div.report-meta > table.report-meta__table > tbody > tr.spec-reported-scope-meta-item > td.spec-meta-item-contents > div > div.text-truncate')
        if asset is not None:
            asset = asset.text
        else:
            asset = ""

        asset_type = soup.select_one('div.report-meta > table.report-meta__table > tbody > tr.spec-reported-scope-meta-item > td.spec-meta-item-contents > div > span.text-muted')
        if asset_type is not None:
            asset_type = asset_type.text.replace("(", "").replace(")", "")
        else:
            asset_type = ""

        data['asset'] = asset
        data['asset_type'] = asset_type

        #취약점 종류
        vuln = soup.select_one('div.report-meta > table.report-meta__table > tbody > tr.spec-weakness-meta-item > td.spec-meta-item-contents')
        if vuln is not None:
            vuln = vuln.text 
        else:
            vuln = ""

        data['vuln'] = vuln

        #바운티 금액
        bounty = soup.select_one('div.report-meta > table.report-meta__table > tbody > tr.spec-bounty-amount-meta-item > td.spec-meta-item-contents')
        if bounty is not None:
            bounty= bounty.text.replace("$", "").replace(",", "")
        else:
            bounty = ""
        data['bounty'] = bounty

        #severity 정보
        severity_rating = soup.select_one('div.report-meta > table.report-meta__table > tbody > tr.spec-report-severity-meta-item > td.spec-meta-item-contents > span.severity-label > span.severity-label__text > span.spec-severity-rating')
        if severity_rating is not None:
            severity_rating = severity_rating.text
        else:
            severity_rating = ""
        
        severity_score = soup.select_one('div.report-meta > table.report-meta__table > tbody > tr.spec-report-severity-meta-item > td.spec-meta-item-contents > span.severity-label > span.severity-label__text > span.spec-severity-score')
        if severity_score is not None:
            severity_score = severity_score.text.strip()
        else:
            severity_score = ""

        data['severity_rating'] = severity_rating
        data['severity_score'] = severity_score

        #제보자, 참여자 리스트
        reporter_list = []
        member_list = []
        reporter = soup.select('div.report-meta > table.report-meta__table > tbody > tr.spec-participants-meta-item > td.spec-meta-item-contents > span.spec-participant-reporter > a')
        member = soup.select('div.report-meta > table.report-meta__table > tbody > tr.spec-participants-meta-item > td.spec-meta-item-contents > span.spec-participant-team-member > a')
        for tmp in reporter:
            reporter_list.append(tmp['href'].split("/")[-1])
        for tmp in member:
            member_list.append(tmp['href'].split("/")[-1])


        #공개여부
        visibility = soup.select_one('div.report-meta > table.report-meta__table > tbody > tr.spec-public-view-meta-item > td.spec-meta-item-contents > ul > li > span.spec-visibility-label')
        if visibility is not None:
            visibility = visibility.text
        else:
            visibility = ""

        data['visibility'] = visibility

        #코멘트 이력
        comment_user = soup.select('div.timeline > div.timeline-item')
        comment_history = []
        for tmp in comment_user:
            a_list = tmp.select('div.timeline-avatar-placeholder > a')
            for each_a in a_list:
                comment_user = each_a['href'].replace("/", "")
                comment_history.append({"author":comment_user, "content" : "", "date":""})

        history_list = []
        time_list = []

        #첫번째 코멘트
        comment_list = soup.select('div.timeline > div.timeline-item')
        for comment_detail in comment_list:
            content = comment_detail.select('div.timeline-container > div.timeline-container-content > div > div.markdownable')
            line_arr = []
            for line in content:
                line_arr.append(line.text)
                if len(line_arr) > 0: 
                    time = comment_detail.select_one('div.timeline-container > div.timeline-container-subject > span.timeline-timestamp > span')
                    if time is not None:
                        val = datetime.datetime.strptime(time['title'][:-4], "%B %d, %Y %H:%M:%S")
                        val = ("{:%Y-%m-%d %H:%M:%S}".format(val))
                        time_list.append(val)
                    history_list.append(line_arr)

        #그 이후 코멘트
        comment_list = soup.select('div.timeline > div.timeline-item')
        for comment_detail in comment_list:
            content = comment_detail.select('div.timeline-container > div > div.timeline-container-content > div > div.markdownable')
            line_arr = []
            for line in content:
                line_arr.append(line.text)
                if len(line_arr) > 0: 
                    time = comment_detail.select_one('div.timeline-container > div.timeline-container-subject > span.timeline-timestamp > a > span')
                    if time is not None:
                        #time_list.append(datetime.datetime.strptime(time['title'][:-4], "%B %d, %Y %H:%M:%S"))
                        val = datetime.datetime.strptime(time['title'][:-4], "%B %d, %Y %H:%M:%S")
                        val = ("{:%Y-%m-%d %H:%M:%S}".format(val))
                        #print(val)
                        time_list.append(val)
                    history_list.append(line_arr)

        #정리된 history 리스트 merge
        for index, tmp in enumerate(history_list):
            comment_history[index]['content'] = tmp[0]
            comment_history[index]['date'] = time_list[index] 


        data['comment'] = comment_history

        f_data = open('C:/dev/python/hackerone/result/success/'+report_id, 'w')
        json_string = json.dumps(data)
        f_data.write(json_string)
        f_data.close()

        print("Success Crawl:"+report_id)
        f.write("Success Crawl:"+report_id+"\n")



        #except Exception, e:
    except Exception as e:
        print("Crawl Fail:"+report_id)
        fail = open("result/fail.log", 'a')
        fail.write(report_id+",\n")
        fail.write(str(e)+"\n")
        fail.write(str(traceback.print_tb(e.__traceback__))+"\n")
        fail.close()
        #logger.error('Failed to upload to ftp: '+ str(e))

#getReport(report_id)
total = len(json_data)
count = 1 
for url in json_data:
    report_id = url.split("/")[-1]
    #report_id = str(url)
    print(str(count)+" / "+str(total))
    fname = 'C:/dev/python/hackerone/result/success/'+report_id
    if not os.path.exists(fname):
        getReport(report_id)
        time.sleep(1)
    #report_id="666557"
    count+=1



f.close()
'''
comment_list = soup.select('div.timeline > div.timeline-item')
for comment_detail in comment_list:
    user = comment_detail.select_one('div.timeline-container > div.timeline-container-subject div.timeline-container-subject-entry > span > span > a > span')
    subject = comment_detail.select('div.timeline-container > div.timeline-container-subject div.timeline-container-subject-entry > span')
    for name in subject:
        if len(name.select('a')) > 0:
            #사람 이름
            print(name.select_one('a').text)
        else:
            #상태
            print(name.text)
        #if user is not None:
            #print(user)
'''

'''
reporter_comment = []
for comment_detail in comment_list:
    history = comment_detail.select('div.timeline-container > div.timeline-container-content')
    for tmp in history:
        for content in tmp:
            reporter_comment.append(content.text)
    


for comment_detail in comment_list:
    history = comment_detail.select('div.timeline-container > div >  div.timeline-container-content')
    for tmp in history:
        for content in tmp:
            reporter_comment.append(content.text)
'''