# Chương 2.4. Sao Lưu & Tổ Chức (Backup & Organization): Bảo Vệ Và Sắp Xếp Công Việc

## 1. 📌 Bản Chất & Triết Lý Cốt Lõi (The Core Philosophy)

Sự thật phũ phàng: một bản thảo không được sao lưu không phải tài sản sáng tạo; nó là một tai nạn đang chờ xảy ra.

Người viết thường nghĩ tổ chức file là việc phụ, thấp hơn nghệ thuật. Nhưng khi ổ cứng hỏng, tài khoản cloud lỗi, file bị ghi đè, hoặc bạn không tìm thấy bản đã sửa, không có câu văn đẹp nào cứu được. Bảo vệ bản thảo là một phần của đạo đức nghề nghiệp với chính tác phẩm.

Sao lưu không chỉ chống mất dữ liệu. Tổ chức tốt còn chống mất trí nhớ dự án. Một câu chuyện dài chứa hàng trăm quyết định nhỏ: tên nhân vật phụ, luật thế giới, tuổi, ngày tháng, vật phẩm, lời hứa, chi tiết đã cắt, phản hồi đã nhận. Nếu những thứ này rải rác trong đầu bạn, chúng sẽ rơi rụng khi dự án kéo dài.

Ví dụ từ *Dune* rất rõ: thế giới có chính trị, tôn giáo, sinh thái, kinh tế, thuật ngữ và hệ quyền lực. Nếu viết một dự án tương tự mà không tổ chức tư liệu, người viết sẽ hoặc info-dump vì không biết chọn gì, hoặc mâu thuẫn vì không biết mình đã quyết gì.

Triết lý cốt lõi: hệ thống tổ chức tốt làm cho dự án trở lại được. Dù bạn nghỉ một tuần, một tháng, hay bị gián đoạn bởi đời sống, bạn vẫn biết mở đâu, đọc gì, viết tiếp thế nào.

## 2. ⚙️ Cơ Chế Hoạt Động & Kỹ Thuật Chuyên Sâu (The Mechanics - HYPER DETAILED)

### 2.1. Quy tắc sao lưu 3-2-1 cho nhà văn

Quy tắc cơ bản:

- 3 bản sao.
- 2 loại nơi lưu khác nhau.
- 1 bản nằm ngoài máy chính.

Ví dụ:

- Bản 1: thư mục trên máy.
- Bản 2: cloud đồng bộ.
- Bản 3: file nén hàng tuần trên ổ ngoài hoặc dịch vụ khác.

Nếu bạn chỉ dùng cloud, vẫn có rủi ro: đồng bộ lỗi, xóa nhầm đồng bộ theo, tài khoản bị khóa. Nếu bạn chỉ dùng ổ cứng, rủi ro hỏng máy. Cần phân tán.

### 2.2. Cấu trúc thư mục dự án

Một cấu trúc tối thiểu:

```text
Ten_Du_An/
  00_Admin/
    Timeline.md
    Milestones.md
    Submission_Log.md
  01_Outline/
    Outline_Tong.md
    Danh_Sach_Canh.md
  02_Ban_Thao/
    Draft_0/
    Draft_1/
    Draft_2_Sua_Cau_Truc/
  03_Ghi_Chu/
    Characters.md
    Worldbuilding.md
    Continuity.md
    Payoff.md
  04_Research/
  05_Feedback/
  06_Exports/
  99_Archive/
```

Bạn có thể đơn giản hóa, nhưng các vùng chức năng phải rõ: bản thảo, outline, ghi chú, research, feedback, exports, archive.

### 2.3. Nguyên tắc "một nơi sự thật"

Mỗi loại thông tin quan trọng phải có một nơi chính thức. Nếu tuổi nhân vật nằm trong ba file khác nhau, bạn sẽ mâu thuẫn.

Ví dụ:

- Tuổi, quan hệ, bí mật nhân vật: `Characters.md`.
- Luật thế giới: `Worldbuilding.md`.
- Chi tiết đã gieo và payoff: `Payoff.md`.
- Timeline trong truyện: `Continuity.md`.

Khi bản thảo thay đổi, cập nhật nơi sự thật trong vòng 5 phút sau phiên viết. Đây là khoản đầu tư nhỏ cứu hàng giờ sửa lỗi về sau.

### 2.4. Tổ chức research để không chết chìm

Research cần phục vụ cảnh. Nếu lưu quá nhiều mà không phân loại, tư liệu biến thành kho bụi.

Mỗi ghi chú research nên có:

```text
Chu de:
Ket luan dung duoc:
Canh su dung:
Do tin cay:
Can kiem tra them:
```

Đừng lưu 20 trang về lịch sử tiền tệ nếu cảnh chỉ cần một chi tiết giao dịch. Hãy ghi kết luận dùng được: "Trong chợ ký ức, giá không niêm yết bằng tiền mà bằng độ riêng tư của ký ức."

### 2.5. Lịch bảo trì dữ liệu

Mỗi tuần dành 20-30 phút:

- Kiểm tra file chưa được đặt tên.
- Di chuyển bản xuất vào `Exports`.
- Lưu snapshot nếu vừa sửa lớn.
- Cập nhật `Continuity.md`.
- Nén hoặc sao lưu thư mục dự án.

Phiên bảo trì không phải viết mới, nhưng nó giúp phiên viết mới tuần sau trơn hơn.

## 3. ⚔️ Mổ Xẻ Thực Chiến: Nghiệp Dư vs. Bậc Thầy (Show, Don't Tell)

### 🚫 CÁCH VIẾT TỆ (Nghiệp dư)

> Ghi chú của tôi nằm trong điện thoại, vài trang Google Docs, một file Word, tin nhắn tự gửi, và một cuốn sổ. Tôi nhớ đại khái nên chắc không sao. Bản thảo chính nằm trên laptop. Khi cần sao lưu, tôi copy ra desktop.

Đây là hệ thống chỉ hoạt động khi dự án nhỏ và trí nhớ còn mới. Khi bản thảo dài lên, nó biến thành bãi lầy tìm kiếm.

### ✅ CÁCH VIẾT XUẤT SẮC (Bậc thầy)

> Mỗi dự án có thư mục chuẩn. Bản thảo nằm trong `02_Ban_Thao`, ghi chú chính thức nằm trong `03_Ghi_Chu`. Mỗi Chủ nhật tôi cập nhật continuity, nén toàn bộ dự án thành file ngày tháng, và lưu lên cloud thứ hai. Ý tưởng rời được gom vào inbox, nhưng cuối tuần phải được chuyển vào nơi chính thức hoặc xóa.

Sự khác biệt là bậc thầy không tin trí nhớ dài hạn khi có thể thiết kế hệ thống.

## 4. 🎬 Đa Đạng Case Study & Ứng Dụng Thực Tế (Abundant Examples)

### Case Study 1: *Game of Thrones* và tổ chức thông tin nhân vật

Truyện nhiều gia tộc, huyết thống, liên minh và phản bội cần hồ sơ nhân vật rõ. Nếu một nhân vật phụ xuất hiện lại sau 20 chương, bạn phải biết họ từng gặp ai, biết gì, mất gì, và muốn gì.

Mẫu hồ sơ:

```text
Ten:
Lan dau xuat hien:
Quan he:
Bi mat dang giu:
Lan cuoi xuat hien:
Trang thai hien tai:
Can payoff:
```

### Case Study 2: *Lord of the Mysteries* và tổ chức thuật ngữ/hệ thống

Một thế giới có nghi thức, tổ chức bí mật, năng lực và vật phẩm cần glossary. Nếu thuật ngữ thay đổi lung tung, độc giả mất niềm tin.

Mẫu glossary:

```text
Thuat ngu:
Dinh nghia ngan:
Luat lien quan:
Xuat hien o:
Khong duoc nham voi:
```

### Tình huống ứng dụng 1: Bạn đang có dự án rối file

Đừng tổ chức lại cả đời viết trong một ngày. Làm theo thứ tự:

1. Tạo thư mục dự án chuẩn.
2. Di chuyển bản thảo chính vào trước.
3. Tạo `Continuity.md`.
4. Gom ghi chú rời vào `Inbox.md`.
5. Mỗi ngày xử lý 10 mục trong inbox.

### Tình huống ứng dụng 2: Bạn sợ mất bản thảo

Thiết lập ngay:

- Cloud sync cho thư mục dự án.
- File nén mỗi Chủ nhật.
- Một bản export PDF hoặc DOCX sau mỗi mốc lớn.
- Kiểm tra phục hồi mỗi tháng: thử mở bản backup.

Backup chưa được thử mở vẫn chỉ là niềm tin, chưa phải hệ thống.

## 5. 👉 Đúc Kết & Bài Tập Hành Động (Takeaways & Action Steps)

### 📎 KẾT LUẬN SẮC BÉN

- Sao lưu là bảo hiểm tồn tại của bản thảo; tổ chức là bảo hiểm trí nhớ của dự án.
- Mỗi loại thông tin phải có một nơi sự thật, nếu không continuity sẽ phân rã.
- Hệ thống tổ chức tốt phải giúp bạn quay lại dự án sau gián đoạn mà không mất nửa ngày định hướng.

### 🏋️ BÀI TẬP THỰC HÀNH

1. Tạo cấu trúc thư mục chuẩn cho dự án hiện tại với ít nhất 6 vùng: admin, outline, bản thảo, ghi chú, feedback, exports.

2. Thiết lập quy tắc backup 3-2-1. Ghi rõ ba bản sao của bạn đang nằm ở đâu.

3. Tạo `Inbox.md` cho ghi chú rời. Trong tuần này, mỗi ngày chuyển 10 mục vào nơi chính thức hoặc xóa.
