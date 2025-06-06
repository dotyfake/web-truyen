import os
import re
from pathlib import Path

def process_markdown_file(md_file_path):
    """
    Hàm xử lý một file markdown duy nhất: đọc, tạo front matter và ghi lại.
    """
    try:
        # --- Bước 1: Đọc nội dung file và kiểm tra xem đã có front matter chưa ---
        with open(md_file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
            # Đưa con trỏ về đầu file để đọc lại dòng đầu tiên
            f.seek(0) 
            first_line = f.readline().strip()

        if first_line == '---':
            print(f"  [BỎ QUA] File '{md_file_path.name}' đã có Front Matter.")
            return False

        # --- Bước 2: Trích xuất thông tin từ tên file và thư mục ---
        
        # Tên truyện (slug) là tên của thư mục cha
        story_slug = md_file_path.parent.name

        # Tên file không bao gồm phần mở rộng (.md)
        filename_stem = md_file_path.stem
        
        # Title sẽ là tên file, thay gạch ngang bằng dấu cách và viết hoa chữ cái đầu
        title = filename_stem.replace('-', ' ').replace('_', ' ').capitalize()

        # Tìm số chương đầu tiên trong tên file
        chapter_match = re.search(r'\d+', filename_stem)
        if not chapter_match:
            print(f"  [LỖI] Không tìm thấy số chương trong tên file '{md_file_path.name}'. Bỏ qua.")
            return False
        chapter_number = int(chapter_match.group(0))

        # layout: giá trị cố định
        layout = "chapter.njk"

        # permalink: tạo đường dẫn URL đẹp
        permalink = f"/truyen/{story_slug}/chuong-{chapter_number}/"

        # --- Bước 3: Tạo khối Front Matter ---
        front_matter = f"""---
title: "{title}"
story: "{story_slug}"
chapterNumber: {chapter_number}
layout: "{layout}"
permalink: "{permalink}"
---

"""
        # --- Bước 4: Kết hợp Front Matter và nội dung gốc rồi ghi lại file ---
        new_content = front_matter + original_content
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  [THÀNH CÔNG] Đã thêm Front Matter cho file '{md_file_path.name}'.")
        return True

    except Exception as e:
        print(f"  [LỖI] Đã xảy ra lỗi khi xử lý file {md_file_path.name}: {e}")
        return False


def main():
    """
    Hàm chính để chạy chương trình, nhận input từ người dùng và duyệt thư mục.
    """
    print("="*50)
    print("SCRIPT TỰ ĐỘNG THÊM FRONT MATTER CHO FILE TRUYỆN (.md)")
    print("="*50)
    
    # Lấy đường dẫn từ người dùng
    target_dir = input(">> Vui lòng nhập đường dẫn tới thư mục chứa các bộ truyện: ").strip()

    # Chuyển đổi thành đối tượng Path để xử lý dễ dàng hơn
    root_path = Path(target_dir)

    # Kiểm tra xem đường dẫn có hợp lệ không
    if not root_path.is_dir():
        print(f"\n[LỖI] Đường dẫn '{target_dir}' không tồn tại hoặc không phải là một thư mục.")
        return

    print(f"\nBắt đầu quét thư mục '{root_path}'...\n")
    
    processed_count = 0
    # Dùng rglob để quét đệ quy tất cả các file .md
    all_md_files = list(root_path.rglob('*.md'))

    if not all_md_files:
        print("Không tìm thấy file .md nào trong thư mục được chỉ định.")
        return

    for md_file in all_md_files:
        print(f"Đang xử lý file: {md_file}")
        if process_markdown_file(md_file):
            processed_count += 1
            
    print("\n-------------------------------------------------")
    print("Hoàn tất!")
    print(f"Tổng cộng đã xử lý và thêm Front Matter cho {processed_count} file.")
    print("-------------------------------------------------")


if __name__ == "__main__":
    main()