import subprocess
import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

HTML_FILE = os.path.abspath(r"D:\smart-parking-system\Bai_Luyen_Tap_Tong_Hop_De_Va_Loi_Giai.html")
PDF_FILE = os.path.abspath(r"D:\smart-parking-system\Bai_Luyen_Tap_Tong_Hop_De_Va_Loi_Giai.pdf")
DOWNLOAD_PDF = os.path.abspath(r"C:\Users\LENOVO\Downloads\Bai_Luyen_Tap_Tong_Hop_De_Va_Loi_Giai.pdf")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bài Luyện Tập Tổng Hợp (Bài 1-6) - Đề Bài & Lời Giải Chi Tiết Chuẩn Tự Luận</title>
<style>
  @page {
    size: A4;
    margin: 14mm 15mm 16mm 15mm;
    @bottom-right {
      content: "Trang " counter(page);
      font-size: 9pt;
      color: #64748b;
    }
  }

  *, *::before, *::after {
    box-sizing: border-box;
  }

  body {
    font-family: 'Segoe UI', 'Times New Roman', Times, serif, sans-serif;
    font-size: 10.5pt;
    line-height: 1.5;
    color: #1e293b;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }

  /* Academic Header */
  .univ-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 8px;
    margin-bottom: 12px;
  }
  .univ-left {
    text-align: left;
    font-size: 9.5pt;
    text-transform: uppercase;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.35;
  }
  .univ-right {
    text-align: right;
    font-size: 9.5pt;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.35;
  }
  .sub-unit {
    font-weight: 600;
    color: #334155;
    font-size: 8.5pt;
  }

  .title-block {
    text-align: center;
    margin: 12px 0 16px 0;
  }
  .title-main {
    font-size: 17pt;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 3px;
  }
  .title-sub {
    font-size: 12pt;
    font-weight: 700;
    color: #1d4ed8;
    margin-bottom: 3px;
  }
  .title-desc {
    font-size: 10pt;
    font-style: italic;
    color: #475569;
  }

  /* Info Meta Box */
  .info-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 14px;
    font-size: 9.5pt;
  }
  .info-table td {
    padding: 4px 6px;
    border: 1px solid #cbd5e1;
  }
  .info-label {
    background-color: #f8fafc;
    font-weight: 600;
    width: 16%;
    color: #334155;
  }
  .info-value {
    width: 34%;
  }

  /* Rules Box */
  .rules-box {
    background: #f0fdf4;
    border: 1.5px solid #86efac;
    border-left: 5px solid #16a34a;
    border-radius: 4px;
    padding: 8px 12px;
    margin-bottom: 16px;
    font-size: 9pt;
  }
  .rules-title {
    font-weight: 700;
    color: #166534;
    margin-bottom: 4px;
    text-transform: uppercase;
    font-size: 9.5pt;
  }
  .rules-box ul {
    margin: 0;
    padding-left: 18px;
  }
  .rules-box li {
    margin-bottom: 3px;
    color: #14532d;
  }

  /* Content Structure Table */
  .structure-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 18px;
    font-size: 9pt;
  }
  .structure-table th {
    background-color: #1e3a8a;
    color: #ffffff;
    padding: 6px 8px;
    text-align: center;
    border: 1px solid #1e3a8a;
  }
  .structure-table td {
    padding: 5px 8px;
    border: 1px solid #cbd5e1;
    text-align: center;
  }
  .structure-table tr:nth-child(even) td {
    background-color: #f8fafc;
  }

  /* Question Card */
  .question-container {
    margin-bottom: 22px;
    page-break-inside: auto;
  }

  .question-header {
    background-color: #0f172a;
    color: #ffffff;
    padding: 8px 12px;
    font-weight: 700;
    font-size: 11pt;
    border-radius: 4px 4px 0 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .question-header .score-tag {
    background: #e0e7ff;
    color: #312e81;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 8.5pt;
    font-weight: 800;
  }

  /* De bai box */
  .de-bai-box {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-top: none;
    padding: 10px 14px;
    font-size: 9.5pt;
    color: #334155;
    margin-bottom: 10px;
    border-left: 4px solid #64748b;
  }
  .de-bai-label {
    font-weight: 700;
    color: #475569;
    text-transform: uppercase;
    font-size: 8.5pt;
    margin-bottom: 4px;
    letter-spacing: 0.5px;
  }

  /* Solution Box */
  .solution-box {
    background: #ffffff;
    border: 1.5px solid #2563eb;
    border-radius: 4px;
    padding: 12px 14px;
    margin-bottom: 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  .solution-header {
    display: flex;
    align-items: center;
    color: #1e40af;
    font-weight: 800;
    font-size: 10.5pt;
    margin-bottom: 10px;
    padding-bottom: 5px;
    border-bottom: 1.5px solid #dbeafe;
    text-transform: uppercase;
  }
  .solution-header::before {
    content: "✍ BÀI LÀM TRÌNH BÀY TỰ LUẬN TRÊN GIẤY";
  }

  /* Sub items */
  .sub-item {
    margin-bottom: 10px;
  }
  .sub-title {
    font-weight: 700;
    color: #1e3a8a;
    font-size: 10pt;
    margin-bottom: 4px;
  }

  /* Code block */
  .code-block {
    background: #0f172a;
    color: #e2e8f0;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    padding: 8px 12px;
    border-radius: 4px;
    line-height: 1.4;
    margin: 6px 0;
    white-space: pre;
    overflow-x: auto;
  }

  /* Formula / Highlight */
  .math-inline {
    font-family: 'Cambria Math', 'Times New Roman', serif;
    font-style: italic;
    font-size: 10.5pt;
    color: #0f172a;
  }
  .math-box {
    background: #eff6ff;
    border-left: 3px solid #3b82f6;
    padding: 6px 12px;
    margin: 6px 0;
    font-family: 'Cambria Math', 'Times New Roman', serif;
    font-size: 10pt;
  }

  /* Data Table */
  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0;
    font-size: 9pt;
  }
  table.data-table th {
    background-color: #f1f5f9;
    color: #1e293b;
    border: 1px solid #cbd5e1;
    padding: 6px 8px;
    font-weight: 700;
    text-align: center;
  }
  table.data-table td {
    border: 1px solid #cbd5e1;
    padding: 5px 8px;
    text-align: center;
  }
  table.data-table tr.highlight-row td {
    background-color: #fef3c7;
    font-weight: 700;
  }

  /* Callout Note */
  .tip-box {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-left: 4px solid #d97706;
    padding: 6px 10px;
    margin: 6px 0;
    font-size: 8.5pt;
    color: #92400e;
    border-radius: 2px;
  }
  .tip-title {
    font-weight: 700;
    margin-bottom: 2px;
  }

  .step-tag {
    display: inline-block;
    background: #e2e8f0;
    color: #334155;
    font-weight: 700;
    padding: 1px 6px;
    border-radius: 3px;
    font-size: 8.5pt;
    margin-right: 4px;
  }

  .conclusion-badge {
    background: #dcfce7;
    color: #166534;
    border: 1px solid #86efac;
    padding: 4px 10px;
    font-weight: 700;
    display: inline-block;
    border-radius: 4px;
    margin-top: 4px;
  }

  .page-break {
    page-break-before: always;
  }
</style>
</head>
<body>

  <!-- Header -->
  <div class="univ-header">
    <div class="univ-left">
      BỘ GIÁO DỤC VÀ ĐÀO TẠO<br>
      <span class="sub-unit">TRƯỜNG ĐẠI HỌC CÔNG NGHỆ – KHOA CÔNG NGHỆ THÔNG TIN</span><br>
      <span class="sub-unit">BỘ MÔN: KHOA HỌC MÁY TÍNH & HỆ THỐNG THÔNG TIN</span>
    </div>
    <div class="univ-right">
      MÃ MÔN HỌC: IT3010<br>
      <span class="sub-unit">HỌC KỲ I – NĂM HỌC 2026 – 2027</span><br>
      <span class="sub-unit">THỜI GIAN LÀM BÀI: 160 PHÚT</span>
    </div>
  </div>

  <div class="title-block">
    <div class="title-main">BÀI LUYỆN TẬP TỔNG HỢP</div>
    <div class="title-sub">Bài 1–6: Từ Độ Phức Tạp Đến Đường Đi Ngắn Nhất</div>
    <div class="title-desc">MÔN HỌC: THUẬT TOÁN ỨNG DỤNG (APPLIED ALGORITHMS)</div>
    <div style="font-size: 9.5pt; color: #0284c7; font-weight: 700; margin-top: 3px;">
      [TÀI LIỆU CHÍNH THỨC: TOÀN BỘ ĐỀ THI & HƯỚNG DẪN TRÌNH BÀY LỜI GIẢI CHUẨN TỰ LUẬN TRÊN GIẤY]
    </div>
  </div>

  <!-- Bảng Thông Tin Học Viên -->
  <table class="info-table">
    <tr>
      <td class="info-label">Họ và tên:</td>
      <td class="info-value">.......................................................................</td>
      <td class="info-label">Mã sinh viên:</td>
      <td class="info-value">...................................................</td>
    </tr>
    <tr>
      <td class="info-label">Lớp sinh hoạt:</td>
      <td class="info-value">.......................................................................</td>
      <td class="info-label">Ngày kiểm tra:</td>
      <td class="info-value">....... / ....... / 2026</td>
    </tr>
  </table>

  <!-- Quy Định Làm Bài -->
  <div class="rules-box">
    <div class="rules-title">📌 YÊU CẦU CHUNG KHI LÀM BÀI TRÊN GIẤY THI:</div>
    <ul>
      <li><strong>Trình bày đầy đủ các bước suy luận:</strong> Tuyệt đối không chỉ ghi mỗi kết quả cuối cùng; phải nêu rõ căn cứ toán học và lập luận logic.</li>
      <li><strong>Mô phỏng thuật toán:</strong> Bắt buộc lập bảng trace hoặc ghi tường minh thứ tự xét/chọn, trạng thái trung gian (hàng đợi, nhãn khoảng cách, ngăn xếp) và điều kiện dừng.</li>
      <li><strong>Quy ước đồng nhất:</strong> Nếu có nhiều nghiệm đúng hoặc nhiều cách phân chia (như chia mảng 3+4 hay 4+3), cần nêu rõ quy ước lựa chọn ngay từ đầu.</li>
      <li><strong>Quy tắc đồ thị:</strong> Với BFS/DFS luôn duyệt đỉnh kề theo thứ tự chữ cái tăng dần (alphabet). Với Dijkstra chỉ cố định một đỉnh khi đỉnh đó có nhãn tạm thời nhỏ nhất.</li>
    </ul>
  </div>

  <!-- Ma Trận Đề Thi -->
  <table class="structure-table">
    <thead>
      <tr>
        <th style="width: 8%;">Phần</th>
        <th style="width: 25%;">Nội dung trọng tâm</th>
        <th style="width: 17%;">Thời gian gợi ý</th>
        <th style="width: 15%;">Số điểm</th>
        <th style="width: 35%;">Mục tiêu kiểm tra</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1</strong></td>
        <td>Kiến thức nền</td>
        <td>10 phút</td>
        <td><strong>10 điểm</strong></td>
        <td>Cấp tăng trưởng, truy hồi cơ bản, bản chất Tham lam, DP, Dijkstra</td>
      </tr>
      <tr>
        <td><strong>2</strong></td>
        <td>Độ phức tạp thời gian</td>
        <td>20 phút</td>
        <td><strong>15 điểm</strong></td>
        <td>Phân tích vòng lặp lồng nhau, cấp số cộng, số mũ cơ số 2, ký hiệu tiệm cận &Theta;</td>
      </tr>
      <tr>
        <td><strong>3</strong></td>
        <td>Thuật toán tham lam</td>
        <td>20 phút</td>
        <td><strong>15 điểm</strong></td>
        <td>Lập lịch khoảng (Interval Scheduling), phản ví dụ bài toán đổi tiền (Coin Change)</td>
      </tr>
      <tr>
        <td><strong>4</strong></td>
        <td>Chia để trị</td>
        <td>20 phút</td>
        <td><strong>15 điểm</strong></td>
        <td>Hệ thức Merge Sort, Định lý Master, Cây đệ quy, Phân hoạch Quick Sort</td>
      </tr>
      <tr>
        <td><strong>5</strong></td>
        <td>Quy hoạch động</td>
        <td>25 phút</td>
        <td><strong>15 điểm</strong></td>
        <td>Bài toán Ba lô 0-1 (Knapsack), bảng DP 2 chiều, điều kiện cơ sở & truy vết</td>
      </tr>
      <tr>
        <td><strong>6</strong></td>
        <td>Duyệt đồ thị BFS / DFS</td>
        <td>25 phút</td>
        <td><strong>15 điểm</strong></td>
        <td>Danh sách kề, hàng đợi BFS, đường đi ngắn nhất, ngăn xếp DFS, so sánh Ma trận kề</td>
      </tr>
      <tr>
        <td><strong>7</strong></td>
        <td>Đường đi ngắn nhất</td>
        <td>30 phút</td>
        <td><strong>15 điểm</strong></td>
        <td>Mô phỏng Dijkstra bảng nhãn, đường đi tối ưu, xử lý cạnh âm, Bellman-Ford, Floyd-Warshall</td>
      </tr>
    </tbody>
  </table>

  <!-- ========================================================================= -->
  <!-- CÂU 1 -->
  <!-- ========================================================================= -->
  <div class="question-container">
    <div class="question-header">
      <span>CÂU 1: CÂU HỎI NGẮN KIẾN THỨC NỀN TẢNG</span>
      <span class="score-tag">10 ĐIỂM (MỖI Ý 2 ĐIỂM)</span>
    </div>
    <div class="de-bai-box">
      <div class="de-bai-label">Đề bài gốc:</div>
      Trả lời ngắn gọn các ý sau. Mỗi ý 2 điểm.<br>
      <strong>a)</strong> Sắp xếp theo thứ tự tăng dần tốc độ tăng trưởng khi <em>n &rarr; &infin;</em>: <code>log n</code>, <code>&radic;n</code>, <code>n</code>, <code>n log n</code>, <code>n&sup2;</code>.<br>
      <strong>b)</strong> Cho truy hồi <em>T(n) = 2T(&lfloor;n/2&rfloor;) + n</em> với <em>T(1) = &Theta;(1)</em>. Nêu cấp độ tăng trưởng tiệm cận của <em>T(n)</em> và tên phương pháp có thể dùng để giải.<br>
      <strong>c)</strong> Với hệ mệnh giá {1, 3, 4} và số tiền 6, hãy ghi nghiệm do chiến lược chọn đồng xu lớn nhất trước tạo ra. Nghiệm đó có tối ưu không?<br>
      <strong>d)</strong> Nêu hai dấu hiệu quan trọng cho thấy một bài toán phù hợp với quy hoạch động.<br>
      <strong>e)</strong> Nêu điều kiện về trọng số cạnh để Dijkstra cho kết quả đúng; giải thích ngắn gọn vì sao cạnh âm gây vấn đề.
    </div>

    <div class="solution-box">
      <div class="solution-header"></div>
      
      <div class="sub-item">
        <div class="sub-title">a) Sắp xếp thứ tự tăng dần tốc độ tăng trưởng tiệm cận:</div>
        <p>Ta so sánh giới hạn tỉ số giữa các hàm khi <em>n &rarr; &infin;</em>:</p>
        <div class="math-box">
          <strong>log n &nbsp;&prec;&nbsp; &radic;n &nbsp;&prec;&nbsp; n &nbsp;&prec;&nbsp; n log n &nbsp;&prec;&nbsp; n&sup2;</strong>
        </div>
        <p style="font-size: 9pt; color: #475569;">
          <em>Giải thích ngắn trên giấy:</em> lim<sub>n&rarr;&infin;</sub> (log n / &radic;n) = 0; lim<sub>n&rarr;&infin;</sub> (&radic;n / n) = 0; lim<sub>n&rarr;&infin;</sub> (n / (n log n)) = 0; lim<sub>n&rarr;&infin;</sub> ((n log n) / n&sup2;) = 0.
        </p>
      </div>

      <div class="sub-item">
        <div class="sub-title">b) Cấp độ tăng trưởng tiệm cận và phương pháp giải:</div>
        <ul>
          <li><strong>Cấp độ tăng trưởng tiệm cận:</strong> <strong>T(n) = &Theta;(n log n)</strong>.</li>
          <li><strong>Tên các phương pháp có thể dùng để giải:</strong>
            <ul>
              <li><strong>Định lý Thợ (Master Theorem):</strong> Dạng <em>T(n) = aT(n/b) + f(n)</em> với <em>a = 2, b = 2 &rArr; n<sup>log<sub>b</sub> a</sup> = n<sup>1</sup> = n</em>. Do <em>f(n) = n = &Theta;(n<sup>1</sup>)</em> (Trường hợp 2), suy ra <em>T(n) = &Theta;(n log n)</em>.</li>
              <li>Hoặc phương pháp <strong>Cây đệ quy (Recursion Tree)</strong> / phương pháp <strong>Đoán và chứng minh quy nạp (Substitution Method)</strong>.</li>
            </ul>
          </li>
        </ul>
      </div>

      <div class="sub-item">
        <div class="sub-title">c) Nghiệm của chiến lược chọn đồng xu lớn nhất trước:</div>
        <ul>
          <li><strong>Mô phỏng tham lam:</strong>
            <br>&bull; Lấy đồng lớn nhất &le; 6 là <strong>4</strong> &rarr; Còn dư: <em>6 - 4 = 2</em>.
            <br>&bull; Lấy đồng lớn nhất &le; 2 là <strong>1</strong> &rarr; Còn dư: <em>2 - 1 = 1</em>.
            <br>&bull; Lấy đồng lớn nhất &le; 1 là <strong>1</strong> &rarr; Còn dư: <em>1 - 1 = 0</em>.
          </li>
          <li><strong>Nghiệm do tham lam tạo ra:</strong> Gồm <strong>3 đồng xu</strong>: <strong>{4, 1, 1}</strong> (tổng 4 + 1 + 1 = 6).</li>
          <li><strong>Đánh giá tính tối ưu:</strong> Nghiệm này <strong>KHÔNG TỐI ƯU</strong>. Vì tồn tại phương án chỉ cần <strong>2 đồng xu</strong>: <strong>{3, 3}</strong> (tổng 3 + 3 = 6).</li>
        </ul>
      </div>

      <div class="sub-item">
        <div class="sub-title">d) Hai dấu hiệu nhận biết bài toán phù hợp với Quy hoạch động (DP):</div>
        <ol>
          <li><strong>Cấu trúc con tối ưu (Optimal Substructure):</strong> Lời giải tối ưu của bài toán lớn được xây dựng từ các lời giải tối ưu của các bài toán con cấp thấp hơn.</li>
          <li><strong>Các bài toán con gối nhau / chồng chéo (Overlapping Subproblems):</strong> Không gian bài toán con nhỏ, các bài toán con bị gọi lặp đi lặp lại nhiều lần trong quá trình đệ quy (cho phép lưu bảng/memoization để tránh tính lại).</li>
        </ol>
      </div>

      <div class="sub-item">
        <div class="sub-title">e) Điều kiện trọng số của Dijkstra và giải thích vì sao cạnh âm gây vấn đề:</div>
        <ul>
          <li><strong>Điều kiện:</strong> Tất cả các cạnh trong đồ thị phải có <strong>trọng số không âm</strong> (tức là <em>w(u, v) &ge; 0</em> với mọi cung <em>(u, v) &isin; E</em>).</li>
          <li><strong>Giải thích vì sao cạnh âm gây vấn đề:</strong> 
            Dijkstra hoạt động theo chiến lược tham lam: một khi đỉnh <em>u</em> có nhãn tạm thời nhỏ nhất được chọn để <strong>cố định</strong> (đưa vào tập đã duyệt), thuật toán mặc định rằng khoảng cách <em>d(u)</em> đã tối ưu và <strong>sẽ không bao giờ cập nhật lại nhãn của đỉnh u</strong>. 
            Nếu tồn tại cạnh âm, có thể có một đường đi khác đi vòng qua nhiều cạnh nhưng có chứa cạnh âm mang trọng số âm lớn, làm cho tổng khoảng cách thực tế đến <em>u</em> nhỏ hơn <em>d(u)</em> sau khi <em>u</em> đã bị chốt cố định, dẫn đến thuật toán cho kết quả sai hoàn toàn (chưa kể trường hợp chu trình âm khiến đường đi giảm vô hạn).
          </li>
        </ul>
      </div>

    </div>
  </div>

  <div class="page-break"></div>

  <!-- ========================================================================= -->
  <!-- CÂU 2 -->
  <!-- ========================================================================= -->
  <div class="question-container">
    <div class="question-header">
      <span>CÂU 2: PHÂN TÍCH THUẬT TOÁN & ĐỘ PHỨC TẠP ĐOẠN MÃ GIẢ</span>
      <span class="score-tag">15 ĐIỂM</span>
    </div>
    <div class="de-bai-box">
      <div class="de-bai-label">Đề bài gốc:</div>
      Xét đoạn giả mã sau, trong đó phép gán cho <code>count</code> có chi phí &Theta;(1):
      <div class="code-block">count &larr; 0
for i &larr; 1 to n do
    for j &larr; 1 to i do
        count &larr; count + 1
i &larr; 1
while i &le; n do
    j &larr; 1
    while j &le; n do
        count &larr; count + 1
        j &larr; 2j
    i &larr; 2i</div>
      <strong>a)</strong> Tính chính xác số lần tăng <code>count</code> của hai khối lệnh theo <em>n</em> và <em>&lfloor;log<sub>2</sub> n&rfloor;</em>.<br>
      <strong>b)</strong> Suy ra độ phức tạp thời gian của toàn bộ đoạn giả mã bằng ký hiệu &Theta;.<br>
      <strong>c)</strong> Giải thích vì sao có thể bỏ qua các hạng bậc thấp khi kết luận độ phức tạp.
    </div>

    <div class="solution-box">
      <div class="solution-header"></div>

      <div class="sub-item">
        <div class="sub-title">a) Tính chính xác số lần tăng <code>count</code> của hai khối lệnh:</div>
        
        <p><strong>1. Khối lệnh 1 (Hai vòng lặp for lồng nhau):</strong></p>
        <ul>
          <li>Vòng ngoài: biến <em>i</em> chạy nhận tuần tự các giá trị <em>1, 2, 3, &hellip;, n</em>.</li>
          <li>Vòng trong: với mỗi giá trị <em>i</em>, biến <em>j</em> chạy từ <em>1</em> đến <em>i</em>, nghĩa là thân vòng lặp thực hiện đúng <em>i</em> lần tăng <code>count</code>.</li>
        </ul>
        <div class="math-box">
          Số lần tăng <code>count</code> ở Khối 1: &nbsp; 
          <strong>S<sub>1</sub> = &sum;<sub>i=1</sub><sup>n</sup> i = 1 + 2 + 3 + &hellip; + n = <span style="font-size:11pt;">n(n + 1) / 2</span> = n&sup2;/2 + n/2</strong>
        </div>

        <p><strong>2. Khối lệnh 2 (Hai vòng lặp while lồng nhau với bước nhảy nhân đôi):</strong></p>
        <ul>
          <li><strong>Vòng ngoài:</strong> Bắt đầu <em>i = 1 = 2<sup>0</sup></em>. Sau mỗi bước lặp <em>i &larr; 2i</em>. 
          Các giá trị của <em>i</em> là: <em>2<sup>0</sup>, 2<sup>1</sup>, 2<sup>2</sup>, &hellip;, 2<sup>k</sup> &le; n</em>.
          Điều kiện dừng là <em>i &gt; n &hArr; 2<sup>k</sup> &le; n &lt; 2<sup>k+1</sup> &rArr; k = &lfloor;log<sub>2</sub> n&rfloor;</em>.
          <br>&rArr; Số lần lặp của vòng ngoài là: <strong>k + 1 = &lfloor;log<sub>2</sub> n&rfloor; + 1</strong> bước.
          </li>
          <li><strong>Vòng trong:</strong> Với mỗi bước của <em>i</em>, biến <em>j</em> được khởi gán lại <em>j = 1 = 2<sup>0</sup></em> và nhân đôi sau mỗi bước <em>j &larr; 2j</em> đến khi <em>j &gt; n</em>.
          Tương tự, các giá trị của <em>j</em> là <em>2<sup>0</sup>, 2<sup>1</sup>, &hellip;, 2<sup>&lfloor;log<sub>2</sub> n&rfloor;</sup></em>.
          <br>&rArr; Số lần lặp của vòng trong ở mỗi bước <em>i</em> là hoàn toàn độc lập với <em>i</em> và bằng đúng: <strong>&lfloor;log<sub>2</sub> n&rfloor; + 1</strong> bước.
          </li>
        </ul>
        <div class="math-box">
          Số lần tăng <code>count</code> ở Khối 2: &nbsp; 
          <strong>S<sub>2</sub> = (&lfloor;log<sub>2</sub> n&rfloor; + 1) &times; (&lfloor;log<sub>2</sub> n&rfloor; + 1) = (&lfloor;log<sub>2</sub> n&rfloor; + 1)&sup2;</strong>
        </div>

        <p><strong>3. Tổng số lần tăng <code>count</code> của toàn bộ đoạn mã:</strong></p>
        <div class="math-box" style="background:#e0f2fe; border-left: 3px solid #0284c7;">
          <strong>S<sub>tổng</sub> = S<sub>1</sub> + S<sub>2</sub> = <span style="font-size:11.5pt;">n(n + 1)/2 + (&lfloor;log<sub>2</sub> n&rfloor; + 1)&sup2;</span></strong>
        </div>
      </div>

      <div class="sub-item">
        <div class="sub-title">b) Độ phức tạp thời gian của toàn bộ đoạn giả mã bằng ký hiệu &Theta;:</div>
        <ul>
          <li>Khối 1 có chi phí: <em>T<sub>1</sub>(n) = &Theta;(n&sup2;)</em>.</li>
          <li>Khối 2 có chi phí: <em>T<sub>2</sub>(n) = &Theta;((log<sub>2</sub> n)&sup2;) = &Theta;(log&sup2; n)</em>.</li>
          <li>Toàn bộ thuật toán thực hiện tuần tự Khối 1 rồi đến Khối 2:
            <br><em>T(n) = T<sub>1</sub>(n) + T<sub>2</sub>(n) = &Theta;(n&sup2; + log&sup2; n)</em>.
          </li>
        </ul>
        <div class="conclusion-badge" style="font-size: 10.5pt;">
          &rArr; Kết luận độ phức tạp: <strong>T(n) = &Theta;(n&sup2;)</strong>
        </div>
      </div>

      <div class="sub-item">
        <div class="sub-title">c) Giải thích vì sao có thể bỏ qua các hạng bậc thấp khi kết luận độ phức tạp:</div>
        <ul>
          <li><strong>Theo định nghĩa tiệm cận &Theta;:</strong> Ta xét giới hạn hành vi của hàm khi <em>n &rarr; &infin;</em>. Khi kích thước dữ liệu <em>n</em> tăng lên rất lớn, số hạng có tốc độ tăng trưởng cao nhất (ở đây là <em>n&sup2;</em>) sẽ <strong>hoàn toàn chi phối và lấn át</strong> mọi số hạng bậc thấp hơn như <em>n/2</em>, <em>log&sup2; n</em>, <em>log n</em> và hằng số.</li>
          <li><strong>Chứng minh toán học qua giới hạn:</strong>
            <div class="math-box">
              lim<sub>n&rarr;&infin;</sub> <span style="font-size:11pt;">[n(n+1)/2 + (&lfloor;log<sub>2</sub> n&rfloor; + 1)&sup2;] / n&sup2;</span> 
              = lim<sub>n&rarr;&infin;</sub> [ 1/2 + 1/(2n) + (&lfloor;log<sub>2</sub> n&rfloor; + 1)&sup2; / n&sup2; ] = <strong>1/2 &gt; 0</strong> (hằng số dương hữu hạn).
            </div>
            Theo tiêu chuẩn so sánh giới hạn, hàm tổng <em>S<sub>tổng</sub>(n)</em> cùng cấp tăng trưởng tiệm cận với <em>n&sup2;</em>. Tồn tại các hằng số <em>c<sub>1</sub>, c<sub>2</sub> &gt; 0</em> và <em>n<sub>0</sub></em> sao cho <em>c<sub>1</sub>n&sup2; &le; S<sub>tổng</sub>(n) &le; c<sub>2</sub>n&sup2;</em> với mọi <em>n &ge; n<sub>0</sub></em>. Do đó, việc bỏ qua các hạng bậc thấp không làm ảnh hưởng đến bản chất đánh giá thời gian tiệm cận của thuật toán.
          </li>
        </ul>
      </div>

    </div>
  </div>

  <div class="page-break"></div>

  <!-- ========================================================================= -->
  <!-- CÂU 3 -->
  <!-- ========================================================================= -->
  <div class="question-container">
    <div class="question-header">
      <span>CÂU 3: THUẬT TOÁN THAM LAM (GREEDY ALGORITHM)</span>
      <span class="score-tag">15 ĐIỂM</span>
    </div>
    <div class="de-bai-box">
      <div class="de-bai-label">Đề bài gốc:</div>
      <strong>a) Lập lịch khoảng (8 điểm).</strong> Cho các hoạt động sau, mỗi hoạt động có dạng (bắt đầu, kết thúc):
      <table class="data-table" style="margin: 4px 0;">
        <tr>
          <th>Hoạt động</th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>F</th><th>G</th><th>H</th><th>I</th><th>J</th><th>K</th>
        </tr>
        <tr>
          <td><strong>Khoảng</strong></td><td>(1,4)</td><td>(3,5)</td><td>(0,6)</td><td>(5,7)</td><td>(3,9)</td><td>(5,9)</td><td>(6,10)</td><td>(8,11)</td><td>(8,12)</td><td>(2,14)</td><td>(12,16)</td>
        </tr>
      </table>
      Áp dụng chiến lược chọn hoạt động có thời điểm kết thúc sớm nhất. Ghi thứ tự các hoạt động được chọn và số hoạt động tối đa.<br>
      <strong>b) Phản ví dụ cho đổi tiền (7 điểm).</strong> Với hệ mệnh giá {1, 3, 4} và số tiền 6:<br>
      i) mô phỏng chiến lược tham lam;<br>
      ii) tìm một nghiệm tốt hơn;<br>
      iii) giải thích kết luận rút ra về việc dùng tham lam cho bài toán đổi tiền với hệ mệnh giá tùy ý.
    </div>

    <div class="solution-box">
      <div class="solution-header"></div>

      <div class="sub-item">
        <div class="sub-title">a) Bài toán Lập lịch khoảng (Interval Scheduling):</div>
        <p><strong>Bước 1: Sắp xếp các hoạt động theo thời điểm kết thúc (f<sub>i</sub>) tăng dần:</strong></p>
        <table class="data-table">
          <thead>
            <tr>
              <th>TT</th><th>Hoạt động</th><th>Khoảng [s<sub>i</sub>, f<sub>i</sub>]</th><th>Thời điểm kết thúc f<sub>i</sub></th><th>Trạng thái xét duyệt tham lam</th>
            </tr>
          </thead>
          <tbody>
            <tr style="background:#dcfce7; font-weight: bold;">
              <td>1</td><td><strong>A</strong></td><td>(1, 4)</td><td><strong>4</strong></td><td><strong>CHỌN (kết thúc sớm nhất, chốt mốc f = 4)</strong></td>
            </tr>
            <tr>
              <td>2</td><td>B</td><td>(3, 5)</td><td>5</td><td>Loại (bắt đầu s = 3 &lt; 4, bị xung đột với A)</td>
            </tr>
            <tr>
              <td>3</td><td>C</td><td>(0, 6)</td><td>6</td><td>Loại (bắt đầu s = 0 &lt; 4, bị xung đột với A)</td>
            </tr>
            <tr style="background:#dcfce7; font-weight: bold;">
              <td>4</td><td><strong>D</strong></td><td>(5, 7)</td><td><strong>7</strong></td><td><strong>CHỌN (bắt đầu s = 5 &ge; 4, hợp lệ! Cập nhật mốc f = 7)</strong></td>
            </tr>
            <tr>
              <td>5</td><td>E</td><td>(3, 9)</td><td>9</td><td>Loại (bắt đầu s = 3 &lt; 7, xung đột với D)</td>
            </tr>
            <tr>
              <td>6</td><td>F</td><td>(5, 9)</td><td>9</td><td>Loại (bắt đầu s = 5 &lt; 7, xung đột với D)</td>
            </tr>
            <tr>
              <td>7</td><td>G</td><td>(6, 10)</td><td>10</td><td>Loại (bắt đầu s = 6 &lt; 7, xung đột với D)</td>
            </tr>
            <tr style="background:#dcfce7; font-weight: bold;">
              <td>8</td><td><strong>H</strong></td><td>(8, 11)</td><td><strong>11</strong></td><td><strong>CHỌN (bắt đầu s = 8 &ge; 7, hợp lệ! Cập nhật mốc f = 11)</strong></td>
            </tr>
            <tr>
              <td>9</td><td>I</td><td>(8, 12)</td><td>12</td><td>Loại (bắt đầu s = 8 &lt; 11, xung đột với H)</td>
            </tr>
            <tr>
              <td>10</td><td>J</td><td>(2, 14)</td><td>14</td><td>Loại (bắt đầu s = 2 &lt; 11, xung đột với H)</td>
            </tr>
            <tr style="background:#dcfce7; font-weight: bold;">
              <td>11</td><td><strong>K</strong></td><td>(12, 16)</td><td><strong>16</strong></td><td><strong>CHỌN (bắt đầu s = 12 &ge; 11, hợp lệ! Cập nhật mốc f = 16)</strong></td>
            </tr>
          </tbody>
        </table>

        <p><strong>Bước 2: Kết luận:</strong></p>
        <div class="conclusion-badge">
          &bull; Thứ tự các hoạt động được chọn: <strong>A &rarr; D &rarr; H &rarr; K</strong><br>
          &bull; Số lượng hoạt động tối đa không chồng chéo nhau là: <strong>4 hoạt động</strong> (Tập nghiệm: {A, D, H, K}).
        </div>
      </div>

      <div class="sub-item" style="margin-top: 12px;">
        <div class="sub-title">b) Phản ví dụ cho bài toán đổi tiền (Coin Change) với hệ {1, 3, 4} và số tiền 6:</div>
        
        <p><strong>i) Mô phỏng chiến lược tham lam (ưu tiên đồng có mệnh giá lớn nhất trước):</strong></p>
        <ul>
          <li>Bước 1: Chọn đồng lớn nhất không vượt quá 6 là đồng <strong>4</strong>. Số tiền còn lại: <em>6 - 4 = 2</em>.</li>
          <li>Bước 2: Các đồng 4 và 3 đều &gt; 2, do đó chọn đồng <strong>1</strong>. Số tiền còn lại: <em>2 - 1 = 1</em>.</li>
          <li>Bước 3: Chọn tiếp đồng <strong>1</strong>. Số tiền còn lại: <em>1 - 1 = 0</em> (Hoàn thành đổi tiền).</li>
          <li>&rArr; <strong>Nghiệm tham lam:</strong> Sử dụng <strong>3 đồng xu</strong>: <strong>{4, 1, 1}</strong>.</li>
        </ul>

        <p><strong>ii) Tìm một nghiệm tốt hơn:</strong></p>
        <ul>
          <li>Ta chọn <strong>2 đồng xu mệnh giá 3</strong>: <em>3 + 3 = 6</em>.</li>
          <li>&rArr; <strong>Nghiệm tối ưu:</strong> Sử dụng <strong>2 đồng xu</strong>: <strong>{3, 3}</strong>.</li>
          <li>Vì <em>2 &lt; 3</em>, nên nghiệm {3, 3} tốt hơn rõ rệt so với nghiệm do chiến lược tham lam tạo ra.</li>
        </ul>

        <p><strong>iii) Giải thích kết luận rút ra:</strong></p>
        <ul>
          <li>Chiến lược tham lam <strong>không luôn đảm bảo tính tối ưu toàn cục</strong> cho bài toán đổi tiền với hệ mệnh giá tùy ý. Tham lam chỉ cho nghiệm tối ưu với các hệ tiền tệ đặc biệt thỏa mãn tính chất chính quy (canonical coin system, như tiền VND: 1k, 2k, 5k, 10k... hay USD: 1, 5, 10, 25).</li>
          <li>Với hệ mệnh giá tổng quát bất kỳ, lựa chọn tối ưu cục bộ tại từng bước có thể dẫn vào "ngõ cụt" (sub-optimal). Để tìm nghiệm tối ưu ít đồng xu nhất trong trường hợp tổng quát, bắt buộc phải sử dụng phương pháp <strong>Quy hoạch động (Dynamic Programming)</strong> hoặc <strong>Nhánh cận (Branch and Bound)</strong>.</li>
        </ul>
      </div>

    </div>
  </div>

  <div class="page-break"></div>

  <!-- ========================================================================= -->
  <!-- CÂU 4 -->
  <!-- ========================================================================= -->
  <div class="question-container">
    <div class="question-header">
      <span>CÂU 4: CHIẾN LƯỢC CHIA ĐỂ TRỊ (DIVIDE AND CONQUER)</span>
      <span class="score-tag">15 ĐIỂM</span>
    </div>
    <div class="de-bai-box">
      <div class="de-bai-label">Đề bài gốc:</div>
      <strong>a) Merge Sort (8 điểm).</strong> Với <em>n</em> phần tử, xét cài đặt Merge Sort chuẩn dùng một mảng phụ cho bước trộn. Thuật toán chia thành hai nửa gần bằng nhau và thực hiện bước trộn trong thời gian &Theta;(n).<br>
      i) Viết hệ thức truy hồi của thời gian chạy.<br>
      ii) Giải truy hồi bằng cây đệ quy hoặc định lý Master.<br>
      iii) Nêu độ phức tạp bộ nhớ phụ của Merge Sort nếu không tính vùng chứa đầu vào, bao gồm cả ngăn xếp đệ quy.<br>
      <strong>b) Chạy một lần chia để trị (4 điểm).</strong> Với mảng <code>[38, 27, 43, 3, 9, 82, 10]</code>, hãy ghi các mảng con sau bước chia đầu tiên và kết quả cuối cùng sau khi sắp xếp tăng dần bằng Merge Sort. Có thể chia theo 3 + 4 hoặc 4 + 3 phần tử; chấp nhận cả hai nếu thực hiện nhất quán.<br>
      <strong>c) Quick Sort (3 điểm).</strong> Chọn phần tử đầu tiên làm chốt cho mảng <code>[5, 2, 8, 1, 3]</code>. Ghi một phân hoạch hợp lệ sau lần phân hoạch đầu tiên và nêu trường hợp làm Quick Sort có độ phức tạp &Theta;(n&sup2;).
    </div>

    <div class="solution-box">
      <div class="solution-header"></div>

      <div class="sub-item">
        <div class="sub-title">a) Phân tích thuật toán Merge Sort:</div>
        
        <p><strong>i) Hệ thức truy hồi của thời gian chạy:</strong></p>
        <div class="math-box">
          T(n) = <strong>&Theta;(1)</strong> khi n = 1<br>
          T(n) = <strong>2 T(n/2) + &Theta;(n)</strong> khi n &gt; 1 &nbsp; <em>(hoặc viết chặt chẽ: T(n) = T(&lfloor;n/2&rfloor;) + T(&lceil;n/2&rceil;) + cn)</em>
        </div>

        <p><strong>ii) Giải truy hồi:</strong></p>
        <p><em>Cách 1: Áp dụng Định lý Thợ (Master Theorem):</em></p>
        <ul>
          <li>Phương trình dạng: <em>T(n) = aT(n/b) + f(n)</em> với hệ số <em>a = 2</em>, <em>b = 2</em>, và <em>f(n) = &Theta;(n)</em>.</li>
          <li>Tính: <em>n<sup>log<sub>b</sub> a</sup> = n<sup>log<sub>2</sub> 2</sup> = n<sup>1</sup> = n</em>.</li>
          <li>So sánh: <em>f(n) = &Theta;(n<sup>log<sub>b</sub> a</sup>) = &Theta;(n)</em> &rarr; Thỏa mãn <strong>Trường hợp 2 (Case 2)</strong> của Định lý Master.</li>
          <li>Công thức nghiệm: <em>T(n) = &Theta;(n<sup>log<sub>b</sub> a</sup> &times; log n)</em> = <strong>&Theta;(n log n)</strong>.</li>
        </ul>

        <p><em>Cách 2: Minh họa bằng Cây đệ quy (Recursion Tree):</em></p>
        <ul>
          <li>Mỗi nút ở tầng <em>i</em> (với <em>i = 0, 1, &hellip;, log<sub>2</sub> n</em>) xử lý bài toán kích thước <em>n / 2<sup>i</sup></em>.</li>
          <li>Tầng <em>i</em> có đúng <em>2<sup>i</sup></em> nút, chi phí trộn tại tầng <em>i</em> là: <em>2<sup>i</sup> &times; c(n / 2<sup>i</sup>) = cn</em>.</li>
          <li>Chiều cao cây đệ quy là <em>log<sub>2</sub> n + 1</em> tầng.</li>
          <li>Tổng chi phí toàn bộ cây: <em>&sum;<sub>i=0</sub><sup>log<sub>2</sub> n</sup> cn = cn(log<sub>2</sub> n + 1) = <strong>&Theta;(n log n)</strong></em>.</li>
        </ul>

        <p><strong>iii) Độ phức tạp bộ nhớ phụ (Auxiliary Space):</strong></p>
        <ul>
          <li>Mảng phụ cấp phát tạm thời để thực hiện thao tác trộn (Merge): <strong>&Theta;(n)</strong>.</li>
          <li>Bộ nhớ ngăn xếp đệ quy (Recursion call stack) lưu các khung hàm: tương ứng với chiều cao cây đệ quy là <strong>&Theta;(log n)</strong>.</li>
          <li>Tổng độ phức tạp bộ nhớ phụ: <em>&Theta;(n) + &Theta;(log n) = <strong>&Theta;(n)</strong></em>.</li>
        </ul>
      </div>

      <div class="sub-item" style="margin-top: 10px;">
        <div class="sub-title">b) Thực hiện bước chia và kết quả của Merge Sort với mảng [38, 27, 43, 3, 9, 82, 10]:</div>
        <p>Mảng có kích thước <em>n = 7</em>. Vị trí giữa <em>mid = &lfloor;7/2&rfloor; = 3</em> (hoặc <em>&lceil;7/2&rceil; = 4</em>):</p>
        <ul>
          <li><strong>Các mảng con sau bước chia đầu tiên:</strong>
            <br>&bull; <em>Cách chia 4 + 3:</em> Mảng con trái: <strong>[38, 27, 43, 3]</strong> &nbsp;|&nbsp; Mảng con phải: <strong>[9, 82, 10]</strong>
            <br>&bull; <em>Cách chia 3 + 4:</em> Mảng con trái: <strong>[38, 27, 43]</strong> &nbsp;|&nbsp; Mảng con phải: <strong>[3, 9, 82, 10]</strong>
            <br><em>(Sinh viên chọn 1 trong 2 cách chia đều đạt điểm tối đa).</em>
          </li>
          <li><strong>Kết quả cuối cùng sau khi hoàn tất sắp xếp tăng dần:</strong>
            <div class="conclusion-badge" style="font-size: 10pt;">
              <strong>[3, 9, 10, 27, 38, 43, 82]</strong>
            </div>
          </li>
        </ul>
      </div>

      <div class="sub-item" style="margin-top: 10px;">
        <div class="sub-title">c) Phân hoạch Quick Sort và trường hợp xấu nhất &Theta;(n&sup2;):</div>
        <ul>
          <li>Mảng đầu vào: <code>[5, 2, 8, 1, 3]</code>. Chọn <strong>chốt (pivot) = 5</strong> (phần tử đầu tiên).</li>
          <li><strong>Một phân hoạch hợp lệ:</strong> Sau khi phân hoạch, chốt 5 phải đứng ở vị trí phân định sao cho mọi phần tử bên trái đều &le; 5 và bên phải đều &gt; 5.
            <br>&bull; Các phần tử &le; 5: {2, 1, 3}.
            <br>&bull; Các phần tử &gt; 5: {8}.
            <br>&bull; <em>Ví dụ mảng hợp lệ sau phân hoạch (theo Lomuto hoặc Hoare chuẩn):</em>
            <div class="math-box">
              <strong>[3, 2, 1, 5, 8]</strong> &nbsp; hoặc &nbsp; <strong>[2, 1, 3, 5, 8]</strong> &nbsp; hoặc &nbsp; <strong>[1, 2, 3, 5, 8]</strong>
              <br><small style="color:#64748b;">(Trong đó chốt 5 nằm ở chỉ số index = 3, bên trái là tập {1, 2, 3}, bên phải là {8}).</small>
            </div>
          </li>
          <li><strong>Trường hợp Quick Sort có độ phức tạp xấu nhất &Theta;(n&sup2;):</strong>
            Xảy ra khi ở <em>mọi bước đệ quy</em>, chốt được chọn luôn là <strong>phần tử cực trị (nhỏ nhất hoặc lớn nhất)</strong> của mảng con. Điều này dẫn đến phân hoạch bị <strong>lệch hoàn toàn</strong>: một nửa có <em>0</em> phần tử và nửa còn lại có <em>n - 1</em> phần tử.
            <br>&bull; <em>Ví dụ điển hình:</em> Mảng đã được sắp xếp tăng dần (hoặc giảm dần) mà thuật toán lại luôn chọn phần tử đầu tiên (hoặc cuối cùng) làm chốt. Khi đó hệ thức truy hồi trở thành <em>T(n) = T(n - 1) + &Theta;(n) &rArr; T(n) = &Theta;(n&sup2;)</em>.
          </li>
        </ul>
      </div>

    </div>
  </div>

  <div class="page-break"></div>

  <!-- ========================================================================= -->
  <!-- CÂU 5 -->
  <!-- ========================================================================= -->
  <div class="question-container">
    <div class="question-header">
      <span>CÂU 5: QUY HOẠCH ĐỘNG – BÀI TOÁN BA LÔ 0–1 (KNAPSACK)</span>
      <span class="score-tag">15 ĐIỂM</span>
    </div>
    <div class="de-bai-box">
      <div class="de-bai-label">Đề bài gốc:</div>
      Xét bài toán ba lô 0–1 với sức chứa <em>C = 7</em> và các đồ vật:
      <table class="data-table" style="width: 50%; margin: 6px auto;">
        <tr><th>Đồ vật i</th><th>1</th><th>2</th><th>3</th></tr>
        <tr><td>Trọng lượng w<sub>i</sub></td><td>2</td><td>3</td><td>4</td></tr>
        <tr><td>Giá trị v<sub>i</sub></td><td>6</td><td>10</td><td>12</td></tr>
      </table>
      Đặt <em>DP[i][c]</em> là giá trị lớn nhất khi chỉ xét <em>i</em> đồ vật đầu tiên và sức chứa là <em>c</em>.<br>
      <strong>a)</strong> Viết điều kiện cơ sở và công thức truy hồi cho <em>DP[i][c]</em>.<br>
      <strong>b)</strong> Điền bảng sau. Các cột sức chứa chạy từ 0 đến 7.<br>
      <strong>c)</strong> Ghi giá trị tối ưu, tập đồ vật được chọn và tổng trọng lượng.<br>
      <strong>d)</strong> Nêu độ phức tạp thời gian và bộ nhớ của cách làm bằng bảng DP này theo <em>n</em> và <em>C</em>.
    </div>

    <div class="solution-box">
      <div class="solution-header"></div>

      <div class="sub-item">
        <div class="sub-title">a) Điều kiện cơ sở và công thức truy hồi:</div>
        <ul>
          <li><strong>Ý nghĩa trạng thái:</strong> <em>DP[i][c]</em> là giá trị lớn nhất thu được khi chọn trong tập <em>i</em> đồ vật đầu tiên <em>{1, ..., i}</em> với giới hạn sức chứa ba lô là <em>c</em> (với <em>0 &le; i &le; 3</em> và <em>0 &le; c &le; 7</em>).</li>
          <li><strong>Điều kiện cơ sở:</strong>
            <br>&bull; <em>DP[0][c] = 0</em> với mọi <em>c &isin; {0, 1, ..., 7}</em> (khi không chọn đồ vật nào thì tổng giá trị bằng 0).
            <br>&bull; <em>DP[i][0] = 0</em> với mọi <em>i &isin; {0, 1, 2, 3}</em> (khi sức chứa ba lô bằng 0 thì không thể chứa đồ vật nào).
          </li>
          <li><strong>Công thức truy hồi (với i &ge; 1 và c &ge; 0):</strong>
            <div class="math-box">
              DP[i][c] = <strong>DP[i-1][c]</strong> &nbsp;&nbsp;&nbsp; nếu <em>w<sub>i</sub> &gt; c</em> (không thể chọn đồ vật i vì vượt quá sức chứa)<br>
              DP[i][c] = <strong>max( DP[i-1][c], &nbsp; DP[i-1][c - w<sub>i</sub>] + v<sub>i</sub> )</strong> &nbsp;&nbsp;&nbsp; nếu <em>w<sub>i</sub> &le; c</em> (cân nhắc giữa bỏ qua hoặc chọn đồ vật i)
            </div>
          </li>
        </ul>
      </div>

      <div class="sub-item">
        <div class="sub-title">b) Bảng quy hoạch động DP hoàn chỉnh (4 hàng &times; 8 cột):</div>
        <table class="data-table" style="font-size: 10pt;">
          <thead>
            <tr>
              <th style="background:#1e3a8a; color:#fff; width: 14%;">i \ c</th>
              <th style="width: 10%;">0</th>
              <th style="width: 10%;">1</th>
              <th style="width: 10%;">2</th>
              <th style="width: 10%;">3</th>
              <th style="width: 10%;">4</th>
              <th style="width: 10%;">5</th>
              <th style="width: 10%;">6</th>
              <th style="background:#fef08a; width: 16%;">7</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>i = 0</strong> (khởi tạo)</td>
              <td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
            </tr>
            <tr>
              <td><strong>i = 1</strong> (w<sub>1</sub>=2, v<sub>1</sub>=6)</td>
              <td>0</td><td>0</td><td>6</td><td>6</td><td>6</td><td>6</td><td>6</td><td>6</td>
            </tr>
            <tr>
              <td><strong>i = 2</strong> (w<sub>2</sub>=3, v<sub>2</sub>=10)</td>
              <td>0</td><td>0</td><td>6</td><td>10</td><td>10</td><td>16</td><td>16</td><td>16</td>
            </tr>
            <tr style="background:#eff6ff; font-weight: bold;">
              <td><strong>i = 3</strong> (w<sub>3</sub>=4, v<sub>3</sub>=12)</td>
              <td>0</td><td>0</td><td>6</td><td>10</td><td>12</td><td>16</td><td>18</td>
              <td style="background:#bbf7d0; color:#14532d; font-size:11pt; border: 2px solid #16a34a;">22</td>
            </tr>
          </tbody>
        </table>
        
        <div class="tip-box">
          <div class="tip-title">💡 Giải thích chi tiết cách tính các ô quan trọng của hàng i = 3:</div>
          &bull; Ô [3][4]: max(DP[2][4]=10, DP[2][4-4] + 12 = 0 + 12 = 12) = 12.<br>
          &bull; Ô [3][5]: max(DP[2][5]=16, DP[2][5-4] + 12 = 0 + 12 = 12) = 16.<br>
          &bull; Ô [3][6]: max(DP[2][6]=16, DP[2][6-4] + 12 = 6 + 12 = 18) = 18.<br>
          &bull; Ô [3][7]: max(DP[2][7]=16, DP[2][7-4] + 12 = 10 + 12 = 22) = <strong>22</strong>.
        </div>
      </div>

      <div class="sub-item" style="margin-top: 10px;">
        <div class="sub-title">c) Giá trị tối ưu, Tập đồ vật được chọn và Tổng trọng lượng:</div>
        <ul>
          <li><strong>Giá trị tối ưu:</strong> <strong>DP[3][7] = 22</strong>.</li>
          <li><strong>Các bước truy vết ngược (Backtracking / Traceback):</strong>
            <ul>
              <li>Bắt đầu tại ô <em>(i = 3, c = 7)</em>: So sánh thấy <em>DP[3][7] = 22 &ne; DP[2][7] = 16</em>.
                <br>&rArr; <strong>CHỌN ĐỒ VẬT 3</strong> (w<sub>3</sub> = 4, v<sub>3</sub> = 12).
                <br>Sức chứa còn lại chuyển về: <em>c = 7 - w<sub>3</sub> = 7 - 4 = 3</em>.
              </li>
              <li>Xét tại ô <em>(i = 2, c = 3)</em>: So sánh thấy <em>DP[2][3] = 10 &ne; DP[1][3] = 6</em>.
                <br>&rArr; <strong>CHỌN ĐỒ VẬT 2</strong> (w<sub>2</sub> = 3, v<sub>2</sub> = 10).
                <br>Sức chứa còn lại chuyển về: <em>c = 3 - w<sub>2</sub> = 3 - 3 = 0</em>.
              </li>
              <li>Xét tại ô <em>(i = 1, c = 0)</em>: Sức chứa <em>c = 0</em>, không chọn đồ vật 1. Thuật toán truy vết kết thúc.</li>
            </ul>
          </li>
          <li><strong>Tập đồ vật được chọn:</strong> <strong>{Đồ vật 2, Đồ vật 3}</strong> (hoặc viết {2, 3}).</li>
          <li><strong>Tổng trọng lượng thực tế:</strong> <em>w<sub>2</sub> + w<sub>3</sub> = 3 + 4 = <strong>7</strong></em> (vừa khít sức chứa tối đa C = 7).</li>
          <li><strong>Tổng giá trị thực tế:</strong> <em>v<sub>2</sub> + v<sub>3</sub> = 10 + 12 = <strong>22</strong></em>.</li>
        </ul>
      </div>

      <div class="sub-item" style="margin-top: 10px;">
        <div class="sub-title">d) Độ phức tạp thời gian và bộ nhớ của thuật toán:</div>
        <ul>
          <li><strong>Độ phức tạp thời gian:</strong> <strong>&Theta;(n &times; C)</strong> (bài toán có <em>n = 3, C = 7</em>, cần tính <em>(n + 1)(C + 1) = 4 &times; 8 = 32</em> ô, mỗi ô mất thời gian <em>&Theta;(1)</em>). Đây là độ phức tạp đa thức giả (pseudo-polynomial time).</li>
          <li><strong>Độ phức tạp bộ nhớ:</strong> <strong>&Theta;(n &times; C)</strong> để lưu toàn bộ bảng 2 chiều phục vụ cho bước truy vết tìm nghiệm (nếu chỉ cần tìm giá trị tối ưu thì có thể tối ưu mảng 1 chiều về <em>&Theta;(C)</em>).</li>
        </ul>
      </div>

    </div>
  </div>

  <div class="page-break"></div>

  <!-- ========================================================================= -->
  <!-- CÂU 6 -->
  <!-- ========================================================================= -->
  <div class="question-container">
    <div class="question-header">
      <span>CÂU 6: DUYỆT ĐỒ THỊ VÔ HƯỚNG – BFS & DFS</span>
      <span class="score-tag">15 ĐIỂM</span>
    </div>
    <div class="de-bai-box">
      <div class="de-bai-label">Đề bài gốc:</div>
      Cho đồ thị vô hướng <em>G = (V, E)</em> với:<br>
      <em>V = {A, B, C, D, E, F, G}</em><br>
      <em>E = {AB, AC, BD, BE, CF, EF, DG, FG}</em><br>
      Khi duyệt, luôn xét các đỉnh kề theo thứ tự chữ cái tăng dần.<br>
      <strong>a)</strong> Viết danh sách kề của đồ thị. (3 điểm)<br>
      <strong>b)</strong> Thực hiện BFS từ đỉnh A. Ghi thứ tự thăm, mảng cha của các đỉnh và đường đi ngắn nhất từ A đến G. (6 điểm)<br>
      <strong>c)</strong> Thực hiện DFS đệ quy từ đỉnh A, đánh dấu đỉnh ngay khi đi vào đỉnh đó. Ghi thứ tự thăm. (4 điểm)<br>
      <strong>d)</strong> Nếu thay danh sách kề bằng ma trận kề, hãy so sánh độ phức tạp khi cần liệt kê toàn bộ các đỉnh kề của một đỉnh. (2 điểm)
    </div>

    <div class="solution-box">
      <div class="solution-header"></div>

      <div class="sub-item">
        <div class="sub-title">a) Danh sách kề của đồ thị (sắp xếp tăng dần theo bảng chữ cái):</div>
        <table class="data-table" style="width: 70%; margin: 6px 0;">
          <thead>
            <tr><th style="width: 20%;">Đỉnh (u)</th><th style="width: 50%;">Danh sách đỉnh kề Adj(u)</th><th style="width: 30%;">Bậc deg(u)</th></tr>
          </thead>
          <tbody>
            <tr><td><strong>A</strong></td><td style="text-align: left; padding-left: 20px;"><strong>B, C</strong></td><td>2</td></tr>
            <tr><td><strong>B</strong></td><td style="text-align: left; padding-left: 20px;"><strong>A, D, E</strong></td><td>3</td></tr>
            <tr><td><strong>C</strong></td><td style="text-align: left; padding-left: 20px;"><strong>A, F</strong></td><td>2</td></tr>
            <tr><td><strong>D</strong></td><td style="text-align: left; padding-left: 20px;"><strong>B, G</strong></td><td>2</td></tr>
            <tr><td><strong>E</strong></td><td style="text-align: left; padding-left: 20px;"><strong>B, F</strong></td><td>2</td></tr>
            <tr><td><strong>F</strong></td><td style="text-align: left; padding-left: 20px;"><strong>C, E, G</strong></td><td>3</td></tr>
            <tr><td><strong>G</strong></td><td style="text-align: left; padding-left: 20px;"><strong>D, F</strong></td><td>2</td></tr>
          </tbody>
        </table>
        <small style="color:#64748b;">(Kiểm tra: Tổng bậc = 2 + 3 + 2 + 2 + 2 + 3 + 2 = 16 = 2 &times; 8 cạnh. Hoàn toàn chính xác!)</small>
      </div>

      <div class="sub-item" style="margin-top: 10px;">
        <div class="sub-title">b) Thực hiện thuật toán BFS từ đỉnh A:</div>
        <p><em>Mô phỏng hàng đợi FIFO Q (xét kề theo thứ tự alphabet):</em></p>
        <table class="data-table">
          <thead>
            <tr>
              <th>Bước</th><th>Đỉnh lấy ra</th><th>Đỉnh kề xét duyệt</th><th>Đỉnh mới được thăm & đưa vào Q</th><th>Trạng thái hàng đợi Q</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Khởi tạo</td><td>-</td><td>-</td><td>Thăm A, p[A] = null</td><td>[A]</td></tr>
            <tr><td>1</td><td><strong>A</strong></td><td>B, C</td><td>Thăm B (p[B]=A), thăm C (p[C]=A)</td><td>[B, C]</td></tr>
            <tr><td>2</td><td><strong>B</strong></td><td>A(bỏ), D, E</td><td>Thăm D (p[D]=B), thăm E (p[E]=B)</td><td>[C, D, E]</td></tr>
            <tr><td>3</td><td><strong>C</strong></td><td>A(bỏ), F</td><td>Thăm F (p[F]=C)</td><td>[D, E, F]</td></tr>
            <tr><td>4</td><td><strong>D</strong></td><td>B(bỏ), G</td><td>Thăm G (p[G]=D)</td><td>[E, F, G]</td></tr>
            <tr><td>5</td><td><strong>E</strong></td><td>B(bỏ), F(bỏ)</td><td>Không có đỉnh mới</td><td>[F, G]</td></tr>
            <tr><td>6</td><td><strong>F</strong></td><td>C(bỏ), E(bỏ), G(bỏ)</td><td>Không có đỉnh mới</td><td>[G]</td></tr>
            <tr><td>7</td><td><strong>G</strong></td><td>D(bỏ), F(bỏ)</td><td>Không có đỉnh mới</td><td>[ ] (rỗng &rarr; DỪNG)</td></tr>
          </tbody>
        </table>

        <div style="margin-top: 6px;">
          &bull; <strong>Thứ tự thăm các đỉnh:</strong> <strong>A &rarr; B &rarr; C &rarr; D &rarr; E &rarr; F &rarr; G</strong><br>
          &bull; <strong>Mảng cha (parent array):</strong>
          <table class="data-table" style="width: 75%; margin: 4px 0;">
            <tr><th>Đỉnh v</th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>F</th><th>G</th></tr>
            <tr><td><strong>parent(v)</strong></td><td><strong>null</strong></td><td><strong>A</strong></td><td><strong>A</strong></td><td><strong>B</strong></td><td><strong>B</strong></td><td><strong>C</strong></td><td><strong>D</strong></td></tr>
          </table>
          &bull; <strong>Đường đi ngắn nhất từ A đến G:</strong><br>
          Truy vết ngược từ đích: <em>G &larr; parent[G]=D &larr; parent[D]=B &larr; parent[B]=A</em>.<br>
          <div class="conclusion-badge">
            Đường đi ngắn nhất: <strong>A &rarr; B &rarr; D &rarr; G</strong> &nbsp;(chiều dài: 3 cạnh).
          </div>
        </div>
      </div>

      <div class="sub-item" style="margin-top: 10px;">
        <div class="sub-title">c) Thực hiện DFS đệ quy từ đỉnh A (đánh dấu ngay khi đi vào đỉnh):</div>
        <p><em>Quy trình gọi hàm đệ quy và quay lui (Backtracking) theo thứ tự alphabet:</em></p>
        <ol style="margin-bottom: 6px; padding-left: 20px;">
          <li>Từ <strong>A</strong>, thăm đỉnh kề đầu tiên là <strong>B</strong>.</li>
          <li>Từ <strong>B</strong>, đỉnh kề chưa thăm là D, E &rarr; chọn <strong>D</strong>.</li>
          <li>Từ <strong>D</strong>, đỉnh kề chưa thăm là G &rarr; chọn <strong>G</strong>.</li>
          <li>Từ <strong>G</strong>, đỉnh kề chưa thăm là F &rarr; chọn <strong>F</strong>.</li>
          <li>Từ <strong>F</strong>, đỉnh kề chưa thăm là C, E &rarr; thứ tự alphabet chọn <strong>C</strong>.</li>
          <li>Từ <strong>C</strong>, đỉnh kề là A và F đều đã thăm &rarr; hết đường, đệ quy quay lui về F.</li>
          <li>Tại <strong>F</strong>, xét đỉnh kề tiếp theo chưa thăm là <strong>E</strong> &rarr; đi vào thăm <strong>E</strong>.</li>
          <li>Từ <strong>E</strong>, các đỉnh kề (B, F) đều đã thăm &rarr; quay lui lần lượt về F &rarr; G &rarr; D &rarr; B &rarr; A. Kết thúc DFS.</li>
        </ol>
        <div class="conclusion-badge">
          &rArr; Thứ tự thăm các đỉnh trong DFS: <strong>A &rarr; B &rarr; D &rarr; G &rarr; F &rarr; C &rarr; E</strong>
        </div>
      </div>

      <div class="sub-item" style="margin-top: 10px;">
        <div class="sub-title">d) So sánh độ phức tạp khi liệt kê các đỉnh kề giữa Danh sách kề và Ma trận kề:</div>
        <ul>
          <li><strong>Với Danh sách kề (Adjacency List):</strong> Để liệt kê các đỉnh kề của đỉnh <em>u</em>, ta chỉ việc duyệt qua danh sách liên kết lưu các đỉnh kề của <em>u</em>. Chi phí thời gian là <strong>&Theta;(deg(u))</strong>. Với đồ thị thưa, <em>deg(u) &ll; |V|</em>, do đó thao tác này cực kỳ nhanh và tối ưu bộ nhớ.</li>
          <li><strong>Với Ma trận kề (Adjacency Matrix):</strong> Để tìm các đỉnh kề của đỉnh <em>u</em>, ta bắt buộc phải quét toàn bộ hàng <em>u</em> gồm đúng <em>|V|</em> phần tử để kiểm tra điều kiện <em>A[u][v] &ne; 0</em>. Do đó chi phí luôn là <strong>&Theta;(|V|)</strong>, bất kể đỉnh <em>u</em> có bậc nhỏ hay bằng 0.</li>
          <li><strong>Kết luận so sánh:</strong> Biểu diễn bằng danh sách kề vượt trội hơn hẳn về thời gian duyệt kề trên đồ thị thưa so với ma trận kề.</li>
        </ul>
      </div>

    </div>
  </div>

  <div class="page-break"></div>

  <!-- ========================================================================= -->
  <!-- CÂU 7 -->
  <!-- ========================================================================= -->
  <div class="question-container">
    <div class="question-header">
      <span>CÂU 7: THUẬT TOÁN ĐƯỜNG ĐI NGẮN NHẤT (DIJKSTRA & XỬ LÝ CẠNH ÂM)</span>
      <span class="score-tag">15 ĐIỂM</span>
    </div>
    <div class="de-bai-box">
      <div class="de-bai-label">Đề bài gốc:</div>
      Cho đồ thị có hướng, có trọng số không âm, với nguồn <em>A</em> và các cung:
      <table class="data-table" style="margin: 4px 0;">
        <tr>
          <th>Cung</th><th>A&rarr;B</th><th>A&rarr;C</th><th>B&rarr;C</th><th>B&rarr;D</th><th>C&rarr;B</th><th>C&rarr;D</th><th>C&rarr;E</th><th>D&rarr;E</th><th>E&rarr;D</th>
        </tr>
        <tr>
          <td><strong>Trọng số</strong></td><td>4</td><td>2</td><td>1</td><td>5</td><td>1</td><td>8</td><td>10</td><td>2</td><td>3</td>
        </tr>
      </table>
      <strong>a)</strong> Giải thích vì sao BFS không phải lựa chọn phù hợp cho đồ thị này và vì sao Dijkstra có thể được dùng. (3 điểm)<br>
      <strong>b)</strong> Mô phỏng Dijkstra từ nguồn A. Ở mỗi bước ghi đỉnh vừa được cố định và các giá trị tạm thời <em>d(A), d(B), d(C), d(D), d(E)</em>. Cuối cùng ghi đường đi ngắn nhất từ A đến E. (9 điểm)<br>
      <strong>c)</strong> Nếu bổ sung cung <em>B &rarr; A</em> có trọng số <em>-6</em> thì:<br>
      i) Dijkstra còn được dùng an toàn không?<br>
      ii) nên dùng thuật toán nào để phát hiện vấn đề?<br>
      iii) trong trường hợp đồ thị không có chu trình âm, nếu cần khoảng cách giữa mọi cặp đỉnh, thuật toán nào trong Bài 6 phù hợp hơn? (3 điểm)
    </div>

    <div class="solution-box">
      <div class="solution-header"></div>

      <div class="sub-item">
        <div class="sub-title">a) Giải thích tính phù hợp của BFS và Dijkstra:</div>
        <ul>
          <li><strong>Vì sao BFS không phù hợp:</strong> BFS chỉ tìm được đường đi ngắn nhất trên đồ thị <strong>không có trọng số</strong> (hoặc đồ thị mà tất cả các cạnh có trọng số đồng nhất bằng nhau). Với đồ thị có trọng số bất kỳ, đường đi qua ít cạnh nhất không đồng nghĩa với đường đi có tổng trọng số nhỏ nhất. Ví dụ: từ A đến B có đường trực tiếp A&rarr;B (1 cạnh, trọng số = 4) nhưng đường đi A&rarr;C&rarr;B (2 cạnh) lại có tổng trọng số chỉ bằng <em>2 + 1 = 3 &lt; 4</em>.</li>
          <li><strong>Vì sao Dijkstra có thể được dùng:</strong> Vì toàn bộ các cung trong đồ thị đều có <strong>trọng số không âm</strong> (<em>w(e) &ge; 0</em> với mọi <em>e &isin; E</em>), thỏa mãn điều kiện tiên quyết bắt buộc để thuật toán Dijkstra đảm bảo tính đúng đắn.</li>
        </ul>
      </div>

      <div class="sub-item" style="margin-top: 10px;">
        <div class="sub-title">b) Mô phỏng từng bước thuật toán Dijkstra từ nguồn A:</div>
        <p><em>Quy tắc:</em> Ký hiệu dấu sao (<code>*</code>) thể hiện đỉnh đã được cố định vĩnh viễn (thuộc tập S). Công thức nới lỏng: <em>d(v) = min(d(v), d(u) + w(u &rarr; v))</em>.</p>
        
        <table class="data-table" style="font-size: 10pt;">
          <thead>
            <tr>
              <th style="width: 14%;">Bước</th>
              <th style="width: 20%;">Đỉnh vừa cố định</th>
              <th style="width: 13%;">d(A)</th>
              <th style="width: 13%;">d(B)</th>
              <th style="width: 13%;">d(C)</th>
              <th style="width: 13%;">d(D)</th>
              <th style="width: 13%;">d(E)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Khởi tạo</strong></td>
              <td>-</td>
              <td><strong>0</strong></td>
              <td>&infin;</td>
              <td>&infin;</td>
              <td>&infin;</td>
              <td>&infin;</td>
            </tr>
            <tr style="background:#f8fafc;">
              <td><strong>Bước 1</strong></td>
              <td><strong>A</strong> (nhãn min = 0)</td>
              <td><strong>0*</strong></td>
              <td>4</td>
              <td>2</td>
              <td>&infin;</td>
              <td>&infin;</td>
            </tr>
            <tr style="background:#eff6ff;">
              <td><strong>Bước 2</strong></td>
              <td><strong>C</strong> (nhãn min = 2)</td>
              <td><strong>0*</strong></td>
              <td style="color:#1d4ed8; font-weight:bold;">3</td>
              <td><strong>2*</strong></td>
              <td style="color:#1d4ed8; font-weight:bold;">10</td>
              <td style="color:#1d4ed8; font-weight:bold;">12</td>
            </tr>
            <tr style="background:#f8fafc;">
              <td><strong>Bước 3</strong></td>
              <td><strong>B</strong> (nhãn min = 3)</td>
              <td><strong>0*</strong></td>
              <td><strong>3*</strong></td>
              <td><strong>2*</strong></td>
              <td style="color:#1d4ed8; font-weight:bold;">8</td>
              <td>12</td>
            </tr>
            <tr style="background:#eff6ff;">
              <td><strong>Bước 4</strong></td>
              <td><strong>D</strong> (nhãn min = 8)</td>
              <td><strong>0*</strong></td>
              <td><strong>3*</strong></td>
              <td><strong>2*</strong></td>
              <td><strong>8*</strong></td>
              <td style="color:#1d4ed8; font-weight:bold;">10</td>
            </tr>
            <tr style="background:#f0fdf4;">
              <td><strong>Bước 5</strong></td>
              <td><strong>E</strong> (nhãn min = 10)</td>
              <td><strong>0*</strong></td>
              <td><strong>3*</strong></td>
              <td><strong>2*</strong></td>
              <td><strong>8*</strong></td>
              <td><strong>10*</strong></td>
            </tr>
          </tbody>
        </table>

        <div class="tip-box">
          <div class="tip-title">🔍 Thuyết minh chi tiết các bước cập nhật nhãn (Relaxation):</div>
          &bull; <strong>Bước 1:</strong> Cố định A. Kề của A là B và C &rarr; <em>d(B) = min(&infin;, 0 + 4) = 4</em> (parent=A); <em>d(C) = min(&infin;, 0 + 2) = 2</em> (parent=A).<br>
          &bull; <strong>Bước 2:</strong> Trong {B:4, C:2, D:&infin;, E:&infin;}, min là C (d=2). Cố định C. Cung đi từ C:
          <br>&nbsp;&nbsp;- Đến B: <em>d(B) = min(4, d(C) + w(C&rarr;B)) = min(4, 2 + 1) = 3</em> &lt; 4 &rarr; <strong>Cập nhật d(B) = 3</strong>, parent[B] = C.
          <br>&nbsp;&nbsp;- Đến D: <em>d(D) = min(&infin;, 2 + 8) = 10</em>, parent[D] = C.
          <br>&nbsp;&nbsp;- Đến E: <em>d(E) = min(&infin;, 2 + 10) = 12</em>, parent[E] = C.<br>
          &bull; <strong>Bước 3:</strong> Trong {B:3, D:10, E:12}, min là B (d=3). Cố định B. Cung đi từ B:
          <br>&nbsp;&nbsp;- Đến D: <em>d(D) = min(10, d(B) + w(B&rarr;D)) = min(10, 3 + 5) = 8</em> &lt; 10 &rarr; <strong>Cập nhật d(D) = 8</strong>, parent[D] = B.<br>
          &bull; <strong>Bước 4:</strong> Trong {D:8, E:12}, min là D (d=8). Cố định D. Cung đi từ D:
          <br>&nbsp;&nbsp;- Đến E: <em>d(E) = min(12, d(D) + w(D&rarr;E)) = min(12, 8 + 2) = 10</em> &lt; 12 &rarr; <strong>Cập nhật d(E) = 10</strong>, parent[E] = D.<br>
          &bull; <strong>Bước 5:</strong> Cố định E (d=10). Kiểm tra cung E&rarr;D (w=3): <em>10 + 3 = 13 &gt; 8</em>, không đổi. Hoàn tất thuật toán.
        </div>

        <p style="margin-top: 8px;">
          <strong>Truy vết đường đi ngắn nhất từ A đến E:</strong><br>
          Từ đích E: <em>E &larr; parent[E]=D &larr; parent[D]=B &larr; parent[B]=C &larr; parent[C]=A</em>.
        </p>
        <div class="conclusion-badge" style="font-size: 10.5pt;">
          Đường đi ngắn nhất từ A đến E: &nbsp; <strong>A &rarr; C &rarr; B &rarr; D &rarr; E</strong>
          <br>Tổng độ dài đường đi: <strong>w(A&rarr;C) + w(C&rarr;B) + w(B&rarr;D) + w(D&rarr;E) = 2 + 1 + 5 + 2 = 10</strong>
        </div>
      </div>

      <div class="sub-item" style="margin-top: 12px;">
        <div class="sub-title">c) Khi bổ sung cung B &rarr; A có trọng số -6:</div>
        <ul>
          <li><strong>i) Dijkstra còn được dùng an toàn không?</strong>
            <br><strong>KHÔNG ĐƯỢC DÙNG</strong>. Vì xuất hiện cạnh có trọng số âm (<em>w(B &rarr; A) = -6 &lt; 0</em>), vi phạm giả định nền tảng của Dijkstra. 
            Đặc biệt, xét chu trình <strong>A &rarr; C &rarr; B &rarr; A</strong>:
            <div class="math-box">
              Tổng trọng số chu trình = w(A &rarr; C) + w(C &rarr; B) + w(B &rarr; A) = 2 + 1 + (-6) = <strong>-3 &lt; 0</strong> (Chu trình âm - Negative Cycle).
            </div>
            Chu trình âm này đi qua được từ nguồn A, làm cho khoảng cách đến các đỉnh liên quan có thể giảm vô hạn về <em>-&infin;</em> khi đi vòng qua chu trình này nhiều lần.
          </li>
          <li><strong>ii) Nên dùng thuật toán nào để phát hiện vấn đề?</strong>
            <br>Nên dùng thuật toán <strong>Bellman-Ford</strong>. Thuật toán này cho phép tìm đường đi ngắn nhất trên đồ thị có trọng số âm và có khả năng <strong>phát hiện chu trình âm</strong>: sau khi thực hiện <em>|V| - 1</em> lần nới lỏng toàn bộ các cạnh, nếu ở bước thứ <em>|V|</em> vẫn còn ít nhất một cạnh có thể nới lỏng được nữa (tức <em>d(v) &gt; d(u) + w(u, v)</em>) thì đồ thị chắc chắn chứa chu trình âm đến được từ nguồn.
          </li>
          <li><strong>iii) Thuật toán tìm khoảng cách giữa mọi cặp đỉnh (All-Pairs Shortest Paths):</strong>
            <br>Thuật toán phù hợp nhất trong chương trình Bài 6 là thuật toán <strong>Floyd-Warshall</strong> (thuật toán quy hoạch động giải bài toán mọi cặp đỉnh có độ phức tạp thời gian <em>&Theta;(|V|&sup3;)</em>, hoạt động chính xác với đồ thị có cạnh âm miễn là không có chu trình âm).
          </li>
        </ul>
      </div>

    </div>
  </div>

  <!-- Footer note -->
  <div style="text-align: center; font-style: italic; color: #64748b; font-size: 9pt; border-top: 1px dashed #cbd5e1; padding-top: 8px; margin-top: 16px;">
    ─── HẾT TOÀN BỘ ĐỀ BÀI VÀ BÀI LÀM MẪU ───<br>
    Học viên đối chiếu kỹ các bước lập luận, bảng biến thiên và truy vết trước khi hoàn thành bài nộp.
  </div>

</body>
</html>
"""

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Đã ghi xong file HTML tại: {HTML_FILE}")

# Render to PDF using Edge headless
cmd = [
    EDGE_PATH,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={PDF_FILE}",
    HTML_FILE
]

print("Đang chuyển đổi HTML sang PDF bằng Edge Headless...")
result = subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(PDF_FILE):
    size_kb = os.path.getsize(PDF_FILE) / 1024
    print(f"Xuất file PDF thành công: {PDF_FILE} ({size_kb:.2f} KB)")
    try:
        shutil.copy2(PDF_FILE, DOWNLOAD_PDF)
        print(f"Đã sao chép vào thư mục Downloads: {DOWNLOAD_PDF}")
    except Exception as e:
        print(f"Không thể chép vào Downloads: {e}")
else:
    print("Xuất file PDF thất bại!")
    print("Stderr:", result.stderr)

