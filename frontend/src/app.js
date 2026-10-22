/**
 * Smart Parking System — Fullstack Frontend Application
 * Tích hợp Vue 3 + GSAP Frameworks & GSAP Utils
 */

const {
  createApp,
  ref,
  reactive,
  computed,
  onMounted,
  onUnmounted,
  watch,
  nextTick,
} = window.Vue;

// API Helper
const BASE_URL =
  typeof window !== "undefined" && window.location.port === "3000"
    ? "http://localhost:8000"
    : "";

async function apiRequest(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  const token = localStorage.getItem("sps_token") || "";
  const headers = { "Content-Type": "application/json", ...options.headers };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  try {
    const res = await fetch(url, { ...options, headers });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Lỗi HTTP ${res.status}`);
    }
    return await res.json();
  } catch (e) {
    throw e;
  }
}

// Sound Effects Engine sử dụng Web Audio API (Zero external audio files)
const SoundFX = {
  ctx: null,
  init() {
    if (
      !this.ctx &&
      typeof window !== "undefined" &&
      (window.AudioContext || window.webkitAudioContext)
    ) {
      this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    }
  },
  playTone(freq, type = "sine", duration = 0.15, gainVal = 0.08) {
    try {
      this.init();
      if (!this.ctx) return;
      if (this.ctx.state === "suspended") this.ctx.resume();
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      gain.gain.setValueAtTime(gainVal, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(
        0.0001,
        this.ctx.currentTime + duration,
      );
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + duration);
    } catch (e) {}
  },
  scan() {
    this.playTone(1350, "sine", 0.09, 0.12);
  },
  success() {
    this.playTone(523.25, "triangle", 0.12, 0.12);
    setTimeout(() => this.playTone(659.25, "triangle", 0.22, 0.12), 100);
  },
  barrier() {
    this.playTone(880, "sine", 0.1, 0.1);
    setTimeout(() => this.playTone(1174, "sine", 0.16, 0.1), 120);
  },
  warning() {
    this.playTone(330, "sawtooth", 0.18, 0.1);
  },
};

// Khởi tạo dữ liệu bãi xe mẫu chuẩn
function generateDefaultLot() {
  const lot = {
    id: "lot-mock-01",
    name: "Bãi Xe Trung Tâm — Khu A (Tầng 1)",
    width: 8,
    height: 6,
    slots: [],
  };

  for (let y = 0; y < 6; y++) {
    for (let x = 0; x < 8; x++) {
      // Tạo tường phân cách và vật cản thực tế (lối đi thông thoáng)
      const isObstacle = (x === 3 && y >= 1 && y <= 4) || (x === 0 && y === 0);
      let status = "available";
      if (!isObstacle) {
        if (
          (x === 1 && y === 1) ||
          (x === 6 && y === 2) ||
          (x === 5 && y === 5)
        )
          status = "occupied";
        else if ((x === 2 && y === 4) || (x === 7 && y === 1))
          status = "booked";
      }

      lot.slots.push({
        id: `slot-${x}-${y}`,
        lot_id: lot.id,
        slot_code: isObstacle ? "OBSTACLE" : `A-${x + 1}0${y + 1}`,
        x,
        y,
        is_obstacle: isObstacle,
        status: isObstacle ? "obstacle" : status,
      });
    }
  }
  return lot;
}

// Thuật toán A* giải lập tìm đường ngắn nhất trên lưới (Grid Pathfinding)
function solveAStar(width, height, obstacles, start, end) {
  const [sx, sy] = start;
  const [ex, ey] = end;
  const obsSet = new Set(obstacles.map(([ox, oy]) => `${ox},${oy}`));

  const openSet = [
    {
      x: sx,
      y: sy,
      g: 0,
      h: Math.abs(sx - ex) + Math.abs(sy - ey),
      parent: null,
    },
  ];
  const closedSet = new Set();

  while (openSet.length > 0) {
    openSet.sort((a, b) => a.g + a.h - (b.g + b.h));
    const curr = openSet.shift();

    if (curr.x === ex && curr.y === ey) {
      const path = [];
      let temp = curr;
      while (temp) {
        path.unshift([temp.x, temp.y]);
        temp = temp.parent;
      }
      return path;
    }

    closedSet.add(`${curr.x},${curr.y}`);

    const directions = [
      [0, 1],
      [0, -1],
      [1, 0],
      [-1, 0],
    ];
    for (const [dx, dy] of directions) {
      const nx = curr.x + dx;
      const ny = curr.y + dy;

      if (nx < 0 || nx >= width || ny < 0 || ny >= height) continue;
      if (closedSet.has(`${nx},${ny}`)) continue;
      if (obsSet.has(`${nx},${ny}`) && !(nx === ex && ny === ey)) continue;

      const g = curr.g + 1;
      const h = Math.abs(nx - ex) + Math.abs(ny - ey);
      const existing = openSet.find((node) => node.x === nx && node.y === ny);

      if (!existing) {
        openSet.push({ x: nx, y: ny, g, h, parent: curr });
      } else if (g < existing.g) {
        existing.g = g;
        existing.parent = curr;
      }
    }
  }
  return [
    [sx, sy],
    [ex, ey],
  ];
}

// Khởi tạo ứng dụng Vue
const app = createApp({
  setup() {
    // State chính
    const activeTab = ref("map"); // 'map', 'forecast', 'barrier', 'bookings'
    const isConnected = ref(false);

    // State xác thực (Authentication Guard)
    const currentUser = ref(null);
    const authTab = ref("login"); // 'login' | 'register'
    const authLoading = ref(false);
    const authError = ref("");
    const authForm = reactive({
      email: "",
      password: "",
      fullName: "",
      confirmPassword: "",
    });

    const activeLot = ref(generateDefaultLot());
    const selectedSlot = ref(null);
    const navigationPath = ref([]);
    const statusFilter = ref("all");
    const isBookingModalOpen = ref(false);

    // State Tìm xe thông minh (Find My Car)
    const searchPlate = ref("");
    const foundCarInfo = ref(null);

    // State Thanh toán & Hóa đơn điện tử
    const isPaymentModalOpen = ref(false);
    const paymentTarget = ref(null);
    const isReceiptModalOpen = ref(false);
    const receiptTarget = ref(null);

    // Phân hệ Quản trị Doanh Thu & Vé Tháng Cư Dân (Admin Intelligence)
    const adminSection = ref("overview"); // 'overview', 'passes', 'pricing'
    const isAddPassModalOpen = ref(false);
    const newPassForm = reactive({
      plate: "",
      owner_name: "",
      phone: "",
      room_no: "P.1205",
      vehicle_type: "car",
      months: 1,
    });

    const pricingConfig = reactive({
      hourlyRate: 25000,
      overnightSurcharge: 50000,
      monthlyCar: 1200000,
      monthlyMoto: 150000,
    });

    const revenueStats = reactive({
      today: 2850000,
      month: 68450000,
      sessions: 1420,
      cashlessRate: 92,
      daily: [
        { day: "T2", date: "18/09", amount: 1850000, sessions: 85 },
        { day: "T3", date: "19/09", amount: 2100000, sessions: 97 },
        { day: "T4", date: "20/09", amount: 1950000, sessions: 92 },
        { day: "T5", date: "21/09", amount: 2450000, sessions: 110 },
        { day: "T6", date: "22/09", amount: 2800000, sessions: 125 },
        { day: "T7", date: "23/09", amount: 3600000, sessions: 158 },
        { day: "CN", date: "24/09", amount: 3250000, sessions: 145 },
      ],
      methods: { vietqr: 65, momo: 25, cash: 10 },
    });

    const monthlyPasses = ref([
      {
        id: "PASS-8801",
        plate: "30H-999.99",
        owner_name: "Lê Hoàng Long (Penthouse 01)",
        phone: "0912 345 678",
        room_no: "PH-01",
        vehicle_type: "car",
        start_date: "2026-09-01",
        expiry_date: "2026-10-01",
        fee: 1200000,
        status: "active",
      },
      {
        id: "PASS-8802",
        plate: "51K-888.66",
        owner_name: "Trần Thị Mai (Căn hộ A-1205)",
        phone: "0988 765 432",
        room_no: "A-1205",
        vehicle_type: "car",
        start_date: "2026-08-15",
        expiry_date: "2026-10-15",
        fee: 1200000,
        status: "active",
      },
      {
        id: "PASS-8803",
        plate: "29B1-123.45",
        owner_name: "Nguyễn Tuấn Anh (Shophouse 03)",
        phone: "0904 112 233",
        room_no: "SH-03",
        vehicle_type: "moto",
        start_date: "2026-09-10",
        expiry_date: "2026-10-10",
        fee: 150000,
        status: "active",
      },
    ]);
    // Phân hệ Công nghệ & Đồng bộ Realtime (WebSocket & IoT Telemetry)
    const wsConnected = ref(false);
    const wsLatency = ref(16);
    const wsMessageCount = ref(0);
    const emergencyAlert = ref(null);
    const isBroadcastModalOpen = ref(false);
    const broadcastForm = reactive({
      title: "Thông Báo Khẩn Cấp Bãi Xe",
      message:
        "Khu vực tầng B2 đang vệ sinh hệ thống thoát nước từ 22:00. Kính mong quý cư dân lưu ý!",
      level: "warning",
    });

    const iotSensors = ref([]);
    const iotLoading = ref(false);
    const iotFilter = ref("all"); // 'all', 'occupied', 'warning'
    const isSimulatingTraffic = ref(false);
    const simulationSpeed = ref(8); // giây mỗi lượt
    let simulationTimer = null;
    let wsClient = null;
    let pingInterval = null;
    const trafficLogs = ref([]);

    const addTrafficLog = (level, tag, message) => {
      const time = new Date().toLocaleTimeString("vi-VN", { hour12: false });
      trafficLogs.value.unshift({
        id: Date.now() + Math.random(),
        time,
        level,
        tag,
        message,
      });
      if (trafficLogs.value.length > 50) trafficLogs.value.pop();
    };

    const bookingsList = ref([
      {
        id: "BK-89021",
        slot_code: "A-205",
        plate: "51F-889.92",
        time: "09:30",
        duration: 3,
        status: "Đang đỗ",
        fee: 75000,
        paid: false,
        entryTime: "2026-09-23 09:30",
        paymentMethod: "",
      },
      {
        id: "BK-89020",
        slot_code: "A-702",
        plate: "29A-345.67",
        time: "10:15",
        duration: 2,
        status: "Đã thanh toán",
        fee: 50000,
        paid: true,
        entryTime: "2026-09-23 10:15",
        paymentMethod: "VietQR (MB Bank)",
      },
    ]);

    // Toast notifications
    const toasts = ref([]);
    const showToast = (message, type = "info") => {
      const id = Date.now();
      toasts.value.push({ id, message, type });
      setTimeout(() => {
        toasts.value = toasts.value.filter((t) => t.id !== id);
      }, 3500);
    };

    // Barrier simulation state
    const barrierStatus = ref("closed"); // 'closed', 'opening', 'open'
    const barrierPlate = ref("51K-999.88");
    const barrierArmRef = ref(null);

    // ML Forecast state
    const forecastHour = ref(new Date().getHours());
    const forecastData = ref([]);
    const animatedRate = ref(42);

    // Phân hệ AI & Dynamic Pricing Engine
    const currentDynamicPricing = ref({
      current_hour: new Date().getHours(),
      base_rate: 25000,
      final_rate: 25000,
      multiplier: 1.0,
      tier: "normal",
      tier_name: "Giờ Tiêu Chuẩn",
      badge_color: "cyan",
      badge_text: "Tiêu Chuẩn",
      occupancy_rate: 0.45,
    });

    const dynamicPricing24h = ref([]);
    const aiRecommendations = ref({
      best_value_hours: [],
      peak_avoid_hours: [],
      max_savings_percent: 20,
      ai_summary: "Trợ lý AI đang phân tích dữ liệu lấp đầy...",
    });

    const mlModelInfo = ref({
      model_name: "RandomForestRegressor (Ensemble Learning)",
      n_estimators: 200,
      max_depth: 10,
      metrics: {
        mae: 0.0248,
        rmse: 0.0381,
        r2_score: 0.9642,
        accuracy_percent: 96.4,
      },
      last_trained: "Hôm nay",
    });

    const isRetrainingML = ref(false);

    // KPI Counters
    const stats = reactive({
      total: 48,
      available: 32,
      occupancyRate: 0.33,
    });

    const displayStats = reactive({
      total: 0,
      available: 0,
      occupancyRate: 0,
    });

    // Refs cho GSAP DOM
    const gridRef = ref(null);
    const carRef = ref(null);
    const cellSize = 64;
    let gridCtx = null;
    let carTimeline = null;
    let barrierCtx = null;

    // Lọc slots theo trạng thái
    const filteredSlots = computed(() => {
      if (!activeLot.value || !activeLot.value.slots) return [];
      if (statusFilter.value === "all") return activeLot.value.slots;
      return activeLot.value.slots.filter(
        (s) => s.status === statusFilter.value,
      );
    });

    const getSlotAt = (x, y) => {
      if (!activeLot.value || !activeLot.value.slots) return null;
      return activeLot.value.slots.find(
        (s) =>
          (s.x !== undefined ? s.x : s.pos_x) === x &&
          (s.y !== undefined ? s.y : s.pos_y) === y,
      );
    };

    const isPathCell = (x, y) => {
      if (!navigationPath.value || navigationPath.value.length === 0)
        return false;
      return navigationPath.value.some(([px, py]) => px === x && py === y);
    };

    const getPathIndex = (x, y) => {
      if (!navigationPath.value) return -1;
      return navigationPath.value.findIndex(([px, py]) => px === x && py === y);
    };

    // Hàm cập nhật KPI với GSAP Tweens
    const updateStats = () => {
      if (!activeLot.value || !activeLot.value.slots) return;
      const valid = activeLot.value.slots.filter((s) => !s.is_obstacle);
      stats.total = valid.length;
      stats.available = valid.filter((s) => s.status === "available").length;
      stats.occupancyRate =
        stats.total > 0 ? (stats.total - stats.available) / stats.total : 0;

      if (window.gsap) {
        window.gsap.to(displayStats, {
          total: stats.total,
          available: stats.available,
          occupancyRate: Math.round(stats.occupancyRate * 100),
          duration: 0.6,
          ease: "power2.out",
          roundProps: "total,available,occupancyRate",
        });
      } else {
        displayStats.total = stats.total;
        displayStats.available = stats.available;
        displayStats.occupancyRate = Math.round(stats.occupancyRate * 100);
      }
    };

    // Tải dữ liệu từ backend hoặc mock
    const loadData = async () => {
      try {
        const health = await apiRequest("/api/health");
        if (health && health.status === "ok") {
          isConnected.value = true;
          showToast(
            "Đã kết nối thành công với Backend FastAPI (:8000)",
            "success",
          );
        }

        const lots = await apiRequest("/api/lots");
        if (lots && lots.length > 0) {
          const detail = await apiRequest(`/api/lots/${lots[0].id}`);
          if (detail && detail.slots && detail.slots.length > 0) {
            const mappedSlots = detail.slots.map((s) => ({
              ...s,
              x: s.pos_x !== undefined ? s.pos_x : s.x,
              y: s.pos_y !== undefined ? s.pos_y : s.y,
            }));
            const valid = mappedSlots.filter((s) => !s.is_obstacle);
            if (valid.length >= 2) {
              valid[0].status = "occupied";
              valid[1].status = "booked";
              if (bookingsList.value[0])
                bookingsList.value[0].slot_code = valid[0].slot_code;
              if (bookingsList.value[1])
                bookingsList.value[1].slot_code = valid[1].slot_code;
            }
            activeLot.value = {
              ...detail,
              width: detail.grid_width || detail.width || 8,
              height: detail.grid_height || detail.height || 6,
              slots: mappedSlots,
            };
          }
        }

        const today = new Date().toISOString().split("T")[0];
        const forecast = await apiRequest(
          `/api/predict-occupancy/day?date=${today}`,
        );
        if (forecast && forecast.hourly_forecast) {
          forecastData.value = forecast.hourly_forecast;
        }
      } catch (err) {
        console.log(
          "[App] Dùng Mock Engine do backend chưa có data:",
          err.message,
        );
        // Sinh 24h ML mock data
        const mockF = [];
        for (let h = 0; h < 24; h++) {
          const rate = Math.max(
            0.15,
            Math.min(
              0.94,
              Math.sin(((h - 8) / 12) * Math.PI) * 0.42 +
                0.46 +
                (Math.random() * 0.06 - 0.03),
            ),
          );
          mockF.push({ hour_of_day: h, predicted_occupancy_rate: rate });
        }
        forecastData.value = mockF;
      }

      updateStats();
    };

    // Chọn vị trí ô đỗ
    const handleSelectSlot = async (slot) => {
      if (!slot || slot.is_obstacle) return;
      selectedSlot.value = slot;

      // Tính đường đi ngắn nhất A*
      try {
        if (isConnected.value && activeLot.value.id !== "lot-mock-01") {
          const nav = await apiRequest(
            `/api/lots/${activeLot.value.id}/navigate?slot_id=${slot.id}&from_x=0&from_y=0`,
          );
          navigationPath.value = nav.path;
        } else {
          const obstacles = activeLot.value.slots
            .filter(
              (s) =>
                s.is_obstacle || (s.status === "occupied" && s.id !== slot.id),
            )
            .map((s) => [s.x, s.y]);
          const path = solveAStar(
            activeLot.value.width,
            activeLot.value.height,
            obstacles,
            [0, 0],
            [slot.x, slot.y],
          );
          navigationPath.value = path;
        }
        showToast(
          `Đã tìm thấy lộ trình A* đến ${slot.slot_code} (${navigationPath.value.length - 1} bước)`,
          "info",
        );
      } catch (e) {
        navigationPath.value = [
          [0, 0],
          [slot.x, slot.y],
        ];
      }
    };

    // Tìm ô trống gần cổng (0,0) nhất
    const findNearestAvailableSlot = () => {
      if (!activeLot.value || !activeLot.value.slots) return;
      const availables = activeLot.value.slots.filter(
        (s) => s.status === "available" && !s.is_obstacle,
      );
      if (availables.length === 0) {
        showToast("Hiện tại không còn ô trống nào!", "warning");
        return;
      }

      // Sắp xếp theo khoảng cách Manhattan tới (0,0)
      availables.sort((a, b) => a.x + a.y - (b.x + b.y));
      const nearest = availables[0];
      handleSelectSlot(nearest);
      showToast(
        `Đã tìm thấy ô trống gần nhất: ${nearest.slot_code} tại toạ độ (${nearest.x}, ${nearest.y})`,
        "success",
      );
    };

    // Chạy hoạt họa xe A* bằng GSAP Timeline & Utils
    const runCarAnimation = (path) => {
      if (!path || path.length === 0 || !carRef.value || !window.gsap) return;

      if (carTimeline) carTimeline.kill();

      const [startX, startY] = path[0];
      window.gsap.set(carRef.value, {
        x: startX * cellSize + cellSize / 2,
        y: startY * cellSize + cellSize / 2,
        rotation: 0,
        opacity: 1,
        scale: 1,
      });

      carTimeline = window.gsap.timeline({
        defaults: { ease: "power1.inOut" },
      });
      carTimeline.fromTo(
        carRef.value,
        { scale: 0.6 },
        { scale: 1.15, duration: 0.25, yoyo: true, repeat: 1 },
      );

      for (let i = 1; i < path.length; i++) {
        const [prevX, prevY] = path[i - 1];
        const [currX, currY] = path[i];

        let targetAngle = 0;
        if (currX > prevX) targetAngle = 90;
        else if (currX < prevX) targetAngle = -90;
        else if (currY > prevY) targetAngle = 180;
        else if (currY < prevY) targetAngle = 0;

        carTimeline
          .to(carRef.value, { rotation: targetAngle, duration: 0.12 })
          .to(carRef.value, {
            x: currX * cellSize + cellSize / 2,
            y: currY * cellSize + cellSize / 2,
            duration: 0.28,
          });
      }

      carTimeline.to(carRef.value, {
        scale: 1.25,
        duration: 0.2,
        yoyo: true,
        repeat: 3,
        ease: "power2.out",
      });
    };

    // Khởi tạo WebSocket Client Full-Duplex
    const initWebSocket = () => {
      if (typeof window === "undefined" || !window.WebSocket) return;

      const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      const host = window.location.host || "localhost:8000";
      const wsUrl = `${wsProtocol}//${host}/ws/realtime`;

      try {
        wsClient = new WebSocket(wsUrl);

        wsClient.onopen = () => {
          wsConnected.value = true;
          isConnected.value = true;
          addTrafficLog(
            "info",
            "WS_CLIENT",
            "WebSocket Hub connected successfully (:8000/ws/realtime)",
          );

          if (pingInterval) clearInterval(pingInterval);
          pingInterval = setInterval(() => {
            if (wsClient && wsClient.readyState === WebSocket.OPEN) {
              wsClient.send(
                JSON.stringify({
                  type: "ping",
                  client_time: performance.now(),
                }),
              );
            }
          }, 3500);
        };

        wsClient.onmessage = (event) => {
          try {
            wsMessageCount.value++;
            const msg = JSON.parse(event.data);

            if (msg.type === "pong") {
              const rtt = Math.max(
                1,
                Math.round(performance.now() - msg.client_time),
              );
              wsLatency.value = rtt;
            } else if (msg.type === "SLOT_UPDATED") {
              const { slot_code, status } = msg.data;
              const slot = activeLot.value.slots.find(
                (s) => s.slot_code === slot_code,
              );
              if (slot) {
                slot.status = status;
                updateStats();
                SoundFX.scan();
                showToast(
                  `⚡ Realtime: Ô ${slot_code} vừa chuyển trạng thái sang "${slotStatusText(status)}"`,
                  "info",
                );
                addTrafficLog(
                  "event",
                  "SLOT_SYNC",
                  `Ô ${slot_code} cập nhật: ${status}`,
                );
              }
            } else if (msg.type === "IOT_SENSOR_TRIGGERED") {
              const { sensor, slot_code, is_occupied, distance_cm } = msg.data;
              const s = iotSensors.value.find(
                (item) => item.sensor_id === sensor.sensor_id,
              );
              if (s) {
                Object.assign(s, sensor);
              }
              const slot = activeLot.value.slots.find(
                (sl) => sl.slot_code === slot_code,
              );
              if (slot && !slot.is_obstacle) {
                slot.status = is_occupied ? "occupied" : "available";
                updateStats();
              }
              addTrafficLog(
                is_occupied ? "warning" : "info",
                "IOT_SENSOR",
                `[${sensor.sensor_id}] Ô ${slot_code}: ${is_occupied ? "Phát hiện xe đỗ" : "Xe đã rời đi"} (Khoảng cách: ${distance_cm} cm)`,
              );
            } else if (msg.type === "ADMIN_ANNOUNCEMENT") {
              emergencyAlert.value = msg.data;
              SoundFX.warning();
              showToast(`🚨 THÔNG BÁO: ${msg.data.message}`, "warning");
              addTrafficLog(
                "warning",
                "BROADCAST",
                `Thông báo khẩn từ Admin: ${msg.data.message}`,
              );
            } else if (msg.type === "INIT") {
              addTrafficLog(
                "info",
                "WS_INIT",
                `Kết nối Realtime thành công (Phiên #${msg.active_connections})`,
              );
            }
          } catch (err) {
            console.error("WS error parsing message:", err);
          }
        };

        wsClient.onerror = () => {
          wsConnected.value = false;
        };

        wsClient.onclose = () => {
          wsConnected.value = false;
          if (pingInterval) clearInterval(pingInterval);
          setTimeout(initWebSocket, 3500);
        };
      } catch (err) {
        wsConnected.value = false;
        setTimeout(initWebSocket, 4000);
      }
    };

    // Tải dữ liệu Cảm biến IoT
    const loadIoTSensors = async () => {
      iotLoading.value = true;
      try {
        const data = await apiRequest("/api/realtime/iot-telemetry");
        if (data && data.sensors) {
          iotSensors.value = data.sensors;
        }
      } catch (e) {
        console.warn("Fallback local mock sensors:", e);
      } finally {
        iotLoading.value = false;
      }
    };

    const triggerSensorPing = (sensor) => {
      sensor.last_heartbeat = new Date().toLocaleTimeString("vi-VN", {
        hour12: false,
      });
      SoundFX.scan();
      showToast(
        `Đã ping cảm biến ${sensor.sensor_id} (${sensor.slot_code}) • RSSI: ${sensor.rssi_dbm} dBm`,
        "success",
      );
      addTrafficLog(
        "info",
        "PING",
        `Ping ${sensor.sensor_id}: OK (${sensor.rssi_dbm} dBm)`,
      );
    };

    const triggerSensorToggle = async (sensor) => {
      const newOccupied = !sensor.is_occupied;
      sensor.is_occupied = newOccupied;
      sensor.distance_cm = newOccupied
        ? Math.floor(18 + Math.random() * 20)
        : Math.floor(205 + Math.random() * 30);
      sensor.last_heartbeat = new Date().toLocaleTimeString("vi-VN", {
        hour12: false,
      });

      try {
        await apiRequest("/api/realtime/simulate-iot-event", {
          method: "POST",
          body: JSON.stringify({
            sensor_id: sensor.sensor_id,
            slot_code: sensor.slot_code,
            is_occupied: newOccupied,
            distance_cm: sensor.distance_cm,
          }),
        });
      } catch (e) {
        if (wsClient && wsClient.readyState === WebSocket.OPEN) {
          wsClient.send(
            JSON.stringify({
              type: "broadcast",
              event_type: "IOT_SENSOR_TRIGGERED",
              data: {
                sensor,
                slot_code: sensor.slot_code,
                is_occupied: newOccupied,
                distance_cm: sensor.distance_cm,
              },
            }),
          );
        }
      }

      const slot = activeLot.value.slots.find(
        (s) => s.slot_code === sensor.slot_code,
      );
      if (slot && !slot.is_obstacle) {
        slot.status = newOccupied ? "occupied" : "available";
        updateStats();
      }
      SoundFX.scan();
    };

    const sendAdminBroadcast = async () => {
      if (!broadcastForm.message) return;
      const payload = {
        title: broadcastForm.title || "Thông Báo Toàn Hệ Thống",
        message: broadcastForm.message,
        level: broadcastForm.level,
        sender: currentUser.value
          ? currentUser.value.full_name || currentUser.value.email
          : "Ban Quản Lý",
        timestamp: new Date().toLocaleTimeString("vi-VN", { hour12: false }),
      };

      try {
        await apiRequest("/api/realtime/broadcast", {
          method: "POST",
          body: JSON.stringify({
            event_type: "ADMIN_ANNOUNCEMENT",
            data: payload,
          }),
        });
      } catch (e) {
        if (wsClient && wsClient.readyState === WebSocket.OPEN) {
          wsClient.send(
            JSON.stringify({
              type: "broadcast",
              event_type: "ADMIN_ANNOUNCEMENT",
              data: payload,
            }),
          );
        }
      }

      emergencyAlert.value = payload;
      isBroadcastModalOpen.value = false;
      SoundFX.warning();
      showToast(
        "Đã phát sóng thông báo khẩn cấp tới tất cả màn hình kết nối!",
        "success",
      );
    };

    const mockSimPlates = [
      "30H-123.45",
      "29A-678.90",
      "51K-555.88",
      "14A-999.11",
      "98A-432.10",
      "30E-888.66",
      "29B-456.78",
      "51F-112.23",
    ];

    const runSimulationStep = () => {
      if (!activeLot.value || !activeLot.value.slots) return;

      const isEntry = Math.random() > 0.4;
      const availables = activeLot.value.slots.filter(
        (s) => s.status === "available" && !s.is_obstacle,
      );
      const occupieds = activeLot.value.slots.filter(
        (s) => s.status === "occupied" && !s.is_obstacle,
      );

      if (isEntry && availables.length > 0) {
        const slot = availables[Math.floor(Math.random() * availables.length)];
        const plate =
          mockSimPlates[Math.floor(Math.random() * mockSimPlates.length)];
        slot.status = "occupied";
        updateStats();

        const sens = iotSensors.value.find(
          (s) => s.slot_code === slot.slot_code,
        );
        if (sens) {
          sens.is_occupied = true;
          sens.distance_cm = Math.floor(18 + Math.random() * 18);
          sens.last_heartbeat = new Date().toLocaleTimeString("vi-VN", {
            hour12: false,
          });
        }

        addTrafficLog(
          "event",
          "AUTO_IN",
          `Xe ${plate} Check-in qua Barrier -> Đỗ tại ô ${slot.slot_code}`,
        );
        SoundFX.barrier();
      } else if (!isEntry && occupieds.length > 0) {
        const slot = occupieds[Math.floor(Math.random() * occupieds.length)];
        slot.status = "available";
        updateStats();

        const sens = iotSensors.value.find(
          (s) => s.slot_code === slot.slot_code,
        );
        if (sens) {
          sens.is_occupied = false;
          sens.distance_cm = Math.floor(210 + Math.random() * 25);
          sens.last_heartbeat = new Date().toLocaleTimeString("vi-VN", {
            hour12: false,
          });
        }

        const fee = (Math.floor(Math.random() * 3) + 1) * 25000;
        revenueStats.today += fee;
        revenueStats.sessions += 1;
        addTrafficLog(
          "success",
          "AUTO_OUT",
          `Xe rời ô ${slot.slot_code} -> Check-out barrier -> Thu cước ${fee.toLocaleString("vi-VN")} đ (VietQR Napas)`,
        );
        SoundFX.success();
      }
    };

    const toggleTrafficSimulation = () => {
      isSimulatingTraffic.value = !isSimulatingTraffic.value;
      if (isSimulatingTraffic.value) {
        showToast(
          "Đã kích hoạt Bộ Giả Lập Giao Thông Realtime tự động!",
          "success",
        );
        addTrafficLog(
          "info",
          "SIMULATOR",
          "Bắt đầu mô phỏng giao thông tự động...",
        );
        runSimulationStep();
        simulationTimer = setInterval(
          runSimulationStep,
          simulationSpeed.value * 1000,
        );
      } else {
        if (simulationTimer) clearInterval(simulationTimer);
        showToast("Đã tạm dừng mô phỏng giao thông.", "info");
        addTrafficLog("info", "SIMULATOR", "Đã dừng mô phỏng giao thông.");
      }
    };

    // Tải dữ liệu Định Giá Động & Gợi ý AI
    const loadDynamicPricing = async () => {
      try {
        const cur = await apiRequest("/api/dynamic-pricing/current");
        if (cur && cur.final_rate) currentDynamicPricing.value = cur;

        const matrix = await apiRequest("/api/dynamic-pricing/24h");
        if (matrix && matrix.hourly_pricing)
          dynamicPricing24h.value = matrix.hourly_pricing;

        const recs = await apiRequest(
          "/api/dynamic-pricing/ai-recommendations",
        );
        if (recs && recs.best_value_hours) aiRecommendations.value = recs;

        const info = await apiRequest("/api/predict-occupancy/model-info");
        if (info && info.metrics) mlModelInfo.value = info;
      } catch (err) {
        console.warn("[DynamicPricing] Dùng fallback local data:", err);
      }
    };

    // Kích hoạt Huấn Luyện Lại Model Machine Learning
    const handleRetrainModel = async () => {
      isRetrainingML.value = true;
      SoundFX.scan();
      showToast(
        "Đang kích hoạt thuật toán huấn luyện lại Random Forest với 200 trees...",
        "info",
      );

      try {
        const res = await apiRequest("/api/predict-occupancy/retrain", {
          method: "POST",
        });
        if (res && res.metrics) {
          mlModelInfo.value.metrics = res.metrics;
          mlModelInfo.value.last_trained = "Vừa xong";
          await loadDynamicPricing();
          loadCityLotsNetwork();
          await loadData();
          SoundFX.success();
          showToast(
            `Huấn luyện thành công! Độ chính xác R²: ${res.metrics.accuracy_percent}% (Thời gian: ${res.duration_seconds}s)`,
            "success",
          );
          addTrafficLog(
            "success",
            "ML_TRAIN",
            `Đã Retrain Model (${res.total_samples} mẫu): MAE=${res.metrics.mae}, R²=${res.metrics.r2_score}`,
          );
        }
      } catch (err) {
        showToast(`Lỗi huấn luyện: ${err.message}`, "warning");
      } finally {
        isRetrainingML.value = false;
      }
    };

    // Áp dụng khung giờ vàng AI gợi ý vào đặt chỗ
    const applyBestHourForBooking = (bestHour) => {
      forecastHour.value = bestHour.hour;
      activeTab.value = "map";
      findNearestAvailableSlot();
      SoundFX.success();
      showToast(
        `Đã chọn khung giờ vàng ${bestHour.time_range} (${bestHour.discount_text})! Ô đỗ đã được định vị.`,
        "success",
      );
    };

    // Điều hướng nhanh đến Barrier sau khi đặt vé
    const handleGoToBarrier = (data) => {
      isBookingModalOpen.value = false;
      activeTab.value = "barrier";
      if (data && data.plate) {
        barrierPlate.value = data.plate;
      }
      showToast(
        `Đã nạp vé ${data.code} (${data.plate}). Đang mở barrier đón xe vào bãi...`,
        "success",
      );
      setTimeout(() => {
        triggerBarrier("in");
      }, 700);
    };

    // Theo dõi navigationPath để kích hoạt xe chạy
    watch(
      navigationPath,
      (newPath) => {
        nextTick(() => {
          runCarAnimation(newPath);
        });
      },
      { deep: true },
    );

    // Tìm vị trí xe thông minh & Dẫn đường A* (Find My Car)
    const handleFindCar = () => {
      const q = searchPlate.value.trim().toUpperCase();
      if (!q) {
        showToast("Vui lòng nhập biển số xe hoặc mã ô để tìm kiếm!", "warning");
        SoundFX.warning();
        return;
      }

      // 1. Tìm trong bookingsList theo biển số hoặc mã vé
      const booking = bookingsList.value.find(
        (b) =>
          b.plate.toUpperCase().includes(q) ||
          b.id.toUpperCase().includes(q) ||
          b.slot_code.toUpperCase() === q,
      );

      let targetSlot = null;
      if (booking) {
        targetSlot = activeLot.value.slots.find(
          (s) => s.slot_code === booking.slot_code,
        );
      }

      // 2. Tìm trực tiếp theo mã slot (ví dụ "B2", "B3", "A-205")
      if (!targetSlot) {
        targetSlot = activeLot.value.slots.find(
          (s) => !s.is_obstacle && s.slot_code.toUpperCase() === q,
        );
      }

      // 3. Fallback: tìm ô occupied/booked đầu tiên
      if (!targetSlot) {
        targetSlot = activeLot.value.slots.find(
          (s) =>
            !s.is_obstacle &&
            (s.status === "occupied" || s.status === "booked"),
        );
      }

      if (targetSlot) {
        selectedSlot.value = targetSlot;
        foundCarInfo.value = {
          plate: booking ? booking.plate : q,
          slot: targetSlot.slot_code,
          status: targetSlot.status,
        };
        handleSelectSlot(targetSlot);
        SoundFX.success();
        showToast(
          `Đã tìm thấy xe [${booking ? booking.plate : q}] tại vị trí ô ${targetSlot.slot_code}!`,
          "success",
        );

        if (window.gsap) {
          window.gsap.fromTo(
            ".slot-cell.ring-cyan-400",
            { scale: 1 },
            {
              scale: 1.25,
              duration: 0.25,
              yoyo: true,
              repeat: 4,
              ease: "power2.inOut",
            },
          );
        }
      } else {
        SoundFX.warning();
        showToast(
          `Không tìm thấy phương tiện có biển số [${q}] trong bãi!`,
          "warning",
        );
      }
    };

    // Mở modal thanh toán cho 1 vé
    const openPayment = (booking) => {
      paymentTarget.value = booking;
      isPaymentModalOpen.value = true;
      SoundFX.scan();
    };

    // Xử lý sau khi thanh toán thành công
    const handlePaymentCompleted = (paymentResult) => {
      isPaymentModalOpen.value = false;
      if (paymentTarget.value) {
        paymentTarget.value.paid = true;
        paymentTarget.value.status = "Đã thanh toán";
        paymentTarget.value.paymentMethod = paymentResult.method;
        receiptTarget.value = { ...paymentTarget.value };
      }

      SoundFX.success();
      showToast(
        `Thanh toán ${paymentResult.amount.toLocaleString("vi-VN")} đ thành công qua ${paymentResult.method}!`,
        "success",
      );

      // Nếu đang ở tab barrier và biển số trùng, tự động mở barrier cho xe rời bãi
      if (
        activeTab.value === "barrier" &&
        paymentResult.plate.toUpperCase() ===
          barrierPlate.value.trim().toUpperCase()
      ) {
        setTimeout(() => {
          showToast(
            "Đã thanh toán cước phí! Đang nâng barrier mở cổng cho xe ra...",
            "success",
          );
          triggerBarrier("out-confirmed");
        }, 800);
      }
    };

    // Mở modal hóa đơn / biên lai
    const openReceipt = (booking) => {
      receiptTarget.value = booking;
      isReceiptModalOpen.value = true;
      SoundFX.scan();
    };

    // Kiểm tra xe có thuộc diện Thuê bao Vé Tháng Cư Dân (VIP) hay không
    const barrierVehicleMonthlyPass = computed(() => {
      const p = barrierPlate.value.trim().toUpperCase();
      return monthlyPasses.value.find(
        (m) => m.plate.toUpperCase() === p && m.status === "active",
      );
    });

    const barrierVehicleIsMonthly = computed(
      () => !!barrierVehicleMonthlyPass.value,
    );

    // Trạng thái xe tại Barrier Cổng
    const barrierVehicleBooking = computed(() => {
      const p = barrierPlate.value.trim().toUpperCase();
      return bookingsList.value.find(
        (b) => b.plate.toUpperCase() === p && b.status !== "Hoàn thành",
      );
    });

    const barrierVehicleNeedsPayment = computed(() => {
      if (barrierVehicleIsMonthly.value) return false;
      const b = barrierVehicleBooking.value;
      return b && !b.paid;
    });

    const barrierVehicleStatusText = computed(() => {
      if (barrierVehicleIsMonthly.value) {
        return (
          "Thẻ Cư Dân VIP (" +
          barrierVehicleMonthlyPass.value.owner_name +
          ") • Miễn phí lượt"
        );
      }
      const b = barrierVehicleBooking.value;
      if (!b) return "Xe vãng lai (Chưa đăng ký trước)";
      if (b.paid) return "Đã thanh toán • Vị trí ô " + b.slot_code;
      return (
        "Chưa thanh toán (" +
        b.fee.toLocaleString("vi-VN") +
        " đ) • Ô " +
        b.slot_code
      );
    });

    const openPaymentForBarrier = () => {
      const b = barrierVehicleBooking.value;
      if (b) {
        openPayment(b);
      } else {
        const guestBooking = {
          id: "BK-" + Math.floor(10000 + Math.random() * 90000),
          slot_code: "Vãng lai",
          plate: barrierPlate.value.trim().toUpperCase(),
          time: new Date().toLocaleTimeString("vi-VN", {
            hour: "2-digit",
            minute: "2-digit",
          }),
          duration: 1,
          status: "Đang đỗ",
          fee: 25000,
          paid: false,
          entryTime: new Date().toLocaleTimeString("vi-VN"),
        };
        bookingsList.value.unshift(guestBooking);
        openPayment(guestBooking);
      }
    };

    // Quản lý vé tháng cư dân (Admin methods)
    const handleAddMonthlyPass = async () => {
      if (!newPassForm.plate || !newPassForm.owner_name) {
        showToast("Vui lòng điền đầy đủ Biển số xe và Tên chủ xe!", "warning");
        SoundFX.warning();
        return;
      }
      const p = newPassForm.plate.trim().toUpperCase();
      const unitFee =
        newPassForm.vehicle_type === "car"
          ? pricingConfig.monthlyCar
          : pricingConfig.monthlyMoto;
      const totalFee = unitFee * (newPassForm.months || 1);

      const expDate = new Date();
      expDate.setDate(expDate.getDate() + 30 * (newPassForm.months || 1));

      const passObj = {
        id: "PASS-" + Math.floor(1000 + Math.random() * 9000),
        plate: p,
        owner_name: newPassForm.owner_name.trim(),
        phone: newPassForm.phone || "0988 123 456",
        room_no: newPassForm.room_no || "A-1205",
        vehicle_type: newPassForm.vehicle_type,
        start_date: new Date().toISOString().split("T")[0],
        expiry_date: expDate.toISOString().split("T")[0],
        fee: totalFee,
        status: "active",
      };

      try {
        await apiRequest("/api/analytics/monthly-passes", {
          method: "POST",
          body: JSON.stringify({
            plate: passObj.plate,
            owner_name: passObj.owner_name,
            phone: passObj.phone,
            room_no: passObj.room_no,
            vehicle_type: passObj.vehicle_type,
            months: newPassForm.months || 1,
          }),
        });
      } catch (e) {}

      monthlyPasses.value.unshift(passObj);
      revenueStats.month += totalFee;
      isAddPassModalOpen.value = false;
      newPassForm.plate = "";
      newPassForm.owner_name = "";
      newPassForm.phone = "";

      SoundFX.success();
      showToast(
        `Đã cấp Thẻ Cư Dân VIP cho xe ${p} (${totalFee.toLocaleString("vi-VN")} đ)!`,
        "success",
      );
    };

    const renewPass = (pass) => {
      const currentExp = new Date(pass.expiry_date);
      const baseDate = currentExp > new Date() ? currentExp : new Date();
      baseDate.setDate(baseDate.getDate() + 30);
      pass.expiry_date = baseDate.toISOString().split("T")[0];
      revenueStats.month += pass.fee;
      SoundFX.success();
      showToast(
        `Đã gia hạn thẻ ${pass.plate} thành công đến ${pass.expiry_date}!`,
        "success",
      );
    };

    const deletePass = (passId) => {
      monthlyPasses.value = monthlyPasses.value.filter((m) => m.id !== passId);
      SoundFX.warning();
      showToast("Đã thu hồi thẻ cư dân thành công.", "info");
    };

    const savePricing = () => {
      SoundFX.success();
      showToast(
        "Đã cập nhật bảng cấu hình biểu phí đỗ xe mới thành công!",
        "success",
      );
    };

    const toggleSlotMaintenance = (slot) => {
      if (!slot) return;
      if (slot.status === "maintenance" || slot.is_obstacle) {
        slot.status = "available";
        slot.is_obstacle = false;
        showToast(`Đã mở lại ô ${slot.slot_code} sẵn sàng đón xe!`, "success");
      } else {
        slot.status = "maintenance";
        slot.is_obstacle = true;
        showToast(
          `Đã khóa ô ${slot.slot_code} để bảo trì kỹ thuật!`,
          "warning",
        );
      }
      updateStats();
      SoundFX.barrier();
    };

    const exportRevenueCSV = () => {
      let csvContent = "\uFEFF";
      csvContent +=
        "MÃ GIAO DỊCH,BIỂN SỐ XE,VỊ TRÍ Ô,THỜI LƯỢNG,TIỀN CƯỚC (VNĐ),PHƯƠNG THỨC,TRẠNG THÁI,THỜI GIAN\n";

      bookingsList.value.forEach((b) => {
        csvContent += `"${b.id}","${b.plate}","${b.slot_code}","${b.duration} Tiếng","${b.fee}","${b.paymentMethod || "Chưa thanh toán"}","${b.status}","${b.entryTime || b.time}"\n`;
      });

      monthlyPasses.value.forEach((m) => {
        csvContent += `"${m.id}","${m.plate}","Cư dân ${m.room_no}","Thuê bao tháng","${m.fee}","VietQR Napas","Đã kích hoạt","${m.start_date}"\n`;
      });

      const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.setAttribute("href", url);
      link.setAttribute(
        "download",
        `Bao_Cao_Doanh_Thu_SmartParking_${new Date().toISOString().split("T")[0]}.csv`,
      );
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      SoundFX.success();
      showToast(
        "Đã xuất Báo Cáo Doanh Thu (Excel / CSV) thành công!",
        "success",
      );
    };

    const printRevenueReport = () => {
      window.print();
    };

    // Xác nhận đặt chỗ
    const handleConfirmBooking = (bookingData) => {
      if (!selectedSlot.value) return;
      const target = activeLot.value.slots.find(
        (s) => s.id === selectedSlot.value.id,
      );
      if (target) {
        target.status = "booked";
        updateStats();
      }

      const newBooking = {
        id: "BK-" + Math.floor(10000 + Math.random() * 90000),
        slot_code: selectedSlot.value.slot_code,
        plate: bookingData.plate,
        time: new Date().toLocaleTimeString("vi-VN", {
          hour: "2-digit",
          minute: "2-digit",
        }),
        duration: bookingData.duration,
        status: "Đã đặt",
        fee: bookingData.duration * 25000,
        paid: false,
        entryTime: new Date().toLocaleTimeString("vi-VN"),
        paymentMethod: "",
      };
      bookingsList.value.unshift(newBooking);

      SoundFX.success();
      showToast(
        `Đặt chỗ thành công vị trí ${selectedSlot.value.slot_code}!`,
        "success",
      );
    };

    // Hoạt họa Barrier Check-in / Check-out bằng GSAP
    const triggerBarrier = (action = "in") => {
      if (!window.gsap) return;

      const plate = barrierPlate.value.trim().toUpperCase();

      // Nếu là xe cư dân vé tháng VIP: Mở ngay và miễn phí lượt!
      if (barrierVehicleIsMonthly.value) {
        SoundFX.success();
        showToast(
          `Nhận diện: Thẻ Cư Dân VIP (${barrierVehicleMonthlyPass.value.owner_name})! Mời xe qua cổng...`,
          "success",
        );
      } else if (action === "out") {
        const activeBooking = bookingsList.value.find(
          (b) => b.plate.toUpperCase() === plate && b.status !== "Hoàn thành",
        );

        if (activeBooking && !activeBooking.paid) {
          SoundFX.warning();
          showToast(
            `Xe ${plate} chưa thanh toán cước (${activeBooking.fee.toLocaleString("vi-VN")} đ)! Mở cổng thanh toán...`,
            "warning",
          );
          openPayment(activeBooking);
          return;
        }
      }

      barrierStatus.value = "opening";
      SoundFX.barrier();
      showToast(
        `Đang quét biển số ${barrierPlate.value}... Barrier đang mở!`,
        "info",
      );

      // GSAP animate barrier arm xoay lên 85 độ
      window.gsap.to(".barrier-arm", {
        rotation: -85,
        transformOrigin: "left bottom",
        duration: 0.7,
        ease: "power2.out",
        onComplete: () => {
          barrierStatus.value = "open";
          setTimeout(() => {
            // Đóng barrier lại sau 2.5s
            window.gsap.to(".barrier-arm", {
              rotation: 0,
              transformOrigin: "left bottom",
              duration: 0.8,
              ease: "bounce.out",
              onComplete: () => {
                barrierStatus.value = "closed";
                const isOut = action === "out" || action === "out-confirmed";
                if (isOut) {
                  const bk = bookingsList.value.find(
                    (b) => b.plate.toUpperCase() === plate,
                  );
                  if (bk) {
                    bk.status = "Hoàn thành";
                    const slot = activeLot.value.slots.find(
                      (s) => s.slot_code === bk.slot_code,
                    );
                    if (slot) {
                      slot.status = "available";
                      updateStats();
                    }
                  }
                }
                showToast(
                  `Xe ${barrierPlate.value} đã ${isOut ? "rời bãi" : "vào bãi"}. Barrier đã đóng!`,
                  "success",
                );
              },
            });
          }, 2500);
        },
      });
    };

    // Xử lý Đăng Nhập
    const handleLogin = async () => {
      authError.value = "";
      if (!authForm.email || !authForm.password) {
        authError.value = "Vui lòng nhập đầy đủ Email và Mật khẩu!";
        return;
      }
      authLoading.value = true;
      try {
        const res = await apiRequest("/api/auth/login", {
          method: "POST",
          body: JSON.stringify({
            email: authForm.email,
            password: authForm.password,
          }),
        });
        if (res && res.access_token) {
          localStorage.setItem("sps_token", res.access_token);
          // Thử lấy thông tin user qua /api/users/me
          try {
            const user = await apiRequest("/api/users/me");
            currentUser.value = user;
            localStorage.setItem("sps_user", JSON.stringify(user));
          } catch (e) {
            currentUser.value = {
              email: authForm.email,
              full_name: authForm.email.split("@")[0],
              role: "user",
            };
            localStorage.setItem("sps_user", JSON.stringify(currentUser.value));
          }
          showToast(
            `Xin chào ${currentUser.value.full_name || currentUser.value.email}!`,
            "success",
          );
          loadData();
        }
      } catch (err) {
        authError.value =
          err.message || "Đăng nhập thất bại. Vui lòng kiểm tra lại tài khoản!";
      } finally {
        authLoading.value = false;
      }
    };

    // Xử lý Đăng Ký
    const handleRegister = async () => {
      authError.value = "";
      if (!authForm.fullName || !authForm.email || !authForm.password) {
        authError.value = "Vui lòng điền đầy đủ các thông tin bắt buộc!";
        return;
      }
      if (authForm.password.length < 6) {
        authError.value = "Mật khẩu phải có ít nhất 6 ký tự!";
        return;
      }
      if (authForm.password !== authForm.confirmPassword) {
        authError.value = "Mật khẩu xác nhận không trùng khớp!";
        return;
      }
      authLoading.value = true;
      try {
        await apiRequest("/api/auth/register", {
          method: "POST",
          body: JSON.stringify({
            email: authForm.email,
            password: authForm.password,
            full_name: authForm.fullName,
          }),
        });
        showToast("Đăng ký thành công! Đang tự động đăng nhập...", "success");
        await handleLogin();
      } catch (err) {
        authError.value =
          err.message || "Đăng ký không thành công. Email có thể đã tồn tại!";
      } finally {
        authLoading.value = false;
      }
    };

    // Đăng nhập nhanh tài khoản thử nghiệm (1-Click Demo)
    const quickLoginDemo = (role = "admin") => {
      authError.value = "";
      const demoUser =
        role === "admin"
          ? {
              id: "usr-admin-demo",
              email: "admin@smartparking.vn",
              full_name: "Quản Trị Viên (Demo)",
              role: "admin",
            }
          : {
              id: "usr-driver-demo",
              email: "khachhang@smartparking.vn",
              full_name: "Nguyễn Văn Khách",
              role: "user",
            };
      localStorage.setItem("sps_token", "demo-token-" + Date.now());
      localStorage.setItem("sps_user", JSON.stringify(demoUser));
      currentUser.value = demoUser;
      showToast(`Đăng nhập thành công với: ${demoUser.full_name}`, "success");
      loadData();
    };

    // Đăng xuất
    const handleLogout = () => {
      localStorage.removeItem("sps_token");
      localStorage.removeItem("sps_user");
      currentUser.value = null;
      authForm.password = "";
      authForm.confirmPassword = "";
      showToast("Đã đăng xuất khỏi hệ thống an toàn.", "info");
    };

    // Chữ cái đại diện Avatar
    const userInitials = computed(() => {
      if (!currentUser.value) return "U";
      const name =
        currentUser.value.full_name || currentUser.value.email || "User";
      const parts = name.trim().split(" ");
      if (parts.length >= 2) {
        return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
      }
      return name.slice(0, 2).toUpperCase();
    });

    // Helper formatters an toan tuyet doi truoc moi auto-formatter
    const toastIcon = (t) =>
      t.type === "success" ? "✓" : t.type === "warning" ? "⚠" : "ℹ";

    const connectionStatusText = computed(() => {
      if (wsConnected.value) {
        return `Realtime WS: ${wsLatency.value}ms`;
      }
      return isConnected.value
        ? "FastAPI Connected (:8000)"
        : "Đang kết nối lại...";
    });

    const filteredIoTSensors = computed(() => {
      if (iotFilter.value === "occupied")
        return iotSensors.value.filter((s) => s.is_occupied);
      if (iotFilter.value === "warning")
        return iotSensors.value.filter(
          (s) => s.status === "warning" || s.battery_level < 20,
        );
      return iotSensors.value;
    });

    const iotOnlineCount = computed(
      () => iotSensors.value.filter((s) => s.status === "online").length,
    );
    const iotWarningCount = computed(
      () =>
        iotSensors.value.filter(
          (s) => s.status === "warning" || s.battery_level < 20,
        ).length,
    );
    const iotOccupiedCount = computed(
      () => iotSensors.value.filter((s) => s.is_occupied).length,
    );

    const slotStatusText = (status) =>
      status === "available"
        ? "Còn trống"
        : status === "booked"
          ? "Đã đặt"
          : "Đang đỗ";
    const pathStepCount = computed(() =>
      navigationPath.value.length > 0
        ? navigationPath.value.length - 1 + " bước"
        : "0",
    );
    const forecastRatePercent = computed(() =>
      Math.round(
        (forecastData.value[forecastHour.value]?.predicted_occupancy_rate ||
          0.45) * 100,
      ),
    );
    const barrierStatusText = computed(() =>
      barrierStatus.value === "open"
        ? "Barrier Đang Mở (Xe đi qua)"
        : "Barrier Đang Đóng",
    );
    const userRoleText = computed(() =>
      !currentUser.value
        ? ""
        : currentUser.value.role === "admin"
          ? "Quản Trị Viên"
          : "Khách Hàng",
    );
    const loginBtnText = computed(() =>
      authLoading.value ? "Đang xác thực..." : "Đăng Nhập Ngay",
    );
    const registerBtnText = computed(() =>
      authLoading.value ? "Đang tạo tài khoản..." : "Đăng Ký Tài Khoản",
    );

    // ==========================================
    // GIS MAP & CHUỖI BÃI ĐỖ XE ĐÔ THỊ (MULTI-LOT)
    // ==========================================
    const DEFAULT_CITY_LOTS = [
      {
            "id": "LOT-HN-01",
            "name": "Bãi Đỗ Xe Vincom Center Bà Triệu",
            "address": "191 Bà Triệu, Phường Lê Đại Hành, Quận Hai Bà Trưng, Hà Nội",
            "district": "Hai Bà Trưng",
            "city": "Hà Nội",
            "latitude": 21.0118,
            "longitude": 105.8505,
            "grid_width": 8,
            "grid_height": 6,
            "total_slots": 48,
            "available_slots": 22,
            "occupancy_rate": 0.54,
            "base_rate": 25000,
            "dynamic_rate": 25000,
            "tier": "normal",
            "tier_name": "Tiêu Chuẩn (1.0x)",
            "has_ev": true,
            "has_roof": true,
            "status": "active",
            "distance_km": 1.4,
            "travel_time_min": 6
      },
      {
            "id": "LOT-HN-02",
            "name": "Bãi Xe Tràng Tiền Plaza & Hồ Gươm",
            "address": "24 Hai Bà Trưng, Phường Tràng Tiền, Quận Hoàn Kiếm, Hà Nội",
            "district": "Hoàn Kiếm",
            "city": "Hà Nội",
            "latitude": 21.0245,
            "longitude": 105.8538,
            "grid_width": 8,
            "grid_height": 8,
            "total_slots": 64,
            "available_slots": 6,
            "occupancy_rate": 0.91,
            "base_rate": 30000,
            "dynamic_rate": 45000,
            "tier": "surge",
            "tier_name": "Quá Tải (+50%)",
            "has_ev": true,
            "has_roof": true,
            "status": "active",
            "distance_km": 0.5,
            "travel_time_min": 2
      },
      {
            "id": "LOT-HN-03",
            "name": "Bãi Xe Lotte Center Liễu Giai",
            "address": "54 Liễu Giai, Phường Cống Vị, Quận Ba Đình, Hà Nội",
            "district": "Ba Đình",
            "city": "Hà Nội",
            "latitude": 21.0332,
            "longitude": 105.813,
            "grid_width": 10,
            "grid_height": 6,
            "total_slots": 60,
            "available_slots": 38,
            "occupancy_rate": 0.37,
            "base_rate": 25000,
            "dynamic_rate": 20000,
            "tier": "off_peak",
            "tier_name": "Tiết Kiệm (-20%)",
            "has_ev": true,
            "has_roof": true,
            "status": "active",
            "distance_km": 4.2,
            "travel_time_min": 14
      },
      {
            "id": "LOT-HN-04",
            "name": "Bãi Xe Keangnam Landmark 72",
            "address": "Phạm Hùng, Phường Mễ Trì, Quận Cầu Giấy, Hà Nội",
            "district": "Cầu Giấy",
            "city": "Hà Nội",
            "latitude": 21.0172,
            "longitude": 105.7838,
            "grid_width": 10,
            "grid_height": 7,
            "total_slots": 70,
            "available_slots": 48,
            "occupancy_rate": 0.31,
            "base_rate": 25000,
            "dynamic_rate": 20000,
            "tier": "off_peak",
            "tier_name": "Tiết Kiệm (-20%)",
            "has_ev": true,
            "has_roof": true,
            "status": "active",
            "distance_km": 6.8,
            "travel_time_min": 19
      },
      {
            "id": "LOT-HN-05",
            "name": "Bãi Đỗ Xe Đông Kinh Nghĩa Thục",
            "address": "07 Đinh Tiên Hoàng, Hàng Bạc, Hoàn Kiếm, Hà Nội",
            "district": "Hoàn Kiếm",
            "city": "Hà Nội",
            "latitude": 21.0315,
            "longitude": 105.8525,
            "grid_width": 8,
            "grid_height": 6,
            "total_slots": 48,
            "available_slots": 28,
            "occupancy_rate": 0.42,
            "base_rate": 25000,
            "dynamic_rate": 25000,
            "tier": "normal",
            "tier_name": "Tiêu Chuẩn (1.0x)",
            "has_ev": false,
            "has_roof": false,
            "status": "active",
            "distance_km": 0.3,
            "travel_time_min": 1
      },
      {
            "id": "LOT-HN-06",
            "name": "Bãi Đỗ Xe Siêu Thị Aeon Mall Hà Đông",
            "address": "Khu đô thị Dương Nội, Phường Dương Nội, Quận Hà Đông, Hà Nội",
            "district": "Hà Đông",
            "city": "Hà Nội",
            "latitude": 20.9832,
            "longitude": 105.7485,
            "grid_width": 10,
            "grid_height": 8,
            "total_slots": 80,
            "available_slots": 46,
            "occupancy_rate": 0.42,
            "base_rate": 20000,
            "dynamic_rate": 20000,
            "tier": "normal",
            "tier_name": "Tiêu Chuẩn (1.0x)",
            "has_ev": true,
            "has_roof": true,
            "status": "active",
            "distance_km": 11.2,
            "travel_time_min": 24
      },
      {
            "id": "LOT-HN-07",
            "name": "Bãi Xe Hồ Gươm Plaza & Big C Hà Đông",
            "address": "102 Trần Phú, Phường Mộ Lao, Quận Hà Đông, Hà Nội",
            "district": "Hà Đông",
            "city": "Hà Nội",
            "latitude": 20.9785,
            "longitude": 105.7874,
            "grid_width": 9,
            "grid_height": 7,
            "total_slots": 63,
            "available_slots": 19,
            "occupancy_rate": 0.7,
            "base_rate": 20000,
            "dynamic_rate": 25000,
            "tier": "peak",
            "tier_name": "Cao Điểm (+25%)",
            "has_ev": true,
            "has_roof": true,
            "status": "active",
            "distance_km": 9.2,
            "travel_time_min": 20
      },
      {
            "id": "LOT-HN-08",
            "name": "Bãi Đỗ Xe Ga Thường Tín & Chợ Phố",
            "address": "Thị trấn Thường Tín, Huyện Thường Tín, Hà Nội (Quốc Lộ 1A)",
            "district": "Thường Tín",
            "city": "Hà Nội",
            "latitude": 20.8712,
            "longitude": 105.8645,
            "grid_width": 8,
            "grid_height": 6,
            "total_slots": 48,
            "available_slots": 36,
            "occupancy_rate": 0.25,
            "base_rate": 15000,
            "dynamic_rate": 12000,
            "tier": "off_peak",
            "tier_name": "Tiết Kiệm (-20%)",
            "has_ev": true,
            "has_roof": false,
            "status": "active",
            "distance_km": 18.5,
            "travel_time_min": 32
      },
      {
            "id": "LOT-HN-09",
            "name": "Bãi Xe Lotte Mall Tây Hồ & Thủy Cung",
            "address": "272 Võ Chí Công, Phường Phú Thượng, Quận Tây Hồ, Hà Nội",
            "district": "Tây Hồ",
            "city": "Hà Nội",
            "latitude": 21.0725,
            "longitude": 105.8135,
            "grid_width": 10,
            "grid_height": 8,
            "total_slots": 80,
            "available_slots": 26,
            "occupancy_rate": 0.67,
            "base_rate": 25000,
            "dynamic_rate": 25000,
            "tier": "normal",
            "tier_name": "Tiêu Chuẩn (1.0x)",
            "has_ev": true,
            "has_roof": true,
            "status": "active",
            "distance_km": 5.8,
            "travel_time_min": 13
      },
      {
            "id": "LOT-HN-10",
            "name": "Bãi Đỗ Xe Aeon Mall Long Biên",
            "address": "27 Cổ Linh, Phường Long Biên, Quận Long Biên, Hà Nội",
            "district": "Long Biên",
            "city": "Hà Nội",
            "latitude": 21.0268,
            "longitude": 105.9015,
            "grid_width": 10,
            "grid_height": 8,
            "total_slots": 80,
            "available_slots": 35,
            "occupancy_rate": 0.56,
            "base_rate": 20000,
            "dynamic_rate": 20000,
            "tier": "normal",
            "tier_name": "Tiêu Chuẩn (1.0x)",
            "has_ev": true,
            "has_roof": true,
            "status": "active",
            "distance_km": 6.2,
            "travel_time_min": 15
      },
      {
            "id": "LOT-HN-11",
            "name": "Bãi Đỗ Xe Vinhomes Royal City",
            "address": "72A Nguyễn Trãi, Phường Thượng Đình, Quận Thanh Xuân, Hà Nội",
            "district": "Thanh Xuân",
            "city": "Hà Nội",
            "latitude": 21.0028,
            "longitude": 105.8152,
            "grid_width": 10,
            "grid_height": 8,
            "total_slots": 80,
            "available_slots": 22,
            "occupancy_rate": 0.72,
            "base_rate": 25000,
            "dynamic_rate": 31000,
            "tier": "peak",
            "tier_name": "Cao Điểm (+25%)",
            "has_ev": true,
            "has_roof": true,
            "status": "active",
            "distance_km": 4.5,
            "travel_time_min": 12
      },
      {
            "id": "LOT-HN-12",
            "name": "Bãi Đỗ Xe Sân Vận Động Quốc Gia Mỹ Đình",
            "address": "Đường Lê Đức Thọ, Phường Mỹ Đình 1, Quận Nam Từ Liêm, Hà Nội",
            "district": "Nam Từ Liêm",
            "city": "Hà Nội",
            "latitude": 21.0205,
            "longitude": 105.7645,
            "grid_width": 12,
            "grid_height": 10,
            "total_slots": 120,
            "available_slots": 85,
            "occupancy_rate": 0.29,
            "base_rate": 20000,
            "dynamic_rate": 16000,
            "tier": "off_peak",
            "tier_name": "Tiết Kiệm (-20%)",
            "has_ev": true,
            "has_roof": false,
            "status": "active",
            "distance_km": 8.5,
            "travel_time_min": 22
      },
      {
            "id": "LOT-HN-13",
            "name": "Bãi Xe Vincom Mega Mall Smart City",
            "address": "Đại đô thị Vinhomes Smart City, Tây Mỗ, Quận Nam Từ Liêm, Hà Nội",
            "district": "Nam Từ Liêm",
            "city": "Hà Nội",
            "latitude": 20.9995,
            "longitude": 105.7425,
            "grid_width": 10,
            "grid_height": 10,
            "total_slots": 100,
            "available_slots": 68,
            "occupancy_rate": 0.32,
            "base_rate": 20000,
            "dynamic_rate": 16000,
            "tier": "off_peak",
            "tier_name": "Tiết Kiệm (-20%)",
            "has_ev": true,
            "has_roof": true,
            "status": "active",
            "distance_km": 11.8,
            "travel_time_min": 25
      },
      {
            "id": "LOT-HN-14",
            "name": "Bãi Xe Công Viên Cầu Giấy & Phố Duy Tân",
            "address": "Phố Thành Thái, Phường Dịch Vọng Hậu, Quận Cầu Giấy, Hà Nội",
            "district": "Cầu Giấy",
            "city": "Hà Nội",
            "latitude": 21.0289,
            "longitude": 105.7905,
            "grid_width": 9,
            "grid_height": 7,
            "total_slots": 63,
            "available_slots": 34,
            "occupancy_rate": 0.46,
            "base_rate": 25000,
            "dynamic_rate": 25000,
            "tier": "normal",
            "tier_name": "Tiêu Chuẩn (1.0x)",
            "has_ev": true,
            "has_roof": true,
            "status": "active",
            "distance_km": 6.1,
            "travel_time_min": 16
      },
      {
            "id": "LOT-HN-15",
            "name": "Bãi Đỗ Xe Bệnh Viện Bạch Mai & ĐH Bách Khoa",
            "address": "78 Giải Phóng, Phường Phương Mai, Quận Đống Đa, Hà Nội",
            "district": "Đống Đa",
            "city": "Hà Nội",
            "latitude": 21.0035,
            "longitude": 105.8415,
            "grid_width": 9,
            "grid_height": 8,
            "total_slots": 72,
            "available_slots": 14,
            "occupancy_rate": 0.81,
            "base_rate": 25000,
            "dynamic_rate": 31000,
            "tier": "peak",
            "tier_name": "Cao Điểm (+25%)",
            "has_ev": true,
            "has_roof": true,
            "status": "active",
            "distance_km": 3.2,
            "travel_time_min": 9
      },
      {
            "id": "LOT-HN-16",
            "name": "Bãi Đỗ Xe Vincom Center Nguyễn Chí Thanh",
            "address": "54A Nguyễn Chí Thanh, Phường Láng Thượng, Quận Đống Đa, Hà Nội",
            "district": "Đống Đa",
            "city": "Hà Nội",
            "latitude": 21.0242,
            "longitude": 105.8118,
            "grid_width": 10,
            "grid_height": 8,
            "total_slots": 80,
            "available_slots": 42,
            "occupancy_rate": 0.47,
            "base_rate": 25000,
            "dynamic_rate": 25000,
            "tier": "normal",
            "tier_name": "Tiêu Chuẩn (1.0x)",
            "has_ev": true,
            "has_roof": true,
            "status": "active",
            "distance_km": 4.8,
            "travel_time_min": 14
      },
      {
            "id": "LOT-HN-17",
            "name": "Bãi Xe Hoàng Thành Thăng Long & Lăng Bác",
            "address": "19C Hoàng Diệu, Phường Điện Biên, Quận Ba Đình, Hà Nội",
            "district": "Ba Đình",
            "city": "Hà Nội",
            "latitude": 21.0372,
            "longitude": 105.8402,
            "grid_width": 8,
            "grid_height": 7,
            "total_slots": 56,
            "available_slots": 31,
            "occupancy_rate": 0.45,
            "base_rate": 25000,
            "dynamic_rate": 25000,
            "tier": "normal",
            "tier_name": "Tiêu Chuẩn (1.0x)",
            "has_ev": false,
            "has_roof": true,
            "status": "active",
            "distance_km": 1.9,
            "travel_time_min": 5
      },
      {
            "id": "LOT-HN-18",
            "name": "Bãi Xe Nhà Ga Metro Văn Quán (Hà Đông)",
            "address": "Đường Trần Phú, Phường Văn Mỗ, Quận Hà Đông, Hà Nội (Ga Tàu Điện)",
            "district": "Hà Đông",
            "city": "Hà Nội",
            "latitude": 20.974,
            "longitude": 105.782,
            "grid_width": 8,
            "grid_height": 7,
            "total_slots": 56,
            "available_slots": 38,
            "occupancy_rate": 0.32,
            "base_rate": 15000,
            "dynamic_rate": 12000,
            "tier": "off_peak",
            "tier_name": "Tiết Kiệm (-20%)",
            "has_ev": true,
            "has_roof": true,
            "status": "active",
            "distance_km": 8.7,
            "travel_time_min": 19
      },
      {
            "id": "LOT-HN-19",
            "name": "Bãi Đỗ Xe Bến Xe Nước Ngầm & Pháp Vân",
            "address": "01 Ngọc Hồi, Phường Hoàng Liệt, Quận Hoàng Mai, Hà Nội",
            "district": "Hoàng Mai",
            "city": "Hà Nội",
            "latitude": 20.9655,
            "longitude": 105.8425,
            "grid_width": 10,
            "grid_height": 8,
            "total_slots": 80,
            "available_slots": 50,
            "occupancy_rate": 0.37,
            "base_rate": 20000,
            "dynamic_rate": 20000,
            "tier": "normal",
            "tier_name": "Tiêu Chuẩn (1.0x)",
            "has_ev": true,
            "has_roof": false,
            "status": "active",
            "distance_km": 7.4,
            "travel_time_min": 17
      },
      {
            "id": "LOT-HN-20",
            "name": "Bãi Xe Khu Công Nghiệp Hà Bình Phương",
            "address": "Xã Văn Bình, Huyện Thường Tín, Hà Nội (Cụm KCN Phía Nam)",
            "district": "Thường Tín",
            "city": "Hà Nội",
            "latitude": 20.885,
            "longitude": 105.86,
            "grid_width": 8,
            "grid_height": 7,
            "total_slots": 56,
            "available_slots": 42,
            "occupancy_rate": 0.25,
            "base_rate": 15000,
            "dynamic_rate": 12000,
            "tier": "off_peak",
            "tier_name": "Tiết Kiệm (-20%)",
            "has_ev": true,
            "has_roof": true,
            "status": "active",
            "distance_km": 16.8,
            "travel_time_min": 28
      },
      {
            "id": "LOT-HN-21",
            "name": "Bãi Xe Công Viên Nước Hồ Tây & Thung Lũng Hoa",
            "address": "614 Lạc Long Quân, Phường Nhật Tân, Quận Tây Hồ, Hà Nội",
            "district": "Tây Hồ",
            "city": "Hà Nội",
            "latitude": 21.0695,
            "longitude": 105.821,
            "grid_width": 9,
            "grid_height": 8,
            "total_slots": 72,
            "available_slots": 45,
            "occupancy_rate": 0.37,
            "base_rate": 25000,
            "dynamic_rate": 20000,
            "tier": "off_peak",
            "tier_name": "Tiết Kiệm (-20%)",
            "has_ev": true,
            "has_roof": false,
            "status": "active",
            "distance_km": 5.4,
            "travel_time_min": 12
      },
      {
            "id": "LOT-HN-22",
            "name": "Bãi Đỗ Xe Ga T1-T2 Sân Bay Quốc Tế Nội Bài",
            "address": "Cảng Hàng Không Quốc Tế Nội Bài, Xã Phú Minh, Huyện Sóc Sơn, Hà Nội",
            "district": "Sóc Sơn",
            "city": "Hà Nội",
            "latitude": 21.2187,
            "longitude": 105.8042,
            "grid_width": 12,
            "grid_height": 12,
            "total_slots": 144,
            "available_slots": 78,
            "occupancy_rate": 0.46,
            "base_rate": 20000,
            "dynamic_rate": 20000,
            "tier": "normal",
            "tier_name": "Tiêu Chuẩn (1.0x)",
            "has_ev": true,
            "has_roof": true,
            "status": "active",
            "distance_km": 24.5,
            "travel_time_min": 35
      }
];
    const cityLotsList = ref(DEFAULT_CITY_LOTS);
    const selectedCityLot = ref(DEFAULT_CITY_LOTS[0]);
    const gisSearchQuery = ref("");
    const gisFilterDistrict = ref("all");
    const gisOnlyEV = ref(false);
    const gisSortBy = ref("nearest");
    const gisFilterQuick = ref("all"); // 'all' | 'near' | 'cheap' | 'ev' | 'available' | 'roof'
    const isAddCityLotModalOpen = ref(false);
    const newCityLotForm = reactive({
      name: "",
      district: "Hoàn Kiếm",
      rate: 25000,
      width: 8,
      height: 6,
      coords: "21.0205, 105.7645",
      has_ev: true,
      has_roof: true,
    });
    let cityMapInstance = null;
    let cityMarkersMap = {};
    let cityUserMarker = null;
    let routePolyline = null;

    const filteredCityLots = computed(() => {
      let list = [...cityLotsList.value];
      if (gisSearchQuery.value.trim()) {
        const q = gisSearchQuery.value.toLowerCase().trim();
        list = list.filter(
          (lot) =>
            (lot.name && lot.name.toLowerCase().includes(q)) ||
            (lot.address && lot.address.toLowerCase().includes(q)) ||
            (lot.district && lot.district.toLowerCase().includes(q)),
        );
      }
      if (gisFilterDistrict.value !== "all") {
        list = list.filter((lot) => lot.district === gisFilterDistrict.value);
      }
      if (gisOnlyEV.value) {
        list = list.filter((lot) => lot.has_ev);
      }

      // Quick filter
      if (gisFilterQuick.value === "near") {
        list = list.filter((lot) => (lot.distance_km || 99) <= 5.0);
      } else if (gisFilterQuick.value === "cheap") {
        list = list.filter(
          (lot) => (lot.dynamic_rate || lot.base_rate || 25000) <= 20000,
        );
      } else if (gisFilterQuick.value === "ev") {
        list = list.filter((lot) => lot.has_ev);
      } else if (gisFilterQuick.value === "available") {
        list = list.filter(
          (lot) => (lot.available_slots || 0) / (lot.total_slots || 1) >= 0.45,
        );
      } else if (gisFilterQuick.value === "roof") {
        list = list.filter((lot) => lot.has_roof);
      }

      if (gisSortBy.value === "nearest") {
        list.sort((a, b) => (a.distance_km || 0) - (b.distance_km || 0));
      } else if (gisSortBy.value === "available") {
        list.sort(
          (a, b) => (b.available_slots || 0) - (a.available_slots || 0),
        );
      } else if (gisSortBy.value === "cheapest" || gisSortBy.value === "rate") {
        list.sort(
          (a, b) =>
            (a.dynamic_rate || a.base_rate || 0) -
            (b.dynamic_rate || b.base_rate || 0),
        );
      }
      return list;
    });

    const totalCityAvailableSlots = computed(() =>
      cityLotsList.value.reduce(
        (sum, lot) => sum + (lot.available_slots || 0),
        0,
      ),
    );
    const totalCityCapacity = computed(() =>
      cityLotsList.value.reduce((sum, lot) => sum + (lot.total_slots || 0), 0),
    );
    const avgCityOccupancyRate = computed(() => {
      if (!totalCityCapacity.value) return 0;
      return Math.round(
        ((totalCityCapacity.value - totalCityAvailableSlots.value) /
          totalCityCapacity.value) *
          100,
      );
    });

    const updateGISMarkers = () => {
      if (!cityMapInstance || !window.L) return;
      Object.values(cityMarkersMap).forEach((marker) => marker.remove());
      cityMarkersMap = {};

      cityLotsList.value.forEach((lot) => {
        const ratio = (lot.available_slots || 0) / (lot.total_slots || 1);
        const color =
          ratio < 0.12 ? "#f43f5e" : ratio < 0.35 ? "#f59e0b" : "#10b981";
        const ringBg =
          ratio < 0.12
            ? "rgba(244,63,94,0.35)"
            : ratio < 0.35
              ? "rgba(245,158,11,0.35)"
              : "rgba(16,185,129,0.35)";

        const customHtml = `
          <div style="position:relative;display:flex;align-items:center;justify-content:center;width:44px;height:44px;cursor:pointer;">
            <div style="position:absolute;inset:2px;border-radius:50%;background:${ringBg};animation:ping 2s cubic-bezier(0,0,0.2,1) infinite;"></div>
            <div style="position:relative;background:#0f172a;border:2px solid ${color};color:${color};font-weight:900;font-size:11px;border-radius:12px;padding:3px 7px;box-shadow:0 4px 14px rgba(0,0,0,0.8);display:flex;align-items:center;gap:3px;font-family:monospace;">
              <span>🅿</span><span>${lot.available_slots}</span>
            </div>
          </div>
        `;

        const icon = window.L.divIcon({
          className: "city-lot-div-marker",
          html: customHtml,
          iconSize: [44, 44],
          iconAnchor: [22, 22],
        });

        const marker = window.L.marker([lot.latitude, lot.longitude], {
          icon,
        }).addTo(cityMapInstance);
        const popupContent = `
          <div style="color:#0f172a;font-family:sans-serif;padding:4px;min-width:180px;">
            <b style="font-size:13px;color:#0369a1;">${lot.name}</b>
            <div style="font-size:11px;color:#475569;margin-top:2px;">📍 ${lot.address || lot.district}</div>
            <div style="font-size:11px;font-weight:bold;color:${color};margin-top:4px;">
              Trống: ${lot.available_slots} / ${lot.total_slots} ô (${ratio < 0.12 ? "Hết chỗ" : ratio < 0.35 ? "Sắp đầy" : "Còn chỗ"})
            </div>
            <div style="font-size:11px;color:#1e293b;margin-top:2px;">
              Giá: <b>${(lot.dynamic_rate || lot.base_rate || 25000).toLocaleString("vi-VN")} đ/h</b>
            </div>
          </div>
        `;
        marker.bindPopup(popupContent);
        marker.on("click", () => {
          selectCityLot(lot);
        });

        cityMarkersMap[lot.id] = marker;
      });
    };

    const loadCityLotsNetwork = async () => {
      try {
        const data = await apiRequest("/api/lots/city-network");
        const lots = Array.isArray(data)
          ? data
          : data && data.lots
            ? data.lots
            : null;
        if (lots && lots.length > 0) {
          cityLotsList.value = lots;
          if (!selectedCityLot.value) {
            selectedCityLot.value = lots[0];
          }
          if (cityMapInstance) {
            updateGISMarkers();
          }
        }
      } catch (e) {
        console.warn("loadCityLotsNetwork fallback:", e);
      }
    };

    const initCityGISMap = () => {
      if (!window.L) return;
      const el = document.getElementById("gis-city-map");
      if (!el) return;

      if (cityMapInstance) {
        cityMapInstance.invalidateSize();
        return;
      }

      cityMapInstance = window.L.map("gis-city-map", {
        zoomControl: true,
        scrollWheelZoom: true,
      }).setView([20.985, 105.82], 11);

      window.L.tileLayer(
        "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        {
          attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
          subdomains: "abcd",
          maxZoom: 19,
        },
      ).addTo(cityMapInstance);

      const userDivIcon = window.L.divIcon({
        className: "gis-user-location-marker",
        html: `
          <div style="position:relative;width:30px;height:30px;display:flex;align-items:center;justify-content:center;">
            <div style="position:absolute;inset:0;background:rgba(6,182,212,0.4);border-radius:50%;animation:ping 1.5s cubic-bezier(0,0,0.2,1) infinite;"></div>
            <div style="position:relative;width:28px;height:28px;background:#06b6d4;border:2px solid #ffffff;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#0f172a;font-size:13px;font-weight:bold;box-shadow:0 0 14px rgba(6,182,212,0.9);">
              📍
            </div>
          </div>
        `,
        iconSize: [30, 30],
        iconAnchor: [15, 15],
      });

      cityUserMarker = window.L.marker([21.0305, 105.8528], {
        icon: userDivIcon,
      })
        .addTo(cityMapInstance)
        .bindPopup(
          `<div style="color:#0f172a;padding:4px;font-family:sans-serif;"><b style="color:#0891b2">Vị Trí Hiện Tại Của Bạn</b><br><span style="font-size:11px;color:#64748b">Tòa nhà Hàm Cá Mập, Quảng trường Đông Kinh Nghĩa Thục, Hoàn Kiếm</span></div>`,
        );

      updateGISMarkers();
    };

    const selectCityLot = (lot) => {
      selectedCityLot.value = lot;
      if (cityMapInstance) {
        cityMapInstance.flyTo([lot.latitude, lot.longitude], 14, {
          duration: 0.8,
        });
        if (cityMarkersMap[lot.id]) {
          cityMarkersMap[lot.id].openPopup();
        }
        if (routePolyline) {
          routePolyline.remove();
          routePolyline = null;
        }
        if (window.L) {
          routePolyline = window.L.polyline(
            [
              [21.0305, 105.8528],
              [lot.latitude, lot.longitude],
            ],
            {
              color: "#06b6d4",
              weight: 3.5,
              opacity: 0.85,
              dashArray: "6, 8",
            },
          ).addTo(cityMapInstance);
        }
      }
    };

    const locateUserOnGIS = () => {
      if (cityMapInstance) {
        cityMapInstance.flyTo([21.0305, 105.8528], 15, { duration: 1.0 });
        if (cityUserMarker) {
          cityUserMarker.openPopup();
        }
        if (routePolyline) {
          routePolyline.remove();
          routePolyline = null;
        }
        SoundFX.scan();
        addToast("Đã định vị vị trí người dùng (Hàm Cá Mập)", "info");
      }
    };

    const switchToLotGrid = (lot) => {
      if (!lot) return;
      const w = lot.grid_width || 8;
      const h = lot.grid_height || 6;
      const slots = [];
      const prefix = lot.name.includes("Tràng Tiền")
        ? "TT"
        : lot.name.includes("Mỹ Đình")
          ? "MĐ"
          : lot.name.includes("Smart City")
            ? "SC"
            : lot.name.includes("Duy Tân") || lot.name.includes("Cầu Giấy")
              ? "CG"
              : lot.name.includes("Bạch Mai")
                ? "BM"
                : lot.name.includes("Nguyễn Chí Thanh")
                  ? "NCT"
                  : lot.name.includes("Hoàng Thành")
                    ? "HT"
                    : lot.name.includes("Văn Quán")
                      ? "VQ"
                      : lot.name.includes("Nước Ngầm")
                        ? "NN"
                        : lot.name.includes("Nội Bài")
                          ? "NB"
                          : lot.name.includes("Lotte Mall")
                            ? "LM"
                            : lot.name.includes("Lotte Center") ||
                                lot.name.includes("Lotte")
                              ? "LT"
                              : lot.name.includes("Keangnam")
                                ? "KN"
                                : lot.name.includes("Đông Kinh")
                                  ? "DK"
                                  : lot.district === "Hà Đông" ||
                                      lot.name.includes("Hà Đông")
                                    ? "HĐ"
                                    : lot.district === "Thường Tín" ||
                                        lot.name.includes("Thường Tín")
                                      ? "T-TIN"
                                      : lot.name.includes("Tây Hồ")
                                        ? "TH"
                                        : lot.name.includes("Long Biên")
                                          ? "LB"
                                          : lot.name.includes("Royal City")
                                            ? "RC"
                                            : "A";

      for (let y = 0; y < h; y++) {
        for (let x = 0; x < w; x++) {
          const isObstacle =
            (x === Math.floor(w / 2) - 1 && y >= 1 && y <= h - 2) ||
            (x === 0 && y === 0);
          let status = "available";
          if (!isObstacle) {
            const occRatio =
              1 - (lot.available_slots || 20) / (lot.total_slots || 48);
            const rand = ((x * 17 + y * 11 + lot.name.length) % 100) / 100;
            if (rand < occRatio * 0.75) status = "occupied";
            else if (rand < occRatio) status = "booked";
          }
          slots.push({
            id: `slot-${lot.id}-${x}-${y}`,
            lot_id: lot.id,
            slot_code: isObstacle ? "OBSTACLE" : `${prefix}-${x + 1}0${y + 1}`,
            x,
            y,
            is_obstacle: isObstacle,
            status: isObstacle ? "obstacle" : status,
          });
        }
      }

      activeLot.value = {
        id: lot.id,
        name: lot.name,
        width: w,
        height: h,
        slots: slots,
        district: lot.district,
        base_rate: lot.base_rate,
        dynamic_rate: lot.dynamic_rate,
      };

      selectedSlot.value = null;
      navigationPath.value = [];
      updateStats();
      activeTab.value = "map";

      addToast(
        `Đã nạp sơ đồ ${lot.name} (${lot.district}) — ${w}×${h} ô`,
        "success",
      );
      SoundFX.success();

      nextTick(() => {
        if (window.gsap) {
          window.gsap.from(".slot-cell", {
            scale: 0.65,
            opacity: 0,
            duration: 0.45,
            stagger: {
              grid: [h, w],
              from: "center",
              amount: 0.45,
            },
            ease: "back.out(1.4)",
          });
        }
      });
    };

    const handleSelectLotFromDropdown = (lotId) => {
      const target = cityLotsList.value.find((l) => l.id === lotId);
      if (target) {
        switchToLotGrid(target);
      }
    };

    const handleAddCityLot = async () => {
      if (!newCityLotForm.name.trim()) return;
      const parts = newCityLotForm.coords
        .split(",")
        .map((s) => parseFloat(s.trim()));
      const lat = !isNaN(parts[0]) ? parts[0] : 21.0205;
      const lng = !isNaN(parts[1]) ? parts[1] : 105.7645;
      const w = Number(newCityLotForm.width) || 8;
      const h = Number(newCityLotForm.height) || 6;
      const total = w * h - 6;
      const available = Math.floor(total * 0.75);

      const payload = {
        id: `lot-hn-0${cityLotsList.value.length + 1}`,
        name: newCityLotForm.name.trim(),
        district: newCityLotForm.district,
        city: "Hà Nội",
        address: `${newCityLotForm.name}, ${newCityLotForm.district}, Hà Nội`,
        latitude: lat,
        longitude: lng,
        grid_width: w,
        grid_height: h,
        total_slots: total,
        available_slots: available,
        base_rate: Number(newCityLotForm.rate) || 25000,
        dynamic_rate: Number(newCityLotForm.rate) || 25000,
        has_ev: Boolean(newCityLotForm.has_ev),
        has_roof: Boolean(newCityLotForm.has_roof),
        distance_km: 4.5,
        travel_time_min: 15,
        tier_name: "Tiêu chuẩn (1.0x)",
      };

      try {
        await apiRequest("/api/lots", {
          method: "POST",
          body: JSON.stringify({
            name: payload.name,
            grid_width: payload.grid_width,
            grid_height: payload.grid_height,
            latitude: payload.latitude,
            longitude: payload.longitude,
            district: payload.district,
            city: payload.city,
            hourly_base_rate: payload.base_rate,
            has_ev_charging: payload.has_ev,
            has_roof: payload.has_roof,
          }),
        }).catch(() => null);
      } catch (e) {}

      cityLotsList.value.push(payload);
      selectedCityLot.value = payload;
      isAddCityLotModalOpen.value = false;

      newCityLotForm.name = "";
      newCityLotForm.rate = 25000;
      newCityLotForm.width = 8;
      newCityLotForm.height = 6;
      newCityLotForm.coords = "21.0205, 105.7645";

      addToast(
        `Đã thêm thành công bãi xe "${payload.name}" vào chuỗi đô thị!`,
        "success",
      );
      SoundFX.barrier();

      if (cityMapInstance) {
        updateGISMarkers();
        cityMapInstance.flyTo([lat, lng], 14);
      }
    };

    const resetGisFilters = () => {
      gisSearchQuery.value = "";
      gisFilterDistrict.value = "all";
      gisOnlyEV.value = false;
      gisSortBy.value = "nearest";
      gisFilterQuick.value = "all";
      if (routePolyline) {
        routePolyline.remove();
        routePolyline = null;
      }
    };

    watch(activeTab, async (val) => {
      if (val === "city-map") {
        await nextTick();
        initCityGISMap();
        setTimeout(() => {
          if (cityMapInstance) {
            cityMapInstance.invalidateSize();
          }
        }, 150);
      }
    });

    onMounted(() => {
      // Khôi phục phiên đăng nhập từ localStorage
      const savedUser = localStorage.getItem("sps_user");
      const savedToken = localStorage.getItem("sps_token");
      if (savedUser && savedToken) {
        try {
          currentUser.value = JSON.parse(savedUser);
        } catch (e) {
          localStorage.removeItem("sps_user");
        }
      }

      loadData();
      initWebSocket();
      loadIoTSensors();
      loadDynamicPricing();
      loadCityLotsNetwork();

      if (window.gsap) {
        gridCtx = window.gsap.context(() => {
          window.gsap.from(".slot-cell", {
            scale: 0.7,
            opacity: 0,
            duration: 0.45,
            stagger: {
              grid: [6, 8],
              from: "center",
              amount: 0.5,
            },
            ease: "back.out(1.4)",
          });
        });
      }
    });

    // Kích hoạt animation khi đăng nhập
    watch(currentUser, async (val) => {
      if (val) {
        await nextTick();
        if (window.gsap) {
          window.gsap.from(".slot-cell", {
            scale: 0.7,
            opacity: 0,
            duration: 0.45,
            stagger: {
              grid: [activeLot.value.height || 6, activeLot.value.width || 8],
              from: "center",
              amount: 0.5,
            },
            ease: "back.out(1.4)",
          });
        }
      }
    });

    onUnmounted(() => {
      if (carTimeline) carTimeline.kill();
      if (simulationTimer) clearInterval(simulationTimer);
      if (pingInterval) clearInterval(pingInterval);
      if (wsClient) wsClient.close();
      gridCtx?.revert();
      barrierCtx?.revert();
    });

    return {
      activeTab,
      isConnected,
      connectionStatusText,
      currentUser,
      userInitials,
      userRoleText,
      authTab,
      authLoading,
      authError,
      authForm,
      loginBtnText,
      registerBtnText,
      handleLogin,
      handleRegister,
      quickLoginDemo,
      handleLogout,
      activeLot,
      selectedSlot,
      navigationPath,
      pathStepCount,
      statusFilter,
      isBookingModalOpen,
      bookingsList,
      toasts,
      toastIcon,
      slotStatusText,
      stats,
      displayStats,
      gridRef,
      carRef,
      cellSize,
      barrierStatus,
      barrierStatusText,
      barrierPlate,
      forecastHour,
      forecastData,
      forecastRatePercent,
      animatedRate,
      filteredSlots,
      getSlotAt,
      isPathCell,
      getPathIndex,
      searchPlate,
      foundCarInfo,
      handleFindCar,
      isPaymentModalOpen,
      paymentTarget,
      openPayment,
      handlePaymentCompleted,
      isReceiptModalOpen,
      receiptTarget,
      openReceipt,
      adminSection,
      isAddPassModalOpen,
      newPassForm,
      pricingConfig,
      revenueStats,
      monthlyPasses,
      handleAddMonthlyPass,
      renewPass,
      deletePass,
      savePricing,
      toggleSlotMaintenance,
      exportRevenueCSV,
      printRevenueReport,
      barrierVehicleMonthlyPass,
      barrierVehicleIsMonthly,
      barrierVehicleBooking,
      barrierVehicleNeedsPayment,
      barrierVehicleStatusText,
      openPaymentForBarrier,
      handleSelectSlot,
      findNearestAvailableSlot,
      handleConfirmBooking,
      handleGoToBarrier,
      triggerBarrier,
      replayCarAnimation: () => runCarAnimation(navigationPath.value),
      wsConnected,
      wsLatency,
      wsMessageCount,
      emergencyAlert,
      closeEmergencyAlert: () => (emergencyAlert.value = null),
      isBroadcastModalOpen,
      broadcastForm,
      sendAdminBroadcast,
      iotSensors,
      iotLoading,
      iotFilter,
      filteredIoTSensors,
      iotOnlineCount,
      iotWarningCount,
      iotOccupiedCount,
      triggerSensorPing,
      triggerSensorToggle,
      isSimulatingTraffic,
      simulationSpeed,
      toggleTrafficSimulation,
      trafficLogs,
      clearTrafficLogs: () => (trafficLogs.value = []),
      // AI & Dynamic Pricing Engine
      currentDynamicPricing,
      dynamicPricing24h,
      aiRecommendations,
      mlModelInfo,
      isRetrainingML,
      loadDynamicPricing,
      handleRetrainModel,
      applyBestHourForBooking,
      // GIS Map & Chuỗi Bãi Đỗ Xe Đô Thị (Multi-Lot Network)
      cityLotsList,
      selectedCityLot,
      gisSearchQuery,
      gisFilterDistrict,
      gisOnlyEV,
      gisSortBy,
      gisFilterQuick,
      isAddCityLotModalOpen,
      newCityLotForm,
      filteredCityLots,
      totalCityAvailableSlots,
      totalCityCapacity,
      avgCityOccupancyRate,
      selectCityLot,
      locateUserOnGIS,
      switchToLotGrid,
      handleSelectLotFromDropdown,
      handleAddCityLot,
      resetGisFilters,
    };
  },
});

// Gắn component Modal Đặt chỗ vào App
app.component("booking-modal", {
  props: ["slot", "isOpen", "pricing"],
  emits: ["close", "confirm", "go-to-barrier"],
  data() {
    return {
      durationHours: 2,
      licensePlate: "51F-123.45",
      isSuccess: false,
      bookingResult: null,
    };
  },
  methods: {
    calculateFee() {
      const unitRate =
        this.pricing && this.pricing.final_rate
          ? this.pricing.final_rate
          : 25000;
      return this.durationHours * unitRate;
    },
    qrDataString() {
      if (!this.bookingResult) return "";
      const text = `[VE GUI XE THONG MINH]
Ma ve: ${this.bookingResult.code}
Vi tri: ${this.slot ? this.slot.slot_code : "A-101"} (Khu A)
Bien so xe: ${this.licensePlate}
Thoi gian do: ${this.durationHours} tieng
Tong cuoc: ${this.calculateFee().toLocaleString("vi-VN")} VND
Trang thai: Hop le - San sang vao bai`;
      return encodeURIComponent(text);
    },
    goToBarrier() {
      this.$emit("go-to-barrier", {
        plate: this.licensePlate,
        code: this.bookingResult ? this.bookingResult.code : "PARK-000000",
      });
      this.close();
    },
    confirm() {
      this.isSuccess = true;
      this.bookingResult = {
        code: "PARK-" + Math.floor(100000 + Math.random() * 900000),
        slot: this.slot.slot_code,
        licensePlate: this.licensePlate,
        fee: this.calculateFee(),
      };
      this.$emit("confirm", {
        slot_id: this.slot.id,
        duration: this.durationHours,
        plate: this.licensePlate,
      });
    },
    close() {
      this.isSuccess = false;
      this.$emit("close");
    },
  },
  template: `
    <div v-if="isOpen && slot" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm" @click.self="close">
      <div class="relative w-full max-w-md bg-slate-900 border border-slate-700 rounded-3xl p-6 shadow-2xl text-white">
        <button @click="close" class="absolute top-5 right-5 text-slate-400 hover:text-white text-xl">✕</button>
        
        <div v-if="!isSuccess">
          <div class="flex items-center gap-3 mb-5">
            <div class="w-12 h-12 rounded-2xl bg-cyan-500/20 border border-cyan-500/40 flex items-center justify-center text-cyan-400 font-bold text-lg font-mono">
              {{ slot.slot_code }}
            </div>
            <div>
              <h3 class="text-lg font-bold">Đặt Chỗ Đỗ Xe</h3>
              <p class="text-xs text-slate-400">Tọa độ: ({{ slot.x }}, {{ slot.y }}) | Khu A</p>
            </div>
          </div>

          <div class="space-y-4">
            <div>
              <label class="block text-xs font-semibold text-slate-300 mb-1.5">Biển số phương tiện</label>
              <input v-model="licensePlate" type="text" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-sm font-mono text-cyan-400 focus:outline-none focus:border-cyan-400">
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-300 mb-1.5">Thời gian đỗ dự kiến</label>
              <div class="grid grid-cols-4 gap-2">
                <button v-for="h in [1, 2, 4, 8]" :key="h" type="button" @click="durationHours = h"
                  class="py-2 rounded-xl text-xs font-semibold border transition-all"
                  :class="durationHours === h ? 'bg-cyan-500 text-slate-950 border-cyan-400 font-bold' : 'bg-slate-800 text-slate-300 border-slate-700'">
                  {{ h }} Tiếng
                </button>
              </div>
            </div>

            <!-- Khối Định Giá Động Realtime -->
            <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 flex justify-between items-center text-sm">
              <div>
                <span class="text-slate-400 text-xs block">Biểu phí định giá động:</span>
                <div class="flex items-center gap-1.5 mt-1" v-if="pricing">
                  <span class="text-[11px] px-2 py-0.5 rounded font-bold"
                    :class="{
                      'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30': pricing.tier === 'off_peak',
                      'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30': pricing.tier === 'normal',
                      'bg-amber-500/20 text-amber-400 border border-amber-500/30': pricing.tier === 'peak',
                      'bg-rose-500/20 text-rose-400 border border-rose-500/30': pricing.tier === 'surge'
                    }">
                    {{ pricing.tier_name }} ({{ Math.round(pricing.multiplier * 100) }}%)
                  </span>
                  <span class="text-xs text-slate-300 font-mono">{{ (pricing.final_rate || 25000).toLocaleString('vi-VN') }} đ/h</span>
                </div>
                <div v-else class="text-xs text-slate-400 font-mono">25.000 đ/h</div>
              </div>
              <div class="text-right">
                <span class="text-[10px] text-slate-400 uppercase tracking-wider block">Tổng cước</span>
                <span class="text-base font-bold text-emerald-400 font-mono">{{ calculateFee().toLocaleString('vi-VN') }} VNĐ</span>
              </div>
            </div>

            <div class="pt-2 flex gap-3">
              <button type="button" @click="close" class="flex-1 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-sm font-semibold">Hủy</button>
              <button type="button" @click="confirm" class="flex-1 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold rounded-xl text-sm shadow-lg shadow-cyan-500/30">Xác Nhận Đặt Chỗ</button>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-2">
          <div class="w-12 h-12 bg-emerald-500/20 border border-emerald-500/40 rounded-full flex items-center justify-center text-emerald-400 mx-auto mb-2 text-xl">✓</div>
          <h3 class="text-lg font-bold text-white mb-1">Đặt Chỗ Thành Công!</h3>
          <p class="text-xs text-slate-400 mb-3">Mã vé chuẩn chứa thông tin chi tiết (quét bằng camera điện thoại hoặc tại cổng)</p>

          <div class="bg-white p-3 rounded-2xl inline-block shadow-2xl mb-3 border border-slate-200">
            <img :src="'https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=' + qrDataString()" alt="QR Code" class="w-40 h-40 object-contain mx-auto" />
            <div class="text-slate-900 font-mono font-black text-sm mt-2 tracking-wider">{{ bookingResult.code }}</div>
            <div class="text-[10px] text-slate-500 font-medium mt-0.5">Ô: {{ slot.slot_code }} • {{ licensePlate }}</div>
          </div>

          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-left text-xs mb-4 space-y-1">
            <div class="flex justify-between"><span class="text-slate-400">Vị trí đỗ:</span><span class="font-bold text-cyan-400 font-mono">{{ slot.slot_code }} (Khu A)</span></div>
            <div class="flex justify-between"><span class="text-slate-400">Biển số xe:</span><span class="font-bold text-white font-mono">{{ licensePlate }}</span></div>
            <div class="flex justify-between"><span class="text-slate-400">Thời gian đỗ:</span><span class="font-bold text-slate-200">{{ durationHours }} Tiếng</span></div>
            <div class="flex justify-between" v-if="pricing"><span class="text-slate-400">Biểu giá:</span><span class="font-bold text-cyan-400 font-mono">{{ (pricing.final_rate || 25000).toLocaleString('vi-VN') }} đ/h ({{ pricing.tier_name }})</span></div>
            <div class="flex justify-between"><span class="text-slate-400">Tổng cước:</span><span class="font-bold text-emerald-400 font-mono">{{ calculateFee().toLocaleString('vi-VN') }} VNĐ</span></div>
          </div>

          <div class="flex gap-2">
            <button type="button" @click="goToBarrier" class="flex-1 py-2.5 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-bold rounded-xl text-xs shadow-lg shadow-emerald-500/20 transition-all flex items-center justify-center gap-1.5">
              <span>🚧</span> Check-in Barrier Ngay
            </button>
            <button type="button" @click="close" class="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-semibold">Đóng</button>
          </div>
        </div>
      </div>
    </div>
  `,
});

// Gắn component Modal Thanh Toán Đa Kênh (VietQR / MoMo / Tiền mặt)
app.component("payment-modal", {
  props: ["booking", "isOpen"],
  emits: ["close", "paid"],
  data() {
    return {
      paymentMethod: "vietqr",
      isSubmitting: false,
      bankAccount: "0988889999",
      bankName: "MB Bank (Quân Đội)",
      accountName: "CONG TY BAI XE THONG MINH",
      momoPhone: "0988 889 999",
    };
  },
  computed: {
    feeAmount() {
      return this.booking ? this.booking.fee || 25000 : 25000;
    },
    formattedFee() {
      return this.feeAmount.toLocaleString("vi-VN");
    },
    ticketCode() {
      return this.booking ? this.booking.id || "BK-00000" : "BK-00000";
    },
    vietQrUrl() {
      const code = this.ticketCode;
      const amount = this.feeAmount;
      return `https://img.vietqr.io/image/MB-0988889999-compact2.png?amount=${amount}&addInfo=THANH%20TOAN%20${code}&accountName=${encodeURIComponent(this.accountName)}`;
    },
    momoQrUrl() {
      const text = `2|99|0988889999|CONG TY BAI XE THONG MINH||0|0|${this.feeAmount}|THANH TOAN ${this.ticketCode}|transfer_myqr`;
      return `https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=${encodeURIComponent(text)}`;
    },
  },
  methods: {
    confirmPayment() {
      this.isSubmitting = true;
      setTimeout(() => {
        this.isSubmitting = false;
        const methodName =
          this.paymentMethod === "vietqr"
            ? "VietQR (MB Bank)"
            : this.paymentMethod === "momo"
              ? "Ví MoMo"
              : "Tiền mặt tại trạm";
        this.$emit("paid", {
          bookingId: this.ticketCode,
          plate: this.booking ? this.booking.plate : "",
          slot_code: this.booking ? this.booking.slot_code : "",
          amount: this.feeAmount,
          method: methodName,
        });
      }, 700);
    },
    close() {
      this.$emit("close");
    },
  },
  template: `
    <div v-if="isOpen && booking" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md" @click.self="close">
      <div class="relative w-full max-w-lg bg-slate-900 border border-slate-700 rounded-3xl p-6 sm:p-7 shadow-2xl text-white">
        <button @click="close" class="absolute top-5 right-5 text-slate-400 hover:text-white text-xl">✕</button>

        <div class="flex items-center gap-3 mb-5 border-b border-slate-800 pb-4">
          <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-emerald-500 to-teal-600 flex items-center justify-center text-slate-950 font-bold text-xl shadow-lg shadow-emerald-500/20">
            💳
          </div>
          <div>
            <h3 class="text-lg font-bold text-white">Cổng Thanh Toán Cước Đỗ Xe</h3>
            <p class="text-xs text-slate-400 font-mono">Vé: {{ ticketCode }} • Xe: {{ booking.plate }} • Ô: {{ booking.slot_code }}</p>
          </div>
        </div>

        <!-- Chọn Phương Thức Thanh Toán -->
        <div class="grid grid-cols-3 gap-2 mb-5">
          <button type="button" @click="paymentMethod = 'vietqr'"
            class="py-2.5 px-2 rounded-xl text-xs font-bold border transition-all flex flex-col items-center gap-1"
            :class="paymentMethod === 'vietqr' ? 'bg-cyan-500/20 border-cyan-400 text-cyan-300 shadow-md shadow-cyan-500/10' : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-white'">
            <span class="text-base">🏦</span>
            <span>VietQR Napas</span>
          </button>
          <button type="button" @click="paymentMethod = 'momo'"
            class="py-2.5 px-2 rounded-xl text-xs font-bold border transition-all flex flex-col items-center gap-1"
            :class="paymentMethod === 'momo' ? 'bg-pink-500/20 border-pink-400 text-pink-300 shadow-md shadow-pink-500/10' : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-white'">
            <span class="text-base">👛</span>
            <span>Ví MoMo</span>
          </button>
          <button type="button" @click="paymentMethod = 'cash'"
            class="py-2.5 px-2 rounded-xl text-xs font-bold border transition-all flex flex-col items-center gap-1"
            :class="paymentMethod === 'cash' ? 'bg-amber-500/20 border-amber-400 text-amber-300 shadow-md shadow-amber-500/10' : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-white'">
            <span class="text-base">💵</span>
            <span>Tiền Mặt</span>
          </button>
        </div>

        <!-- Tab 1: VietQR -->
        <div v-if="paymentMethod === 'vietqr'" class="space-y-4 text-center">
          <div class="bg-white p-3.5 rounded-2xl inline-block shadow-2xl border border-slate-200">
            <img :src="vietQrUrl" alt="VietQR Napas 247" class="w-48 h-48 object-contain mx-auto" />
            <div class="text-[11px] font-bold text-slate-900 mt-2 flex items-center justify-center gap-1">
              <span>Napas 247 • MB Bank</span>
            </div>
          </div>
          <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 text-left text-xs space-y-1.5 font-mono">
            <div class="flex justify-between"><span class="text-slate-500">Ngân hàng:</span><span class="text-white font-bold">{{ bankName }}</span></div>
            <div class="flex justify-between"><span class="text-slate-500">Số tài khoản:</span><span class="text-cyan-400 font-bold">{{ bankAccount }}</span></div>
            <div class="flex justify-between"><span class="text-slate-500">Chủ tài khoản:</span><span class="text-white">{{ accountName }}</span></div>
            <div class="flex justify-between"><span class="text-slate-500">Nội dung CK:</span><span class="text-amber-400 font-bold">THANH TOAN {{ ticketCode }}</span></div>
            <div class="flex justify-between border-t border-slate-800 pt-1.5"><span class="text-slate-400 font-sans">Số tiền cước:</span><span class="text-base text-emerald-400 font-bold">{{ formattedFee }} VNĐ</span></div>
          </div>
          <p class="text-[11px] text-slate-400">Dùng app bất kỳ ngân hàng nào (MB, VCB, Techcombank, VPBank...) để quét mã</p>
        </div>

        <!-- Tab 2: Ví MoMo -->
        <div v-if="paymentMethod === 'momo'" class="space-y-4 text-center">
          <div class="bg-white p-3.5 rounded-2xl inline-block shadow-2xl border border-pink-200">
            <img :src="momoQrUrl" alt="MoMo QR" class="w-44 h-44 object-contain mx-auto" />
            <div class="text-[11px] font-bold text-pink-600 mt-2">Ví Điện Tử MoMo</div>
          </div>
          <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 text-left text-xs space-y-1.5 font-mono">
            <div class="flex justify-between"><span class="text-slate-500">Số MoMo:</span><span class="text-pink-400 font-bold">{{ momoPhone }}</span></div>
            <div class="flex justify-between"><span class="text-slate-500">Người nhận:</span><span class="text-white">{{ accountName }}</span></div>
            <div class="flex justify-between"><span class="text-slate-500">Nội dung:</span><span class="text-amber-400 font-bold">THANH TOAN {{ ticketCode }}</span></div>
            <div class="flex justify-between border-t border-slate-800 pt-1.5"><span class="text-slate-400 font-sans">Số tiền:</span><span class="text-base text-emerald-400 font-bold">{{ formattedFee }} VNĐ</span></div>
          </div>
          <p class="text-[11px] text-slate-400">Mở ứng dụng MoMo quét mã để thanh toán tức thì</p>
        </div>

        <!-- Tab 3: Tiền Mặt -->
        <div v-if="paymentMethod === 'cash'" class="space-y-4 py-4 text-center">
          <div class="w-16 h-16 rounded-full bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-3xl mx-auto text-amber-400">
            💵
          </div>
          <div>
            <h4 class="text-base font-bold text-white">Thanh Toán Tiền Mặt Tại Trạm</h4>
            <p class="text-xs text-slate-400 mt-1 max-w-sm mx-auto">Vui lòng nộp số tiền trực tiếp cho nhân viên thu ngân tại quầy kiểm soát barrier.</p>
          </div>
          <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 max-w-sm mx-auto text-center font-mono">
            <span class="text-xs text-slate-500 block">Số tiền cần thu:</span>
            <span class="text-2xl font-black text-emerald-400">{{ formattedFee }} VNĐ</span>
          </div>
        </div>

        <!-- Nút hành động -->
        <div class="pt-4 mt-2 border-t border-slate-800 flex gap-3">
          <button type="button" @click="close" class="flex-1 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold">
            Hủy Bỏ
          </button>
          <button type="button" @click="confirmPayment" :disabled="isSubmitting"
            class="flex-2 py-3 px-5 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-bold rounded-xl text-xs shadow-lg shadow-emerald-500/20 transition-all flex items-center justify-center gap-2">
            <span v-if="isSubmitting">Đang xử lý...</span>
            <span v-else>✓ Xác Nhận Đã Thanh Toán</span>
          </button>
        </div>
      </div>
    </div>
  `,
});

// Gắn component Modal Hóa Đơn / Biên Lai Đỗ Xe Điện Tử
app.component("receipt-modal", {
  props: ["booking", "isOpen"],
  emits: ["close"],
  computed: {
    receiptId() {
      return this.booking
        ? "HD-" + this.booking.id.replace("BK-", "")
        : "HD-00000";
    },
    currentDate() {
      return new Date().toLocaleDateString("vi-VN");
    },
    currentTime() {
      return new Date().toLocaleTimeString("vi-VN", {
        hour: "2-digit",
        minute: "2-digit",
      });
    },
    subtotal() {
      if (!this.booking) return 0;
      return Math.round((this.booking.fee || 25000) / 1.08);
    },
    vatAmount() {
      if (!this.booking) return 0;
      return (this.booking.fee || 25000) - this.subtotal;
    },
    formattedFee() {
      return this.booking
        ? (this.booking.fee || 25000).toLocaleString("vi-VN")
        : "0";
    },
    formattedSubtotal() {
      return this.subtotal.toLocaleString("vi-VN");
    },
    formattedVat() {
      return this.vatAmount.toLocaleString("vi-VN");
    },
  },
  methods: {
    printReceipt() {
      window.print();
    },
    close() {
      this.$emit("close");
    },
  },
  template: `
    <div v-if="isOpen && booking" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md" @click.self="close">
      <div class="relative w-full max-w-md bg-white text-slate-900 rounded-3xl p-6 sm:p-8 shadow-2xl border border-slate-300">
        <button @click="close" class="absolute top-5 right-5 text-slate-400 hover:text-slate-800 text-xl print:hidden">✕</button>

        <!-- Header Hóa Đơn -->
        <div class="text-center border-b border-slate-200 pb-4 mb-4">
          <div class="text-[10px] font-bold uppercase tracking-wider text-slate-500">TRUNG TÂM BÃI ĐỖ XE THÔNG MINH</div>
          <h3 class="text-lg font-black text-slate-900 mt-0.5">BIÊN LAI THU CƯỚC ĐỖ XE</h3>
          <p class="text-[11px] text-slate-500 font-mono mt-0.5">Số HĐ: {{ receiptId }} • Ngày: {{ currentDate }}</p>
        </div>

        <!-- Chi tiết thông tin -->
        <div class="space-y-2 text-xs mb-5 font-mono">
          <div class="flex justify-between border-b border-slate-100 pb-1.5"><span class="text-slate-500">Mã vé xe:</span><span class="font-bold text-slate-900">{{ booking.id }}</span></div>
          <div class="flex justify-between border-b border-slate-100 pb-1.5"><span class="text-slate-500">Biển số xe:</span><span class="font-bold text-blue-600 text-sm">{{ booking.plate }}</span></div>
          <div class="flex justify-between border-b border-slate-100 pb-1.5"><span class="text-slate-500">Vị trí đỗ:</span><span class="font-bold text-slate-900">{{ booking.slot_code }} (Khu A)</span></div>
          <div class="flex justify-between border-b border-slate-100 pb-1.5"><span class="text-slate-500">Thời gian đỗ:</span><span class="text-slate-700">{{ booking.duration }} Tiếng</span></div>
          <div class="flex justify-between border-b border-slate-100 pb-1.5"><span class="text-slate-500">Phương thức:</span><span class="text-emerald-600 font-bold">{{ booking.paymentMethod || 'VietQR Napas' }}</span></div>
        </div>

        <!-- Bảng tính tiền -->
        <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-200 text-xs mb-5 space-y-1.5 font-mono">
          <div class="flex justify-between text-slate-500"><span>Tiền cước trước thuế:</span><span>{{ formattedSubtotal }} đ</span></div>
          <div class="flex justify-between text-slate-500"><span>Thuế GTGT (VAT 8%):</span><span>{{ formattedVat }} đ</span></div>
          <div class="flex justify-between border-t border-slate-300 pt-2 font-bold text-sm text-slate-900">
            <span>TỔNG THANH TOÁN:</span>
            <span class="text-emerald-600 text-base">{{ formattedFee }} VNĐ</span>
          </div>
        </div>

        <!-- Dấu mộc ĐÃ THANH TOÁN -->
        <div class="border-2 border-dashed border-emerald-500 rounded-xl p-2.5 text-center mb-6 bg-emerald-50/60">
          <span class="text-xs font-black text-emerald-700 tracking-widest uppercase">✓ ĐÃ THANH TOÁN THÀNH CÔNG</span>
          <p class="text-[9px] text-emerald-600 mt-0.5 font-mono">Giao dịch được xác thực tự động qua Smart Parking IoT</p>
        </div>

        <!-- Action buttons -->
        <div class="flex gap-3 print:hidden">
          <button type="button" @click="printReceipt"
            class="flex-1 py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-xl text-xs transition-colors flex items-center justify-center gap-1.5">
            <span>🖨️</span> In Hóa Đơn
          </button>
          <button type="button" @click="close"
            class="px-5 py-2.5 bg-slate-200 hover:bg-slate-300 text-slate-700 font-semibold rounded-xl text-xs transition-colors">
            Đóng
          </button>
        </div>
      </div>
    </div>
  `,
});

// Gắn component Modal Thanh Toán Đa Kênh (VietQR / MoMo / Tiền mặt)
// Bắt lỗi toàn cục
window.onerror = function (msg, url, line, col, error) {
  window.__last_error = {
    msg,
    url,
    line,
    col,
    error: error ? error.stack : null,
  };
  console.error("GLOBAL ERROR:", msg, "at line", line, col);
};

app.config.errorHandler = function (err, instance, info) {
  window.__vue_error = { message: err.message, stack: err.stack, info: info };
  console.error("VUE ERROR:", err, info);
};

// Chuẩn hóa và làm sạch template DOM (loại bỏ mọi ngắt dòng trong các biểu thức {{ ... }} trước khi Vue compile)
const appEl = document.getElementById("app");
if (appEl) {
  appEl.innerHTML = appEl.innerHTML.replace(
    /\{\{([\s\S]*?)\}\}/g,
    (match, expr) => {
      return "{{" + expr.replace(/\r?\n\s*/g, " ").trim() + "}}";
    },
  );
}

// Khởi tạo app
try {
  app.mount("#app");
  console.log("App mounted successfully!");
} catch (e) {
  window.__mount_error = { message: e.message, stack: e.stack };
  console.error("MOUNT ERROR:", e);
}
