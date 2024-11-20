import os

# 클래스 매핑: 필터링할 클래스와 변경된 클래스 번호
class_mapping = {
    0: 0,  # smallship
    4: 1,  # smallcar
    7: 2,  # train
    17: 3, # indiviualcontainer
    18: 4  # groupcontainer
}

# 사용할 클래스 목록
valid_classes = set(class_mapping.keys())

def remap_and_filter_labels_in_txt_files(txt_folder, output_folder):
    # 폴더 내의 모든 txt 파일 목록 가져오기
    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]

    # 출력 폴더가 존재하지 않으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 각 txt 파일을 처리
    for txt_file in txt_files:
        txt_path = os.path.join(txt_folder, txt_file)

        # txt 파일 읽기
        with open(txt_path, 'r') as file:
            lines = file.readlines()

        # 각 줄의 첫 번째 값(클래스 ID)을 필터링 및 리맵핑
        filtered_lines = []
        for line in lines:
            parts = line.split()  # 문자열을 공백으로 분리
            if len(parts) > 0:
                class_id = int(parts[0])
                # 유효한 클래스인지 확인 후 리맵핑
                if class_id in valid_classes:
                    parts[0] = str(class_mapping[class_id])  # 클래스 번호 변경
                    filtered_lines.append(' '.join(parts) + '\n')  # 다시 하나의 문자열로 결합

        # 파일이 비어있지 않으면, 출력 폴더에 저장
        if filtered_lines:
            output_txt_path = os.path.join(output_folder, txt_file)
            with open(output_txt_path, 'w') as file:
                file.writelines(filtered_lines)
            print(f"Processed file: {output_txt_path}")
        else:
            # 내용이 없으면 파일 삭제
            print(f"Deleting empty file: {txt_file}")

# 사용 예시
txt_folder = 'D:/roas_dataset1/labels/test'  # 원본 txt 파일이 있는 폴더 경로
output_folder = 'D:/roas_dataset1/class_5_label/test'  # 결과를 저장할 폴더 경로
remap_and_filter_labels_in_txt_files(txt_folder, output_folder)

