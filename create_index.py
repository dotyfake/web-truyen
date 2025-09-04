#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo file index.json cho web đọc truyện với giao diện đồ họa (GUI).
Tác giả: Gemini (dựa trên script gốc)
Mô tả: Quét thư mục mẹ chứa các thư mục truyện, tự động tạo file index.json
cho các truyện chưa có, hoặc ghi đè nếu được chọn.
"""

import os
import json
import re
import threading
import queue
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# --- Imports cho GUI ---
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext

# ==============================================================================
# PHẦN LOGIC CỐT LÕI (Không thay đổi nhiều so với bản gốc)
# ==============================================================================

def extract_title_from_content(file_path: str) -> Optional[str]:
    """Trích xuất title từ nội dung file markdown."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        chapter_pattern = re.compile(r'.*(chương|chapter).*', re.IGNORECASE | re.UNICODE)
        for line in lines[:20]:
            line = line.strip()
            if not line:
                continue
            clean_line = re.sub(r'^#+\s*', '', line).strip()
            if chapter_pattern.search(clean_line):
                return clean_line
    except Exception:
        return None
    return None

def get_title_from_filename(filename: str) -> str:
    """Tạo title từ tên file."""
    name = os.path.splitext(filename)[0]
    name = re.sub(r'[-_]', ' ', name)
    name = ' '.join(word.capitalize() for word in name.split())
    return name

def scan_folder(folder_path: str, log_queue: queue.Queue) -> List[Dict[str, any]]:
    """
    Quét thư mục và tạo danh sách chương.
    Hàm này đã được sửa để thêm thuộc tính 'index'.
    """
    chapters = []
    folder = Path(folder_path)
    if not folder.exists():
        log_queue.put(f"Lỗi: Thư mục không tồn tại: {folder_path}")
        return chapters

    md_files = sorted(
        list(folder.glob("*.md")),
        key=lambda f: int(re.search(r'\d+', f.stem).group() or 0) if re.search(r'\d+', f.stem) else 99999
    )

    if not md_files:
        log_queue.put(f"  -> Cảnh báo: Không tìm thấy file .md nào trong: {folder.name}")
        return chapters

    log_queue.put(f"  -> Tìm thấy {len(md_files)} file markdown. Đang xử lý...")
    
    for i, md_file in enumerate(md_files):
        filename = md_file.name
        title = extract_title_from_content(str(md_file)) or get_title_from_filename(filename)
        
        chapters.append({
            "index": i,  # Thuộc tính index để sắp xếp chính xác
            "title": title,
            "file": filename
        })
    return chapters

# ==============================================================================
# PHẦN LOGIC XỬ LÝ BATCH (Đã được sửa đổi)
# ==============================================================================

def create_index_for_story(story_folder_path: str, log_queue: queue.Queue) -> bool:
    """
    Tạo file index.json cho một thư mục truyện cụ thể (không tương tác).
    """
    try:
        chapters = scan_folder(story_folder_path, log_queue)
        if not chapters:
            log_queue.put(f"  -> Bỏ qua tạo index cho '{os.path.basename(story_folder_path)}' vì không có chương.")
            return False

        folder_name = os.path.basename(story_folder_path)
        auto_title = get_title_from_filename(folder_name)
        description = f"Truyện {len(chapters)} chương"

        index_data = {
            "title": auto_title,
            "description": description,
            "folder": folder_name,
            "chapters": chapters,
            "total": len(chapters),
            "created_by": "auto_script_v2",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }

        output_path = os.path.join(story_folder_path, "index.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)

        log_queue.put(f"  -> ✅ Đã tạo thành công index.json cho '{folder_name}' với {len(chapters)} chương.")
        return True
    except Exception as e:
        log_queue.put(f"  -> ❌ Lỗi khi tạo index cho '{os.path.basename(story_folder_path)}': {e}")
        return False

def process_parent_directory(parent_path: str, overwrite: bool, log_queue: queue.Queue):
    """
    Hàm chính để quét thư mục mẹ và xử lý các thư mục con.
    """
    log_queue.put("="*60)
    log_queue.put(f"🚀 Bắt đầu quét thư mục: {parent_path}")
    log_queue.put(f"Tùy chọn ghi đè: {'Bật' if overwrite else 'Tắt'}")
    log_queue.put("="*60)

    parent = Path(parent_path)
    if not parent.is_dir():
        log_queue.put("Lỗi: Đường dẫn đã chọn không phải là một thư mục.")
        log_queue.put("Hoàn thành với lỗi.")
        return

    story_folders = [d for d in parent.iterdir() if d.is_dir() and not d.name.startswith('.')]
    if not story_folders:
        log_queue.put("Không tìm thấy thư mục truyện nào trong thư mục đã chọn.")
        log_queue.put("Hoàn thành.")
        return

    log_queue.put(f"Tìm thấy {len(story_folders)} thư mục truyện. Bắt đầu xử lý...")
    success_count = 0
    skipped_count = 0
    
    for i, folder in enumerate(story_folders, 1):
        log_queue.put(f"\n({i}/{len(story_folders)}) Đang xử lý thư mục: {folder.name}")
        index_file = folder / "index.json"
        
        if index_file.exists() and not overwrite:
            log_queue.put("  -> index.json đã tồn tại. Bỏ qua.")
            skipped_count += 1
            continue

        if create_index_for_story(str(folder), log_queue):
            success_count += 1
    
    log_queue.put("\n" + "="*60)
    log_queue.put("🎉 Xử lý hoàn tất!")
    log_queue.put(f"- Tạo/Cập nhật thành công: {success_count} truyện.")
    log_queue.put(f"- Bỏ qua (đã có index): {skipped_count} truyện.")
    log_queue.put("="*60)


# ==============================================================================
# PHẦN GIAO DIỆN ĐỒ HỌA (GUI) VỚI TKINTER
# ==============================================================================

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Công Cụ Tạo Index Truyện")
        self.master.geometry("800x600")
        self.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.folder_path = tk.StringVar()
        self.overwrite_var = tk.BooleanVar(value=False)
        self.log_queue = queue.Queue()
        
        self.create_widgets()
        self.process_log_queue()

    def create_widgets(self):
        # --- Frame chọn thư mục ---
        folder_frame = ttk.LabelFrame(self, text="1. Chọn thư mục mẹ chứa truyện")
        folder_frame.pack(fill="x", padx=5, pady=5)

        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path, state="readonly", width=80)
        folder_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        browse_btn = ttk.Button(folder_frame, text="Chọn Thư Mục...", command=self.select_folder)
        browse_btn.pack(side="left", padx=5, pady=5)

        # --- Frame tùy chọn và thực thi ---
        action_frame = ttk.LabelFrame(self, text="2. Tùy chọn và Thực thi")
        action_frame.pack(fill="x", padx=5, pady=5)
        
        overwrite_check = ttk.Checkbutton(action_frame, text="Ghi đè file index.json đã có", variable=self.overwrite_var)
        overwrite_check.pack(side="left", padx=5, pady=10)
        
        self.run_button = ttk.Button(action_frame, text="Bắt Đầu Quét & Tạo Index", command=self.start_processing)
        self.run_button.pack(side="right", padx=5, pady=10)

        # --- Frame hiển thị log ---
        log_frame = ttk.LabelFrame(self, text="3. Tiến trình")
        log_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state="disabled", font=("Courier New", 10))
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)

    def select_folder(self):
        path = filedialog.askdirectory(title="Chọn thư mục mẹ chứa các thư mục truyện")
        if path:
            self.folder_path.set(path)

    def start_processing(self):
        path = self.folder_path.get()
        if not path:
            self.log("Lỗi: Vui lòng chọn một thư mục trước.", error=True)
            return

        self.log_text.config(state="normal")
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state="disabled")
        
        self.run_button.config(state="disabled", text="Đang xử lý...")
        
        # Chạy tác vụ nặng trong một thread riêng để không làm treo GUI
        thread = threading.Thread(
            target=self.run_task_in_thread,
            args=(path, self.overwrite_var.get()),
            daemon=True
        )
        thread.start()

    def run_task_in_thread(self, path, overwrite):
        """Hàm này sẽ được thực thi trong thread riêng biệt."""
        try:
            process_parent_directory(path, overwrite, self.log_queue)
        except Exception as e:
            self.log_queue.put(f"\nLỖI NGOẠI LỆ: {e}")
        finally:
            # Báo cho main thread biết là đã xong
            self.log_queue.put("TASK_COMPLETE")

    def process_log_queue(self):
        """Kiểm tra queue và cập nhật log trên GUI."""
        try:
            while True:
                message = self.log_queue.get_nowait()
                if message == "TASK_COMPLETE":
                    self.run_button.config(state="normal", text="Bắt Đầu Quét & Tạo Index")
                else:
                    self.log(message)
        except queue.Empty:
            pass
        finally:
            self.master.after(100, self.process_log_queue)

    def log(self, message: str, error=False):
        """Ghi log vào ScrolledText widget."""
        self.log_text.config(state="normal")
        if error:
            self.log_text.insert(tk.END, f"LỖI: {message}\n")
        else:
            self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END) # Tự động cuộn xuống cuối
        self.log_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()