# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. API key hardcoded (dễ lộ secret nếu push code).
2. Không quản lý config qua environment variables.
3. Sử dụng `print()` thay vì structured logging (JSON logging).
4. Không có endpoint health check.
5. Port bị gán cứng (`host="localhost"`, `port=8000`) và bật chế độ `reload=True`.

### Exercise 1.3: Comparison table
| Feature | Develop | Production | Why Important? |
|---------|---------|------------|----------------|
| Config  | Hardcode| Env vars   | Bảo mật an toàn, dễ dàng đổi config trên các môi trường. |
| Health check | Không có | Có (`/health`) | Nền tảng (Platform/Cloud) dựa vào đây để restart nếu app crash. |
| Logging | `print()` | JSON | Dễ dàng quản lý log và truy vấn tự động trên cloud. |
| Shutdown | Đột ngột | Graceful | Đảm bảo các request đang thực thi hoàn thành xong rồi mới tắt. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image: `python:3.11` (Develop) hoặc `python:3.11-slim` (Production).
2. Working directory: `/app`
3. Tại sao COPY requirements.txt trước? Để tận dụng Docker layer caching, chỉ cài lại các package nếu file requirements thay đổi, giúp build nhanh hơn.
4. CMD vs ENTRYPOINT khác nhau thế nào? CMD cung cấp tham số mặc định và có thể dễ dàng bị ghi đè lúc `docker run`, trong khi ENTRYPOINT thiết lập lệnh chính sẽ luôn được thực thi (để container chạy như một executable).

### Exercise 2.3: Image size comparison
- Develop: ~1000 MB
- Production: ~150-200 MB
- Difference: ~80%
*Multi-stage build giúp loại bỏ các build tools (gcc, thư viện biên dịch) không cần thiết cho runtime, chỉ giữ lại source code và dependency đã được build.*

## Part 3: Cloud Deployment

### Exercise 3.1: Render deployment
- URL: `https://day12-ha-tang-cloud-va-deployment-i0sw.onrender.com`
- Screenshot: Xem trong thư mục `screenshots/`

## Part 4: API Security

### Exercise 4.1-4.3: Test results
- Gọi không có header xác thực: Return `401 Unauthorized`.
- Gọi có `X-API-Key` đúng: Return `200 OK`.
- Rate Limit Exceeded: Return `429 Too Many Requests` sau khi spam quá số lần cho phép (10 lần/phút).

### Exercise 4.4: Cost guard implementation
Logic sử dụng Redis để lưu trạng thái `budget:<user_id>:<month>`. Mỗi lần gọi LLM sẽ tính toán lượng token (input/output) quy đổi ra USD và cộng dồn vào Redis bằng `incrbyfloat`. Khi số tiền lớn hơn giới hạn ngày (5.0 USD) thì trả về False, API chặn request bằng lỗi `503` (hoặc `402`).

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
- Health & Readiness check: `/health` cho biết container sống hay chết để platform khởi động lại. `/ready` kiểm tra kết nối với các service ngoài (Redis/DB) để Load balancer bắt đầu gửi traffic.
- Stateless với Redis: Tất cả lịch sử chat và bộ đếm giới hạn (Rate limit, Cost guard) được lưu trong Redis, không lưu trên RAM cục bộ (in-memory) để đảm bảo khi scale lên N instance thì không bị mất đồng bộ.
- Graceful shutdown: Container bắt signal `SIGTERM` và từ chối traffic mới trong khi vẫn xử lý nốt các traffic hiện tại.
