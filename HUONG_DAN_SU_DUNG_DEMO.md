# 📖 Hướng Dẫn Sử Dụng Demo - CS229 WSD Project

## 🎯 Tổng Quan

Demo này là một ứng dụng web tương tác để trình bày đồ án **Word Sense Disambiguation (WSD)** - Gán Nhãn Nghĩa Của Từ. Demo bao gồm 5 tab chính, mỗi tab phục vụ một mục đích cụ thể trong đồ án.

---

## 📑 Các Tab Chính

### 1️⃣ **Tab "Tổng Quan"** 📊

#### Mục đích:
- Hiển thị thống kê tổng quan về dự án
- Giới thiệu đoạn văn bản Privacy Policy được sử dụng

#### Nội dung hiển thị:

**Thống kê (6 cards):**
- **📝 Ký tự văn bản**: Số ký tự trong đoạn Privacy Policy (1,682 ký tự)
- **🏷️ Từ được gán nhãn**: Số từ đã được gán nhãn nghĩa (82 từ)
- **🎯 MFS Accuracy**: Độ chính xác của mô hình MFS Baseline (76.83%)
- **🧠 Tri thức gốc**: Số facts trong Knowledge Base gốc (26 facts)
- **🔗 Tri thức bổ sung**: Số facts được bổ sung từ WordNet (271 facts)
- **❓ Câu truy vấn**: Số câu truy vấn Prolog (8 câu)

**Đoạn văn bản:**
- Hiển thị toàn bộ đoạn Privacy Policy của Google
- Đây là văn bản nguồn được sử dụng để trích xuất tri thức

#### Cách sử dụng:
- Chỉ cần xem, không có tương tác
- Giúp người xem hiểu tổng quan về quy mô và kết quả của dự án

---

### 2️⃣ **Tab "WSD"** 🏷️ (Word Sense Disambiguation)

#### Mục đích:
- Tra cứu nghĩa của từ tiếng Anh
- So sánh hiệu suất giữa 2 mô hình WSD
- Xem danh sách các từ đã được gán nhãn

#### Tính năng 1: **Tra cứu nghĩa từ** 🔍

**Cách sử dụng:**
1. Nhập từ tiếng Anh vào ô "Nhập từ" (ví dụ: `policy`, `information`, `privacy`)
2. Chọn loại từ (Part of Speech):
   - **Danh từ (n)** - noun
   - **Động từ (v)** - verb
   - **Tính từ (a)** - adjective
   - **Trạng từ (r)** - adverb
3. Click nút **"Tra cứu"**

**Kết quả hiển thị:**
- **MFS (Most Frequent Sense)**: Nghĩa phổ biến nhất của từ
- **Danh sách các nghĩa** (tối đa 5 nghĩa):
  - Tên synset (ví dụ: `policy.n.01`)
  - Định nghĩa chi tiết
  - Ví dụ sử dụng
  - Các từ đồng nghĩa (lemmas)

**Ví dụ thực tế** (từ ảnh chụp màn hình):
```
Từ: "policy" (n)
Kết quả: 3 nghĩa được tìm thấy

✓ MFS: policy.n.01
  Định nghĩa: a plan of action adopted by an individual or social group
  Ví dụ: "it was a policy of retribution"

  policy.n.02
  Định nghĩa: a line of argument rationalizing the course of action of a government
  Ví dụ: "they debated the policy or impolicy of the proposed legislation"

  policy.n.03
  Định nghĩa: written contract or certificate of insurance
```

**Tác dụng:**
- Hiểu rõ các nghĩa khác nhau của một từ
- Thấy được nghĩa nào được chọn bởi mô hình MFS
- Hỗ trợ việc giải thích kết quả WSD

---

#### Tính năng 2: **So sánh MFS vs BERT+SVM** 📊

**Hiển thị:**
- Bảng so sánh hiệu suất của 2 mô hình:
  - **MFS Baseline**: Mô hình đơn giản, chọn nghĩa phổ biến nhất
  - **BERT+SVM**: Mô hình học máy sử dụng BERT embeddings

**Các chỉ số:**
- **Accuracy**: Độ chính xác tổng thể
- **Đúng/Tổng**: Số từ dự đoán đúng / Tổng số từ
- **F1 Score (weighted)**: Điểm F1 có trọng số
- **Precision (macro)**: Độ chính xác trung bình
- **Recall (macro)**: Độ phủ trung bình

**Tác dụng:**
- So sánh hiệu quả của 2 phương pháp WSD
- Chứng minh đã thử nghiệm nhiều mô hình
- Phân tích ưu nhược điểm của từng phương pháp

---

#### Tính năng 3: **Danh sách từ đã gán nhãn** 📋

**Hiển thị:**
- Bảng danh sách 82 từ đã được gán nhãn thủ công
- Mỗi từ có:
  - **Lemma**: Dạng gốc của từ
  - **POS**: Loại từ (n/v/a/r)
  - **Synset**: Nghĩa được gán (ví dụ: `information.n.01`)
  - **FOL Predicate**: Vị từ logic bậc nhất tương ứng

**Tác dụng:**
- Xem ground truth (dữ liệu chuẩn) để đánh giá mô hình
- Hiểu cách ánh xạ từ nghĩa của từ sang biểu diễn logic

---

### 3️⃣ **Tab "Tri Thức"** 🧠 (Knowledge Base)

#### Mục đích:
- Hiển thị tri thức đã được trích xuất từ đoạn văn bản
- Biểu diễn tri thức dưới 2 dạng: Prolog và FOL

#### Tính năng 1: **Knowledge Base (Prolog)** 📜

**Hiển thị:**
- Danh sách 26 facts Prolog được trích xuất từ văn bản
- Ví dụ các facts:
  ```prolog
  company(google).
  collects(google, information).
  uses_for(google, provide_services).
  uses_technology(google, cookies).
  has_policy(google, privacy_policy).
  ```

**Tác dụng:**
- Thể hiện cách biểu diễn tri thức dưới dạng logic
- Cơ sở để thực hiện truy vấn Prolog
- Chứng minh đã hoàn thành phần biểu diễn tri thức

---

#### Tính năng 2: **First-Order Logic (FOL)** 📐

**Hiển thị:**
- Biểu diễn các facts dưới dạng logic bậc nhất
- Ví dụ:
  ```
  ∀x (Company(x) ∧ x = Google → Collects(x, Information))
  ∀x (Company(x) → UsesFor(x, ProvideServices))
  ```

**Tác dụng:**
- Thể hiện cách chuyển đổi từ Prolog sang FOL
- Phục vụ mục đích học thuật và trình bày

---

### 4️⃣ **Tab "Truy Vấn"** ❓ (Query Execution)

#### Mục đích:
- Thực thi các câu truy vấn trên Knowledge Base
- Kiểm chứng tính đúng đắn của tri thức đã biểu diễn

#### Tính năng 1: **Thực thi truy vấn** 🔎

**Cách sử dụng:**
1. Nhập tên predicate vào ô truy vấn
2. Click nút **"Truy vấn"**

**Các loại truy vấn hỗ trợ:**

**A. Truy vấn đơn giản (chỉ tên predicate):**
```
collects          → Tìm tất cả facts có dạng collects(X, Y)
uses_for          → Tìm tất cả facts có dạng uses_for(X, Y)
technology        → Tìm tất cả facts có dạng technology(X)
```

**B. Truy vấn có tham số:**
```
collects(google, X)     → Tìm tất cả thông tin mà Google thu thập
uses_for(google, X)     → Tìm mục đích Google sử dụng dữ liệu
```

**Kết quả hiển thị** (từ ảnh chụp màn hình):
```
Query: collects(google, X)
Tìm thấy 2 kết quả:

collects(google, information).
collects(google, personal_information).
```

**Tác dụng:**
- Truy vấn thông tin từ Knowledge Base
- Kiểm chứng tính chính xác của tri thức
- Demo khả năng suy luận logic

---

#### Tính năng 2: **Danh sách câu hỏi mẫu** 📋

**Hiển thị:**
- 8 câu hỏi mẫu đã được định nghĩa sẵn
- Mỗi câu hỏi bao gồm:
  - **ID**: Mã số câu hỏi (Q1-Q8)
  - **Question**: Câu hỏi bằng tiếng Anh/Việt
  - **Prolog Query**: Câu truy vấn Prolog tương ứng
  - **Answer Shape**: Dạng kết quả mong đợi

**Ví dụ:**
```
Q1: What does Google collect?
Prolog: collects(google, X)
Answer: List of items
```

**Cách sử dụng:**
- Click vào một câu hỏi mẫu để tự động điền vào ô truy vấn
- Hoặc tham khảo để viết truy vấn tương tự

**Tác dụng:**
- Hướng dẫn cách viết truy vấn Prolog
- Chứng minh đã hoàn thành 8 câu truy vấn theo yêu cầu đồ án

---

### 5️⃣ **Tab "WordNet"** 🔗 (WordNet Augmentation)

#### Mục đích:
- Hiển thị tri thức bổ sung từ WordNet
- Mở rộng Knowledge Base với synonyms và hypernyms

#### Hiển thị:

**Thống kê:**
- **Từ đồng nghĩa (Synonyms)**: Số lượng quan hệ synonym
- **Quan hệ is_a (Hypernyms)**: Số lượng quan hệ is_a

**Danh sách chi tiết:**

**A. Synonyms (Từ đồng nghĩa):**
```prolog
synonym(privacy, privateness).
synonym(privacy, seclusion).
synonym(information, data).
synonym(service, service_of_process).
```

**B. Hypernyms (Quan hệ is_a):**
```prolog
is_a(privacy, reclusiveness).
is_a(information, knowledge).
is_a(service, work).
is_a(policy, plan_of_action).
```

**Tác dụng:**
- Mở rộng tri thức từ 26 facts lên 271 facts
- Tăng khả năng truy vấn với từ đồng nghĩa
- Chứng minh đã sử dụng WordNet để augmentation

---

## 🎓 Tổng Kết Công Dụng Của Demo

### 1. **Cho Giảng Viên/Người Chấm:**
- ✅ Xem toàn bộ kết quả đồ án một cách trực quan
- ✅ Kiểm tra tính đúng đắn của WSD, Knowledge Base, và Queries
- ✅ Đánh giá chất lượng qua các chỉ số (accuracy, F1, precision, recall)
- ✅ Tương tác trực tiếp với các tính năng thay vì đọc code

### 2. **Cho Sinh Viên/Người Thuyết Trình:**
- ✅ Trình bày đồ án một cách chuyên nghiệp
- ✅ Demo trực tiếp các tính năng trong buổi bảo vệ
- ✅ Giải thích dễ hiểu hơn so với slides
- ✅ Trả lời câu hỏi bằng cách demo thực tế

### 3. **Cho Người Học/Nghiên Cứu:**
- ✅ Hiểu rõ cách hoạt động của WSD
- ✅ Học cách biểu diễn tri thức bằng Prolog và FOL
- ✅ Thực hành viết truy vấn logic
- ✅ Tham khảo cách xây dựng demo cho đồ án

---

## 💡 Tips Sử Dụng Demo Hiệu Quả

### Khi Thuyết Trình:

1. **Bắt đầu với Tab "Tổng Quan"**
   - Giới thiệu quy mô dự án
   - Cho xem đoạn văn bản nguồn

2. **Chuyển sang Tab "WSD"**
   - Demo tra cứu một vài từ quan trọng (policy, information, privacy)
   - Giải thích kết quả MFS
   - So sánh hiệu suất 2 mô hình

3. **Tab "Tri Thức"**
   - Hiển thị Knowledge Base
   - Giải thích cách biểu diễn Prolog và FOL

4. **Tab "Truy Vấn"**
   - Thực thi 2-3 câu truy vấn mẫu
   - Giải thích kết quả
   - Cho phép người xem đặt câu hỏi và truy vấn trực tiếp

5. **Tab "WordNet"**
   - Hiển thị cách mở rộng tri thức
   - Giải thích tầm quan trọng của augmentation

### Khi Trả Lời Câu Hỏi:

- **"WSD hoạt động như thế nào?"** → Tab WSD, demo tra cứu từ
- **"Có bao nhiêu facts?"** → Tab Tổng Quan, chỉ số thống kê
- **"Truy vấn như thế nào?"** → Tab Truy Vấn, thực thi trực tiếp
- **"Độ chính xác bao nhiêu?"** → Tab WSD, bảng so sánh

---

## 🔧 Lưu Ý Kỹ Thuật

### Yêu cầu:
- Python 3.8+
- Các thư viện trong `requirements.txt`
- NLTK WordNet data

### Khởi động:
```bash
.\run_demo.ps1
# hoặc
python -m uvicorn demo.main:app --reload --port 8000
```

### Truy cập:
```
http://127.0.0.1:8000
```

### Dừng server:
```
Ctrl + C
```

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra server đã chạy chưa
2. Kiểm tra port 8000 có bị chiếm không
3. Xem console log để debug
4. Đọc file `HUONG_DAN_CHAY_DEMO.md` để biết cách khắc phục lỗi

---

**Chúc bạn thuyết trình thành công! 🎉**
