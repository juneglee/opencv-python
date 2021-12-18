import cv2
from header.histogram import draw_ellipse

# 문자열 출력 함수 - 그림자 효과
def put_string(frame, text, pt, value=None, color=(120, 200, 90)) :
    text = str(text) + str(value)
    shade = (pt[0] + 2, pt[1] + 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, shade, font, 0.7, (0, 0, 0), 2) # 그림자 효과
    cv2.putText(frame, text, pt   , font, 0.7, color, 2) # 작성 문자

def classify(image, sims, no):
    criteria = 0.25 if sims[0] > 0.2 else 0.1            # 얼굴-임술: 비슷하면(큰값) 남자
    value = sims[1] > criteria

    text = "Woman" if value else "Man"

    text = '%02dg: ' %no + text
    result = "유사도 [입술-얼굴: %4.3f 윗-귀밑머리: %4.3f]" % (sims)

    put_string(image, text, (10, 30), "")           # 영상 출력
    print(text + " - " + result)                    # 콘솔창 출력

def display(image, face_center, centers, sub):
    cv2.circle(image, face_center, 3, (0, 0, 255), 2)	    # 얼굴 중심점 표시
    cv2.circle(image, tuple(centers[0]), 10, (0, 255, 0), 2)	# 눈 표시
    cv2.circle(image, tuple(centers[1]), 10, (0, 255, 0), 2)
    draw_ellipse(image, sub[2], 0.35,(0, 0, 255),  2)	    # 얼굴 타원
    draw_ellipse(image, sub[3], 0.45,(255, 100, 0), 2)     # 입술 타원
    cv2.imshow("correct_image", image)
