# Web_process_data_project

프로젝트 개요

공정 상황과 실시간으로 모니터링할 수 있는 기능
조립공정에서 Python으로 생성되는 데이터들을 MySQL DB에 적재한 후 웹 서버에서 실시간으로 모니터링 및 품질예측 할 수 있는 웹 애플리케이션

개발 과정

1. 생산할 제품을 선정한 후 제품을 생산할 공정을 설계(EGR 쿨러- 조립,용접 공정)
2. 공정과정에서 생성될 데이터들을 선정하고 그에 맞게 데이터베이스 설계를 MySQL로 진행
3. python으로 데이터를 생성할 수 있는 시뮬레이션 프로그램을 만들고 데이터를 DB에 연결 및 적재
4. Flask를 활용해 API를 설계한다. (데이터 생성, OEE 조회, 제품검색, 분석, 예측 기능, 실시간 모니터링)
5. UI 설계 및 프론트엔드 개발, 대시보드를 만들어 시각적인 부분을 추가
6. AWS EC2 인스턴스, RDS를 이용해 배포
7. 프로젝트 완료 (2020.11.27) - V. 1.0
8. 완성된 페이지 주소: http://54.180.83.130:5000/
