import numpy as np, cv2

def draw_ellipse(image, roi, ratio, color, thickness=cv2.FILLED):
    x, y, w, h = roi
    center = (x + w // 2, y + h // 2)                   # 타원 중심
    size = (int(w * ratio), int(h * ratio))             # 타원 크기
    cv2.ellipse(image, center, size, 0, 0, 360, color, thickness)
    return image

def make_masks(rois, correct_shape):                              # 영역별 마스크 생성
    base_mask = np.full(correct_shape, 255, np.uint8)
    hair_mask = draw_ellipse(base_mask, rois[3], 0.45, 0,  -1)
    lip_mask = draw_ellipse(np.copy(base_mask), rois[2], 0.45, 255)

    masks = [hair_mask, hair_mask, lip_mask, ~lip_mask]
    masks = [mask[y:y+h,x:x+w] for mask,(x,y, w,h) in zip(masks, rois)]

    # for i, mask in enumerate(masks):
    #     cv2.imshow('mask'+str(i), mask)
    # cv2.waitKey()

    return masks

def calc_histo(image, rois, masks):
    bsize = (64, 64,64)  # 히스토그램 계급 개수
    ranges = (0,256, 0,256, 0,256)                                 # 각 채널 빈도 범위

    subs = [image[y:y+h, x:x+w] for x, y, w, h in rois]
    hists = [cv2.calcHist([sub], [0,1,2], mask, bsize, ranges) for sub, mask in zip(subs, masks)]
    hists = [ h/np.sum(h) for h in hists]           # 정규화

    sim1 = cv2.compareHist(hists[2], hists[3], cv2.HISTCMP_CORREL)
    sim2 = cv2.compareHist(hists[0], hists[1], cv2.HISTCMP_CORREL)
    return  sim1, sim2