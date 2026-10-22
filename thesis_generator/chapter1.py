import os
from thesis_generator.style_helper import (
    add_chapter_heading, add_section_heading, add_subsection_heading,
    add_body_paragraph, add_bullet_item, add_image_figure, add_table_data
)

def add_chapter_1(doc):
    """
    CHƯƠNG 1: TỔNG QUAN VÀ ĐẶT VẤN ĐỀ
    Bám sát quy mô, khảo sát hiện trạng, phân tích bài toán thực tế và mục tiêu đề tài.
    """
    add_chapter_heading(doc, "CHƯƠNG 1: TỔNG QUAN VÀ ĐẶT VẤN ĐỀ")

    add_section_heading(doc, "1.1. Tính cấp thiết của đề tài")
    add_body_paragraph(doc, "Trong bối cảnh quá trình đô thị hóa đang diễn ra với tốc độ chóng mặt tại các đô thị lớn ở Việt Nam như Hà Nội, Thành phố Hồ Chí Minh, Đà Nẵng, sự bùng nổ của phương tiện giao thông cá nhân – đặc biệt là ô tô gia đình và xe máy – đã tạo ra áp lực đè nặng lên cơ sở hạ tầng giao thông tĩnh. Quỹ đất dành cho bãi đỗ xe luôn trong tình trạng thiếu hụt trầm trọng so với tốc độ tăng trưởng phương tiện thực tế hàng năm.")
    add_body_paragraph(doc, "Tình trạng người điều khiển phương tiện phải lòng vòng tìm kiếm vị trí đỗ xe tại các trung tâm thương mại, tòa nhà văn phòng, khu chung cư hay bệnh viện là một vấn đề nhức nhối diễn ra hàng ngày. Theo các nghiên cứu giao thông đô thị quốc tế (như nghiên cứu nổi tiếng của GS. Donald Shoup - UCLA), có tới 30% lượng phương tiện lưu thông trên các tuyến phố nội đô vào giờ cao điểm bắt nguồn từ những xe đang đi vòng quanh tìm chỗ đỗ. Hệ quả trực tiếp của thực trạng này là gia tăng ùn tắc giao thông, lãng phí thời gian, tiêu hao nhiên liệu vô ích và phát thải một lượng khí thải carbon khổng lồ gây ô nhiễm môi trường sống.")
    add_body_paragraph(doc, "Tại Việt Nam, phần lớn các bãi đỗ xe hiện nay vẫn đang vận hành theo các phương thức truyền thống mang tính thủ công hoặc bán tự động đơn giản:")
    add_bullet_item(doc, "Quản lý bằng thẻ từ nhựa thủ công: Nhân viên bảo vệ phải quẹt thẻ tại cổng, thu tiền mặt trực tiếp. Quy trình này dễ dẫn đến ùn tắc kéo dài tại cổng barrier vào các khung giờ cao điểm khi lượng xe ra vào dồn dập.", bold_prefix="Hạn chế về tốc độ kiểm soát: ")
    add_bullet_item(doc, "Thiếu thông tin vị trí trống theo thời gian thực: Khách hàng khi di chuyển qua cổng barrier hoàn toàn không biết khu vực nào, tầng nào, hoặc vị trí cụ thể nào còn trống. Việc tự lái xe dò tìm trong bãi đỗ rộng hàng nghìn mét vuông gây ức chế tâm lý và tiềm ẩn rủi ro va quẹt.", bold_prefix="Trải nghiệm người dùng kém: ")
    add_bullet_item(doc, "Nguy cơ thất thoát doanh thu và gian lận vé: Việc thanh toán tiền mặt truyền thống rất khó kiểm soát tuyệt đối, dễ xảy ra sai lệch số liệu doanh thu giữa ca trực, gây khó khăn cho chủ doanh nghiệp khai thác điểm đỗ.", bold_prefix="Khó khăn trong quản trị tài chính: ")
    add_bullet_item(doc, "Thiếu công cụ phân tích dữ liệu phục vụ điều hành: Ban quản lý không nắm bắt được quy luật biến động lưu lượng phương tiện theo giờ, theo ngày hay ngày lễ để tối ưu hóa nhân sự, điều chỉnh mức giá linh hoạt hoặc quy hoạch mở rộng bãi đỗ.", bold_prefix="Bất cập trong dự báo và điều phối: ")

    add_image_figure(
        doc,
        fig_id="Hình 1.1",
        fig_title="Thực trạng ùn tắc phương tiện tại cổng kiểm soát bãi đỗ xe truyền thống",
        image_path=os.path.join(os.getcwd(), "report_images", "fig1_1_traffic.png"),
        note_instructions="Sơ đồ phân tích thực trạng ùn ứ phương tiện tại cổng soát vé bãi giữ xe truyền thống và giải pháp chuyển đổi số SPS."
    )

    add_body_paragraph(doc, "Xuất phát từ những bất cập thực tiễn nêu trên, việc nghiên cứu và xây dựng một giải pháp phần mềm toàn diện – 'Hệ thống Quản lý Bãi đỗ xe Thông minh (Smart Parking System - SPS)' – tích hợp các công nghệ phần mềm hiện đại như Web thời gian thực (WebSocket), thuật toán dẫn đường tối ưu trong không gian 2D (A* Algorithm) và mô hình học máy dự báo nhu cầu (Random Forest Regressor) mang tính thời sự cao, cấp thiết và có giá trị ứng dụng thực tiễn to lớn.")

    add_section_heading(doc, "1.2. Khảo sát hiện trạng và các giải pháp tương tự")
    add_body_paragraph(doc, "Nhằm có cái nhìn toàn diện và khách quan trước khi bắt tay vào thiết kế kiến trúc hệ thống, đề tài đã tiến hành khảo sát và đánh giá ưu nhược điểm của các mô hình quản lý bãi đỗ xe đang được áp dụng phổ biến trên thế giới cũng như tại thị trường Việt Nam hiện nay.")

    add_subsection_heading(doc, "1.2.1. Bãi đỗ xe truyền thống dùng thẻ giấy / vé giấy bấm giờ")
    add_body_paragraph(doc, "Mô hình này phổ biến tại các bãi gửi xe tạm thời hoặc quy mô nhỏ. Khi xe vào, nhân viên bảo vệ ghi biển số xe và giờ vào lên một cuống vé giấy; khi xe ra, nhân viên thu lại cuống vé, tính giờ thủ công và thu tiền mặt.")
    add_bullet_item(doc, "Chi phí đầu tư ban đầu gần như bằng không, không yêu cầu thiết bị công nghệ phức tạp.", bold_prefix="Ưu điểm: ")
    add_bullet_item(doc, "Dễ xảy ra mất mát vé, rách ướt gây tranh chấp; tốc độ phục vụ cực kỳ chậm; khả năng gian lận tiền vé cao; hoàn toàn không có khả năng lưu vết lịch sử hay thống kê báo cáo.", bold_prefix="Nhược điểm: ")

    add_subsection_heading(doc, "1.2.2. Bãi đỗ xe bán tự động dùng thẻ từ RFID kết hợp Barrier")
    add_body_paragraph(doc, "Đây là giải pháp đang được triển khai phổ biến nhất tại các trung tâm thương mại (như Vincom, Aeon Mall), trường đại học và chung cư cao cấp hiện nay. Hệ thống bao gồm đầu đọc thẻ từ RFID, camera chụp ảnh biển số xe vào/ra và barrier tự động.")
    add_bullet_item(doc, "Tốc độ xử lý qua cổng được cải thiện (khoảng 3 – 5 giây/xe), lưu lại hình ảnh đối chiếu biển số xe nhằm hạn chế rủi ro mất cắp phương tiện.", bold_prefix="Ưu điểm: ")
    add_bullet_item(doc, "Chưa cung cấp bản đồ số hướng dẫn lái xe đến vị trí cụ thể. Khi qua barrier, tài xế vẫn phải tự quan sát đèn báo trên trần hoặc tự đi tìm. Đa phần các hệ thống này chưa có cổng thông tin điện tử cho khách hàng đặt chỗ trước (Booking), chưa tích hợp thanh toán số trực tuyến qua mã QR động và chưa có thuật toán dự báo thông minh.", bold_prefix="Nhược điểm: ")

    add_subsection_heading(doc, "1.2.3. Các giải pháp Smart Parking trên thế giới")
    add_body_paragraph(doc, "Tại các quốc gia phát triển như Singapore, Đức, Nhật Bản hay Mỹ, các hệ thống Smart Parking (như Parkopedia, SpotHero, RingGo) đã phát triển ở mức độ cao:")
    add_bullet_item(doc, "Cho phép người dùng tra cứu điểm đỗ trên ứng dụng di động, đặt trước chỗ đỗ (Reservation), thanh toán không chạm qua thẻ tín dụng quốc tế hoặc ví điện tử Apple Pay/Google Pay.", bold_prefix="Đặc điểm nổi bật: ")
    add_bullet_item(doc, "Tuy nhiên, các hệ thống thương mại này thường có chi phí bản quyền và chi phí triển khai phần cứng cảm biến siêu âm/camera AI cực kỳ đắt đỏ (hàng trăm triệu đến hàng tỷ đồng cho một điểm đỗ). Việc chuyển giao, tùy biến hoặc áp dụng cho các doanh nghiệp, chuỗi điểm đỗ vừa và nhỏ tại Việt Nam gặp nhiều rào cản lớn về tài chính và tính tương thích.", bold_prefix="Rào cản áp dụng tại Việt Nam: ")

    table_comp_headers = ["Tiêu chí so sánh", "Bãi xe truyền thống", "Thẻ từ RFID bán tự động", "Smart Parking quốc tế", "Hệ thống SPS đề tài"]
    table_comp_rows = [
        ["Thiết bị nhận diện", "Vé giấy thủ công", "Thẻ từ RFID + Camera", "Cảm biến IoT + Camera AI", "Mã QR động + RFID/Biển số"],
        ["Đặt trước (Booking)", "Không hỗ trợ", "Không hỗ trợ", "Hỗ trợ (App Mobile)", "Hỗ trợ đầy đủ (Web/Mobile)"],
        ["Bản đồ định vị & Dẫn đường", "Không có", "Đèn LED trên trần", "GPS ngoài trời", "Bản đồ 2D + Thuật toán A*"],
        ["Cập nhật thời gian thực", "Thủ công", "Bảng LED tổng cổng", "API / Mobile Push", "WebSocket 2 chiều độ trễ mili-giây"],
        ["Dự báo nhu cầu (AI)", "Không có", "Không có", "Mô hình đám mây lớn", "Random Forest tích hợp (4.320 mẫu)"],
        ["Phương thức thanh toán", "Tiền mặt", "Tiền mặt / Quẹt thẻ", "Thẻ tín dụng", "QR Code đa kênh / Ví số / Tiền mặt"],
        ["Chi phí triển khai", "Rất thấp", "Trung bình - Cao", "Rất cao (bản quyền ngoại)", "Tối ưu, linh hoạt, mã nguồn mở"]
    ]
    add_table_data(doc, "Bảng 1.1", "Bảng so sánh tổng quan giữa các giải pháp quản lý bãi đỗ xe", table_comp_headers, table_comp_rows, col_widths=[3.0, 3.0, 3.2, 3.2, 3.6])

    add_section_heading(doc, "1.3. Mục tiêu nghiên cứu và đối tượng của đề tài")
    add_subsection_heading(doc, "1.3.1. Mục tiêu nghiên cứu")
    add_body_paragraph(doc, "Đề tài được thực hiện nhằm hướng tới các mục tiêu cụ thể sau:")
    add_bullet_item(doc, "Nghiên cứu nguyên lý hoạt động, cấu trúc dữ liệu và triển khai thuật toán tìm đường tối ưu A* (A-Star) trên mô hình lưới 2D (Grid Matrix), ứng dụng điều hướng chỉ dẫn phương tiện từ cổng barrier tới đúng vị trí đỗ được phân bổ, né tránh các chướng ngại vật tĩnh và làn xe đã bị chiếm dụng.", bold_prefix="1. Về thuật toán điều hướng: ")
    add_bullet_item(doc, "Xây dựng pipeline thu thập/sinh dữ liệu chuỗi thời gian lịch sử (4.320 mẫu dữ liệu bao gồm các đặc trưng thời gian, loại xe, sự kiện, thời tiết) và huấn luyện mô hình học máy Random Forest Regressor với 200 cây quyết định, nhằm dự báo chính xác tỷ lệ lấp đầy bãi đỗ xe trong các khung giờ tương lai.", bold_prefix="2. Về mô hình trí tuệ nhân tạo: ")
    add_bullet_item(doc, "Thiết kế kiến trúc hệ thống Client-Server hiện đại, phân tách rõ ràng Frontend (Vue 3, Vite, Tailwind CSS, Pinia) và Backend (FastAPI, SQLAlchemy ORM, Uvicorn, PostgreSQL), đảm bảo tính module hóa cao, độ trễ thấp và khả năng mở rộng (Scalability).", bold_prefix="3. Về kiến trúc phần mềm: ")
    add_bullet_item(doc, "Cung cấp đầy đủ các giao diện phân quyền cho 3 nhóm đối tượng: Khách hàng (Customer), Nhân viên vận hành bãi (Staff/Operator) và Quản trị viên hệ thống (Admin).", bold_prefix="4. Về trải nghiệm người dùng: ")

    add_subsection_heading(doc, "1.3.2. Đối tượng và phạm vi nghiên cứu")
    add_bullet_item(doc, "Hệ thống quản lý điểm đỗ xe ô tô và xe máy tại các tòa nhà văn phòng, khu trung tâm thương mại hoặc các cụm bãi đỗ tập trung đô thị.", bold_prefix="Đối tượng nghiên cứu: ")
    add_bullet_item(doc, "Tập trung xây dựng ứng dụng Web hoàn chỉnh (Responsive trên cả Desktop và thiết bị di động), mô phỏng cơ chế đóng mở barrier và kiểm soát xe vào/ra qua giao thức WebSocket và quét mã QR.", bold_prefix="Phạm vi triển khai: ")
    add_bullet_item(doc, "Đề tài tập trung chuyên sâu vào tầng phần mềm điều hành, xử lý logic nghiệp vụ, thuật toán dẫn đường 2D và mô hình AI dự báo. Các phần cứng vật lý (camera nhận diện biển số thực tế, rào chắn barrier cơ học) được mô phỏng trực quan tương đương trên hệ thống phần mềm.", bold_prefix="Giới hạn đề tài: ")

    add_section_heading(doc, "1.4. Phương pháp nghiên cứu và công nghệ lựa chọn")
    add_body_paragraph(doc, "Để đạt được các mục tiêu đề ra, đề tài áp dụng phương pháp tiếp cận kỹ thuật công nghệ phần mềm thực nghiệm kết hợp với phân tích toán học và học máy:")
    add_bullet_item(doc, "Khảo sát và đặc tả yêu cầu người dùng theo chuẩn UML (Use Case, Activity, Sequence, ERD).", bold_prefix="Phương pháp phân tích & thiết kế: ")
    add_bullet_item(doc, "Mô hình hóa bãi đỗ xe thành ma trận tọa độ lưới 2D $(x, y)$. Áp dụng hàm đánh giá $f(n) = g(n) + h(n)$ với khoảng cách Manhattan để tính toán lộ trình ngắn nhất không va chạm.", bold_prefix="Phương pháp thuật toán: ")
    add_bullet_item(doc, "Sử dụng thư viện Scikit-learn để tiền xử lý đặc trưng, chuẩn hóa dữ liệu, huấn luyện mô hình hồi quy Random Forest và đánh giá mô hình bằng các chỉ số MAE, MSE, RMSE.", bold_prefix="Phương pháp học máy: ")
    add_bullet_item(doc, "Áp dụng phương pháp Agile/Scrum lặp ngắn, phát triển song song các module Backend API và Frontend Component, thực hiện Unit Testing và End-to-End Testing liên tục.", bold_prefix="Quy trình phát triển phần mềm: ")

    add_section_heading(doc, "1.5. Bố cục tổng thể của báo cáo đồ án")
    add_body_paragraph(doc, "Nội dung báo cáo đồ án được cấu trúc mạch lạc thành 5 chương chính và các phần phụ lục đính kèm như sau:")
    add_bullet_item(doc, "Trình bày lý do chọn đề tài, tính cấp thiết, phân tích các giải pháp hiện nay, mục tiêu nghiên cứu, phạm vi và bố cục báo cáo.", bold_prefix="Chương 1: Tổng quan và đặt vấn đề – ")
    add_bullet_item(doc, "Đặc tả yêu cầu chức năng/phi chức năng, sơ đồ Use Case, kiến trúc 3 tầng, thiết kế cơ sở dữ liệu quan hệ chi tiết với 6 bảng cốt lõi, giải pháp chống Race Condition bằng SELECT FOR UPDATE và cơ chế bảo mật JWT/Bcrypt.", bold_prefix="Chương 2: Phân tích yêu cầu và thiết kế hệ thống – ")
    add_bullet_item(doc, "Cơ sở toán học thuật toán A* trong không gian lưới 2D, mô hình hoạt ảnh GSAP 3 và thiết kế đường ống huấn luyện học máy Random Forest Regressor 200 cây dự báo nhu cầu điểm đỗ.", bold_prefix="Chương 3: Thuật toán điều hướng A* và mô hình học máy Random Forest – ")
    add_bullet_item(doc, "Chi tiết triển khai kỹ thuật Backend FastAPI (28 REST endpoints, WebSocket) và Frontend Vue 3 Composition API, Tailwind CSS cho 3 cổng tương tác (Khách hàng, Nhân viên, Quản trị viên).", bold_prefix="Chương 4: Hiện thực hóa và xây dựng hệ thống – ")
    add_bullet_item(doc, "Kế hoạch kiểm thử, kết quả 11 kịch bản Unit Test (Pytest), kiểm thử đặt chỗ đồng thời đa luồng, kiểm thử giao diện Playwright, phân tích rủi ro, kết luận và phương hướng phát triển tương lai.", bold_prefix="Chương 5: Kiểm thử, đánh giá kết quả và kết luận – ")
    add_bullet_item(doc, "Bao gồm Danh mục tài liệu tham khảo theo định dạng chuẩn IEEE, Phụ lục A đặc tả 28 REST API endpoints, Phụ lục B cấu trúc cây thư mục mã nguồn và Phụ lục C tài liệu hướng dẫn thiết lập môi trường.", bold_prefix="Tài liệu tham khảo & Phụ lục – ")

