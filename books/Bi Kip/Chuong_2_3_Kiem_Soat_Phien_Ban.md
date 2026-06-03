# Chương 2.3. Kiểm Soát Phiên Bản (Version Control): Quản Lý Các Bản Nháp Và Bản Sửa Đổi

## 1. 📌 Bản Chất & Triết Lý Cốt Lõi (The Core Philosophy)

Sự thật phũ phàng: người viết không sợ sửa vì họ yếu đuối; họ sợ sửa vì hệ thống lưu phiên bản của họ khiến mọi quyết định lớn giống như một canh bạc.

Nếu bạn chỉ có một file duy nhất và liên tục ghi đè, mỗi lần cắt một chương là một lần mất mát thật. Mỗi lần thử đổi POV là một lần rủi ro. Mỗi lần biên tập viên góp ý sửa hồi 2, bạn do dự vì không biết có quay lại được không. Kiểm soát phiên bản không phải chuyện kỹ thuật khô khan. Nó là điều kiện tâm lý để bạn dám viết lại.

Như 2.2 đã nói, tiến độ thật là bản thảo ít mơ hồ hơn. Version control giúp bạn theo dõi các quyết định đó qua thời gian. Nó trả lời:

- Bản nào mới nhất?
- Bản nào đã gửi cho ai?
- Bản nào là trước khi sửa lớn?
- Thay đổi nào thuộc vòng sửa cấu trúc, thay đổi nào thuộc sửa câu?
- Nếu quyết định sai, quay lại đâu?

Ví dụ từ quá trình phát triển các câu chuyện phức tạp như *Breaking Bad* hoặc *Arcane*: một tuyến nhân vật có thể được điều chỉnh qua nhiều vòng để đạt sức nặng cuối cùng. Nếu không có khả năng thử, so sánh, lùi lại, người viết dễ chọn giải pháp an toàn nhất thay vì giải pháp mạnh nhất.

Triết lý cốt lõi: phiên bản cũ không phải rác; nó là bảo hiểm sáng tạo.

## 2. ⚙️ Cơ Chế Hoạt Động & Kỹ Thuật Chuyên Sâu (The Mechanics - HYPER DETAILED)

### 2.1. Đặt tên file có logic

Tên file tốt phải cho biết dự án, phạm vi, phiên bản hoặc ngày.

Không nên:

```text
truyen.docx
truyen moi.docx
truyen final.docx
truyen final sua.docx
truyen final that.docx
```

Nên:

```text
KyUc_BanThaoDayDu_v01_2026-06-03.docx
KyUc_Chuong07_DauGia_v03_2026-06-10.docx
KyUc_SuaCauTruc_Hoi2_v02_2026-07-01.docx
```

Quy tắc: nếu chỉ nhìn tên file mà không mở, bạn phải biết nó là gì.

### 2.2. Phân biệt vòng sửa

Đừng sửa mọi thứ cùng lúc. Tạo phiên bản theo vòng:

- Draft 0: bản xương, có thể xấu.
- Draft 1: bản thô hoàn chỉnh.
- Draft 2: sửa cấu trúc.
- Draft 3: sửa nhân vật và cảm xúc.
- Draft 4: sửa câu, nhịp, lời thoại.
- Draft 5: proofread và xuất.

Nếu đang Draft 2, đừng mất 40 phút mài một câu trong cảnh có thể bị cắt. Nếu đang Draft 4, đừng tự tiện đổi toàn bộ động cơ phản diện trừ khi phát hiện lỗi chí mạng.

Version control giúp mỗi vòng sửa có phạm vi rõ.

### 2.3. Lưu snapshot trước quyết định lớn

Trước khi làm các việc sau, tạo snapshot:

- Cắt hoặc gộp chương.
- Đổi POV.
- Đổi thứ tự hồi.
- Viết lại động cơ nhân vật chính.
- Thay hệ thống phép thuật/công nghệ.
- Sửa theo phản hồi beta quy mô lớn.

Tên snapshot:

```text
SNAPSHOT_TruocKhi_DoiPOV_Hoi2_2026-06-03
SNAPSHOT_TruocKhi_CatNhanVatMinh_2026-06-12
```

Snapshot cho phép bạn thử táo bạo. Bạn biết đường về.

### 2.4. Quản lý bản đã gửi

Một lỗi phổ biến: sửa tiếp bản thảo sau khi đã gửi beta reader, rồi không biết phản hồi của họ tương ứng với phiên bản nào.

Quy tắc:

- Mọi bản gửi người khác phải có mã phiên bản.
- Không sửa trực tiếp bản đã gửi.
- Lưu phản hồi kèm mã phiên bản.

Ví dụ:

```text
Sent_Beta/
  KyUc_FullDraft_v01_SENT_BetaA_2026-06-03.docx
Feedback/
  BetaA_Feedback_on_v01_2026-06-20.md
```

Khi nhận phản hồi, bạn biết họ đang nói về bản nào.

### 2.5. Nếu dùng Git cho văn bản

Với người quen kỹ thuật, Git có thể hữu ích cho Markdown hoặc plain text. Nhưng đừng dùng Git nếu nó làm bạn sợ viết. Công cụ chỉ tốt khi bạn thật sự dùng được.

Nếu dùng Git, commit theo ý nghĩa:

```text
Add first draft of chapter 7 auction scene
Revise Lan motivation in act two
Cut duplicated mentor scene
```

Commit không cần hoàn hảo; nó cần giúp bạn hiểu lịch sử quyết định.

## 3. ⚔️ Mổ Xẻ Thực Chiến: Nghiệp Dư vs. Bậc Thầy (Show, Don't Tell)

### 🚫 CÁCH VIẾT TỆ (Nghiệp dư)

> Tôi sửa trực tiếp vào file bản thảo chính. Tôi xóa một nhân vật phụ vì thấy thừa. Hai tuần sau tôi nhận ra nhân vật đó giữ một manh mối quan trọng. Tôi không còn bản cũ, nên phải cố nhớ lại các cảnh liên quan.

Đây là cách sửa khiến người viết sợ chính mình. Mỗi quyết định trở thành mất mát không thể hoàn nguyên.

### ✅ CÁCH VIẾT XUẤT SẮC (Bậc thầy)

> Trước khi cắt nhân vật phụ, tôi tạo snapshot `TruocKhi_CatNhanVatHoa`. Tôi ghi lý do cắt: chức năng trùng với Minh, làm chậm hồi 2. Sau khi cắt, tôi cập nhật bảng payoff: manh mối chiếc nhẫn chuyển sang Găng Trắng. Hai tuần sau, nếu thấy mất chiều sâu, tôi có thể mở snapshot để phục hồi hoặc lấy lại một cảnh.

Sự khác biệt không nằm ở việc bậc thầy không sai. Bậc thầy sai có kiểm soát.

## 4. 🎬 Đa Đạng Case Study & Ứng Dụng Thực Tế (Abundant Examples)

### Case Study 1: *The Lord of the Rings* và giá trị của lịch sử bản thảo

Những công trình dài như *The Lord of the Rings* cho thấy bản thảo không sinh ra hoàn chỉnh. Tên gọi, địa lý, quan hệ, huyền thoại, tuyến hành trình đều có thể phát triển qua nhiều lớp. Với người viết hiện đại, lesson rõ ràng: đừng xấu hổ vì bản nháp thay đổi. Hãy lưu lại để thay đổi có trí nhớ.

Ứng dụng:

- Lưu các phiên bản worldbuilding lớn.
- Khi đổi luật thế giới, ghi ngày và lý do.
- Khi đổi tên nhân vật/địa danh, tạo bảng mapping để sửa đồng bộ.

### Case Study 2: *Fullmetal Alchemist* và sự nhất quán qua sửa đổi

Một hệ thống như giả kim thuật cần nhất quán. Nếu trong vòng sửa bạn thêm ngoại lệ mới, nó có thể phá các cảnh trước. Version control giúp bạn biết thay đổi nào ảnh hưởng ngược.

Bảng thay đổi luật:

| Ngày | Thay đổi | Ảnh hưởng chương | Cần sửa ngược |
|---|---|---|---|
| 06-03 | Ký ức tuổi thơ có giá cao hơn | C02, C05, C09 | Thêm setup ở C01 |

### Tình huống ứng dụng 1: Sửa theo beta reader

Đừng mở file và sửa từng comment ngay. Làm ba bước:

1. Lưu bản phản hồi kèm phiên bản.
2. Gom phản hồi theo nhóm: cấu trúc, nhân vật, nhịp, câu.
3. Tạo bản sửa mới chỉ xử lý nhóm lớn trước.

### Tình huống ứng dụng 2: Viết lại chương mở đầu

Tạo ba phiên bản:

- Mở bằng hành động.
- Mở bằng bí ẩn.
- Mở bằng cảm xúc nhân vật.

Đặt tên rõ, đọc sau 48 giờ, chọn bản phục vụ lời hứa thể loại tốt nhất. Đừng xóa hai bản còn lại ngay.

## 5. 👉 Đúc Kết & Bài Tập Hành Động (Takeaways & Action Steps)

### 📎 KẾT LUẬN SẮC BÉN

- Version control là bảo hiểm tâm lý để bạn dám sửa mạnh.
- Mỗi vòng sửa cần phạm vi riêng; đừng mài câu khi cấu trúc còn lung lay.
- Bản gửi người khác phải được đóng phiên bản, nếu không phản hồi sẽ rối.

### 🏋️ BÀI TẬP THỰC HÀNH

1. Đổi tên toàn bộ file bản thảo hiện tại theo cấu trúc: dự án, phạm vi, phiên bản, ngày.

2. Tạo một snapshot trước lần sửa lớn tiếp theo và ghi 3 dòng: sửa gì, vì sao, rủi ro là gì.

3. Lập danh sách các vòng sửa dự kiến cho dự án: cấu trúc, nhân vật, nhịp, câu, proofread. Với mỗi vòng, ghi điều không được làm trong vòng đó.
