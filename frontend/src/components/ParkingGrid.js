import { ref, onMounted, onUnmounted, watch } from "vue";

export default {
  name: "ParkingGrid",
  props: {
    lot: {
      type: Object,
      required: true,
    },
    navigationPath: {
      type: Array,
      default: () => [],
    },
    selectedSlot: {
      type: Object,
      default: null,
    },
  },
  emits: ["select-slot", "start-navigate"],
  setup(props, { emit }) {
    const gridContainer = ref(null);
    const carRef = ref(null);
    const cellSize = 64; // px per grid cell
    let ctx = null;
    let carTimeline = null;

    // Lấy slot theo tọa độ
    const getSlotAt = (x, y) => {
      if (!props.lot || !props.lot.slots) return null;
      return props.lot.slots.find((s) => s.x === x && s.y === y);
    };

    // Kiểm tra xem ô (x,y) có nằm trong đường đi A* không
    const isPathCell = (x, y) => {
      if (!props.navigationPath || props.navigationPath.length === 0)
        return false;
      return props.navigationPath.some(([px, py]) => px === x && py === y);
    };

    const getPathIndex = (x, y) => {
      if (!props.navigationPath) return -1;
      return props.navigationPath.findIndex(([px, py]) => px === x && py === y);
    };

    // Khởi tạo hoạt họa GSAP theo chuẩn gsap-frameworks (gsap.context + cleanup)
    onMounted(() => {
      if (!window.gsap) return;

      ctx = window.gsap.context(() => {
        // Xuất hiện lưới ô đỗ xe mượt mà với stagger 2D
        window.gsap.from(".slot-cell", {
          scale: 0.6,
          opacity: 0,
          duration: 0.45,
          stagger: {
            grid: [props.lot.height || 10, props.lot.width || 10],
            from: "center",
            amount: 0.6,
          },
          ease: "back.out(1.4)",
        });
      }, gridContainer.value);
    });

    onUnmounted(() => {
      if (carTimeline) carTimeline.kill();
      ctx?.revert(); // Dọn dẹp sạch theo chuẩn gsap-frameworks
    });

    // Theo dõi khi có đường đi A* mới -> chạy animation xe di chuyển
    watch(
      () => props.navigationPath,
      (newPath) => {
        if (!newPath || newPath.length === 0 || !carRef.value || !window.gsap)
          return;

        if (carTimeline) carTimeline.kill();

        const [startX, startY] = newPath[0];

        // Đặt xe vào vị trí xuất phát
        window.gsap.set(carRef.value, {
          x: startX * cellSize + cellSize / 2,
          y: startY * cellSize + cellSize / 2,
          rotation: 0,
          opacity: 1,
          scale: 1,
        });

        // Tạo timeline di chuyển mượt mà
        carTimeline = window.gsap.timeline({
          defaults: { ease: "power1.inOut" },
        });

        // Hiệu ứng pulse tại điểm bắt đầu
        carTimeline.fromTo(
          carRef.value,
          { scale: 0.5 },
          { scale: 1.2, duration: 0.25, yoyo: true, repeat: 1 },
        );

        for (let i = 1; i < newPath.length; i++) {
          const [prevX, prevY] = newPath[i - 1];
          const [currX, currY] = newPath[i];

          // Tính góc xoay xe theo hướng di chuyển
          let targetAngle = 0;
          if (currX > prevX)
            targetAngle = 90; // Sang phải
          else if (currX < prevX)
            targetAngle = -90; // Sang trái
          else if (currY > prevY)
            targetAngle = 180; // Xuống dưới
          else if (currY < prevY) targetAngle = 0; // Lên trên

          // Xoay đầu xe rồi tiến tới ô kế tiếp
          carTimeline
            .to(carRef.value, {
              rotation: targetAngle,
              duration: 0.12,
            })
            .to(carRef.value, {
              x: currX * cellSize + cellSize / 2,
              y: currY * cellSize + cellSize / 2,
              duration: 0.28,
            });
        }

        // Khi đến nơi: Nháy đèn phanh / pulse thành công
        carTimeline.to(carRef.value, {
          scale: 1.25,
          duration: 0.2,
          yoyo: true,
          repeat: 3,
          ease: "power2.out",
        });
      },
      { deep: true },
    );

    return {
      gridContainer,
      carRef,
      cellSize,
      getSlotAt,
      isPathCell,
      getPathIndex,
      handleSlotClick: (slot) => {
        if (!slot || slot.is_obstacle) return;
        emit("select-slot", slot);
      },
    };
  },
  template: `
    <div class="relative bg-slate-900/90 backdrop-blur-md rounded-2xl border border-slate-800 p-6 overflow-hidden shadow-2xl">
      <!-- Header điều khiển sơ đồ -->
      <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
        <div>
          <h3 class="text-xl font-bold text-white flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></span>
            Sơ Đồ Mặt Bằng: {{ lot.name }}
          </h3>
          <p class="text-xs text-slate-400 mt-1">
            Kích thước lưới: {{ lot.width }} × {{ lot.height }} ô | Cổng vào: (0,0)
          </p>
        </div>

        <!-- Chú thích trạng thái -->
        <div class="flex items-center gap-3 text-xs bg-slate-800/80 px-4 py-2 rounded-xl border border-slate-700">
          <div class="flex items-center gap-1.5">
            <span class="w-3 h-3 rounded bg-emerald-500/20 border border-emerald-500"></span>
            <span class="text-slate-300">Trống</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="w-3 h-3 rounded bg-amber-500/20 border border-amber-500"></span>
            <span class="text-slate-300">Đã đặt</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="w-3 h-3 rounded bg-rose-500/20 border border-rose-500"></span>
            <span class="text-slate-300">Đang đỗ</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="w-3 h-3 rounded bg-slate-700 border border-slate-600"></span>
            <span class="text-slate-300">Vật cản / Tường</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="w-3 h-3 rounded bg-indigo-500"></span>
            <span class="text-indigo-300 font-semibold">Đường A*</span>
          </div>
        </div>
      </div>

      <!-- Khung hiển thị lưới mặt bằng -->
      <div class="overflow-x-auto pb-4 custom-scrollbar">
        <div 
          ref="gridContainer"
          class="relative inline-block border-2 border-slate-800 rounded-xl bg-slate-950 p-4"
          :style="{
            display: 'grid',
            gridTemplateColumns: 'repeat(' + lot.width + ', ' + cellSize + 'px)',
            gridTemplateRows: 'repeat(' + lot.height + ', ' + cellSize + 'px)',
            gap: '8px'
          }"
        >
          <!-- Xe ảo di chuyển theo lộ trình A* -->
          <div 
            ref="carRef"
            class="absolute pointer-events-none z-30 transition-transform -translate-x-1/2 -translate-y-1/2"
            style="width: 36px; height: 36px; opacity: 0;"
          >
            <div class="w-full h-full bg-gradient-to-r from-blue-500 to-cyan-400 rounded-lg shadow-lg shadow-cyan-500/50 flex items-center justify-center text-white border border-cyan-200">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 fill-current" viewBox="0 0 24 24">
                <path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/>
              </svg>
            </div>
          </div>

          <!-- Các ô trong lưới (Row by Row) -->
          <template v-for="y in lot.height" :key="'row-' + (y-1)">
            <template v-for="x in lot.width" :key="'cell-' + (x-1) + '-' + (y-1)">
              <div 
                class="slot-cell relative rounded-lg flex flex-col items-center justify-center transition-all duration-200 cursor-pointer select-none group"
                :class="[
                  getSlotAt(x-1, y-1)?.is_obstacle 
                    ? 'bg-slate-800/80 border border-slate-700/60 cursor-not-allowed opacity-60' 
                    : getSlotAt(x-1, y-1)?.status === 'available'
                      ? 'bg-emerald-950/30 hover:bg-emerald-900/40 border border-emerald-700/50 hover:border-emerald-400 shadow-sm hover:shadow-emerald-500/20'
                      : getSlotAt(x-1, y-1)?.status === 'booked'
                        ? 'bg-amber-950/40 border border-amber-700/50 hover:border-amber-400'
                        : getSlotAt(x-1, y-1)?.status === 'occupied'
                          ? 'bg-rose-950/40 border border-rose-700/50 hover:border-rose-400'
                          : 'bg-slate-900 border border-slate-800',
                  selectedSlot && selectedSlot.x === (x-1) && selectedSlot.y === (y-1)
                    ? 'ring-2 ring-cyan-400 shadow-lg shadow-cyan-500/30 scale-105 z-20'
                    : '',
                  isPathCell(x-1, y-1) ? 'ring-2 ring-indigo-500/80 bg-indigo-950/40' : ''
                ]"
                :style="{ width: cellSize + 'px', height: cellSize + 'px' }"
                @click="handleSlotClick(getSlotAt(x-1, y-1))"
              >
                <!-- Dấu chỉ đường A* -->
                <div 
                  v-if="isPathCell(x-1, y-1)" 
                  class="absolute -top-1 -right-1 w-4 h-4 bg-indigo-600 text-white rounded-full text-[9px] font-bold flex items-center justify-center shadow"
                >
                  {{ getPathIndex(x-1, y-1) }}
                </div>

                <!-- Cổng vào (0, 0) -->
                <div v-if="x-1 === 0 && y-1 === 0" class="absolute inset-0 bg-blue-600/30 border-2 border-dashed border-blue-400 rounded-lg flex items-center justify-center">
                  <span class="text-[10px] font-extrabold text-blue-200 uppercase tracking-tighter">CỔNG VÀO</span>
                </div>

                <!-- Vật cản -->
                <div v-else-if="getSlotAt(x-1, y-1)?.is_obstacle" class="text-slate-500 flex flex-col items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  <span class="text-[9px]">Vật cản</span>
                </div>

                <!-- Slot đỗ xe thông thường -->
                <template v-else-if="getSlotAt(x-1, y-1)">
                  <span class="text-xs font-bold font-mono tracking-tight" :class="[
                    getSlotAt(x-1, y-1).status === 'available' ? 'text-emerald-400' :
                    getSlotAt(x-1, y-1).status === 'booked' ? 'text-amber-400' : 'text-rose-400'
                  ]">
                    {{ getSlotAt(x-1, y-1).slot_code }}
                  </span>
                  <span class="text-[9px] text-slate-400 font-mono">
                    ({{ x-1 }}, {{ y-1 }})
                  </span>
                </template>

                <!-- Ô trống không có slot -->
                <template v-else>
                  <span class="text-[9px] text-slate-600">({{ x-1 }}, {{ y-1 }})</span>
                </template>
              </div>
            </template>
          </template>
        </div>
      </div>

      <!-- Thanh hướng dẫn thao tác phía dưới -->
      <div class="mt-4 flex flex-wrap items-center justify-between gap-3 text-xs text-slate-400 pt-4 border-t border-slate-800">
        <div class="flex items-center gap-2">
          <span class="text-cyan-400 font-medium">Mẹo:</span>
          <span>Bấm vào một ô trống (Xanh lá) để kiểm tra lộ trình ngắn nhất bằng thuật toán A* và đặt chỗ!</span>
        </div>
        <div v-if="navigationPath.length > 0" class="flex items-center gap-2 text-indigo-400 font-semibold bg-indigo-950/50 px-3 py-1.5 rounded-lg border border-indigo-800/60">
          <span>Lộ trình A*: {{ navigationPath.length - 1 }} bước</span>
          <button 
            @click="$emit('start-navigate')"
            class="ml-2 px-2.5 py-1 bg-indigo-600 hover:bg-indigo-500 text-white rounded text-[11px] font-bold shadow transition-colors"
          >
            Chạy lại mô phỏng xe
          </button>
        </div>
      </div>
    </div>
  `,
};
