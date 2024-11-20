import os
import cv2

def normalize_labels(txt_folder, img_folder, output_folder):
    # 라벨 파일 목록 가져오기
    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]
    
    # output_folder가 존재하지 않으면 생성
    os.makedirs(output_folder, exist_ok=True)
    
    # 각 라벨 파일을 처리
    for txt_file in txt_files:
        txt_path = os.path.join(txt_folder, txt_file)
        
        # 이미지 파일 경로
        img_file = os.path.splitext(txt_file)[0] + '.png'  # 예시로 .png로 설정
        img_path = os.path.join(img_folder, img_file)

        # 이미지 크기 가져오기
        if not os.path.exists(img_path):
            print(f"Warning: Image file {img_file} not found. Skipping {txt_file}.")
            continue

        img = cv2.imread(img_path)
        if img is None:
            print(f"Error: Failed to load image {img_file}. Skipping {txt_file}.")
            continue
        img_height, img_width = img.shape[:2]
        
        # 정규화된 라벨을 저장할 파일 경로
        output_txt_path = os.path.join(output_folder, txt_file)

        # 라벨 파일 읽기
        with open(txt_path, 'r') as file:
            lines = file.readlines()

        # 각 줄 처리
        normalized_lines = []
        for line in lines:
            parts = line.strip().split()  # 공백으로 분리
            if len(parts) > 1:
                # 클래스 ID는 그대로 유지
                class_id = parts[0]
                # 나머지 값들(좌표) 정규화
                coords = list(map(float, parts[1:]))
                normalized_coords = []
                
                for i in range(len(coords)):
                    if i % 2 == 0:  # x좌표
                        normalized_value = coords[i] / img_width
                    else:  # y좌표
                        normalized_value = coords[i] / img_height
                    
                    # 음수를 0으로, 1을 넘는 값을 1로 클리핑
                    normalized_value = max(0, min(1, normalized_value))
                    normalized_coords.append(normalized_value)

                # 클래스 ID + 정규화된 좌표
                normalized_line = f"{class_id} " + " ".join(map(str, normalized_coords)) + "\n"
                normalized_lines.append(normalized_line)
        
        # 정규화된 내용을 새로운 파일에 저장
        with open(output_txt_path, 'w') as out_file:
            out_file.writelines(normalized_lines)

        print(f"Processed {txt_file} and saved to {output_txt_path}")

# 사용 예시
txt_folder = 'D:/roas_dataset1/labels/val'  # txt 파일이 있는 폴더 경로
img_folder = 'D:/roas_dataset1/images/val'  # 이미지 파일이 있는 폴더 경로
output_folder = 'D:/roas_dataset1/labels_1/val'  # 정규화된 결과를 저장할 폴더 경로

normalize_labels(txt_folder, img_folder, output_folder)
