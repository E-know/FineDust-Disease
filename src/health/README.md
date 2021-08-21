# 표본코호트 DB

## 원본 데이터

### 자격DB

국민건강보험에 등록된 회원들의 리스트

|변수명|칼럼 이름|설명|
|---|---|---|
|기준년도|    STND_Y|해당 자격의 연도 기준
|개인일련번호|    PERSON_ID|개인에 부여되는 Primary Key
|성|    SEX| 1 남자 2 여자
|연령대    |AGE_GROUP| 밑의 표 참고
|시도코드|    SIDO| 시도 코드
|시군구코드|    SGG| 시군구코드

`사용하는 코드 기재 했음을 알려드립니다`

### 진료DB

병원이 내원 했을 때 기록되는 진료 데이터

|변수명|칼럼 이름|설명|
|---|---|---|
|개인일련번호    |PERSON_ID    |주민등록번호의 대체식별번호, 조인키
|청구일련번호    |KEY_SEQ    |청구일련번호의 대체식별번호 부여(연도+일련번호), 조인키
|요양개시일자    |RECU_FR_DT|    최초내원일자, 조제투여일자
|주상병            |MAIN_SICK|    주된 상병분류기호 [병 분류사이트 링크](https://www.kcdcode.kr/browse/contents/0)
|부상병            |SUB_SICK

### 건강검진 DB

건강검진 받았던 사람들의 데이터

##### 2002-2008년

|개인일련번호|칼럼 이름|설명|
|---|---|---|
|신장    |HEIGHT
|체중    |WEIGHT
|(본인)과거병력코드1    |HCHK_PMH_CD1|과거병력코드는 아래의 표 참고바람
|(본인)과거병력코드2    |HCHK_PMH_CD2|
|(본인)과거병력코드3    |HCHK_PMH_CD3|
|(가족력)간장질환유무    |FMLY_LIVER_DISE_PATIEN_YN| 1-없음 2-있음
|(가족력)고혈압유무    |FMLY_HPRTS_PATIEN_YN
|(가족력)뇌졸중유무    |FMLY_APOP_PATIEN_YN
|(가족력)심장병유무    |FMLY_HDISE_PATIEN_YN
|(가족력)암유무    |FMLY_CANCER_PATIEN_YN
|흡연상태    |SMK_STAT_TYPE_RSPS_CD| 1-5년미만 2-5~9년 3-10~19년 4-20~29년 5-30년이상
|(과거,현재)흡연기간    |SMK_TERM_RSPS_CD
|(현재)하루흡연량    |DSQTY_RSPS_CD
|음주습관    |DRNK_HABIT_RSPS_CD
|1회 음주량    |TM1_DRKQTY_RSPS_CD
|1주 운동횟수    |EXERCI_FREQ_RSPS_CD

##### 2009-2013년

<table>
    <tr>
        <th>개인일련번호</th> <th>칼럼이름</th> <th>설명</th>
    </tr>
</table>

<div class="tg-wrap"><table>
<tbody>
  <tr>
    <td rowspan="8">(본인)과거병력코드1</td>
    <td rowspan="8">HCHK_PMH_CD1</td>
    <td rowspan="8">char(1)</td>
    <td>과거병력을 3개 까지 기입&nbsp;&nbsp;&nbsp;가능</td>
  </tr>
  <tr>
    <td>1 : 결핵</td>
  </tr>
  <tr>
    <td>2 : 간염</td>
  </tr>
  <tr>
    <td>3 : 간장질환</td>
  </tr>
  <tr>
    <td>4 : 고혈압</td>
  </tr>
  <tr>
    <td>5 : 심장병</td>
  </tr>
  <tr>
    <td>6 : 뇌졸중</td>
  </tr>
  <tr>
    <td>7 : 당뇨병</td>
  </tr>
  <tr>
    <td>(본인)과거병력코드2</td>
    <td>HCHK_PMH_CD2</td>
    <td>char(1)</td>
    <td>8 : 암</td>
  </tr>
  <tr>
    <td>(본인)과거병력코드3</td>
    <td>HCHK_PMH_CD3</td>
    <td>char(1)</td>
    <td>9 : 기타질환</td>
  </tr>
  <tr>
    <td>(가족력)간장질환유무</td>
    <td>FMLY_LIVER_DISE_PATIEN_YN</td>
    <td>char(1)</td>
    <td>1&nbsp;&nbsp;&nbsp;: 없음</td>
  </tr>
  <tr>
    <td>(가족력)고혈압유무</td>
    <td>FMLY_HPRTS_PATIEN_YN</td>
    <td>char(1)</td>
    <td>2 : 있음</td>
  </tr>
  <tr>
    <td>(가족력)뇌졸중유무</td>
    <td>FMLY_APOP_PATIEN_YN</td>
    <td>char(1)</td>
    <td>　</td>
  </tr>
  <tr>
    <td>(가족력)심장병유무</td>
    <td>FMLY_HDISE_PATIEN_YN</td>
    <td>char(1)</td>
    <td>　</td>
  </tr>
  <tr>
    <td>(가족력)당뇨병유무</td>
    <td>FMLY_DIABML_PATIEN_YN</td>
    <td>char(1)</td>
    <td>　</td>
  </tr>
  <tr>
    <td>(가족력)암유무</td>
    <td>FMLY_CANCER_PATIEN_YN</td>
    <td>char(1)</td>
    <td>　</td>
  </tr>
  <tr>
    <td rowspan="3">흡연상태</td>
    <td rowspan="3">SMK_STAT_TYPE_RSPS_CD</td>
    <td rowspan="3">char(1)</td>
    <td>1&nbsp;&nbsp;&nbsp;: 피우지 않는다</td>
  </tr>
  <tr>
    <td>2 : 과거에 피웠으나 지금은 끊었다</td>
  </tr>
  <tr>
    <td>3 : 현재도 피운다</td>
  </tr>
  <tr>
    <td rowspan="5">(과거,현재)흡연기간</td>
    <td rowspan="5">SMK_TERM_RSPS_CD</td>
    <td rowspan="5">char(1)</td>
    <td>1&nbsp;&nbsp;&nbsp;: 5년 미만</td>
  </tr>
  <tr>
    <td>2 : 5~9년</td>
  </tr>
  <tr>
    <td>3 : 10~19년</td>
  </tr>
  <tr>
    <td>4 : 20~29년</td>
  </tr>
  <tr>
    <td>5 : 30년 이상</td>
  </tr>
  <tr>
    <td rowspan="4">(현재)하루흡연량</td>
    <td rowspan="4">DSQTY_RSPS_CD</td>
    <td rowspan="4">char(1)</td>
    <td>1&nbsp;&nbsp;&nbsp;: 반갑미만</td>
  </tr>
  <tr>
    <td>2 : 반갑이상~한갑미만</td>
  </tr>
  <tr>
    <td>3 : 한갑이상~두갑미만</td>
  </tr>
  <tr>
    <td>4 : 두갑이상</td>
  </tr>
  <tr>
    <td rowspan="5">음주습관</td>
    <td rowspan="5">DRNK_HABIT_RSPS_CD</td>
    <td rowspan="5">char(1)</td>
    <td>1&nbsp;&nbsp;&nbsp;: (거의)마시지 않는다</td>
  </tr>
  <tr>
    <td>2 : 월2~3회정도 마신다</td>
  </tr>
  <tr>
    <td>3 : 일주일에 1~2회 마신다</td>
  </tr>
  <tr>
    <td>4 : 일주일에 3~4회 마신다</td>
  </tr>
  <tr>
    <td>5 : 거의 매일 마신다</td>
  </tr>
  <tr>
    <td rowspan="4">1회 음주량</td>
    <td rowspan="4">TM1_DRKQTY_RSPS_CD</td>
    <td rowspan="4">char(1)</td>
    <td>1&nbsp;&nbsp;&nbsp;: 소주 반 병 이하</td>
  </tr>
  <tr>
    <td>2 : 소주 한 병</td>
  </tr>
  <tr>
    <td>3 : 소주 1병 반</td>
  </tr>
  <tr>
    <td>4 : 소주 2병 이상</td>
  </tr>
  <tr>
    <td rowspan="5">1주 운동횟수</td>
    <td rowspan="5">EXERCI_FREQ_RSPS_CD</td>
    <td rowspan="5">char(1)</td>
    <td>1&nbsp;&nbsp;&nbsp;: 안한다</td>
  </tr>
  <tr>
    <td>2 : 1~2회</td>
  </tr>
  <tr>
    <td>3 : 3~4회</td>
  </tr>
  <tr>
    <td>4 : 5~6회</td>
  </tr>
  <tr>
    <td>5 : 거의 매일</td>
  </tr>
</tbody>
</table></div>

|개인일련번호|칼럼 이름|설명|
|---|---|---|
|신장    |HEIGHT|
|체중    |WEIGHT|
|(본인)뇌졸중과거병력유무    |HCHK_APOP_PMH_YN|
|(본인)심장병과거병력유무    |HCHK_HDISE_PMH_YN|
|(본인)고혈압과거병력유무    |HCHK_HPRTS_PMH_YN|
|(본인)당뇨병과거병력유무    |HCHK_DIABML_PMH_YN|
|(본인)고지혈증(이상지질혈증)과거병력유무    |HCHK_HPLPDM_PMH_YN|
|(본인)폐결핵과거병력유무    |HCHK_PHSS_PMH_YN|
|(본인)기타(암포함)질환 과거병력유무    |HCHK_ETCDSE_PMH_YN|
|(가족력)뇌졸중환자유무    |FMLY_APOP_PATIEN_YN|
|(가족력)심장병환자유무    |FMLY_HDISE_PATIEN_YN|
|(가족력)고혈압환자유무    |FMLY_HPRTS_PATIEN_YN|
|(가족력)당뇨병환자유무    |FMLY_DIABML_PATIEN_YN\
|(가족력)기타(암포함)환자유무    |FMLY_CANCER_PATIEN_YN|
|흡연상태    |SMK_STAT_TYPE_RSPS_CD|asf  gg   hhh  dd
|(과거)흡연기간    |PAST_SMK_TERM_RSPS_CD|
|(과거)하루흡연량    |PAST_DSQTY_RSPS_CD|
|(현재)흡연기간    |CUR_SMK_TERM_RSPS_CD|
|(현재)하루흡연량    |CUR_DSQTY_RSPS_CD|
|음주습관    |DRNK_HABIT_RSPS_CD|
|1회 음주량    |TM1_DRKQTY_RSPS_CD|
|1주_20분이상 격렬한 운동    |MOV20_WEK_FREQ_ID|
|1주_30분이상 중간정도 운동    |MOV30_WEK_FREQ_ID|
|1주_총30분이상 걷기 운동    |WLK30_WEK_FREQ_ID|


