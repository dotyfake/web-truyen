#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo file index.json cho web đọc truyện
Tác giả: Script tự động
Mô tả: Quét thư mục chứa file .md và tạo index.json với danh sách chương
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import argparse

def extract_title_from_content(file_path: str) -> Optional[str]:
    """
    Trích xuất title từ nội dung file markdown
    Tìm dòng chứa từ khóa 'chương' hoặc 'chapter' (không phân biệt hoa thường)
    
    Args:
        file_path: Đường dẫn đến file markdown
        
    Returns:
        Title nếu tìm thấy, None nếu không tìm thấy
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        # Tìm dòng chứa "chương" hoặc "chapter"
        chapter_pattern = re.compile(r'.*(chương|chapter).*', re.IGNORECASE | re.UNICODE)
        
        for line in lines[:20]:  # Chỉ tìm trong 20 dòng đầu
            line = line.strip()
            if not line:
                continue
                
            # Loại bỏ markdown formatting
            clean_line = re.sub(r'^#+\s*', '', line)  # Loại bỏ # ## ###
            clean_line = re.sub(r'\*+', '', clean_line)  # Loại bỏ **bold**
            clean_line = clean_line.strip()
            
            if chapter_pattern.search(clean_line):
                return clean_line
                
    except Exception as e:
        print(f"Lỗi khi đọc file {file_path}: {e}")
        
    return None

def get_title_from_filename(filename: str) -> str:
    """
    Tạo title từ tên file
    
    Args:
        filename: Tên file (không bao gồm extension)
        
    Returns:
        Title được format từ tên file
    """
    # Loại bỏ extension
    name = os.path.splitext(filename)[0]
    
    # Thay thế dấu gạch ngang và gạch dưới bằng khoảng trắng
    name = re.sub(r'[-_]', ' ', name)
    
    # Capitalize các từ
    name = ' '.join(word.capitalize() for word in name.split())
    
    return name

def scan_folder(folder_path: str) -> List[Dict[str, str]]:
    """
    Quét thư mục và tạo danh sách chương
    
    Args:
        folder_path: Đường dẫn đến thư mục chứa file .md
        
    Returns:
        Danh sách các chapter với title và file
    """
    chapters = []
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"Thư mục không tồn tại: {folder_path}")
        return chapters
    
    # Lấy tất cả file .md và sắp xếp theo số thứ tự tự nhiên
    md_files = list(folder.glob("*.md"))
    
    # Sắp xếp theo số thứ tự tự nhiên thay vì alphabetical
    def natural_sort_key(file_path):
        # Trích xuất số từ tên file
        filename = file_path.stem
        numbers = re.findall(r'\d+', filename)
        if numbers:
            return int(numbers[0])  # Lấy số đầu tiên
        return 0
    
    md_files.sort(key=natural_sort_key)
    
    if not md_files:
        print(f"Không tìm thấy file .md nào trong thư mục: {folder_path}")
        return chapters
    
    print(f"Tìm thấy {len(md_files)} file markdown:")
    
    for md_file in md_files:
        filename = md_file.name
        print(f"  Đang xử lý: {filename}")
        
        # Thử trích xuất title từ nội dung
        title = extract_title_from_content(str(md_file))
        
        if title:
            print(f"    ✓ Tìm thấy title: {title}")
        else:
            # Sử dụng tên file làm title
            title = get_title_from_filename(filename)
            print(f"    → Sử dụng tên file: {title}")
        
        chapters.append({
            "title": title,
            "file": filename
        })
    
    return chapters

def create_index_json(folder_path: str, output_path: Optional[str] = None) -> bool:
    """
    Tạo file index.json cho thư mục
    
    Args:
        folder_path: Đường dẫn đến thư mục chứa file .md
        output_path: Đường dẫn output (mặc định là folder_path/index.json)
        
    Returns:
        True nếu thành công, False nếu thất bại
    """
    try:
        chapters = scan_folder(folder_path)
        
        if not chapters:
            print("Không có chương nào để tạo index.json")
            return False
        
        folder_name = os.path.basename(folder_path)
        
        # Tự động tạo title và description từ tên folder
        auto_title = get_title_from_filename(folder_name)
        
        # Hỏi người dùng nhập thông tin
        print(f"\n📝 Nhập thông tin cho truyện '{folder_name}':")
        user_title = input(f"Title (Enter để dùng '{auto_title}'): ").strip()
        title = user_title if user_title else auto_title
        
        description = input(f"Mô tả (Enter để tự động): ").strip()
        if not description:
            description = f"Truyện {len(chapters)} chương"
        
        # Tạo cấu trúc JSON với metadata đầy đủ
        index_data = {
            "title": title,
            "description": description,
            "folder": folder_name,
            "chapters": chapters,
            "total": len(chapters),
            "created_by": "auto_script",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        # Xác định đường dẫn output
        if output_path is None:
            output_path = os.path.join(folder_path, "index.json")
        
        # Ghi file JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Đã tạo thành công: {output_path}")
        print(f"📖 Title: {title}")
        print(f"📝 Mô tả: {description}")
        print(f"📊 Tổng số chương: {len(chapters)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi tạo index.json: {e}")
        return False

def main():
    """Hàm chính của script"""
    parser = argparse.ArgumentParser(
        description="Tạo file index.json cho web đọc truyện",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  python create_index.py -f "path/to/truyen-folder"
  python create_index.py -f "truyen-1" -o "custom-index.json"
  python create_index.py --scan-all
        """
    )
    
    parser.add_argument(
        '-f', '--folder',
        type=str,
        help='Đường dẫn đến thư mục chứa file .md'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Đường dẫn file output (mặc định: folder/index.json)'
    )
    
    parser.add_argument(
        '--scan-all',
        action='store_true',
        help='Quét tất cả thư mục con trong thư mục hiện tại'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚀 Script tạo index.json cho web đọc truyện")
    print("=" * 60)
    
    if args.scan_all:
        # Quét tất cả thư mục con
        current_dir = Path('.')
        folders = [d for d in current_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        if not folders:
            print("Không tìm thấy thư mục con nào.")
            return
        
        print(f"Tìm thấy {len(folders)} thư mục:")
        for folder in folders:
            print(f"  📁 {folder.name}")
        
        print("\nBắt đầu xử lý...")
        success_count = 0
        
        for folder in folders:
            print(f"\n📂 Xử lý thư mục: {folder.name}")
            print("-" * 40)
            
            if create_index_json(str(folder)):
                success_count += 1
        
        print(f"\n🎉 Hoàn thành! Đã xử lý thành công {success_count}/{len(folders)} thư mục.")
        
    elif args.folder:
        # Xử lý một thư mục cụ thể
        folder_path = args.folder
        
        if not os.path.exists(folder_path):
            print(f"❌ Thư mục không tồn tại: {folder_path}")
            return
        
        create_index_json(folder_path, args.output)
        
    else:
        # Interactive mode
        print("🔍 Chế độ tương tác")
        print("Các thư mục có sẵn:")
        
        current_dir = Path('.')
        folders = [d for d in current_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        if folders:
            for i, folder in enumerate(folders, 1):
                print(f"  {i}. {folder.name}")
            print(f"  {len(folders) + 1}. Nhập đường dẫn thủ công")
            print(f"  {len(folders) + 2}. Xử lý tất cả thư mục")
        
        try:
            choice = input(f"\nChọn thư mục (1-{len(folders) + 2}): ").strip()
            
            if choice == str(len(folders) + 2):
                # Xử lý tất cả
                success_count = 0
                for folder in folders:
                    print(f"\n📂 Xử lý: {folder.name}")
                    if create_index_json(str(folder)):
                        success_count += 1
                print(f"\n🎉 Hoàn thành! {success_count}/{len(folders)} thư mục.")
                
            elif choice == str(len(folders) + 1):
                # Nhập thủ công
                folder_path = input("Nhập đường dẫn thư mục: ").strip()
                create_index_json(folder_path)
                
            elif choice.isdigit() and 1 <= int(choice) <= len(folders):
                # Chọn thư mục
                selected_folder = folders[int(choice) - 1]
                create_index_json(str(selected_folder))
                
            else:
                print("❌ Lựa chọn không hợp lệ!")
                
        except KeyboardInterrupt:
            print("\n\n👋 Tạm biệt!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()