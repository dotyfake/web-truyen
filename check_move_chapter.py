import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def browse_source():
    directory = filedialog.askdirectory()
    entry_source.delete(0, tk.END)
    entry_source.insert(0, directory)

def browse_dest():
    directory = filedialog.askdirectory()
    entry_dest.delete(0, tk.END)
    entry_dest.insert(0, directory)

def log_message(message):
    txt_log.insert(tk.END, message + "\n")
    txt_log.see(tk.END)

def process_files():
    source_dir = entry_source.get()
    dest_dir = entry_dest.get()
    search_query = entry_string.get()

    if not source_dir or not dest_dir or not search_query:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ các trường!")
        return

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    txt_log.delete(1.0, tk.END)
    count = 0
    
    try:
        # Lấy danh sách file .md
        files = [f for f in os.listdir(source_dir) if f.endswith('.md')]
        
        if not files:
            log_message("⚠️ Không tìm thấy file .md nào trong thư mục nguồn.")
            return

        for filename in files:
            file_path = os.path.join(source_dir, filename)
            
            # Đọc file với encoding utf-8
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            if search_query in content:
                shutil.move(file_path, os.path.join(dest_dir, filename))
                log_message(f"✅ Đã chuyển: {filename}")
                count += 1
        
        log_message(f"\n--- Hoàn tất! Đã chuyển {count} file. ---")
        messagebox.showinfo("Thành công", f"Đã di chuyển xong {count} file!")
        
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

# Khởi tạo giao diện
root = tk.Tk()
root.title("MD File Filter & Mover")
root.geometry("500x500")

# Giao diện nhập liệu
tk.Label(root, text="Thư mục nguồn (chứa file .md):", font=("Arial", 10, "bold")).pack(pady=(15, 5))
frame_source = tk.Frame(root)
frame_source.pack(fill="x", padx=20) # Sửa px thành padx
entry_source = tk.Entry(frame_source)
entry_source.pack(side="left", fill="x", expand=True, padx=(0, 5))
tk.Button(frame_source, text="Chọn", command=browse_source).pack(side="right")

tk.Label(root, text="Thư mục đích:", font=("Arial", 10, "bold")).pack(pady=(15, 5))
frame_dest = tk.Frame(root)
frame_dest.pack(fill="x", padx=20) # Sửa px thành padx
entry_dest = tk.Entry(frame_dest)
entry_dest.pack(side="left", fill="x", expand=True, padx=(0, 5))
tk.Button(frame_dest, text="Chọn", command=browse_dest).pack(side="right")

tk.Label(root, text="Chuỗi ký tự cần tìm trong file:", font=("Arial", 10, "bold")).pack(pady=(15, 5))
entry_string = tk.Entry(root)
entry_string.pack(fill="x", padx=20, pady=5)

# Nút thực hiện
tk.Button(root, text="BẮT ĐẦU CHUYỂN FILE", bg="#2ecc71", fg="white", 
          font=("Arial", 11, "bold"), height=2, command=process_files).pack(pady=20)

# Khu vực hiển thị log
tk.Label(root, text="Trạng thái hệ thống:").pack()
txt_log = scrolledtext.ScrolledText(root, height=10, bg="#f0f0f0")
txt_log.pack(fill="both", expand=True, padx=20, pady=10)

root.mainloop()