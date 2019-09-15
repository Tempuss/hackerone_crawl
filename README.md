# hackerone_crawl

# Step

1. URL 추출
  * 해커원 텔레그램 봇
  * 해커원 웹 사이트에서 무한 스크롤링 하도록 script 짜서 추출
  * 총 6834개 추출 성공
 
2. Crawlling
  * 추출한 URL 링크를 크롤링했음
  * HeadLess Chrome + Selenium으로 크롤링
    * 1차 시도땐 JS 문제떔에 실패
    * 2차 시도땐 계속 빈 값만 요청해서 실패
    * 3차 시도떈 완전한 HTML이 오는 확률이 30%도 안되서 실패
    * 4차 시도때는 JS가 구동중일때 크롤링 해와서 데이터가 절반만 완성상태여서 실패
    * 5차 시도떄는 파싱 실패 예외처리 하느라 실패(예외처리해줘야 될게 존나게 많았음)
    * 6차 시도떄 타임아웃 문제 & 파싱 오류 완전 극복(WebDriverWait기능으로 웹 상의
      모든 기능이 구동 될때까지 기다렸다가 callback으로 작동하도록 수정)
   
3. Insert To ElasticSearch
  * AWS 엘라 쓰려다가 사용법 존나 어려워서 3시간 날림
  * 로컬 엘라에다가 Insert!... 는 성공했으나 데이터 타입이랑 매핑이 달라서 Revert
  * 예전에 사용했던 6.3 버전이랑 7.3 버전이랑 버전이 달라서 삽질하느라 하루 날림
  * Index Mapping 하는 문법이 6.*랑 7.*랑 완전 달라서 삽질함...
  * ElasticSearch에 Insert 성공 인줄 알았으나 날짜 데이터가 형식에 안맞는다고 지랄해서 실패
  ```
  {"type":"date","format":"yyyy-MM-dd HH:mm:ss", "ignore_malformed": true}}
  ```
  * ignore_malformed 옵션을 True로 해줘야지 date 형식의 string 말고도 '' 로 되어있는 데이터도 Insert 가능함
  * Insert 성공 & 검색 잘됨 휴
