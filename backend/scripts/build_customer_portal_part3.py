import re
from pathlib import Path

index_path = Path("frontend/index.html")
content = index_path.read_text(encoding="utf-8")

# 1. Update screenTitle to include customer screens
screen_title_replacement = '''      // Screen title computed
      const screenTitle = computed(() => {
        if (activeNav.value === 'cust-dashboard') return 'Tổng quan Khách hàng (Dashboard)';
        if (activeNav.value === 'cust-find-parking') return 'Tìm bãi đỗ xe & Sơ đồ';
        if (activeNav.value === 'cust-bookings') return 'Đặt chỗ gửi xe (Booking)';
        if (activeNav.value === 'cust-vehicles') return 'Quản lý phương tiện (My Vehicles)';
        if (activeNav.value === 'cust-monthly-pass') return 'Vé tháng (Monthly Pass)';
        if (activeNav.value === 'cust-history') return 'Lịch sử gửi xe';
        if (activeNav.value === 'cust-payments') return 'Thanh toán & Hóa đơn';
        if (activeNav.value === 'cust-profile') return 'Thông tin tài khoản';
        if (activeNav.value === 'parking-lots') return 'Parking Lots';
        if (activeNav.value === 'dashboard') return 'Dashboard';
        if (activeNav.value === 'check-in') return 'Step 1 License Plate';
        if (activeNav.value === 'parking-map') return 'Parking Map';
        if (activeNav.value === 'guest-home') return 'Home';
        if (activeNav.value === 'vehicles') return 'Vehicles Registry';
        if (activeNav.value === 'parking-sessions') return 'Parking Sessions';
        if (activeNav.value === 'staff-accounts') return 'Staff Accounts';
        return 'Smart Parking System';
      });'''

content = re.sub(
    r'// Screen title computed\s+const screenTitle = computed\(\(\) => \{[\s\S]*?return \'Smart Parking System\';\s+\}\);',
    lambda m: screen_title_replacement,
    content
)

# 2. Update routing in handleLogin and restoreSession and enableGuestMode
content = content.replace(
    '''          // Route to appropriate view according to role
          if (currentRole.value === 'admin') {
            activeNav.value = 'parking-lots';
          } else if (currentRole.value === 'staff') {
            activeNav.value = 'check-in';
          } else {
            activeNav.value = 'guest-home';
          }''',
    '''          // Route to appropriate view according to role
          if (currentRole.value === 'admin') {
            activeNav.value = 'parking-lots';
          } else if (currentRole.value === 'staff') {
            activeNav.value = 'check-in';
          } else {
            activeNav.value = 'cust-dashboard';
          }'''
)

content = content.replace(
    '''            if (currentRole.value === 'admin') {
              activeNav.value = 'parking-lots';
            } else if (currentRole.value === 'staff') {
              activeNav.value = 'check-in';
            } else {
              activeNav.value = 'guest-home';
            }''',
    '''            if (currentRole.value === 'admin') {
              activeNav.value = 'parking-lots';
            } else if (currentRole.value === 'staff') {
              activeNav.value = 'check-in';
            } else {
              activeNav.value = 'cust-dashboard';
            }'''
)

content = content.replace(
    '''      function enableGuestMode() {
        guestMode.value = true;
        isLoggedIn.value = true;
        currentRole.value = 'guest';
        activeNav.value = 'parking-map';
      }''',
    '''      function enableGuestMode() {
        guestMode.value = true;
        isLoggedIn.value = true;
        currentRole.value = 'guest';
        activeNav.value = 'cust-dashboard';
      }'''
)

# 3. Add Customer Portal State & Logic right before `// Load data from live FastAPI backend`
customer_logic_js = '''
      // ==============================================================
      // CUSTOMER PORTAL STATE & LOGIC
      // ==============================================================

      // Notifications
      const showNotifDropdown = ref(false);
      const customerNotifications = ref([
        { id: 1, title: 'Phiên đỗ xe đang diễn ra', time: '18:05 hôm nay', text: 'Xe 59A1-123.45 đang đỗ tại ô A-023, bãi Smart Parking Nguyễn Văn Linh.', read: false },
        { id: 2, title: 'Vé tháng kích hoạt', time: '01/10/2026', text: 'Thẻ tháng VIP xe 59A1-123.45 có hiệu lực đến 31/10/2026.', read: false },
        { id: 3, title: 'Nhắc lịch booking', time: '1 ngày trước', text: 'Lịch đặt trước slot A-012 đã hoàn thành suôn sẻ.', read: true }
      ]);

      function markNotifsRead() {
        customerNotifications.value.forEach(n => n.read = true);
      }

      // Parking Lots & Interactive Map Data
      const parkingLots = ref([
        {
          id: 1,
          name: 'Smart Parking - Nguyễn Văn Linh',
          address: '123 Nguyễn Văn Linh, P. Tân Phong, Quận 7, TP.HCM',
          distance: '1.2 km',
          total_spaces: 90,
          available_spaces: 32,
          hourly_rate: 10000,
          hours: '24/7 (Cả tuần)',
          status: 'Đang mở cửa',
          slots: [
            { code: 'A-001', status: 'available', vehicle_type: 'car' },
            { code: 'A-002', status: 'occupied', vehicle_type: 'car' },
            { code: 'A-003', status: 'reserved', vehicle_type: 'car' },
            { code: 'A-004', status: 'available', vehicle_type: 'car' },
            { code: 'A-005', status: 'available', vehicle_type: 'car' },
            { code: 'A-023', status: 'occupied', vehicle_type: 'motorcycle' },
            { code: 'A-024', status: 'available', vehicle_type: 'motorcycle' },
            { code: 'A-025', status: 'available', vehicle_type: 'motorcycle' },
            { code: 'B-001', status: 'available', vehicle_type: 'car' },
            { code: 'B-002', status: 'available', vehicle_type: 'car' },
            { code: 'B-003', status: 'occupied', vehicle_type: 'car' },
            { code: 'B-004', status: 'available', vehicle_type: 'car' },
            { code: 'B-005', status: 'reserved', vehicle_type: 'car' },
            { code: 'B-006', status: 'available', vehicle_type: 'car' },
          ]
        },
        {
          id: 2,
          name: 'Bãi đỗ xe Lê Lợi Central',
          address: '45 Lê Lợi, P. Bến Nghé, Quận 1, TP.HCM',
          distance: '3.5 km',
          total_spaces: 60,
          available_spaces: 14,
          hourly_rate: 15000,
          hours: '06:00 - 23:00',
          status: 'Đang mở cửa',
          slots: [
            { code: 'L-001', status: 'available', vehicle_type: 'car' },
            { code: 'L-002', status: 'occupied', vehicle_type: 'car' },
            { code: 'L-003', status: 'available', vehicle_type: 'car' },
            { code: 'L-004', status: 'reserved', vehicle_type: 'car' },
            { code: 'L-005', status: 'available', vehicle_type: 'motorcycle' },
            { code: 'L-006', status: 'available', vehicle_type: 'motorcycle' },
          ]
        },
        {
          id: 3,
          name: 'Bãi đỗ Landmark 81 Riverside',
          address: '720A Điện Biên Phủ, P. 22, Bình Thạnh, TP.HCM',
          distance: '5.8 km',
          total_spaces: 150,
          available_spaces: 48,
          hourly_rate: 20000,
          hours: '24/7 (Cả tuần)',
          status: 'Đang mở cửa',
          slots: [
            { code: 'LM-01', status: 'available', vehicle_type: 'car' },
            { code: 'LM-02', status: 'occupied', vehicle_type: 'car' },
            { code: 'LM-03', status: 'available', vehicle_type: 'car' },
            { code: 'LM-04', status: 'available', vehicle_type: 'car' },
          ]
        }
      ]);

      const selectedParkingLot = ref(parkingLots.value[0]);
      const chosenSlot = ref(null);

      const filteredParkingLots = computed(() => {
        if (!searchQuery.value.trim()) return parkingLots.value;
        const q = searchQuery.value.toLowerCase();
        return parkingLots.value.filter(lot =>
          lot.name.toLowerCase().includes(q) || lot.address.toLowerCase().includes(q)
        );
      });

      function selectLotToViewMap(lot) {
        selectedParkingLot.value = lot;
        chosenSlot.value = null;
      }

      function startBookingAtLot(lot) {
        selectedParkingLot.value = lot;
        bookingForm.value.lot_id = lot.id;
        const availSlot = lot.slots.find(s => s.status === 'available');
        if (availSlot) {
          bookingForm.value.slot_code = availSlot.code;
        }
        activeNav.value = 'cust-bookings';
      }

      function onCustomerSelectSlot(slot) {
        if (slot.status === 'occupied' || slot.status === 'reserved') return;
        chosenSlot.value = slot;
      }

      function proceedToBookingWithSlot() {
        if (!chosenSlot.value) return;
        bookingForm.value.lot_id = selectedParkingLot.value.id;
        bookingForm.value.slot_code = chosenSlot.value.code;
        activeNav.value = 'cust-bookings';
      }

      // My Vehicles Management
      const myVehicles = ref([
        {
          id: 1,
          license_plate: '59A1-123.45',
          vehicle_type: 'motorcycle',
          brand: 'Honda',
          model: 'Air Blade',
          color: 'Đen nhám (Black)'
        },
        {
          id: 2,
          license_plate: '30F-888.88',
          vehicle_type: 'car',
          brand: 'VinFast',
          model: 'VF8',
          color: 'Trắng Ngọc Trai'
        }
      ]);

      const showAddVehicleModal = ref(false);
      const newVehicleForm = ref({
        license_plate: '',
        vehicle_type: 'motorcycle',
        brand: '',
        model: '',
        color: ''
      });

      function openAddVehicleModal() {
        newVehicleForm.value = {
          license_plate: '',
          vehicle_type: 'motorcycle',
          brand: '',
          model: '',
          color: ''
        };
        showAddVehicleModal.value = true;
      }

      function saveNewVehicle() {
        if (!newVehicleForm.value.license_plate.trim()) {
          alert('Vui lòng nhập biển số xe.');
          return;
        }
        myVehicles.value.push({
          id: Date.now(),
          license_plate: newVehicleForm.value.license_plate.trim().toUpperCase(),
          vehicle_type: newVehicleForm.value.vehicle_type,
          brand: newVehicleForm.value.brand.trim() || 'Hãng khác',
          model: newVehicleForm.value.model.trim() || 'Tiêu chuẩn',
          color: newVehicleForm.value.color.trim() || 'Không rõ'
        });
        showAddVehicleModal.value = false;
      }

      function editVehicle(veh) {
        const newColor = prompt('Nhập màu sơn xe mới:', veh.color);
        if (newColor && newColor.trim()) {
          veh.color = newColor.trim();
        }
      }

      function deleteVehicle(veh) {
        if (confirm(`Bạn có chắc chắn muốn xóa phương tiện ${veh.license_plate}?`)) {
          myVehicles.value = myVehicles.value.filter(v => v.id !== veh.id);
        }
      }

      // Monthly Pass
      const myMonthlyPass = ref({
        lot_name: 'Smart Parking - Nguyễn Văn Linh',
        plate: '59A1-123.45',
        vehicle_type: 'Xe máy (Motorcycle)',
        start_date: '01/10/2026',
        end_date: '31/10/2026',
        status: 'ACTIVE',
        price: 150000
      });

      const showBuyPassModal = ref(false);
      const passForm = ref({
        lot_id: 1,
        vehicle_id: 1,
        months: 1
      });

      function openBuyPassModal() {
        showBuyPassModal.value = true;
      }

      function confirmBuyMonthlyPass() {
        const lot = parkingLots.value.find(l => l.id == passForm.value.lot_id) || parkingLots.value[0];
        const veh = myVehicles.value.find(v => v.id == passForm.value.vehicle_id) || myVehicles.value[0];
        const months = parseInt(passForm.value.months) || 1;
        
        myMonthlyPass.value = {
          lot_name: lot.name,
          plate: veh.license_plate,
          vehicle_type: veh.vehicle_type === 'motorcycle' ? 'Xe máy' : 'Ô tô',
          start_date: '01/10/2026',
          end_date: `31/${10 + months - 1}/2026`,
          status: 'ACTIVE',
          price: (veh.vehicle_type === 'motorcycle' ? 150000 : 1200000) * months
        };
        showBuyPassModal.value = false;
        alert(`Chúc mừng! Bạn đã đăng ký thành công vé tháng ${months} tháng cho xe ${veh.license_plate} tại ${lot.name}.`);
      }

      // Current Parking Session (Theo dõi phiên gửi xe hiện tại)
      const currentParkingSession = ref({
        lot_name: 'Smart Parking - Nguyễn Văn Linh',
        slot_code: 'A-023',
        vehicle_plate: '59A1-123.45',
        check_in_time: '18:05 - 01/10/2026',
        duration_text: '01h 42m',
        base_fee: 15000,
        extra_fee: 2000,
        estimated_fee: 17000,
        status: 'PARKING'
      });

      // Parking History (Lịch sử gửi xe)
      const parkingHistory = ref([
        {
          receipt_id: 'RC00123',
          date: '01/10/2026',
          lot_name: 'Smart Parking - Nguyễn Văn Linh',
          slot_code: 'A-023',
          duration_text: '3h 07m',
          fee_text: '35,000 VND',
          status: 'Completed',
          check_in: '18:05',
          check_out: '21:12',
          base_fee: 30000,
          extra_fee: 5000,
          total_fee: 35000,
          customer_name: 'Nguyễn Văn A',
          vehicle_plate: '59A1-123.45'
        },
        {
          receipt_id: 'RC00119',
          date: '28/09/2026',
          lot_name: 'Smart Parking - Nguyễn Văn Linh',
          slot_code: 'A-015',
          duration_text: '2h 12m',
          fee_text: '20,000 VND',
          status: 'Completed',
          check_in: '08:30',
          check_out: '10:42',
          base_fee: 20000,
          extra_fee: 0,
          total_fee: 20000,
          customer_name: 'Nguyễn Văn A',
          vehicle_plate: '59A1-123.45'
        },
        {
          receipt_id: 'RC00104',
          date: '25/09/2026',
          lot_name: 'Bãi đỗ xe Lê Lợi Central',
          slot_code: 'B-021',
          duration_text: '1h 45m',
          fee_text: '15,000 VND',
          status: 'Completed',
          check_in: '14:00',
          check_out: '15:45',
          base_fee: 15000,
          extra_fee: 0,
          total_fee: 15000,
          customer_name: 'Nguyễn Văn A',
          vehicle_plate: '59A1-123.45'
        }
      ]);

      // Bookings System (My Bookings)
      const bookingForm = ref({
        lot_id: 1,
        date: '2026-10-01',
        start_time: '18:00',
        duration_hours: 3,
        vehicle_id: 1,
        slot_code: 'A-024'
      });

      const calculatedBookingFee = computed(() => {
        const lot = parkingLots.value.find(l => l.id == bookingForm.value.lot_id) || parkingLots.value[0];
        const hours = parseInt(bookingForm.value.duration_hours) || 1;
        return hours * (lot.hourly_rate || 10000);
      });

      function onBookingLotChange() {
        const lot = parkingLots.value.find(l => l.id == bookingForm.value.lot_id);
        if (lot && lot.slots && lot.slots.length > 0) {
          const avail = lot.slots.find(s => s.status === 'available');
          bookingForm.value.slot_code = avail ? avail.code : lot.slots[0].code;
        }
      }

      const myBookings = ref([
        {
          booking_id: 'BK00123',
          lot_name: 'Smart Parking - Nguyễn Văn Linh',
          slot_code: 'A-023',
          vehicle_plate: '59A1-123.45',
          date: '01/10/2026',
          time_range: '18:00 - 21:00',
          duration_text: '3h 00m',
          fee_text: '30,000 VND',
          status: 'upcoming',
          qr_token: 'SP-QR-BK00123-A023-NVL'
        },
        {
          booking_id: 'BK00120',
          lot_name: 'Smart Parking - Nguyễn Văn Linh',
          slot_code: 'A-023',
          vehicle_plate: '59A1-123.45',
          date: '01/10/2026',
          time_range: '18:05 - Đang gửi',
          duration_text: '01h 42m',
          fee_text: '17,000 VND',
          status: 'active',
          qr_token: 'SP-QR-BK00120-ACT-A023'
        },
        {
          booking_id: 'BK00118',
          lot_name: 'Smart Parking - Nguyễn Văn Linh',
          slot_code: 'A-012',
          vehicle_plate: '59A1-123.45',
          date: '01/09/2026',
          time_range: '08:00 - 10:30',
          duration_text: '2h 30m',
          fee_text: '25,000 VND',
          status: 'completed',
          qr_token: 'SP-QR-BK00118-A012-NVL'
        },
        {
          booking_id: 'BK00095',
          lot_name: 'Bãi đỗ xe Lê Lợi Central',
          slot_code: 'L-004',
          vehicle_plate: '30F-888.88',
          date: '20/09/2026',
          time_range: '10:00 - 12:00',
          duration_text: '2h 00m',
          fee_text: '30,000 VND',
          status: 'cancelled',
          qr_token: 'SP-QR-BK00095-CNL'
        }
      ]);

      const activeBookingTab = ref('upcoming');

      const filteredBookings = computed(() => {
        return myBookings.value.filter(b => b.status === activeBookingTab.value);
      });

      const activeBookingCount = computed(() => {
        return myBookings.value.filter(b => b.status === 'upcoming' || b.status === 'active').length;
      });

      const showBookingConfirmedModal = ref(false);
      const confirmedBookingData = ref(null);

      function confirmCreateBooking() {
        const lot = parkingLots.value.find(l => l.id == bookingForm.value.lot_id) || parkingLots.value[0];
        const veh = myVehicles.value.find(v => v.id == bookingForm.value.vehicle_id) || myVehicles.value[0];
        const bookingId = 'BK' + Math.floor(10000 + Math.random() * 90000);
        const hours = parseInt(bookingForm.value.duration_hours) || 2;
        const fee = hours * lot.hourly_rate;

        const newBk = {
          booking_id: bookingId,
          lot_name: lot.name,
          slot_code: bookingForm.value.slot_code || 'A-001',
          vehicle_plate: veh.license_plate,
          date: bookingForm.value.date,
          time_range: `${bookingForm.value.start_time} (${hours} giờ)`,
          duration_text: `${hours}h 00m`,
          fee_text: `${fee.toLocaleString()} VND`,
          status: 'upcoming',
          qr_token: `SP-QR-${bookingId}-${bookingForm.value.slot_code}`
        };

        myBookings.value.unshift(newBk);
        confirmedBookingData.value = newBk;
        showBookingConfirmedModal.value = true;
      }

      function cancelBooking(bk) {
        if (confirm(`Bạn có chắc muốn hủy đặt chỗ ${bk.booking_id} tại ô ${bk.slot_code}?`)) {
          bk.status = 'cancelled';
        }
      }

      // QR Modal
      const showQrModal = ref(false);
      const qrData = ref(null);

      function openQrModal(bk) {
        if (!bk) {
          // Open for current active session
          qrData.value = {
            booking_id: 'SESSION-023',
            slot_code: currentParkingSession.value?.slot_code || 'A-023',
            lot_name: currentParkingSession.value?.lot_name || 'Bãi đỗ chính',
            date: '01/10/2026',
            time_range: currentParkingSession.value?.check_in_time || '18:05',
            qr_token: 'SP-QR-ACT-023-CURRENT'
          };
        } else {
          qrData.value = bk;
        }
        showQrModal.value = true;
      }

      // Receipt Modal
      const showReceiptModal = ref(false);
      const receiptData = ref(null);

      function openReceiptModal(item) {
        receiptData.value = {
          receipt_id: item.receipt_id || 'RC00123',
          customer_name: item.customer_name || currentUser.value?.full_name || 'Nguyễn Văn A',
          vehicle_plate: item.vehicle_plate || '59A1-123.45',
          lot_name: item.lot_name || 'Smart Parking - Nguyễn Văn Linh',
          slot_code: item.slot_code || 'A-023',
          check_in: item.check_in || '18:05',
          check_out: item.check_out || '21:12',
          duration: item.duration_text || '3h 07m',
          base_fee: item.base_fee || 30000,
          extra_fee: item.extra_fee || 5000,
          total_fee: item.total_fee || 35000,
          payment_status: 'Paid ✓'
        };
        showReceiptModal.value = true;
      }

      function viewReceiptForBooking(bk) {
        openReceiptModal({
          receipt_id: 'RC-' + bk.booking_id,
          customer_name: currentUser.value?.full_name || 'Nguyễn Văn A',
          vehicle_plate: bk.vehicle_plate,
          lot_name: bk.lot_name,
          slot_code: bk.slot_code,
          check_in: '18:00',
          check_out: '21:00',
          duration_text: bk.duration_text,
          base_fee: 30000,
          extra_fee: 0,
          total_fee: 30000
        });
      }

      function downloadReceipt() {
        alert('Đang tải hóa đơn đỗ xe điện tử (PDF)... Đã lưu vào máy của bạn.');
      }

      // Help Modal
      const showHelpModal = ref(false);
      function openHelpModal() {
        showHelpModal.value = true;
      }

      // Payments & Simulated Checkout
      const selectedPaymentMethod = ref('simulated_online');
      const isPaymentProcessing = ref(false);
      const paymentSuccessMessage = ref('');

      function executePayment() {
        if (!currentParkingSession.value) return;
        isPaymentProcessing.value = true;

        setTimeout(() => {
          isPaymentProcessing.value = false;
          paymentSuccessMessage.value = 'Thanh toán mô phỏng thành công! Đã ghi nhận thanh toán.';

          const sessionCompleted = {
            receipt_id: 'RC' + Math.floor(10000 + Math.random() * 90000),
            date: '01/10/2026',
            lot_name: currentParkingSession.value.lot_name,
            slot_code: currentParkingSession.value.slot_code,
            duration_text: currentParkingSession.value.duration_text,
            fee_text: `${currentParkingSession.value.estimated_fee.toLocaleString()} VND`,
            status: 'Completed',
            check_in: '18:05',
            check_out: '19:47',
            base_fee: currentParkingSession.value.base_fee,
            extra_fee: currentParkingSession.value.extra_fee,
            total_fee: currentParkingSession.value.estimated_fee,
            customer_name: currentUser.value?.full_name || 'Nguyễn Văn A',
            vehicle_plate: currentParkingSession.value.vehicle_plate
          };

          parkingHistory.value.unshift(sessionCompleted);
          currentParkingSession.value = null;

          // Open receipt for the completed payment
          setTimeout(() => {
            openReceiptModal(sessionCompleted);
          }, 800);
        }, 1000);
      }

      // Customer Profile (Strictly without role editing)
      const profileForm = ref({
        full_name: 'Nguyễn Văn A',
        email: 'customer@parking.vn',
        phone: '0901234567'
      });
      const profileSaveMessage = ref('');

      function saveCustomerProfile() {
        if (currentUser.value) {
          currentUser.value.full_name = profileForm.value.full_name;
          currentUser.value.phone = profileForm.value.phone;
        }
        profileSaveMessage.value = 'Thông tin tài khoản đã được lưu thành công!';
        setTimeout(() => {
          profileSaveMessage.value = '';
        }, 3000);
      }
'''

content = content.replace(
    '      // Load data from live FastAPI backend',
    customer_logic_js + '\n      // Load data from live FastAPI backend'
)

# 4. Expose Customer variables and methods in `return { ... }`
customer_return_exports = '''        // Customer Portal State & Methods
        showNotifDropdown,
        customerNotifications,
        markNotifsRead,
        parkingLots,
        selectedParkingLot,
        chosenSlot,
        filteredParkingLots,
        selectLotToViewMap,
        startBookingAtLot,
        onCustomerSelectSlot,
        proceedToBookingWithSlot,
        myVehicles,
        showAddVehicleModal,
        newVehicleForm,
        openAddVehicleModal,
        saveNewVehicle,
        editVehicle,
        deleteVehicle,
        myMonthlyPass,
        showBuyPassModal,
        passForm,
        openBuyPassModal,
        confirmBuyMonthlyPass,
        currentParkingSession,
        parkingHistory,
        bookingForm,
        calculatedBookingFee,
        onBookingLotChange,
        myBookings,
        activeBookingTab,
        filteredBookings,
        activeBookingCount,
        showBookingConfirmedModal,
        confirmedBookingData,
        confirmCreateBooking,
        cancelBooking,
        showQrModal,
        qrData,
        openQrModal,
        showReceiptModal,
        receiptData,
        openReceiptModal,
        viewReceiptForBooking,
        downloadReceipt,
        showHelpModal,
        openHelpModal,
        selectedPaymentMethod,
        isPaymentProcessing,
        paymentSuccessMessage,
        executePayment,
        profileForm,
        profileSaveMessage,
        saveCustomerProfile,'''

content = content.replace(
    '        handleLogout,',
    '        handleLogout,\n' + customer_return_exports
)

index_path.write_text(content, encoding="utf-8")
print("Customer Portal Vue logic successfully injected into frontend/index.html!")
