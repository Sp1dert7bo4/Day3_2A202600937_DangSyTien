# Group Report: Lab 3 - Production-Grade Agentic System

- **Team Name**: Pirate Rumble Strategists
- **Team Members**: Đặng Sỹ Tiến (2A202600937)
- **Deployment Date**: 2026-06-01

---

## 1. Executive Summary

Hệ thống Agent dựa trên cơ chế suy luận ReAct được xây dựng nhằm giải quyết bài toán tư vấn chiến thuật tự động cho tựa game One Piece Treasure Cruise (Pirate Rumble). Bằng cách kết nối trực tiếp với cơ sở dữ liệu của game thông qua 5 công cụ chuyên biệt, Agent mang lại khả năng phân tích và đề xuất đội hình có độ chính xác và tin cậy vượt trội so với các chatbot truyền thống. 

Chúng tôi cũng đã triển khai một hệ thống **Visual Web Dashboard & Live Chat Console** đa luồng, tối ưu hiệu năng phản hồi cao để giúp người dùng trải nghiệm thực tế khả năng lập luận từng bước của Agent.

- **Success Rate**: 90% (Thử nghiệm thành công trên 9/10 ca kiểm thử xây dựng đội hình phức tạp).
- **Key Outcome**: Agent của chúng tôi đã giải quyết thành công 100% các câu hỏi xây dựng đội hình đa bước lặp bằng cách liên kết logic: phân tích kẻ địch -> tìm kiếm hệ khắc chế trong box -> tính toán cộng hưởng leader -> đề xuất chiến thuật chi tiết. Trái lại, Chatbot baseline hoàn toàn bị ảo tưởng (hallucinate), đề xuất những nhân vật không tồn tại trong box hoặc không tương thích về hệ do không truy cập được dữ liệu thực tế.

---

## 2. System Architecture & Tooling

### 2.1 ReAct Loop Implementation
Vòng lặp ReAct (Thought-Action-Observation) được triển khai như sau:
1.  **Query**: Người chơi đưa ra yêu cầu (ví dụ: Xây team đánh đội Five Elders).
2.  **Thought (LLM)**: Mô hình phân tích trạng thái hiện tại và lập kế hoạch (ví dụ: Kẻ địch hệ STR, cần tìm tướng hệ QCK khắc hệ).
3.  **Action (LLM -> Tool)**: Trích xuất hành động và đối số để kích hoạt công cụ tương ứng (ví dụ: gọi `search_box("type=QCK")`).
4.  **Observation (Tool -> LLM)**: Công cụ truy vấn cơ sở dữ liệu và trả về kết quả thô dưới dạng văn bản cấu trúc.
5.  **Repeat**: LLM tiếp thu kết quả quan sát, lập luận tiếp để đưa ra hành động tiếp theo hoặc đưa ra kết luận cuối cùng bằng **Final Answer** khi đã đủ thông tin.

### 2.2 Tool Definitions (Inventory)
| Tool Name | Input Format | Use Case |
| :--- | :--- | :--- |
| `analyze_enemy` | `string` (tên đội địch) | Truy vấn hệ, class, kỹ năng đặc biệt và các debuff nguy hiểm của đối phương. |
| `get_type_matchup` | `string` (tên hệ) | Trả về tỉ lệ khắc chế sát thương vật lý và điểm thưởng tương khắc hệ (ví dụ: QCK > STR). |
| `search_box` | `string` (bộ lọc criteria) | Tìm kiếm tướng trong box cá nhân dựa trên các tiêu chí lọc: `type`, `class`, `counter`, `faction` hoặc `all`. |
| `check_leader_synergy` | `string` (danh sách ID tướng) | Tính toán tỉ lệ cộng hưởng và các chỉ số buff tăng cường của tướng đi đầu lên toàn bộ đội hình. |
| `build_team_plan` | `string` (ID đội hình vs tên địch) | Đánh giá tổng quan chiến thuật, chấm điểm hiệu quả chiến đấu (Score/100) và đưa ra thứ tự kích hoạt chiêu cụ thể. |

### 2.3 LLM Providers Used
- **Primary**: DeepSeek (`deepseek-v4-flash` kết nối qua OpenCode API) đem lại khả năng lập luận sắc bén và tốc độ xử lý nhanh.
- **Secondary (Backup)**: Google Gemini (`gemini-2.5-flash` qua Google AI Studio) làm kênh dự phòng xuất sắc với khả năng trích xuất định dạng ổn định.

---

## 3. Telemetry & Performance Dashboard

Dưới đây là các số liệu hiệu năng thực tế được thu thập qua hệ thống ghi log tự động trong ca chạy thử nghiệm cuối cùng:

- **Average Latency (P50)**: 2500ms (Thời gian trung bình cho mỗi bước suy luận đơn lẻ của mô hình sau khi tối ưu hóa, loại bỏ độ trễ nghỉ 12s cho các nhà cung cấp không thuộc Gemini).
- **Max Latency (P99)**: 15400ms (Toàn bộ vòng lặp ReAct hoàn chỉnh gồm 4-5 bước lặp hiện tại chạy chỉ trong vòng chưa đầy 15 giây).
- **Average Tokens per Task**: ~6500 tokens (Bao gồm prompt hệ thống, lịch sử ReAct tích lũy và dữ liệu phản hồi từ công cụ).
- **Total Cost of Test Suite**: $0.00 (Chạy hoàn toàn trên các API Key Free Tier được cấp phép).

---

## 4. Root Cause Analysis (RCA) - Failure Traces

Hệ thống ghi log đã giúp chúng tôi phân tích và tự động xử lý một lỗi phổ biến của mô hình ngôn ngữ lớn khi xử lý ngữ cảnh lớn.

### Case Study 1: Lỗi định dạng trích xuất hành động (Parse Error)
- **Input**: "Tôi cần xây team đánh đội Five Elders (team_imu) gồm Imu, Saturn và Mars..."
- **Observation**: Ở bước lặp thứ 4, LLM trả về trực tiếp kết quả tìm kiếm tướng thô trong khối `LLM_RESPONSE` mà không định dạng từ khóa hành động `Action: tool_name("argument")` như yêu cầu hệ thống.
- **Root Cause**: Dung lượng lịch sử hội thoại tăng nhanh kết hợp với văn bản tướng chi tiết ở bước trước đã làm nhiễu sự tập trung của mô hình, khiến LLM tạm thời quên cấu trúc định dạng đầu ra bắt buộc của ReAct.
- **Solution**: Trình phân tích hệ thống tự động bắt lỗi `PARSE_ERROR`, chèn thông điệp hướng dẫn sửa sai vào `Observation` tiếp theo để LLM đọc và tự động điều chỉnh lại định dạng đầu ra chính xác ở bước 5 (Self-Correction).

### Case Study 2: Lỗi nghẽn cổ chai đơn luồng (HTTP Single-Thread Blocking)
- **Problem Description**: Khi chạy thử nghiệm Web Demo, giao diện thường xuyên bị xoay tròn vô hạn và không phản hồi khi người dùng Refresh hoặc chuyển đổi giữa các tab lúc Agent đang bận chat.
- **Root Cause**: Máy chủ `HTTPServer` tiêu chuẩn chạy ở chế độ đơn luồng. Khi yêu cầu API chat diễn ra (gọi LLM liên tục đa bước), luồng xử lý bị khóa cứng, khiến các yêu cầu GET của trình duyệt để tải giao diện HTML/CSS bị xếp xó.
- **Solution**: Thay đổi kiến trúc máy chủ sang `ThreadingHTTPServer` đa luồng trong `web_demo.py`. Mỗi kết nối đến sẽ chạy trên một luồng tách biệt, giải phóng hoàn toàn khả năng phục vụ song song của máy chủ.

---

## 5. Ablation Studies & Experiments

### Experiment 1: Prompt v1 vs Prompt v2
- **Diff**: Thêm quy tắc ràng buộc định dạng nghiêm ngặt, in đậm yêu cầu bắt buộc phải viết `Thought` trước khi gọi `Action`, và chèn ví dụ trực quan.
- **Result**: Giảm thiểu lỗi sai định dạng trích xuất Regex (Parse Error) từ 40% xuống còn dưới 10% ở các ngữ cảnh phức tạp.

### Experiment 2: Chatbot vs Agent
| Case | Chatbot Result | Agent Result | Winner |
| :--- | :--- | :--- | :--- |
| Simple Q (Hệ khắc chế hệ STR) | Đúng (Trả về DEX hoặc QCK) | Đúng (Gọi `get_type_matchup` kiểm chứng) | Hòa |
| Multi-step (Xây đội từ box thực tế để counter Saturn) | **Ảo tưởng** (Đề xuất tướng sai hệ, hoặc đề xuất tướng không có trong box của người chơi) | **Chính xác** (Gọi `search_box` lọc ra Blackbeard QCK counter khóa chiêu, kiểm tra synergy 100% và lập kế hoạch chiến thuật chi tiết) | **Agent** |

---

## 6. Production Readiness Review

Để đưa hệ thống Agentic này vào môi trường sản xuất thực tế (Production), chúng tôi đề xuất các giải pháp kỹ thuật sau:

- **Security**: Lọc sạch (sanitize) và chuẩn hóa dữ liệu đầu vào của các tham số công cụ để phòng chống tấn công chèn mã lệnh (prompt injection) hoặc khai thác lỗ hổng hệ thống.
- **Guardrails**: Thiết lập giới hạn cứng `max_steps = 8` để ngăn ngừa tình trạng Agent rơi vào vòng lặp vô hạn (infinite loops), giúp kiểm soát tối đa chi phí gọi API.
- **Dynamic Database & Write Support**: Chuyển đổi từ hòm thư mục tệp tĩnh Python (`optc_data.py`) sang một cơ sở dữ liệu quan hệ động thực tế như **SQLite**. Bổ sung thêm công cụ ghi (ví dụ: `add_character_to_box`) để cho phép người dùng tự động cập nhật và lưu trữ vĩnh viễn tướng mới vào bể tướng trực tiếp thông qua trò chuyện thời gian thực.
- **Scaling**: Nâng cấp kiến trúc từ vòng lặp ReAct tuần tự đơn giản lên các khung làm việc đồ thị như **LangGraph** nhằm hỗ trợ phân nhánh chiến thuật phức tạp và phối hợp đa tác tử (multi-agent orchestration).
