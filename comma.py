import os

def fix_obb_label_files(label_folder):
    # 라벨 파일을 모두 가져옴
    label_files = [f for f in os.listdir(label_folder) if f.endswith('.txt')]

    for label_file in label_files:
        label_path = os.path.join(label_folder, label_file)
        
        # 파일 읽기
        with open(label_path, 'r') as f:
            lines = f.readlines()

        fixed_lines = []
        
        for line in lines:
            # 콤마가 있으면 공백으로 바꾸기
            line = line.replace(',', ' ')
            parts = line.strip().split()
            
            # 클래스 ID와 8개의 좌표가 있는지 확인
            if len(parts) == 9:
                try:
                    class_id = int(parts[0])
                    coords = [float(x) for x in parts[1:]]
                    fixed_lines.append(f"{class_id} {' '.join(map(str, coords))}\n")
                except ValueError:
                    print(f"Skipping invalid data in {label_file}: {line}")
            else:
                print(f"Skipping corrupt line in {label_file}: {line}")
        
        # 수정된 내용을 다시 파일에 저장
        with open(label_path, 'w') as f:
            f.writelines(fixed_lines)

# 사용 예시
label_folder = 'D:/roas_dataset/labels/test'  # 라벨 파일 폴더 경로
fix_obb_label_files(label_folder)
