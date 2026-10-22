import { ref, onMounted, onUnmounted, watch } from "vue";

export default {
  name: "OccupancyForecast",
  props: {
    forecastData: {
      type: Array,
      default: () => [],
    },
    selectedDate: {
      type: String,
      default: "",
    },
  },
  setup(props) {
    const container = ref(null);
    const selectedHour = ref(new Date().getHours());
    const isHoliday = ref(false);
    const animatedRate = ref(0);
    let ctx = null;

    // Lấy tỷ lệ lấp đầy của giờ đang chọn
    const getCurrentHourData = () => {
      if (!props.forecastData || props.forecastData.length === 0) {
        // Fallback demo data nếu chưa gọi được ML backend
        const hour = selectedHour.value;
        const base = Math.sin(((hour - 8) / 12) * Math.PI) * 0.45 + 0.4;
        return {
          hour_of_day: hour,
          predicted_occupancy_rate: Math.max(0.1, Math.min(0.95, base)),
        };
      }
      return (
        props.forecastData.find((f) => f.hour_of_day === selectedHour.value) ||
        props.forecastData[0]
      );
    };

    // Hàm cập nhật tỷ lệ với GSAP tween mượt mà
    const animateMetric = (targetValue) => {
      if (!window.gsap) {
        animatedRate.value = Math.round(targetValue * 100);
        return;
      }
      const obj = { val: animatedRate.value };
      window.gsap.to(obj, {
        val: Math.round(targetValue * 100),
        duration: 0.5,
        ease: "power2.out",
        onUpdate: () => {
          animatedRate.value = Math.round(obj.val);
        },
      });
    };

    onMounted(() => {
      if (!window.gsap) return;

      ctx = window.gsap.context(() => {
        // Animate thanh bar biểu đồ với GSAP Stagger
        window.gsap.from(".chart-bar", {
          scaleY: 0,
          transformOrigin: "bottom",
          duration: 0.6,
          stagger: 0.02,
          ease: "power3.out",
        });
      }, container.value);

      const current = getCurrentHourData();
      if (current) animateMetric(current.predicted_occupancy_rate);
    });

    onUnmounted(() => {
      ctx?.revert();
    });

    // Theo dõi khi đổi giờ hoặc có dữ liệu mới từ backend
    watch(selectedHour, (newHour) => {
      const current = getCurrentHourData();
      if (current) animateMetric(current.predicted_occupancy_rate);
    });

    watch(
      () => props.forecastData,
      (newData) => {
        if (newData && newData.length > 0) {
          const current = getCurrentHourData();
          if (current) animateMetric(current.predicted_occupancy_rate);

          // Re-animate bars
          if (window.gsap && container.value) {
            window.gsap.fromTo(
              ".chart-bar",
              { scaleY: 0 },
              { scaleY: 1, duration: 0.5, stagger: 0.02, ease: "power2.out" },
            );
          }
        }
      },
    );

    // Sử dụng gsap.utils.mapRange để tính màu sắc thanh bar
    const getBarColor = (rate) => {
      if (rate >= 0.75) return "from-rose-500 to-amber-500";
      if (rate >= 0.45) return "from-amber-500 to-emerald-500";
      return "from-emerald-500 to-cyan-500";
    };

    const getStatusText = (rate) => {
      if (rate >= 0.8)
        return {
          text: "Rất đông (Cao điểm)",
          color: "text-rose-400",
          bg: "bg-rose-950/60 border-rose-700",
        };
      if (rate >= 0.5)
        return {
          text: "Trung bình",
          color: "text-amber-400",
          bg: "bg-amber-950/60 border-amber-700",
        };
      return {
        text: "Thông thoáng (Nhiều chỗ)",
        color: "text-emerald-400",
        bg: "bg-emerald-950/60 border-emerald-700",
      };
    };

    return {
      container,
      selectedHour,
      isHoliday,
      animatedRate,
      getCurrentHourData,
      getBarColor,
      getStatusText,
    };
  },
  template: `
    <div ref="container" class="bg-slate-900/90 backdrop-blur-md rounded-2xl border border-slate-800 p-6 shadow-2xl">
      <!-- Header dự báo -->
      <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
        <div>
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase bg-purple-500/20 text-purple-300 border border-purple-500/40">
              AI / ML Engine
            </span>
            <h3 class="text-xl font-bold text-white">Dự Báo Tỷ Lệ Lấp Đầy (24 Giờ)</h3>
          </div>
          <p class="text-xs text-slate-400 mt-1">
            Mô hình Random Forest / Gradient Boosting dự báo nhu cầu đỗ xe theo ngày & giờ
          </p>
        </div>

        <!-- Trạng thái tóm tắt giờ hiện tại -->
        <div class="flex items-center gap-4">
          <div class="text-right">
            <div class="text-xs text-slate-400">Khung giờ đang xem: <span class="text-cyan-400 font-bold font-mono">{{ selectedHour }}:00</span></div>
            <div class="text-2xl font-black font-mono tracking-tight text-white flex items-center justify-end gap-1">
              <span>{{ animatedRate }}%</span>
              <span class="text-xs font-normal text-slate-400">công suất</span>
            </div>
          </div>
          <div 
            class="px-3 py-2 rounded-xl border text-xs font-semibold"
            :class="getStatusText(animatedRate / 100).bg"
          >
            <span :class="getStatusText(animatedRate / 100).color">
              {{ getStatusText(animatedRate / 100).text }}
            </span>
          </div>
        </div>
      </div>

      <!-- Biểu đồ 24 cột đại diện cho 24 giờ -->
      <div class="relative bg-slate-950/70 border border-slate-800 rounded-xl p-5 mb-6">
        <!-- Đường giới hạn cao điểm 80% -->
        <div class="absolute inset-x-5 top-1/4 border-b border-dashed border-rose-500/30 flex justify-end">
          <span class="text-[10px] text-rose-400/80 -mt-4 pr-1">Ngưỡng cao điểm 75%</span>
        </div>

        <div class="h-44 flex items-end justify-between gap-1.5 pt-6 pb-2">
          <template v-for="h in 24" :key="'hour-bar-' + (h-1)">
            <div 
              class="flex-1 flex flex-col items-center h-full justify-end cursor-pointer group"
              @click="selectedHour = h-1"
            >
              <!-- Bar -->
              <div 
                class="chart-bar w-full rounded-t-md transition-all duration-200 relative"
                :class="[
                  'bg-gradient-to-t ' + getBarColor(forecastData[h-1]?.predicted_occupancy_rate || 0.3),
                  selectedHour === (h-1) ? 'ring-2 ring-cyan-300 scale-x-125 z-10 brightness-125' : 'hover:brightness-110'
                ]"
                :style="{
                  height: Math.max(12, Math.round(((forecastData[h-1]?.predicted_occupancy_rate || 0.25) * 100))) + '%'
                }"
              >
                <!-- Tooltip hover -->
                <div class="opacity-0 group-hover:opacity-100 transition-opacity absolute -top-8 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-[10px] py-1 px-2 rounded shadow-lg whitespace-nowrap pointer-events-none z-20 border border-slate-700">
                  {{ h-1 }}h: {{ Math.round((forecastData[h-1]?.predicted_occupancy_rate || 0) * 100) }}%
                </div>
              </div>

              <!-- Nhãn giờ phía dưới -->
              <span 
                class="text-[9px] mt-2 font-mono"
                :class="selectedHour === (h-1) ? 'text-cyan-400 font-bold' : 'text-slate-500'"
              >
                {{ (h-1) % 3 === 0 ? (h-1) + 'h' : '' }}
              </span>
            </div>
          </template>
        </div>
      </div>

      <!-- Thanh trượt điều khiển giờ (Time Scrubber) -->
      <div class="flex items-center gap-4 bg-slate-800/40 p-4 rounded-xl border border-slate-800">
        <label class="text-xs font-semibold text-slate-300 whitespace-nowrap flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Kéo chọn giờ:
        </label>
        <input 
          type="range" 
          min="0" 
          max="23" 
          v-model.number="selectedHour"
          class="w-full accent-cyan-400 cursor-pointer h-2 bg-slate-700 rounded-lg"
        />
        <div class="px-3 py-1 bg-slate-800 rounded-lg border border-slate-700 text-xs font-mono font-bold text-cyan-400 min-w-[50px] text-center">
          {{ selectedHour }}:00
        </div>
      </div>
    </div>
  `,
};
