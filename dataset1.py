import os
import shutil
import random

def split_dataset(image_folder, label_folder, output_folder, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    # 이미지 및 라벨 파일 목록 가져오기
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])
    label_files = sorted([f for f in os.listdir(label_folder) if f.endswith('.txt')])  # 라벨 파일을 .txt로 처리

    # 디버깅: 파일 목록 출력
    print(f"Found {len(image_files)} images and {len(label_files)} labels")

    # 이미지와 라벨 파일이 이름에 맞춰 한 쌍으로 이루어져 있는지 확인
    paired_files = [(img, lbl) for img in image_files for lbl in label_files 
                    if os.path.splitext(img)[0] == os.path.splitext(lbl)[0]]
    
    # 라벨이 없는 배경 이미지 찾기
    background_images = [img for img in image_files if not any(os.path.splitext(img)[0] == os.path.splitext(lbl)[0] for lbl in label_files)]
    
    # 디버깅: 짝이 맞는 파일 목록 출력 및 배경 이미지 개수 출력
    if len(paired_files) == 0:
        print("No matching image-label pairs found!")
    else:
        print(f"Found {len(paired_files)} matching image-label pairs")
    
    print(f"Found {len(background_images)} background images")

    # 데이터셋 섞기
    random.shuffle(paired_files)
    random.shuffle(background_images)

    # 7:2:1 비율로 나누기 (레이블이 있는 이미지와 라벨 파일 쌍)
    total_paired = len(paired_files)
    train_size = int(total_paired * train_ratio)
    val_size = int(total_paired * val_ratio)
    
    train_files = paired_files[:train_size]
    val_files = paired_files[train_size:train_size + val_size]
    test_files = paired_files[train_size + val_size:]

    # 7:2:1 비율로 나누기 (배경 이미지)
    total_background = len(background_images)
    train_bg_size = int(total_background * train_ratio)
    val_bg_size = int(total_background * val_ratio)
    
    train_bg_files = background_images[:train_bg_size]
    val_bg_files = background_images[train_bg_size:train_bg_size + val_bg_size]
    test_bg_files = background_images[train_bg_size + val_bg_size:]

    # 새로운 폴더 구조 설정
    train_img_dir = os.path.join(output_folder, 'images', 'train')
    train_label_dir = os.path.join(output_folder, 'labels', 'train')
    val_img_dir = os.path.join(output_folder, 'images', 'val')
    val_label_dir = os.path.join(output_folder, 'labels', 'val')
    test_img_dir = os.path.join(output_folder, 'images', 'test')
    test_label_dir = os.path.join(output_folder, 'labels', 'test')

    os.makedirs(train_img_dir, exist_ok=True)
    os.makedirs(train_label_dir, exist_ok=True)
    os.makedirs(val_img_dir, exist_ok=True)
    os.makedirs(val_label_dir, exist_ok=True)
    os.makedirs(test_img_dir, exist_ok=True)
    os.makedirs(test_label_dir, exist_ok=True)

    # 라벨이 있는 파일을 각각의 폴더로 복사
    for img, lbl in train_files:
        shutil.copy(os.path.join(image_folder, img), os.path.join(train_img_dir, img))
        shutil.copy(os.path.join(label_folder, lbl), os.path.join(train_label_dir, lbl))

    for img, lbl in val_files:
        shutil.copy(os.path.join(image_folder, img), os.path.join(val_img_dir, img))
        shutil.copy(os.path.join(label_folder, lbl), os.path.join(val_label_dir, lbl))

    for img, lbl in test_files:
        shutil.copy(os.path.join(image_folder, img), os.path.join(test_img_dir, img))
        shutil.copy(os.path.join(label_folder, lbl), os.path.join(test_label_dir, lbl))

    # 배경 이미지를 각각의 폴더로 복사 (라벨이 없는 이미지)
    for img in train_bg_files:
        shutil.copy(os.path.join(image_folder, img), os.path.join(train_img_dir, img))

    for img in val_bg_files:
        shutil.copy(os.path.join(image_folder, img), os.path.join(val_img_dir, img))

    for img in test_bg_files:
        shutil.copy(os.path.join(image_folder, img), os.path.join(test_img_dir, img))

    print(f"Dataset split completed: {train_size} train, {len(val_files)} val, {len(test_files)} test")
    print(f"Background images split: {len(train_bg_files)} train, {len(val_bg_files)} val, {len(test_bg_files)} test")

# 사용 예시
image_folder = 'D:/roas_dataset2/txt_conversion/images/train'  # 이미지가 저장된 폴더 경로
label_folder = 'D:/roas_dataset2/txt_conversion/labels/train'  # 라벨 파일이 저장된 폴더 경로 (txt)
output_folder = 'D:/roas_dataset2'  # 결과가 저장될 폴더 경로

split_dataset(image_folder, label_folder, output_folder)
