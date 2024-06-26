# 자율 주차 시스템을 위한 주차 경로 추종 방법의 연구
## 목차
[1. 서론](#1-서론)



## 1. 서론
> 어떠한 초기 위치에서도 주차 경로를 생성하여 주차하는 것을 목표로 한다.
### 파트
- 인지 : 주차 공간 인식
- 경로 생성 : 인식된 주차 공간을 바탕으로 주행 가능한 주차 경로 생성
- 경로 추종 : 주변 차량 및 장애물과의 충돌을 피하면서 정확한 위치에 주차 => **정밀한 추종 필요**
### 주차 경로 추종 문제점
1. 경로 추종 + 차량의 자세를 어떤 하나의 **주차 목표 자세로 수렴시키는 점-안정화 문제**
   - 기존 시-불변 입력 피드백 제어 법칙에 의해 안정화될 수 없다.
     - **Pure-pursuit, PID 제어 활용 불가능**
2. 주차 경로는 주행 경로보다 길이가 짧고 곡률이 크다.
   - 선회 반경이 크기 떄문에 경로 추종 오차를 빠르게 줄이지 못하면 주차가 실패
     - **과도 응답 특성이 좋은 제어기 필요**

### 요약
- 자율 주차에 적용될 수 있는 경로 추종 방법 소개
- 각 제어 방법 별 정성적/정량적 분석 수행
- 곡률이 크며 경로의 길이가 짧고 경로의 끝 점이 있는 후방 주차 경로에 대한 성능 비교 수행

## 2. 관련 연구
- 대표적인 경로 추종 방법 Stanley, Pure-pursuit와 같은 geometric 방법과 PID 제어기 등은 구현이 쉬우며 계산 비용이 적다.
- 단점 1 : 큰 곡률에서의 불안정성
- 단점 2 : 오차에 대해 응답을 하는 방법 -> 급격한 곡률이 있을 때 과도 응답 특성이 좋지 않음

## 3. 주차 경로 추종 방법
- Kanayama Controller
- Preview
- MPC

## 결론
> Kanayama Controller 활용할 것임
### 근거
- 주차 경로 추종의 성능이 각각 4 cm, 1° 내외의 거리 및 방위 오차를 보이기 때문에 주차 경로 추종 알고리즘으로 적합함을 확인
- 제어 노력 비용이 가장 적기 때문에 효율적으로 주차 경로 추종을 수행할 수 있다.
- 제어 입력 외란이 존재 할 때에도 세 가지 알고리즘 중 가장 강인한 경로 추종 성능을 보였음

### 향후 계획
1. Kanayama Controller 스켈레톤 코드 찾기
2. 코드 분석 후 Morai Simulator에서 동작 검증
3. 몬테 카를로 시뮬레이션으로 최적 제어 파라미터 결정
4. 최적 경로에서의 시나리오 테스트 및 성능 평가
  