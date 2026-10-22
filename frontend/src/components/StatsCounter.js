import { ref, watch, onMounted } from "vue";

export default {
  name: "StatsCounter",
  props: {
    total: { type: Number, default: 0 },
    available: { type: Number, default: 0 },
    occupancyRate: { type: Number, default: 0 },
  },
  setup(props) {
    const displayTotal = ref(0);
    const displayAvailable = ref(0);
    const displayRate = ref(0);

    const animateNumber = (displayRef, targetVal, duration = 0.8) => {
      if (!window.gsap) {
        displayRef.value = Math.round(targetVal);
        return;
      }
      const obj = { val: displayRef.value };
      window.gsap.to(obj, {
        val: targetVal,
        duration: duration,
        ease: "power2.out",
        onUpdate: () => {
          displayRef.value = Math.round(obj.val);
        },
      });
    };

    onMounted(() => {
      animateNumber(displayTotal, props.total);
      animateNumber(displayAvailable, props.available);
      animateNumber(displayRate, props.occupancyRate * 100);
    });

    watch(
      () => props.total,
      (val) => animateNumber(displayTotal, val),
    );
    watch(
      () => props.available,
      (val) => animateNumber(displayAvailable, val),
    );
    watch(
      () => props.occupancyRate,
      (val) => animateNumber(displayRate, val * 100),
    );

    return {
      displayTotal,
      displayAvailable,
      displayRate,
    };
  },
  template: `
    <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">
      <!-- Card 1: Tổng số slot -->
      <div class="bg-slate-900/80 backdrop-blur-md border border-slate-800 rounded-2xl p-5 shadow-xl relative overflow-hidden group hover:border-slate-700 transition-all">
        <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-blue-500/10 rounded-full blur-2xl group-hover:bg-blue-500/20 transition-all"></div>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Tổng Vị Trí Đỗ</p>
            <h4 class="text-3xl font-black font-mono text-white mt-1">{{ displayTotal }}</h4>
          </div>
          <div class="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/30 flex items-center justify-center text-blue-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
        </div>
        <p class="text-[11px] text-slate-500 mt-3 flex items-center gap-1">
          <span class="text-blue-400">●</span> Sức chứa quy hoạch khu A
        </p>
      </div>

      <!-- Card 2: Slot khả dụng -->
      <div class="bg-slate-900/80 backdrop-blur-md border border-slate-800 rounded-2xl p-5 shadow-xl relative overflow-hidden group hover:border-emerald-500/30 transition-all">
        <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-emerald-500/10 rounded-full blur-2xl group-hover:bg-emerald-500/20 transition-all"></div>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Chỗ Còn Trống</p>
            <h4 class="text-3xl font-black font-mono text-emerald-400 mt-1">{{ displayAvailable }}</h4>
          </div>
          <div class="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
        <p class="text-[11px] text-slate-500 mt-3 flex items-center gap-1">
          <span class="text-emerald-400 animate-ping">●</span> Sẵn sàng đón xe vào bãi
        </p>
      </div>

      <!-- Card 3: Tỷ lệ lấp đầy -->
      <div class="bg-slate-900/80 backdrop-blur-md border border-slate-800 rounded-2xl p-5 shadow-xl relative overflow-hidden group hover:border-purple-500/30 transition-all">
        <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-purple-500/10 rounded-full blur-2xl group-hover:bg-purple-500/20 transition-all"></div>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Tỷ Lệ Lấp Đầy</p>
            <h4 class="text-3xl font-black font-mono text-purple-400 mt-1">{{ displayRate }}%</h4>
          </div>
          <div class="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
        </div>
        <p class="text-[11px] text-slate-500 mt-3 flex items-center gap-1">
          <span class="text-purple-400">●</span> Cập nhật tự động thời gian thực
        </p>
      </div>
    </div>
  `,
};
