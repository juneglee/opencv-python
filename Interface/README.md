# openCV 인터페이스 기초 / 사용자 인터페이스 및 I/O 처리 

### 윈도우 제어 
- 영상처리는 무엇이라 생각하는가? 영상처리를 한다미로 말하면 2차원 행렬에 대한 연산이라고 할 수 있다 
- OpenCV 에서는 원도우 (window, 창)가 활성화된 상태에서만 마우스나 키보드 이벤트를 감지 할 수 있다. 따라서 이런 이벤트를 감지 해서 처리하려면 원도우를 생성하고 제어할 수 있어야 한다 

- cv2.namedWindow() : 원도우 이름을 설정한 후, 해당 이름으로 원도우 생성
    - namedWindow(winname[,flags])

- cv2.imshow() : 원도우 이름의 mat 행렬을 영상으로 표시함 
    - imshow(winname, mat)

- cv2.destroyAllWindows() : 인수로 지정된 타이들 원도우 파괴

- cv2.moveWindow() : winname 이름의 원도우를 지정된 위치인 (x,y)로 이동, (기존위치는 좌측 상단 )
    - moveWindow(winname, x, y)
 
- cv2.resizeWindow() : 윈도우 크기 재조정 
    - resizeWindow(winname, width, height)