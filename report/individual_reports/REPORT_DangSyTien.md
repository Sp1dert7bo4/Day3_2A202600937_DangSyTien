# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Đặng Sỹ Tiến
- **Student ID**: 2A202600937
- **Date**: 2026-06-01

---

## I. Technical Contribution (15 Points)

Trong bài thực hành này, tôi đã đóng góp quan trọng vào việc xây dựng cấu trúc hệ thống ReAct Agent và Chatbot hoạt động ổn định, linh hoạt với các API bên thứ ba dưới các điều kiện giới hạn tài nguyên nghiêm ngặt, đồng thời thiết kế và tối ưu hóa hệ thống Web Demo tương tác hiệu năng cao.

- **Modules Implemented / Modified**:
  - [web_demo.py](file:///c:/Users/Admin/Downloads/Day3_2A202600937_DangSyTien/src/web_demo.py): Tích hợp máy chủ đa luồng `ThreadingHTTPServer` thay cho `HTTPServer` đơn luồng để ngăn chặn hiện tượng treo tải trang web khi Agent đang bận suy luận ReAct. Đồng thời sửa lỗi JavaScript `json.dumps` thành `JSON.stringify` trong tệp [demo.html](file:///c:/Users/Admin/Downloads/Day3_2A202600937_DangSyTien/src/demo.html) để kết nối chat hoạt động trơn tru.
  - [agent.py](file:///c:/Users/Admin/Downloads/Day3_2A202600937_DangSyTien/src/agent/agent.py): Thiết lập cơ chế trì hoãn thông minh có điều kiện: chỉ gọi `time.sleep(12)` khi sử dụng `GeminiProvider` (nhằm tuân thủ giới hạn 5 RPM). Với các Provider khác như DeepSeek hay MIMO, loại bỏ hoàn toàn thời gian ngủ để tăng tốc độ phản hồi gấp **5 lần** (từ 80s xuống còn 15s).
  - [openai_provider.py](file:///c:/Users/Admin/Downloads/Day3_2A202600937_DangSyTien/src/core/openai_provider.py): Cập nhật phương thức khởi tạo (`__init__`) để tự động phát hiện nhà cung cấp dịch vụ được cấu hình (`DEFAULT_PROVIDER` là `mimo`, `deepseek`, hoặc `openai`) và tự động tải API Key cũng như Base URL tương ứng từ file `.env`. Thêm cấu hình thời gian chờ (`timeout=60.0`) cho các yêu cầu HTTP để ngăn ngừa tình trạng treo tiến trình vô hạn.
  - [agent_runner.py](file:///c:/Users/Admin/Downloads/Day3_2A202600937_DangSyTien/agent_runner.py) & [chatbot.py](file:///c:/Users/Admin/Downloads/Day3_2A202600937_DangSyTien/src/chatbot.py): Tái cấu trúc logic khởi tạo LLM thành cơ chế động, lựa chọn đúng lớp Provider (OpenAIProvider vs GeminiProvider) và tự động nạp tham số từ môi trường.
  - [optc_tools.py](file:///c:/Users/Admin/Downloads/Day3_2A202600937_DangSyTien/src/tools/optc_tools.py): Sửa lỗi cú pháp (`SyntaxError`) trong hàm `build_team_plan` liên quan đến việc lồng dấu nháy thoát (escaped quotes) bên trong f-string của Python.
  - [demo.html](file:///c:/Users/Admin/Downloads/Day3_2A202600937_DangSyTien/src/demo.html): Hoàn thiện giao diện Dark Mode lộng lẫy và bổ sung đầy đủ **10 thẻ tướng** có trong `PLAYER_BOX` đồng bộ 100% với cơ sở dữ liệu backend, sửa lỗi hệ của tướng Luffy & Bonney từ `PSY` thành `INT`.

- **Code Highlights**:
  *Giải quyết lỗi nghẽn cổ chai đơn luồng của HTTP server bằng đa luồng (`web_demo.py`):*
  ```python
  from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
  
  def run(port=8000):
      server_address = ("", port)
      httpd = ThreadingHTTPServer(server_address, DashboardHandler)
      httpd.serve_forever()
  ```
  
  *Cơ chế tự động tránh giới hạn tần suất có điều kiện thông minh (`agent.py`):*
  ```python
  if steps > 0 and self.llm.__class__.__name__ == "GeminiProvider":
      import time
      time.sleep(12)  # Chỉ ngủ 12s khi dùng Gemini để tránh lỗi 429
  result = self.llm.generate(conversation, system_prompt=self.get_system_prompt())
  ```

- **Documentation**:
  Lớp `OpenAIProvider` ánh xạ các endpoint tương thích định dạng OpenAI vào giao diện chuẩn `LLMProvider`. ReAct Agent trong `agent.py` điều phối vòng lặp suy luận: nhận yêu cầu từ người dùng, gọi phương thức `generate`, trích xuất hành động (`Action`) bằng biểu thức chính quy (Regex), thực thi hàm Python tương ứng (ví dụ: `search_box`), trả kết quả về dưới dạng `Observation`, và tiếp tục vòng lặp suy luận cho đến khi tìm thấy từ khóa `Final Answer`.

---

## II. Debugging Case Study (10 Points)

Trong quá trình phát triển, tôi đã phân tích và khắc phục thành công bốn lỗi hệ thống nghiêm trọng thông qua hệ thống giám sát và ghi log.

### Case 1: Lỗi quá tải tần suất yêu cầu API (HTTP 429 Resource Exhausted)
- **Problem Description**: Khi chạy ReAct Agent qua nhiều bước lặp liên tục, tiến trình bị sập ngay lập tức ở bước 2 hoặc 3 với lỗi `google.api_core.exceptions.ResourceExhausted: 429`.
- **Log Source**: Sự kiện `LLM_ERROR` được ghi lại trong thư mục `logs/`:
  ```json
  {"timestamp": "2026-06-01T09:14:30.360701", "event": "LLM_ERROR", "data": {"step": 0, "error": "429 You exceeded your current quota... Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 5"}}
  ```
- **Diagnosis**: Agent thực hiện các suy luận ReAct và gọi công cụ liên tiếp trong thời gian rất ngắn (chưa đầy 5 giây mỗi bước). Với API key miễn phí của Google AI Studio, giới hạn tần suất là 5 yêu cầu/phút. Việc gửi liên tục 3-4 yêu cầu đã làm cạn kiệt hạn mức này ngay lập tức.
- **Solution**: Tôi đã chèn một quãng nghỉ 12 giây (`time.sleep(12)`) trước khi gọi LLM ở các bước lặp từ thứ 2 trở đi. Sau đó, tối ưu hóa cơ chế này bằng cách chỉ kích hoạt quãng nghỉ khi sử dụng `GeminiProvider`, giúp các nhà cung cấp khác không có hạn mức 5 RPM (như DeepSeek/MIMO) có thể chạy ở tốc độ tối đa mà không bị lag.

### Case 2: Sập tiến trình ở cuối luồng stream (IndexError)
- **Problem Description**: Khi chạy các cuộc gọi dạng stream từ API bên thứ ba, chương trình bị sập ở cuối cuộc hội thoại với thông báo: `❌ Streaming failed: list index out of range`.
- **Diagnosis**: Nhiều proxy OpenAI gửi một chunk rỗng có danh sách `choices` trống ở cuối luồng stream để báo hiệu kết thúc. Việc truy cập trực tiếp `chunk.choices[0]` mà không kiểm tra độ dài đã gây ra lỗi chỉ mục `IndexError`.
- **Solution**: Tôi đã thêm một lớp bảo vệ điều kiện: `if chunk.choices and len(chunk.choices) > 0` trước khi truy cập chỉ mục, xử lý triệt để lỗi sập luồng.

### Case 3: Treo tải trang Web Demo khi Agent bận suy luận ReAct
- **Problem Description**: Khi người dùng nhập câu hỏi trên Live Chat, việc Refresh trang hoặc chuyển sang các tab khác hoàn toàn bị treo và xoay tròn vô hạn.
- **Diagnosis**: Máy chủ `HTTPServer` tiêu chuẩn là đơn luồng. Khi yêu cầu POST `/api/chat` đang bận gọi API và lặp suy luận ReAct (mất 15-80 giây), luồng chính duy nhất của máy chủ bị chặn cứng (blocked), khiến các yêu cầu GET tải tài nguyên tĩnh như HTML, CSS từ trình duyệt bị nghẽn trong hàng đợi.
- **Solution**: Thay đổi `HTTPServer` thành `ThreadingHTTPServer` trong `web_demo.py`. Máy chủ sẽ xử lý mỗi yêu cầu trên một luồng độc lập mới, giúp giao diện web luôn phản hồi tức thì và mượt mà.

### Case 4: Lỗi cú pháp JavaScript khi gọi API Chat từ giao diện web
- **Problem Description**: Nhập câu hỏi vào khung chat và nhấn gửi, hệ thống báo lỗi đỏ lòm và không gửi được yêu cầu lên server.
- **Diagnosis**: Trong tệp tin [demo.html](file:///c:/Users/Admin/Downloads/Day3_2A202600937_DangSyTien/src/demo.html) tại dòng 1197 sử dụng cú pháp Python `json.dumps` thay vì cú pháp JavaScript chuẩn `JSON.stringify` để gửi payload JSON qua fetch.
- **Solution**: Sửa `json.dumps` thành `JSON.stringify({ query: query })`, giúp tính năng chat hoạt động mượt mà 100%.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1.  **Reasoning**: Khối suy luận `Thought` đóng vai trò như một nháp tư duy (Chain of Thought). Thay vì đưa ra câu trả lời phỏng đoán trực tiếp như Chatbot, Agent đã bóc tách bài toán một cách khoa học: đầu tiên phân tích hệ của địch (STR), nhận định hệ khắc chế (QCK), sau đó tìm kiếm cụ thể các nhân vật khắc chế hiệu ứng khóa chiêu "Ability Bind" và tìm ra Blackbeard (#4562). Quá trình suy luận từng bước này giúp đảm bảo tính chính xác vượt trội của kết quả đề xuất.
2.  **Reliability**: ReAct Agent có thể hoạt động kém hơn Chatbot trong các trường hợp công cụ trả về dữ liệu quá hỗn độn gây lỗi trích xuất Regex, hoặc khi mô hình ngôn ngữ lớn (LLM) ảo tưởng tham số công cụ (ví dụ gọi `search_box(None)`). Ngược lại, Chatbot thông thường hoạt động rất nhanh và đáng tin cậy đối với các câu hỏi tĩnh đơn giản không yêu cầu tính toán dữ liệu thời gian thực.
3.  **Observation**: Dữ liệu phản hồi từ công cụ (`Observation`) định hướng trực tiếp cho hành động tiếp theo của Agent. Ví dụ, khi công cụ trả về Blackbeard (#4562) có khả năng counter hiệu ứng khóa chiêu, Agent ngay lập tức thay đổi chiến thuật ở bước kế tiếp để kiểm tra chỉ số cộng hưởng (synergy) của các tướng khác trong box với Blackbeard, thể hiện cơ chế phản hồi vòng lặp kín rất thông minh.

---

## IV. Future Improvements (5 Points)

- **Scalability**: Triển khai cơ chế chạy công cụ không đồng bộ (Asynchronous execution) để có thể gọi nhiều bộ lọc `search_box` cùng một lúc nhằm tăng tốc độ xử lý tổng thể của Agent.
- **Safety**: Xây dựng một tầng LLM kiểm duyệt hành động (Supervisor layer) để kiểm tra các tham số công cụ được trích xuất trước khi thực thi nhằm ngăn chặn lỗi chèn mã độc (prompt injection) hoặc phá hoại hệ thống.
- **Database & Write Support**: Chuyển đổi cơ sở dữ liệu tướng từ tệp tĩnh Python (`optc_data.py`) sang cơ sở dữ liệu quan hệ động **SQLite**. Đồng thời phát triển thêm công cụ ghi mới cho Agent (ví dụ: `add_character_to_box`) để cho phép người dùng tự động khai báo, cập nhật và lưu trữ vĩnh viễn tướng mới vào bể tướng trực tiếp thông qua khung chat.
- **Performance**: Chuyển đổi từ tìm kiếm khớp từ khóa thông thường sang cơ sở dữ liệu vector (Vector Database như ChromaDB hoặc FAISS) kết hợp tìm kiếm ngữ nghĩa (semantic search) khi số lượng tướng trong game mở rộng từ hàng chục lên hàng ngàn nhân vật.
