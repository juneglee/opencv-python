import numpy as np, cv2

# 전처리
def preprocessing(no):  # 검출 전처리
    image = cv2.imread('data/face/%02d.jpg' %no, cv2.IMREAD_COLOR)
    if image is None: return None, None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 명암도 영상 변환
    gray = cv2.equalizeHist(gray)  # 히스토그램 평활화
    return image, gray

# 얼굴 기울기 계산 및 보정 
def correct_image(image, face_center, eye_centers):
    pt0, pt1 = eye_centers                              # 좌, 우 눈 중심 좌표
    if pt0[0] > pt1[0]: pt0, pt1 = pt1, pt0             # 좌, 우 눈 위치 맞바꿈

    dx, dy = np.subtract(pt1, pt0).astype(float)        # 두 좌표간 차분 계산
    angle = cv2.fastAtan2(dy, dx)                       # 차분으로 기울기 계산
    rot_mat = cv2.getRotationMatrix2D(face_center, angle, 1)

    size = image.shape[1::-1]                           # 행태와 크기는 역순
    corr_image = cv2.warpAffine(image, rot_mat, size, cv2.INTER_CUBIC)

    eye_centers = np.expand_dims(eye_centers, axis=0)             # 눈 좌표 차원 증가
    corr_centers = cv2.transform(eye_centers, rot_mat)           # 어파인(회전) 변환 좌표 계산
    corr_centers = np.squeeze(corr_centers, axis=0)              # 차원 감소

    return corr_image, corr_centers                 # 보정 결과 반환

# 입술 영역 및 머리 영역 검출
def define_roi(pt, size):
    return np.ravel([pt, size]).astype(int)      # 2원소 튜풀 2개 --> 4 원소 튜플 1개

def detect_object(center, face):
    w, h = face[2:4]                            # 얼굴 영역 크기 (w, h)
    center = np.array(center)                   # 얼굴 중심 좌표 ndarray 객체로 변경
    gap1 = np.multiply((w,h), (0.45, 0.65))      # 얼굴 영역 비율 크기 45%. 65%
    gap2 = np.multiply((w,h), (0.20, 0.1))       # 입술 영역 비율 크기 20%, 10%

    pt1 = center - gap1        # 좌상단 평행이동 - 머리 시작좌표
    pt2 = center + gap1             # 우하단 평행이동 - 머리 종료좌표
    hair = define_roi(pt1, pt2-pt1)       # 머리 영역

    size = np.multiply(hair[2:4], (1, 0.4))
    hair1 = define_roi(pt1, size)             # 윗머리 영역 (x,y,w,h)
    hair2 = define_roi(pt2-size, size)             # 귀밑머리 영역

    lip_center = center + (0, h * 0.3) # 입술 여역 중심 좌표 - 30%
    lip1 = lip_center - gap2    # 좌상단 평행이동
    lip2 = lip_center + gap2         # 우하단 평행이동
    lip = define_roi(lip1, lip2-lip1) # 입술 영역

    return [hair1, hair2, lip, hair]

