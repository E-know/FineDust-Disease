# FineDust-Disease
### 로지스틱 회귀 기반 미세먼지 노출에 따른 질병예측 프로젝트
2021 = 1학기 세종대학교 캡스톤 프로젝트
참여 인원
 * [최인호](https://github.com/E-know)
 * [안건우](https://github.com/agw5256)
---
## 자료출처
이 프로젝트는 아래에 적시된 데이터를 사용합니다. 사용법에 맞게 갖춰주시길 바랍니다.

### 국민건강보홈 표본코호트 DB
![국민건강보험 이미지](https://user-images.githubusercontent.com/55151796/122654834-00dadc00-d189-11eb-8b33-b61feb749016.png)  
[국민건강보험 NHISS](https://nhiss.nhis.or.kr/bd/ab/bdaba001cv.do)  

국민건강보험에서 제공하는 표본코호트를 사용합니다.
별도의 신청이 필요한 절차입니다.  
데이터를 다운 받으셨다면 아래의 폴더에 다음과 같이 넣어주시면 됩니다.  

#### 자격 파일  

`./data/health/jk/파일명`
  
  * 파일명 수정은 없습니다.  
  * nhid_jk_연도.sasbdat 파일을 넣어주세요.

#### 명세서 파일  

`./data/health/mss/파일명`
  
  * 파일명 수정은 없습니다.  
  * nhid_gy20_t1_연도.sas7bdat 파일을 넣어주세요.  
  * **명세서 파일은 반드시 T120 폴더 안에 있는 데이터를 넣어주세요.**

### 건강검진 파일

`./data/health/gggj/파일명`

 * 파일명 수정은 없습니다.
 * nhid_gj_연도.sas7bdat 파일을 넣어주세요.

### 미세먼지
![한국환경공단 이미지](https://user-images.githubusercontent.com/55151796/122654877-38e21f00-d189-11eb-8478-c4a9b400cd86.png)  
[한국환경공단-AirKorea](https://www.airkorea.or.kr/web/last_amb_hour_data?pMENU_NO=123)  

AirKorea 에서 제공하는 미세먼지 데이터를 사용합니다.
별도의 신청 없이 다운이 가능합니다.  
데이터를 다운 받으시고, 아래의 폴더에 다음과 같이 넣어주시면 됩니다.  

`./data/dust/파일명`

  * 파일명 수정은 없습니다.

---

