import re
from pathlib import Path

index_path = Path("frontend/index.html")
content = index_path.read_text(encoding="utf-8")

customer_screens_html = '''
        <!-- ============================================================== -->
        <!-- CUSTOMER SCREEN 1: DASHBOARD (Tổng quan khách hàng)           -->
        <!-- ============================================================== -->
        <div v-if="activeNav === 'cust-dashboard'" class="space-y-6 max-w-6xl mx-auto">
          <!-- Welcome Banner -->
          <div class="bg-gradient-to-r from-[#0b1020] via-slate-900 to-indigo-950 rounded-3xl p-6 sm:p-8 text-white relative overflow-hidden shadow-xl border border-slate-800">
            <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div>
                <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-bold mb-3 border border-emerald-500/30">
                  <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  Tài khoản Khách hàng
                </div>
                <h2 class="text-2xl sm:text-3xl font-black tracking-tight text-white mb-1.5 flex items-center gap-3">
                  <span>👤 Xin chào, {{ currentUser?.full_name || 'Khách hàng' }}!</span>
                </h2>
                <p class="text-xs sm:text-sm text-slate-300 max-w-xl leading-relaxed">
                  Chào mừng bạn đến với hệ thống đỗ xe thông minh Smart Parking. Quản lý đặt chỗ, phương tiện và theo dõi phiên gửi xe trực tiếp ngay tại đây.
                </p>
              </div>
              <div class="flex flex-wrap items-center gap-2.5 shrink-0">
                <button
                  @click="activeNav = 'cust-find-parking'"
                  class="px-5 py-3 rounded-2xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-xs shadow-lg shadow-emerald-500/25 transition active:scale-95 flex items-center gap-2 cursor-pointer"
                >
                  <i class="fa-solid fa-square-parking"></i> Tìm &amp; Đặt chỗ
                </button>
                <button
                  @click="openAddVehicleModal()"
                  class="px-4 py-3 rounded-2xl bg-white/10 hover:bg-white/20 text-white font-semibold text-xs border border-white/15 backdrop-blur-md transition cursor-pointer flex items-center gap-2"
                >
                  <i class="fa-solid fa-car"></i> Thêm xe mới
                </button>
              </div>
            </div>
          </div>

          <!-- Quick Stat Cards (6 thẻ thông số) -->
          <div class="grid grid-cols-2 lg:grid-cols-6 gap-4">
            <!-- 1. Chỗ trống hiện tại -->
            <div class="bg-white rounded-2xl p-4 border border-slate-100 shadow-sm flex flex-col justify-between">
              <div class="flex items-center justify-between text-slate-400 mb-2">
                <span class="text-[11px] font-bold uppercase tracking-wider">Chỗ trống</span>
                <span class="w-7 h-7 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center text-xs font-bold">🅿️</span>
              </div>
              <div class="text-2xl font-black text-slate-900">32</div>
              <div class="text-[10px] text-emerald-600 font-semibold mt-1">Khả dụng tại Bãi chính</div>
            </div>

            <!-- 2. Booking đang hoạt động -->
            <div class="bg-white rounded-2xl p-4 border border-slate-100 shadow-sm flex flex-col justify-between">
              <div class="flex items-center justify-between text-slate-400 mb-2">
                <span class="text-[11px] font-bold uppercase tracking-wider">Booking</span>
                <span class="w-7 h-7 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center text-xs">📅</span>
              </div>
              <div class="text-2xl font-black text-slate-900">{{ activeBookingCount }}</div>
              <div class="text-[10px] text-blue-600 font-semibold mt-1">Đang hoạt động</div>
            </div>

            <!-- 3. Phương tiện của tôi -->
            <div class="bg-white rounded-2xl p-4 border border-slate-100 shadow-sm flex flex-col justify-between">
              <div class="flex items-center justify-between text-slate-400 mb-2">
                <span class="text-[11px] font-bold uppercase tracking-wider">Xe của tôi</span>
                <span class="w-7 h-7 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center text-xs">🚗</span>
              </div>
              <div class="text-2xl font-black text-slate-900">{{ myVehicles.length }}</div>
              <div class="text-[10px] text-indigo-600 font-semibold mt-1">Phương tiện đã lưu</div>
            </div>

            <!-- 4. Vé tháng đang dùng -->
            <div class="bg-white rounded-2xl p-4 border border-slate-100 shadow-sm flex flex-col justify-between">
              <div class="flex items-center justify-between text-slate-400 mb-2">
                <span class="text-[11px] font-bold uppercase tracking-wider">Vé tháng</span>
                <span class="w-7 h-7 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center text-xs">🎫</span>
              </div>
              <div class="text-sm font-black text-emerald-600 uppercase">ACTIVE ✓</div>
              <div class="text-[10px] text-slate-400 font-medium mt-1">Hết hạn: 31/10/26</div>
            </div>

            <!-- 5. Chi phí gần đây -->
            <div class="bg-white rounded-2xl p-4 border border-slate-100 shadow-sm flex flex-col justify-between">
              <div class="flex items-center justify-between text-slate-400 mb-2">
                <span class="text-[11px] font-bold uppercase tracking-wider">Chi phí gần đây</span>
                <span class="w-7 h-7 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center text-xs">💰</span>
              </div>
              <div class="text-lg font-black text-slate-900">35.000 đ</div>
              <div class="text-[10px] text-slate-400 font-medium mt-1">Lần gửi 01/10</div>
            </div>

            <!-- 6. Lịch sử gửi xe -->
            <div class="bg-white rounded-2xl p-4 border border-slate-100 shadow-sm flex flex-col justify-between">
              <div class="flex items-center justify-between text-slate-400 mb-2">
                <span class="text-[11px] font-bold uppercase tracking-wider">Lịch sử</span>
                <span class="w-7 h-7 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center text-xs">📋</span>
              </div>
              <div class="text-2xl font-black text-slate-900">{{ parkingHistory.length }}</div>
              <div class="text-[10px] text-slate-400 font-medium mt-1">Lượt gửi hoàn thành</div>
            </div>
          </div>

          <!-- THEO DÕI PHIÊN GỬI XE HIỆN TẠI (Current Parking Tracker) -->
          <div class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-100 shadow-card">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-5 mb-6">
              <div>
                <div class="flex items-center gap-2">
                  <span class="w-3 h-3 rounded-full bg-emerald-500 animate-ping"></span>
                  <h3 class="text-lg font-black text-slate-900">Theo dõi phiên gửi xe hiện tại (Current Parking)</h3>
                </div>
                <p class="text-xs text-slate-500 mt-1">Hệ thống đang tự động đếm thời gian thực và tính toán chi phí đỗ</p>
              </div>
              <div class="flex items-center gap-2">
                <span class="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-black uppercase tracking-wider">
                  ● ĐANG ĐỖ (PARKING)
                </span>
              </div>
            </div>

            <!-- Detail Grid -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-6 p-5 rounded-2xl bg-slate-50 border border-slate-100 mb-6">
              <div>
                <div class="text-[11px] font-bold text-slate-400 uppercase">Bãi đỗ xe</div>
                <div class="text-sm font-black text-slate-800 mt-1">{{ currentParkingSession.lot_name }}</div>
                <div class="text-xs text-emerald-600 font-semibold mt-0.5">Khu A - Tầng 1</div>
              </div>
              <div>
                <div class="text-[11px] font-bold text-slate-400 uppercase">Ô đỗ xe &amp; Biển số</div>
                <div class="text-sm font-black text-blue-600 font-mono mt-1">Ô {{ currentParkingSession.slot_code }}</div>
                <div class="text-xs text-slate-700 font-mono font-bold mt-0.5">{{ currentParkingSession.plate }}</div>
              </div>
              <div>
                <div class="text-[11px] font-bold text-slate-400 uppercase">Thời gian đỗ thực tế</div>
                <div class="text-sm font-black text-slate-900 mt-1 flex items-center gap-1.5">
                  <i class="fa-regular fa-clock text-emerald-600"></i>
                  <span>{{ currentParkingSession.duration }}</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-0.5">Vào bãi lúc {{ currentParkingSession.check_in }}</div>
              </div>
              <div>
                <div class="text-[11px] font-bold text-slate-400 uppercase">Chi phí tạm tính</div>
                <div class="text-lg font-black text-emerald-600 mt-1">{{ currentParkingSession.fee.toLocaleString() }} VNĐ</div>
                <div class="text-[10px] text-slate-400 mt-0.5">Giá 25.000đ/h · Tự động tính</div>
              </div>
            </div>

            <!-- Action Buttons for Current Parking -->
            <div class="flex flex-wrap items-center justify-between gap-4">
              <div class="flex items-center gap-2 text-xs text-slate-500">
                <i class="fa-solid fa-circle-info text-blue-500"></i>
                <span>Xuất trình mã QR cho bảo vệ hoặc dùng chức năng Checkout để kết thúc lượt gửi.</span>
              </div>
              <div class="flex items-center gap-3">
                <button
                  @click="openQrModal({ booking_id: 'BK00123', slot_code: currentParkingSession.slot_code, plate: currentParkingSession.plate })"
                  class="px-4 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs transition flex items-center gap-2 cursor-pointer"
                >
                  <i class="fa-solid fa-qrcode"></i> Mã QR vào/ra
                </button>
                <button
                  @click="openCheckoutModal(currentParkingSession)"
                  class="px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-xs shadow-md shadow-emerald-500/20 transition active:scale-95 flex items-center gap-2 cursor-pointer"
                >
                  <i class="fa-solid fa-credit-card"></i> Kết thúc &amp; Thanh toán
                </button>
              </div>
            </div>
          </div>

          <!-- 2 Cột Phụ: Đặt chỗ sắp tới & Xe của tôi -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Upcoming Bookings Box -->
            <div class="bg-white rounded-3xl p-6 border border-slate-100 shadow-card">
              <div class="flex items-center justify-between mb-4">
                <h4 class="font-extrabold text-sm text-slate-900 flex items-center gap-2">
                  <i class="fa-solid fa-calendar-days text-blue-600"></i> Lịch đặt chỗ sắp tới
                </h4>
                <button @click="activeNav = 'cust-bookings'" class="text-xs text-blue-600 font-semibold hover:underline cursor-pointer">
                  Xem tất cả &rarr;
                </button>
              </div>
              <div class="space-y-3">
                <div v-for="b in upcomingBookings.slice(0, 2)" :key="b.id" class="p-4 rounded-2xl bg-slate-50 border border-slate-100 flex items-center justify-between">
                  <div>
                    <div class="text-xs font-black text-slate-900">{{ b.lot_name }} · Ô {{ b.slot_code }}</div>
                    <div class="text-[11px] text-slate-500 mt-1 flex items-center gap-2">
                      <span><i class="fa-regular fa-clock"></i> {{ b.time }} ({{ b.date }})</span>
                      <span>•</span>
                      <span class="font-mono font-bold text-slate-700">{{ b.plate }}</span>
                    </div>
                  </div>
                  <button
                    @click="openQrModal(b)"
                    class="px-3 py-1.5 rounded-xl bg-white border border-slate-200 text-xs font-bold text-slate-700 hover:bg-slate-100 transition flex items-center gap-1.5 cursor-pointer"
                  >
                    <i class="fa-solid fa-qrcode text-emerald-600"></i> QR
                  </button>
                </div>
              </div>
            </div>

            <!-- My Vehicles Box -->
            <div class="bg-white rounded-3xl p-6 border border-slate-100 shadow-card">
              <div class="flex items-center justify-between mb-4">
                <h4 class="font-extrabold text-sm text-slate-900 flex items-center gap-2">
                  <i class="fa-solid fa-car text-indigo-600"></i> Phương tiện của tôi
                </h4>
                <button @click="activeNav = 'cust-vehicles'" class="text-xs text-indigo-600 font-semibold hover:underline cursor-pointer">
                  Quản lý xe &rarr;
                </button>
              </div>
              <div class="space-y-3">
                <div v-for="v in myVehicles.slice(0, 2)" :key="v.id" class="p-4 rounded-2xl bg-slate-50 border border-slate-100 flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-white border border-slate-200 flex items-center justify-center text-slate-800 text-lg">
                      <i :class="v.type === 'Motorcycle' ? 'fa-solid fa-motorcycle text-amber-500' : 'fa-solid fa-car text-blue-600'"></i>
                    </div>
                    <div>
                      <div class="text-xs font-black text-slate-900">{{ v.brand }} {{ v.model }}</div>
                      <div class="text-[11px] text-slate-500 font-mono mt-0.5">Biển số: <strong class="text-slate-800">{{ v.plate }}</strong></div>
                    </div>
                  </div>
                  <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-slate-200 text-slate-700 uppercase">{{ v.type }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>


        <!-- ============================================================== -->
        <!-- CUSTOMER SCREEN 2: FIND PARKING (Tìm bãi & Xem sơ đồ)          -->
        <!-- ============================================================== -->
        <div v-if="activeNav === 'cust-find-parking'" class="space-y-6 max-w-6xl mx-auto">
          <!-- Filter & Search Bar -->
          <div class="bg-white rounded-3xl p-6 border border-slate-100 shadow-card flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h3 class="text-lg font-black text-slate-900">Tìm kiếm bãi đỗ xe trong hệ thống</h3>
              <p class="text-xs text-slate-500 mt-0.5">Chọn bãi đỗ phù hợp nhất với vị trí và phương tiện của bạn</p>
            </div>
            <div class="flex items-center gap-3">
              <div class="relative">
                <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
                <input
                  v-model="parkingSearchQuery"
                  type="text"
                  placeholder="Tìm theo tên bãi, đường..."
                  class="pl-9 pr-4 py-2.5 rounded-2xl bg-slate-50 border border-slate-200 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-slate-900 w-64"
                />
              </div>
            </div>
          </div>

          <!-- Danh sách Bãi đỗ xe (Cards) -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div
              v-for="lot in filteredParkingLots"
              :key="lot.id"
              class="bg-white rounded-3xl p-6 border border-slate-100 shadow-card flex flex-col justify-between hover:border-emerald-300 transition duration-200 group"
              :class="selectedParkingLot?.id === lot.id ? 'ring-2 ring-emerald-500' : ''"
            >
              <div>
                <!-- Header Card -->
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div>
                    <h4 class="font-extrabold text-base text-slate-900 group-hover:text-emerald-600 transition">{{ lot.name }}</h4>
                    <p class="text-xs text-slate-400 flex items-center gap-1.5 mt-1">
                      <i class="fa-solid fa-location-dot text-rose-500 text-[11px]"></i> {{ lot.address }}
                    </p>
                  </div>
                  <span
                    class="px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-wider shrink-0"
                    :class="lot.status === 'Open' ? 'bg-emerald-100 text-emerald-800' : lot.status === 'Crowded' ? 'bg-amber-100 text-amber-800' : 'bg-rose-100 text-rose-800'"
                  >
                    {{ lot.status === 'Open' ? 'Mở cửa' : lot.status === 'Crowded' ? 'Đông đúc' : 'Hết chỗ' }}
                  </span>
                </div>

                <!-- Stats details -->
                <div class="grid grid-cols-2 gap-3 py-3 border-y border-slate-100 my-4 text-xs">
                  <div>
                    <span class="text-slate-400 text-[11px]">Khoảng cách:</span>
                    <div class="font-black text-slate-800 mt-0.5">📍 {{ lot.distance }}</div>
                  </div>
                  <div>
                    <span class="text-slate-400 text-[11px]">Chỗ trống:</span>
                    <div class="font-black text-emerald-600 mt-0.5">{{ lot.available_spaces }} / {{ lot.total_spaces }}</div>
                  </div>
                  <div>
                    <span class="text-slate-400 text-[11px]">Giá gửi xe:</span>
                    <div class="font-black text-slate-900 mt-0.5">{{ lot.rate.toLocaleString() }} đ/giờ</div>
                  </div>
                  <div>
                    <span class="text-slate-400 text-[11px]">Giờ mở cửa:</span>
                    <div class="font-semibold text-slate-700 mt-0.5">⏰ {{ lot.hours }}</div>
                  </div>
                </div>
              </div>

              <!-- Buttons -->
              <div class="grid grid-cols-2 gap-2 mt-2">
                <button
                  @click="selectLotToViewMap(lot)"
                  class="py-2.5 rounded-xl border border-slate-200 text-slate-700 hover:bg-slate-100 font-bold text-xs transition flex items-center justify-center gap-1.5 cursor-pointer"
                >
                  <i class="fa-solid fa-map"></i> Xem sơ đồ
                </button>
                <button
                  @click="startBookingAtLot(lot)"
                  class="py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-xs shadow-md shadow-emerald-500/20 transition active:scale-95 flex items-center justify-center gap-1.5 cursor-pointer"
                >
                  <i class="fa-solid fa-calendar-plus"></i> Đặt chỗ ngay
                </button>
              </div>
            </div>
          </div>

          <!-- Sơ đồ chỗ đỗ tương tác của bãi đang chọn -->
          <div v-if="selectedParkingLot" class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-100 shadow-card space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-5">
              <div>
                <h3 class="text-lg font-black text-slate-900 flex items-center gap-2">
                  <i class="fa-solid fa-map-location-dot text-emerald-500"></i>
                  Sơ đồ bãi xe: {{ selectedParkingLot.name }}
                </h3>
                <p class="text-xs text-slate-500 mt-1">Bấm trực tiếp vào các ô màu xanh (trống) để chọn đặt chỗ đỗ xe</p>
              </div>

              <!-- Legends -->
              <div class="flex flex-wrap items-center gap-3 text-xs font-semibold">
                <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-md bg-[#10b981]"></span> Trống (Available)</span>
                <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-md bg-[#ef4444]"></span> Đang đỗ (Occupied)</span>
                <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-md bg-[#f59e0b]"></span> Đã đặt trước (Reserved)</span>
              </div>
            </div>

            <!-- Interactive Slot Grid -->
            <div class="grid grid-cols-4 sm:grid-cols-6 lg:grid-cols-10 gap-3">
              <div
                v-for="slot in activeLotSlots"
                :key="slot.code"
                @click="onCustomerSelectSlot(slot)"
                class="h-20 rounded-2xl flex flex-col items-center justify-center p-2 transition cursor-pointer relative"
                :class="{
                  'bg-[#10b981] hover:brightness-105 text-white shadow-sm': slot.status === 'available' && chosenSlot?.code !== slot.code,
                  'bg-[#ef4444] text-white opacity-85 cursor-not-allowed': slot.status === 'occupied',
                  'bg-[#f59e0b] text-white opacity-85 cursor-not-allowed': slot.status === 'reserved',
                  'bg-slate-900 text-white ring-4 ring-emerald-400 scale-105 font-black': chosenSlot?.code === slot.code
                }"
              >
                <i :class="slot.status === 'occupied' ? 'fa-solid fa-car text-base mb-1' : 'fa-solid fa-circle-check text-base mb-1'"></i>
                <span class="text-xs font-bold">{{ slot.code }}</span>
                <span v-if="chosenSlot?.code === slot.code" class="absolute -top-2 -right-2 w-5 h-5 rounded-full bg-emerald-400 text-slate-900 text-[10px] flex items-center justify-center font-black">✓</span>
              </div>
            </div>

            <!-- Selected Slot Detail Bar -->
            <div v-if="chosenSlot" class="p-5 rounded-2xl bg-emerald-50 border border-emerald-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 rounded-2xl bg-emerald-500 text-white font-black text-lg flex items-center justify-center shadow-md">
                  {{ chosenSlot.code }}
                </div>
                <div>
                  <div class="text-sm font-black text-emerald-950">Bạn đã chọn ô: {{ chosenSlot.code }}</div>
                  <div class="text-xs text-emerald-700 mt-0.5">Bãi đỗ: {{ selectedParkingLot.name }} · Đơn giá: {{ selectedParkingLot.rate.toLocaleString() }} đ/h</div>
                </div>
              </div>
              <button
                @click="proceedToBookingWithSlot(selectedParkingLot, chosenSlot)"
                class="px-6 py-3 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs shadow-lg transition active:scale-95 flex items-center gap-2 cursor-pointer"
              >
                <span>Xác nhận &amp; Tiến hành đặt chỗ</span> &rarr;
              </button>
            </div>
          </div>
        </div>


        <!-- ============================================================== -->
        <!-- CUSTOMER SCREEN 3: BOOKINGS (Đặt chỗ & Quản lý booking)        -->
        <!-- ============================================================== -->
        <div v-if="activeNav === 'cust-bookings'" class="space-y-8 max-w-6xl mx-auto">
          <!-- FORM ĐẶT CHỖ GỬI XE (CORE FEATURE) -->
          <div class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-100 shadow-card space-y-6">
            <div class="border-b border-slate-100 pb-4">
              <h3 class="text-xl font-black text-slate-900 flex items-center gap-2">
                <i class="fa-solid fa-calendar-plus text-emerald-500"></i>
                Đặt chỗ gửi xe mới (Book a Parking Slot)
              </h3>
              <p class="text-xs text-slate-500 mt-1">Chọn thông tin để hệ thống giữ chỗ và cấp mã QR check-in tự động</p>
            </div>

            <form @submit.prevent="confirmCreateBooking" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              <!-- 1. Chọn bãi -->
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1.5">1. Chọn bãi đỗ xe *</label>
                <select
                  v-model="bookingForm.lot_id"
                  @change="onBookingLotChange"
                  class="w-full px-4 py-3 rounded-2xl border border-slate-200 bg-slate-50 text-xs font-semibold text-slate-800 focus:outline-none focus:border-slate-900"
                  required
                >
                  <option v-for="lot in parkingLots" :key="lot.id" :value="lot.id">
                    {{ lot.name }} ({{ lot.available_spaces }} chỗ trống)
                  </option>
                </select>
              </div>

              <!-- 2. Chọn ngày & giờ -->
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1.5">2. Ngày gửi *</label>
                <input
                  v-model="bookingForm.date"
                  type="date"
                  class="w-full px-4 py-3 rounded-2xl border border-slate-200 bg-slate-50 text-xs font-semibold text-slate-800 focus:outline-none focus:border-slate-900"
                  required
                />
              </div>

              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1.5">3. Giờ vào dự kiến &amp; Thời lượng *</label>
                <div class="grid grid-cols-2 gap-2">
                  <input
                    v-model="bookingForm.time"
                    type="time"
                    class="w-full px-3 py-3 rounded-2xl border border-slate-200 bg-slate-50 text-xs font-semibold text-slate-800 focus:outline-none focus:border-slate-900"
                    required
                  />
                  <select
                    v-model="bookingForm.duration_hours"
                    class="w-full px-2 py-3 rounded-2xl border border-slate-200 bg-slate-50 text-xs font-semibold text-slate-800 focus:outline-none focus:border-slate-900"
                  >
                    <option :value="1">1 giờ</option>
                    <option :value="2">2 giờ</option>
                    <option :value="3">3 giờ</option>
                    <option :value="4">4 giờ</option>
                    <option :value="8">Cả ngày (8h)</option>
                  </select>
                </div>
              </div>

              <!-- 4. Chọn phương tiện -->
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1.5">4. Chọn phương tiện *</label>
                <select
                  v-model="bookingForm.vehicle_id"
                  class="w-full px-4 py-3 rounded-2xl border border-slate-200 bg-slate-50 text-xs font-semibold text-slate-800 focus:outline-none focus:border-slate-900"
                  required
                >
                  <option v-for="v in myVehicles" :key="v.id" :value="v.id">
                    {{ v.brand }} {{ v.model }} ({{ v.plate }})
                  </option>
                </select>
              </div>

              <!-- 5. Chọn slot đỗ -->
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1.5">5. Chọn ô đỗ (Slot) *</label>
                <select
                  v-model="bookingForm.slot_code"
                  class="w-full px-4 py-3 rounded-2xl border border-slate-200 bg-slate-50 text-xs font-mono font-bold text-slate-800 focus:outline-none focus:border-slate-900"
                  required
                >
                  <option v-for="slot in availableBookingSlots" :key="slot.code" :value="slot.code">
                    Ô {{ slot.code }} (Khả dụng)
                  </option>
                </select>
              </div>

              <!-- 6. Giá dự kiến & Xác nhận -->
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1.5">6. Giá dự kiến</label>
                <div class="px-4 py-3 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-black flex items-center justify-between">
                  <span>{{ calculatedBookingFee.toLocaleString() }} VNĐ</span>
                  <span class="text-[10px] text-emerald-600 font-semibold font-normal">{{ bookingForm.duration_hours }}h x 25k</span>
                </div>
              </div>

              <!-- Submit -->
              <div class="md:col-span-2 lg:col-span-3 pt-2 flex justify-end">
                <button
                  type="submit"
                  class="px-8 py-3.5 rounded-2xl bg-[#0b1020] hover:bg-slate-800 text-white font-bold text-sm shadow-xl shadow-slate-900/10 transition active:scale-95 flex items-center gap-2 cursor-pointer"
                >
                  <i class="fa-solid fa-check"></i> Xác nhận đặt chỗ (Confirm Booking)
                </button>
              </div>
            </form>
          </div>

          <!-- QUẢN LÝ BOOKING CỦA TÔI (My Bookings Tabs) -->
          <div class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-100 shadow-card space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-5">
              <div>
                <h3 class="text-lg font-black text-slate-900">Danh sách đặt chỗ của tôi (My Bookings)</h3>
                <p class="text-xs text-slate-500 mt-0.5">Theo dõi các lịch đặt chỗ sắp tới, đang đỗ và đã hoàn thành</p>
              </div>

              <!-- 4 Tabs -->
              <div class="flex p-1 bg-slate-100 rounded-2xl text-xs font-bold">
                <button
                  @click="activeBookingTab = 'upcoming'"
                  class="px-4 py-2 rounded-xl transition cursor-pointer"
                  :class="activeBookingTab === 'upcoming' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'"
                >
                  Upcoming ({{ myBookings.filter(b => b.status === 'upcoming').length }})
                </button>
                <button
                  @click="activeBookingTab = 'active'"
                  class="px-4 py-2 rounded-xl transition cursor-pointer"
                  :class="activeBookingTab === 'active' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'"
                >
                  Active ({{ myBookings.filter(b => b.status === 'active').length }})
                </button>
                <button
                  @click="activeBookingTab = 'completed'"
                  class="px-4 py-2 rounded-xl transition cursor-pointer"
                  :class="activeBookingTab === 'completed' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'"
                >
                  Completed ({{ myBookings.filter(b => b.status === 'completed').length }})
                </button>
                <button
                  @click="activeBookingTab = 'cancelled'"
                  class="px-4 py-2 rounded-xl transition cursor-pointer"
                  :class="activeBookingTab === 'cancelled' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'"
                >
                  Cancelled ({{ myBookings.filter(b => b.status === 'cancelled').length }})
                </button>
              </div>
            </div>

            <!-- Booking Cards Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div
                v-for="b in filteredBookings"
                :key="b.id"
                class="p-5 rounded-2xl border border-slate-100 bg-slate-50 flex flex-col justify-between space-y-4 hover:border-slate-300 transition"
              >
                <div class="flex items-start justify-between">
                  <div>
                    <span class="px-2.5 py-0.5 rounded-full text-[10px] font-black font-mono bg-slate-200 text-slate-800">
                      {{ b.code }}
                    </span>
                    <h4 class="font-extrabold text-sm text-slate-900 mt-2">{{ b.lot_name }}</h4>
                    <div class="text-xs text-blue-600 font-bold font-mono mt-0.5">Vị trí ô: Ô {{ b.slot_code }}</div>
                  </div>
                  <span
                    class="px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider"
                    :class="{
                      'bg-blue-100 text-blue-800': b.status === 'upcoming',
                      'bg-emerald-100 text-emerald-800': b.status === 'active',
                      'bg-slate-200 text-slate-700': b.status === 'completed',
                      'bg-rose-100 text-rose-800': b.status === 'cancelled'
                    }"
                  >
                    {{ b.status }}
                  </span>
                </div>

                <div class="grid grid-cols-2 gap-2 text-xs py-2 border-y border-slate-200/60">
                  <div>
                    <span class="text-slate-400 text-[10px]">Thời gian:</span>
                    <div class="font-semibold text-slate-800 mt-0.5">{{ b.time }} ({{ b.date }})</div>
                  </div>
                  <div>
                    <span class="text-slate-400 text-[10px]">Phương tiện:</span>
                    <div class="font-mono font-bold text-slate-800 mt-0.5">{{ b.plate }}</div>
                  </div>
                </div>

                <!-- Actions -->
                <div class="flex items-center justify-between pt-1">
                  <div class="text-xs font-black text-emerald-600">
                    {{ b.fee.toLocaleString() }} VNĐ
                  </div>
                  <div class="flex items-center gap-2">
                    <button
                      v-if="b.status === 'upcoming' || b.status === 'active'"
                      @click="openQrModal(b)"
                      class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs transition flex items-center gap-1.5 cursor-pointer"
                    >
                      <i class="fa-solid fa-qrcode text-emerald-400"></i> My QR
                    </button>
                    <button
                      v-if="b.status === 'upcoming'"
                      @click="cancelBooking(b)"
                      class="px-3 py-1.5 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-600 font-bold text-xs transition cursor-pointer"
                    >
                      Hủy đặt
                    </button>
                    <button
                      v-if="b.status === 'completed'"
                      @click="viewReceiptForBooking(b)"
                      class="px-3 py-1.5 rounded-xl bg-slate-200 hover:bg-slate-300 text-slate-800 font-bold text-xs transition cursor-pointer"
                    >
                      Xem hóa đơn
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="filteredBookings.length === 0" class="text-center py-12 text-slate-400 text-xs">
              <i class="fa-solid fa-calendar-xmark text-3xl mb-2 block"></i>
              Không có lượt đặt chỗ nào trong mục này.
            </div>
          </div>
        </div>


        <!-- ============================================================== -->
        <!-- CUSTOMER SCREEN 4: MY VEHICLES (Quản lý phương tiện)           -->
        <!-- ============================================================== -->
        <div v-if="activeNav === 'cust-vehicles'" class="space-y-6 max-w-5xl mx-auto">
          <div class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-100 shadow-card flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 class="text-xl font-black text-slate-900">Quản lý phương tiện của tôi (My Vehicles)</h3>
              <p class="text-xs text-slate-500 mt-1">Lưu thông tin biển số xe để đặt chỗ và tự động nhận diện tại cổng vào</p>
            </div>
            <button
              @click="openAddVehicleModal()"
              class="px-5 py-3 rounded-2xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-xs shadow-lg shadow-emerald-500/25 transition active:scale-95 flex items-center gap-2 cursor-pointer shrink-0"
            >
              <i class="fa-solid fa-plus"></i> Thêm phương tiện (+ Add Vehicle)
            </button>
          </div>

          <!-- Vehicle Cards Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div
              v-for="v in myVehicles"
              :key="v.id"
              class="bg-white rounded-3xl p-6 border border-slate-100 shadow-card flex flex-col justify-between space-y-5"
            >
              <div class="flex items-start justify-between">
                <div class="flex items-center gap-3.5">
                  <div class="w-12 h-12 rounded-2xl bg-slate-100 flex items-center justify-center text-xl text-slate-800">
                    <i :class="v.type === 'Motorcycle' ? 'fa-solid fa-motorcycle text-amber-500' : 'fa-solid fa-car text-blue-600'"></i>
                  </div>
                  <div>
                    <h4 class="font-extrabold text-base text-slate-900">{{ v.brand }} {{ v.model }}</h4>
                    <span class="text-xs text-slate-400 font-medium">Màu sắc: {{ v.color }}</span>
                  </div>
                </div>
                <span class="px-2.5 py-1 rounded-full text-[10px] font-bold uppercase bg-slate-100 text-slate-700">
                  {{ v.type }}
                </span>
              </div>

              <!-- License Plate Badge -->
              <div class="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center justify-between">
                <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Biển số xe:</span>
                <span class="font-mono text-base font-black px-3 py-1 bg-white border border-slate-300 rounded-xl text-slate-900 shadow-xs">
                  {{ v.plate }}
                </span>
              </div>

              <!-- Actions -->
              <div class="flex items-center justify-end gap-2 pt-1 border-t border-slate-100">
                <button
                  @click="editVehicle(v)"
                  class="px-3.5 py-2 rounded-xl text-xs font-bold text-slate-600 hover:bg-slate-100 transition cursor-pointer"
                >
                  <i class="fa-solid fa-pen-to-square"></i> Chỉnh sửa
                </button>
                <button
                  @click="deleteVehicle(v)"
                  class="px-3.5 py-2 rounded-xl text-xs font-bold text-rose-600 hover:bg-rose-50 transition cursor-pointer"
                >
                  <i class="fa-solid fa-trash"></i> Xóa
                </button>
              </div>
            </div>
          </div>
        </div>


        <!-- ============================================================== -->
        <!-- CUSTOMER SCREEN 5: MONTHLY PASS (Vé tháng)                    -->
        <!-- ============================================================== -->
        <div v-if="activeNav === 'cust-monthly-pass'" class="space-y-8 max-w-5xl mx-auto">
          <div class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-100 shadow-card flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 class="text-xl font-black text-slate-900">Vé tháng đỗ xe (Monthly Pass)</h3>
              <p class="text-xs text-slate-500 mt-1">Đăng ký gói vé tháng để tiết kiệm chi phí và luôn có chỗ đỗ ưu tiên</p>
            </div>
            <button
              @click="openBuyPassModal()"
              class="px-5 py-3 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-bold text-xs shadow-lg shadow-emerald-500/25 transition active:scale-95 flex items-center gap-2 cursor-pointer shrink-0"
            >
              <i class="fa-solid fa-ticket"></i> Mua vé tháng mới (Buy Monthly Pass)
            </button>
          </div>

          <!-- VIP Card Display (My Monthly Pass) -->
          <div class="max-w-xl mx-auto">
            <div class="bg-gradient-to-tr from-[#0b1020] via-slate-900 to-indigo-900 rounded-[32px] p-8 text-white shadow-2xl border border-slate-700/60 relative overflow-hidden">
              <!-- Hologram subtle chip -->
              <div class="flex items-center justify-between mb-8">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-2xl bg-emerald-500 flex items-center justify-center text-white font-black text-lg">
                    P
                  </div>
                  <div>
                    <div class="text-[10px] tracking-widest uppercase text-slate-400 font-bold">Smart Parking VIP</div>
                    <div class="text-sm font-extrabold text-white">MONTHLY PARKING PASS</div>
                  </div>
                </div>
                <span class="px-3 py-1 rounded-full text-xs font-black bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">
                  ACTIVE ✓
                </span>
              </div>

              <!-- Card Details -->
              <div class="space-y-4 my-6">
                <div>
                  <div class="text-[10px] text-slate-400 uppercase font-bold">Bãi áp dụng (Parking Lot)</div>
                  <div class="text-sm font-black text-white mt-0.5">{{ myMonthlyPass.lot_name }}</div>
                </div>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <div class="text-[10px] text-slate-400 uppercase font-bold">Phương tiện</div>
                    <div class="text-sm font-mono font-bold text-white mt-0.5">{{ myMonthlyPass.plate }} ({{ myMonthlyPass.vehicle_type }})</div>
                  </div>
                  <div>
                    <div class="text-[10px] text-slate-400 uppercase font-bold">Giá gói</div>
                    <div class="text-sm font-black text-emerald-400 mt-0.5">{{ myMonthlyPass.price.toLocaleString() }} đ/tháng</div>
                  </div>
                </div>
              </div>

              <!-- Validity dates -->
              <div class="pt-4 border-t border-white/10 flex items-center justify-between text-xs text-slate-300">
                <div>Hiệu lực từ: <strong class="text-white">{{ myMonthlyPass.start_date }}</strong></div>
                <div>Hết hạn: <strong class="text-emerald-400">{{ myMonthlyPass.end_date }}</strong></div>
              </div>
            </div>
          </div>
        </div>


        <!-- ============================================================== -->
        <!-- CUSTOMER SCREEN 6: PARKING HISTORY (Lịch sử gửi xe)            -->
        <!-- ============================================================== -->
        <div v-if="activeNav === 'cust-history'" class="space-y-6 max-w-6xl mx-auto">
          <div class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-100 shadow-card flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 class="text-xl font-black text-slate-900">Lịch sử gửi xe (Parking History)</h3>
              <p class="text-xs text-slate-500 mt-1">Danh sách toàn bộ các lượt gửi xe và hóa đơn chi tiết của bạn</p>
            </div>
            <div class="text-xs font-semibold px-4 py-2 rounded-2xl bg-slate-100 text-slate-700">
              Tổng số: {{ parkingHistory.length }} lượt gửi
            </div>
          </div>

          <div class="bg-white rounded-3xl border border-slate-100 shadow-card overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs border-collapse">
                <thead>
                  <tr class="text-slate-400 font-bold border-b border-slate-100 bg-slate-50/50">
                    <th class="py-4 px-6">Mã lượt</th>
                    <th class="py-4 px-6">Ngày</th>
                    <th class="py-4 px-6">Bãi đỗ xe</th>
                    <th class="py-4 px-6">Vị trí (Slot)</th>
                    <th class="py-4 px-6">Thời lượng</th>
                    <th class="py-4 px-6">Chi phí</th>
                    <th class="py-4 px-6">Trạng thái</th>
                    <th class="py-4 px-6 text-right">Hành động</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 text-slate-800 font-medium">
                  <tr v-for="h in parkingHistory" :key="h.id" class="hover:bg-slate-50 transition">
                    <td class="py-4 px-6 font-mono font-bold text-slate-900">{{ h.id }}</td>
                    <td class="py-4 px-6">{{ h.date }}</td>
                    <td class="py-4 px-6 font-bold">{{ h.lot_name }}</td>
                    <td class="py-4 px-6 font-mono font-bold text-blue-600">{{ h.slot_code }}</td>
                    <td class="py-4 px-6">{{ h.duration }}</td>
                    <td class="py-4 px-6 font-black text-emerald-600">{{ h.fee.toLocaleString() }} đ</td>
                    <td class="py-4 px-6">
                      <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-700">
                        {{ h.status }}
                      </span>
                    </td>
                    <td class="py-4 px-6 text-right">
                      <button
                        @click="openReceiptModal(h)"
                        class="px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-xs transition cursor-pointer"
                      >
                        <i class="fa-solid fa-receipt mr-1"></i> View Receipt
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>


        <!-- ============================================================== -->
        <!-- CUSTOMER SCREEN 7: PAYMENTS (Thanh toán & Hóa đơn)             -->
        <!-- ============================================================== -->
        <div v-if="activeNav === 'cust-payments'" class="space-y-8 max-w-5xl mx-auto">
          <!-- Thanh toán phiên đỗ hiện tại -->
          <div class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-100 shadow-card space-y-6">
            <div>
              <h3 class="text-xl font-black text-slate-900">Check-out &amp; Thanh toán lượt gửi xe</h3>
              <p class="text-xs text-slate-500 mt-1">Tính toán hóa đơn minh bạch theo thời gian thực tế</p>
            </div>

            <!-- Receipt Breakdown Box -->
            <div class="p-6 rounded-2xl bg-slate-50 border border-slate-200/80 max-w-lg space-y-3 font-mono text-xs">
              <div class="flex justify-between text-slate-600">
                <span>Check-in:</span>
                <span class="font-bold text-slate-900">18:05</span>
              </div>
              <div class="flex justify-between text-slate-600">
                <span>Check-out (Dự kiến):</span>
                <span class="font-bold text-slate-900">21:12</span>
              </div>
              <div class="flex justify-between text-slate-600">
                <span>Thời gian đỗ:</span>
                <span class="font-bold text-slate-900">3h 07m</span>
              </div>
              <div class="border-t border-slate-200 pt-2 flex justify-between text-slate-600">
                <span>Phí cơ bản (Base fee):</span>
                <span>30.000 VNĐ</span>
              </div>
              <div class="flex justify-between text-slate-600">
                <span>Phụ phí giờ cao điểm:</span>
                <span>5.000 VNĐ</span>
              </div>
              <div class="border-t-2 border-slate-800 pt-3 flex justify-between font-black text-sm text-slate-900">
                <span>TỔNG CỘNG (TOTAL):</span>
                <span class="text-emerald-600 text-base">35.000 VNĐ</span>
              </div>
            </div>

            <!-- Payment Simulation Radio -->
            <div class="space-y-3 max-w-lg">
              <label class="block text-xs font-bold text-slate-700">Chọn phương thức thanh toán (Payment Method):</label>
              <div class="space-y-2">
                <label class="flex items-center gap-3 p-3.5 rounded-2xl border border-slate-200 bg-white cursor-pointer hover:border-slate-400 transition">
                  <input type="radio" v-model="selectedPaymentMethod" value="cash" class="text-slate-900 focus:ring-0" />
                  <span class="text-xs font-bold text-slate-800"><i class="fa-solid fa-money-bill-wave text-emerald-600 mr-1.5"></i> Tiền mặt tại quầy trực bãi (Cash)</span>
                </label>
                <label class="flex items-center gap-3 p-3.5 rounded-2xl border border-slate-200 bg-white cursor-pointer hover:border-slate-400 transition">
                  <input type="radio" v-model="selectedPaymentMethod" value="online" class="text-slate-900 focus:ring-0" />
                  <span class="text-xs font-bold text-slate-800"><i class="fa-solid fa-qrcode text-blue-600 mr-1.5"></i> Thanh toán mô phỏng trực tuyến (Simulated Online Payment)</span>
                </label>
              </div>
              <p class="text-[11px] text-amber-600 font-semibold bg-amber-50 p-2.5 rounded-xl border border-amber-200 flex items-center gap-2">
                <i class="fa-solid fa-triangle-exclamation"></i>
                Lưu ý: Đây là tính năng mô phỏng thanh toán (Payment Simulation), không trừ tiền thật.
              </p>
            </div>

            <div>
              <button
                @click="executePayment()"
                class="px-8 py-3.5 rounded-2xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-sm shadow-xl shadow-emerald-500/25 transition active:scale-95 flex items-center gap-2 cursor-pointer"
              >
                <i class="fa-solid fa-check"></i> Xác nhận thanh toán (Confirm Payment)
              </button>
            </div>
          </div>
        </div>


        <!-- ============================================================== -->
        <!-- CUSTOMER SCREEN 8: PROFILE (Thông tin tài khoản)              -->
        <!-- ============================================================== -->
        <div v-if="activeNav === 'cust-profile'" class="space-y-6 max-w-4xl mx-auto">
          <div class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-100 shadow-card space-y-6">
            <div class="border-b border-slate-100 pb-4">
              <h3 class="text-xl font-black text-slate-900">Thông tin cá nhân (My Profile)</h3>
              <p class="text-xs text-slate-500 mt-1">Cập nhật họ tên, số điện thoại và thông tin liên hệ của bạn</p>
            </div>

            <!-- Profile Form -->
            <form @submit.prevent="saveCustomerProfile" class="space-y-4 max-w-lg">
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1.5">Họ và tên (Full Name)</label>
                <input
                  v-model="profileForm.full_name"
                  type="text"
                  required
                  class="w-full px-4 py-3 rounded-2xl border border-slate-200 bg-slate-50 text-xs font-semibold text-slate-800 focus:outline-none focus:border-slate-900 focus:bg-white"
                />
              </div>

              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1.5">Email</label>
                <input
                  v-model="profileForm.email"
                  type="email"
                  required
                  class="w-full px-4 py-3 rounded-2xl border border-slate-200 bg-slate-50 text-xs font-semibold text-slate-800 focus:outline-none focus:border-slate-900 focus:bg-white"
                />
              </div>

              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1.5">Số điện thoại (Phone)</label>
                <input
                  v-model="profileForm.phone"
                  type="tel"
                  class="w-full px-4 py-3 rounded-2xl border border-slate-200 bg-slate-50 text-xs font-semibold text-slate-800 focus:outline-none focus:border-slate-900 focus:bg-white"
                />
              </div>

              <!-- Role (Readonly) -->
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1.5">Vai trò hệ thống (Role) - Khóa</label>
                <div class="px-4 py-3 rounded-2xl border border-slate-200 bg-slate-100 text-xs font-bold text-slate-500 flex items-center justify-between">
                  <span>Khách hàng (CUSTOMER)</span>
                  <i class="fa-solid fa-lock text-slate-400"></i>
                </div>
                <p class="text-[10px] text-slate-400 mt-1">Vai trò được kiểm soát và phân quyền tự động bởi hệ thống.</p>
              </div>

              <div v-if="profileSaveMessage" class="p-3 rounded-xl bg-emerald-50 text-emerald-700 text-xs font-semibold border border-emerald-200">
                {{ profileSaveMessage }}
              </div>

              <button
                type="submit"
                class="px-6 py-3 rounded-2xl bg-[#0b1020] hover:bg-slate-800 text-white font-bold text-xs shadow-md transition active:scale-95 cursor-pointer"
              >
                Lưu thay đổi (Save Changes)
              </button>
            </form>
          </div>
        </div>
'''

content = content.replace('</main>', customer_screens_html + '\n      </main>')

# ==============================================================================
# 3. ADD MODALS (QR, Add Vehicle, Buy Pass, Receipt, Help, Booking Confirmed)
# ==============================================================================
modals_html = '''
  <!-- ============================================================== -->
  <!-- MODAL: MY QR / PARKING QR (Modal hiển thị mã QR đặt chỗ)      -->
  <!-- ============================================================== -->
  <div v-if="showQrModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
    <div class="bg-white rounded-3xl max-w-sm w-full p-6 sm:p-8 text-center shadow-2xl border border-slate-100 space-y-5">
      <div class="flex items-center justify-between border-b border-slate-100 pb-3">
        <h3 class="font-extrabold text-base text-slate-900">Mã QR đỗ xe (Parking QR)</h3>
        <button @click="showQrModal = false" class="text-slate-400 hover:text-slate-600 cursor-pointer">
          <i class="fa-solid fa-xmark text-lg"></i>
        </button>
      </div>

      <!-- QR Graphic Render -->
      <div class="p-6 bg-slate-50 rounded-2xl border border-slate-200 inline-block shadow-inner">
        <svg class="w-48 h-48 mx-auto" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect width="100" height="100" fill="white" rx="8"/>
          <!-- Top Left Marker -->
          <rect x="10" y="10" width="24" height="24" rx="4" stroke="#0f172a" stroke-width="4"/>
          <rect x="16" y="16" width="12" height="12" rx="2" fill="#10b981"/>
          <!-- Top Right Marker -->
          <rect x="66" y="10" width="24" height="24" rx="4" stroke="#0f172a" stroke-width="4"/>
          <rect x="72" y="16" width="12" height="12" rx="2" fill="#10b981"/>
          <!-- Bottom Left Marker -->
          <rect x="10" y="66" width="24" height="24" rx="4" stroke="#0f172a" stroke-width="4"/>
          <rect x="16" y="72" width="12" height="12" rx="2" fill="#10b981"/>
          <!-- QR Data Dots Pattern -->
          <rect x="42" y="14" width="6" height="6" fill="#0f172a"/>
          <rect x="52" y="14" width="6" height="12" fill="#0f172a"/>
          <rect x="42" y="26" width="16" height="6" fill="#0f172a"/>
          <rect x="14" y="42" width="12" height="6" fill="#0f172a"/>
          <rect x="32" y="42" width="36" height="6" fill="#0f172a"/>
          <rect x="74" y="42" width="12" height="6" fill="#0f172a"/>
          <rect x="14" y="52" width="6" height="6" fill="#0f172a"/>
          <rect x="26" y="52" width="12" height="6" fill="#0f172a"/>
          <rect x="44" y="52" width="18" height="6" fill="#10b981"/>
          <rect x="68" y="52" width="18" height="6" fill="#0f172a"/>
          <rect x="42" y="66" width="6" height="18" fill="#0f172a"/>
          <rect x="54" y="66" width="12" height="6" fill="#0f172a"/>
          <rect x="72" y="66" width="14" height="14" fill="#0f172a"/>
          <rect x="54" y="78" width="12" height="12" fill="#0f172a"/>
        </svg>
      </div>

      <div class="space-y-1">
        <div class="text-xs font-mono font-black text-slate-800">Booking: {{ qrData.booking_id || 'BK00123' }}</div>
        <div class="text-[11px] text-slate-500">Vị trí: <strong>Ô {{ qrData.slot_code || 'A-023' }}</strong> · Biển số: <strong>{{ qrData.plate || '59A1-123.45' }}</strong></div>
        <p class="text-[10px] text-slate-400 mt-2">Xuất trình mã này cho nhân viên bảo vệ quét tại cổng bãi đỗ xe</p>
      </div>

      <button
        @click="showQrModal = false"
        class="w-full py-3 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs transition cursor-pointer"
      >
        Đóng
      </button>
    </div>
  </div>


  <!-- ============================================================== -->
  <!-- MODAL: ADD VEHICLE (Thêm phương tiện mới)                     -->
  <!-- ============================================================== -->
  <div v-if="showAddVehicleModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
    <div class="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-2xl border border-slate-100 space-y-5">
      <div class="flex items-center justify-between border-b border-slate-100 pb-3">
        <h3 class="font-extrabold text-base text-slate-900">Thêm phương tiện mới (Add Vehicle)</h3>
        <button @click="showAddVehicleModal = false" class="text-slate-400 hover:text-slate-600 cursor-pointer">
          <i class="fa-solid fa-xmark text-lg"></i>
        </button>
      </div>

      <form @submit.prevent="saveNewVehicle" class="space-y-3.5">
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Biển số xe * (License Plate)</label>
          <input
            v-model="newVehicleForm.plate"
            type="text"
            placeholder="Ví dụ: 59A1-123.45"
            required
            class="w-full px-4 py-2.5 rounded-2xl border border-slate-200 bg-slate-50 text-xs font-mono font-bold text-slate-800 focus:outline-none focus:border-slate-900"
          />
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Loại phương tiện * (Vehicle Type)</label>
          <select
            v-model="newVehicleForm.type"
            required
            class="w-full px-4 py-2.5 rounded-2xl border border-slate-200 bg-slate-50 text-xs font-semibold text-slate-800 focus:outline-none focus:border-slate-900"
          >
            <option value="Motorcycle">Xe máy (Motorcycle)</option>
            <option value="Car">Ô tô (Car)</option>
            <option value="EV">Xe điện (EV)</option>
          </select>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Hãng xe (Brand)</label>
            <input
              v-model="newVehicleForm.brand"
              type="text"
              placeholder="Honda, Toyota..."
              class="w-full px-4 py-2.5 rounded-2xl border border-slate-200 bg-slate-50 text-xs text-slate-800 focus:outline-none focus:border-slate-900"
            />
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Dòng xe (Model)</label>
            <input
              v-model="newVehicleForm.model"
              type="text"
              placeholder="Air Blade, CX-5..."
              class="w-full px-4 py-2.5 rounded-2xl border border-slate-200 bg-slate-50 text-xs text-slate-800 focus:outline-none focus:border-slate-900"
            />
          </div>
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Màu sắc (Color)</label>
          <input
            v-model="newVehicleForm.color"
            type="text"
            placeholder="Đen, Trắng, Đỏ..."
            class="w-full px-4 py-2.5 rounded-2xl border border-slate-200 bg-slate-50 text-xs text-slate-800 focus:outline-none focus:border-slate-900"
          />
        </div>

        <div class="pt-2 flex items-center justify-end gap-2">
          <button
            type="button"
            @click="showAddVehicleModal = false"
            class="px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100 transition cursor-pointer"
          >
            Hủy
          </button>
          <button
            type="submit"
            class="px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-xs transition cursor-pointer shadow-md"
          >
            Lưu phương tiện
          </button>
        </div>
      </form>
    </div>
  </div>


  <!-- ============================================================== -->
  <!-- MODAL: BOOKING SUMMARY (Xác nhận đặt chỗ thành công)          -->
  <!-- ============================================================== -->
  <div v-if="showBookingConfirmedModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
    <div class="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 text-center shadow-2xl border border-slate-100 space-y-5">
      <div class="w-14 h-14 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center text-2xl mx-auto shadow-sm">
        <i class="fa-solid fa-circle-check"></i>
      </div>

      <div>
        <h3 class="text-xl font-black text-slate-900">Đặt chỗ thành công!</h3>
        <p class="text-xs text-slate-500 mt-1">Thông tin đặt chỗ đã được lưu trữ vào hệ thống Smart Parking</p>
      </div>

      <!-- Info Table -->
      <div class="p-5 rounded-2xl bg-slate-50 border border-slate-100 text-left text-xs space-y-2.5">
        <div class="flex justify-between">
          <span class="text-slate-400">Mã đặt chỗ:</span>
          <span class="font-mono font-black text-slate-900">{{ confirmedBookingData.code }}</span>
        </div>
        <div class="flex justify-between">
          <span class="text-slate-400">Khách hàng:</span>
          <span class="font-bold text-slate-800">{{ currentUser?.full_name || 'Khách hàng' }}</span>
        </div>
        <div class="flex justify-between">
          <span class="text-slate-400">Bãi đỗ:</span>
          <span class="font-bold text-slate-800">{{ confirmedBookingData.lot_name }}</span>
        </div>
        <div class="flex justify-between">
          <span class="text-slate-400">Vị trí ô đỗ:</span>
          <span class="font-mono font-black text-blue-600">Ô {{ confirmedBookingData.slot_code }}</span>
        </div>
        <div class="flex justify-between">
          <span class="text-slate-400">Thời gian:</span>
          <span class="font-semibold text-slate-800">{{ confirmedBookingData.time }} ({{ confirmedBookingData.date }})</span>
        </div>
        <div class="flex justify-between">
          <span class="text-slate-400">Phương tiện:</span>
          <span class="font-mono font-bold text-slate-800">{{ confirmedBookingData.plate }}</span>
        </div>
        <div class="border-t border-slate-200 pt-2 flex justify-between font-black text-emerald-600">
          <span>Giá dự kiến:</span>
          <span>{{ confirmedBookingData.fee?.toLocaleString() }} VNĐ</span>
        </div>
      </div>

      <div class="flex items-center gap-3 pt-2">
        <button
          @click="showBookingConfirmedModal = false; openQrModal(confirmedBookingData)"
          class="flex-1 py-3 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs transition cursor-pointer flex items-center justify-center gap-1.5"
        >
          <i class="fa-solid fa-qrcode"></i> Xem mã QR
        </button>
        <button
          @click="showBookingConfirmedModal = false; activeNav = 'cust-bookings'"
          class="flex-1 py-3 rounded-2xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-xs transition cursor-pointer"
        >
          Quản lý đặt chỗ
        </button>
      </div>
    </div>
  </div>


  <!-- ============================================================== -->
  <!-- MODAL: VIEW RECEIPT (Hóa đơn gửi xe chi tiết)                 -->
  <!-- ============================================================== -->
  <div v-if="showReceiptModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
    <div class="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-2xl border border-slate-100 space-y-6">
      <div class="flex items-center justify-between border-b border-slate-100 pb-3">
        <h3 class="font-extrabold text-base text-slate-900">Hóa đơn thanh toán (Parking Receipt)</h3>
        <button @click="showReceiptModal = false" class="text-slate-400 hover:text-slate-600 cursor-pointer">
          <i class="fa-solid fa-xmark text-lg"></i>
        </button>
      </div>

      <!-- Receipt Voucher Layout -->
      <div class="p-6 rounded-2xl bg-slate-50 border border-slate-200 text-xs font-mono space-y-3">
        <div class="text-center pb-3 border-b border-dashed border-slate-300">
          <div class="text-sm font-black text-slate-900">SMART PARKING SYSTEM</div>
          <div class="text-[10px] text-slate-400">Receipt #RC00{{ receiptData.id || '123' }}</div>
        </div>

        <div class="space-y-1.5 pt-1">
          <div class="flex justify-between"><span>Customer:</span><strong class="text-slate-900">{{ currentUser?.full_name || 'Nguyen Van A' }}</strong></div>
          <div class="flex justify-between"><span>Vehicle:</span><strong class="text-slate-900">{{ receiptData.plate || '59A1-123.45' }}</strong></div>
          <div class="flex justify-between"><span>Parking Lot:</span><strong>{{ receiptData.lot_name || 'Nguyen Van Linh' }}</strong></div>
          <div class="flex justify-between"><span>Slot:</span><strong class="text-blue-600">Ô {{ receiptData.slot_code || 'A-023' }}</strong></div>
          <div class="flex justify-between"><span>Check-in:</span><span>18:05</span></div>
          <div class="flex justify-between"><span>Check-out:</span><span>21:12</span></div>
          <div class="flex justify-between"><span>Duration:</span><span>{{ receiptData.duration || '3h 07m' }}</span></div>
        </div>

        <div class="border-t-2 border-dashed border-slate-300 pt-3 flex justify-between font-black text-sm">
          <span>TOTAL:</span>
          <span class="text-emerald-600">{{ receiptData.fee?.toLocaleString() || '35,000' }} VND</span>
        </div>

        <div class="text-center pt-2 text-[10px] text-emerald-600 font-bold uppercase">
          Status: Paid ✓
        </div>
      </div>

      <div class="flex items-center gap-3">
        <button
          @click="downloadReceipt()"
          class="flex-1 py-3 rounded-2xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-xs transition cursor-pointer flex items-center justify-center gap-1.5"
        >
          <i class="fa-solid fa-download"></i> Tải hóa đơn (Download)
        </button>
        <button
          @click="showReceiptModal = false"
          class="py-3 px-5 rounded-2xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs transition cursor-pointer"
        >
          Đóng
        </button>
      </div>
    </div>
  </div>


  <!-- ============================================================== -->
  <!-- MODAL: HELP & SUPPORT (Trợ giúp & FAQ)                        -->
  <!-- ============================================================== -->
  <div v-if="showHelpModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
    <div class="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-slate-100 space-y-6">
      <div class="flex items-center justify-between border-b border-slate-100 pb-3">
        <h3 class="font-extrabold text-base text-slate-900 flex items-center gap-2">
          <i class="fa-solid fa-circle-question text-emerald-500"></i>
          Hỗ trợ &amp; Trợ giúp (Help &amp; Support)
        </h3>
        <button @click="showHelpModal = false" class="text-slate-400 hover:text-slate-600 cursor-pointer">
          <i class="fa-solid fa-xmark text-lg"></i>
        </button>
      </div>

      <!-- FAQ Accordion -->
      <div class="space-y-3 text-xs">
        <div class="p-3.5 rounded-2xl bg-slate-50 border border-slate-100">
          <div class="font-black text-slate-800 mb-1">❓ Làm thế nào để đặt chỗ gửi xe?</div>
          <div class="text-slate-500 leading-relaxed">
            Vào menu <strong>Find Parking</strong> hoặc <strong>My Bookings</strong>, chọn bãi đỗ, ngày giờ và ô slot mong muốn, sau đó bấm Xác nhận để nhận mã QR.
          </div>
        </div>

        <div class="p-3.5 rounded-2xl bg-slate-50 border border-slate-100">
          <div class="font-black text-slate-800 mb-1">❓ Làm thế nào để vào/ra bãi xe bằng QR?</div>
          <div class="text-slate-500 leading-relaxed">
            Bấm vào nút <strong>My QR</strong> trên booking hoặc dashboard, đưa mã này cho nhân viên bảo vệ tại bốt trực để quét check-in và check-out tự động.
          </div>
        </div>

        <div class="p-3.5 rounded-2xl bg-slate-50 border border-slate-100">
          <div class="font-black text-slate-800 mb-1">❓ Phương thức thanh toán hoạt động như thế nào?</div>
          <div class="text-slate-500 leading-relaxed">
            Bạn có thể thanh toán bằng tiền mặt tại quầy hoặc chọn hình thức thanh toán mô phỏng trực tuyến ngay trên ứng dụng khi hoàn thành lượt gửi.
          </div>
        </div>
      </div>

      <!-- Contact Hotline Card -->
      <div class="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs flex items-center justify-between">
        <div>
          <div class="font-black text-emerald-950">Tổng đài hỗ trợ 24/7</div>
          <div class="text-emerald-700 mt-0.5">Hotline: 1900-8888 · Email: support@parking.vn</div>
        </div>
        <a href="tel:19008888" class="px-4 py-2 rounded-xl bg-emerald-600 text-white font-bold text-xs shadow-xs hover:bg-emerald-700 transition">
          Gọi ngay
        </a>
      </div>
    </div>
  </div>
'''

content = content.replace('</div>\n\n<!-- Vue 3 Application Script -->', modals_html + '\n</div>\n\n<!-- Vue 3 Application Script -->')

index_path.write_text(content, encoding="utf-8")
print("Customer screens and modals injected successfully!")
