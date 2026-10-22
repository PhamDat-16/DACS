import { ref, watch, onMounted, onUnmounted } from "vue";

export default {
  name: "BookingModal",
  props: {
    slot: {
      type: Object,
      default: null,
    },
    isOpen: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["close", "confirm-booking"],
  setup(props, { emit }) {
    const modalRef = ref(null);
    const durationHours = ref(2);
    const licensePlate = ref("51F-123.45");
    const isSuccess = ref(false);
    const bookingResult = ref(null);
    let ctx = null;

    // Tính toán phí dự kiến
    const calculateFee = () => {
      return durationHours.value * 25000; // 25.000 VNĐ / giờ
    };

    onMounted(() => {
      if (!window.gsap) return;
      ctx = window.gsap.context(() => {}, modalRef.value);
    });

    onUnmounted(() => {
      ctx?.revert();
    });

    watch(
      () => props.isOpen,
      (newVal) => {
        if (newVal && window.gsap) {
          isSuccess.value = false;
          window.gsap.fromTo(
            ".modal-content",
            { scale: 0.85, opacity: 0, y: 20 },
            {
              scale: 1,
              opacity: 1,
              y: 0,
              duration: 0.35,
              ease: "back.out(1.6)",
            },
          );
        }
      },
    );

    const handleConfirm = () => {
      // Giả lập đặt chỗ hoặc gọi API
      isSuccess.value = true;
      bookingResult.value = {
        code: "PARK-" + Math.floor(100000 + Math.random() * 900000),
        slot: props.slot.slot_code,
        licensePlate: licensePlate.value,
        fee: calculateFee(),
        time: new Date().toLocaleTimeString("vi-VN"),
      };

      emit("confirm-booking", {
        slot_id: props.slot.id,
        duration: durationHours.value,
        plate: licensePlate.value,
      });

      // Animate QR Code reveal
      setTimeout(() => {
        if (window.gsap) {
          window.gsap.fromTo(
            ".qr-card",
            { scale: 0.7, opacity: 0 },
            { scale: 1, opacity: 1, duration: 0.4, ease: "power2.out" },
          );
        }
      }, 50);
    };

    return {
      modalRef,
      durationHours,
      licensePlate,
      isSuccess,
      bookingResult,
      calculateFee,
      handleConfirm,
      close: () => emit("close"),
    };
  },
  template: `
    <div 
      v-if="isOpen && slot" 
      ref="modalRef"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm"
      @click.self="close"
    >
      <div class="modal-content relative w-full max-w-md bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-2xl text-white">
        <!-- Close button -->
        <button 
          @click="close"
          class="absolute top-5 right-5 text-slate-400 hover:text-white transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <!-- Form Đặt Chỗ -->
        <div v-if="!isSuccess">
          <div class="flex items-center gap-3 mb-5">
            <div class="w-12 h-12 rounded-2xl bg-cyan-500/20 border border-cyan-500/40 flex items-center justify-center text-cyan-400 font-bold text-lg font-mono">
              {{ slot.slot_code }}
            </div>
            <div>
              <h3 class="text-lg font-bold text-white">Đặt Chỗ Đỗ Xe</h3>
              <p class="text-xs text-slate-400">Tọa độ: ({{ slot.x }}, {{ slot.y }}) | Tầng 1</p>
            </div>
          </div>

          <div class="space-y-4">
            <!-- Biển số xe -->
            <div>
              <label class="block text-xs font-semibold text-slate-300 mb-1.5">Biển số phương tiện</label>
              <input 
                v-model="licensePlate"
                type="text" 
                placeholder="VD: 51F-123.45"
                class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-sm font-mono text-cyan-400 focus:outline-none focus:border-cyan-400"
              />
            </div>

            <!-- Thời lượng gửi xe -->
            <div>
              <label class="block text-xs font-semibold text-slate-300 mb-1.5">Thời gian đỗ dự kiến</label>
              <div class="grid grid-cols-4 gap-2">
                <button 
                  v-for="h in [1, 2, 4, 8]" 
                  :key="'duration-' + h"
                  type="button"
                  @click="durationHours = h"
                  class="py-2 rounded-xl text-xs font-semibold transition-all border"
                  :class="durationHours === h 
                    ? 'bg-cyan-500 text-slate-950 border-cyan-400 shadow-lg shadow-cyan-500/20 font-bold' 
                    : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700'"
                >
                  {{ h }} Tiếng
                </button>
              </div>
            </div>

            <!-- Phí dự tính -->
            <div class="bg-slate-950/70 p-4 rounded-xl border border-slate-800 flex justify-between items-center text-sm">
              <span class="text-slate-400">Đơn giá (25k/giờ):</span>
              <span class="text-base font-bold text-emerald-400 font-mono">
                {{ calculateFee().toLocaleString('vi-VN') }} VNĐ
              </span>
            </div>

            <!-- Nút xác nhận -->
            <div class="pt-2 flex gap-3">
              <button 
                type="button" 
                @click="close"
                class="flex-1 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-sm font-semibold transition-colors"
              >
                Hủy
              </button>
              <button 
                type="button" 
                @click="handleConfirm"
                class="flex-1 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold rounded-xl text-sm shadow-lg shadow-cyan-500/30 transition-all"
              >
                Xác Nhận Đặt Chỗ
              </button>
            </div>
          </div>
        </div>

        <!-- Thành công & Hiển thị mã QR Check-in -->
        <div v-else class="text-center py-2">
          <div class="w-12 h-12 bg-emerald-500/20 border border-emerald-500/40 rounded-full flex items-center justify-center text-emerald-400 mx-auto mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>

          <h3 class="text-lg font-bold text-white mb-1">Đặt Chỗ Thành Công!</h3>
          <p class="text-xs text-slate-400 mb-4">Quét mã QR này tại barrier cổng vào để check-in tự động</p>

          <!-- Thẻ QR Code mô phỏng -->
          <div class="qr-card bg-white p-5 rounded-2xl inline-block shadow-2xl mb-4">
            <img 
              :src="'https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=' + bookingResult.code" 
              alt="QR Code"
              class="w-40 h-40 object-contain mx-auto"
            />
            <div class="text-slate-900 font-mono font-bold text-xs mt-2 tracking-wider">
              {{ bookingResult.code }}
            </div>
          </div>

          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs text-slate-300 space-y-1 text-left mb-5">
            <div class="flex justify-between">
              <span class="text-slate-500">Ô đỗ đã giữ:</span>
              <span class="font-bold text-cyan-400 font-mono">{{ bookingResult.slot }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-500">Biển số:</span>
              <span class="font-bold text-white font-mono">{{ bookingResult.licensePlate }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-500">Tổng tiền:</span>
              <span class="font-bold text-emerald-400 font-mono">{{ bookingResult.fee.toLocaleString('vi-VN') }} VNĐ</span>
            </div>
          </div>

          <button 
            type="button" 
            @click="close"
            class="w-full py-2.5 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-sm font-semibold transition-colors"
          >
            Đóng
          </button>
        </div>
      </div>
    </div>
  `,
};
