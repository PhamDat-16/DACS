import re
from pathlib import Path

index_path = Path("frontend/index.html")
content = index_path.read_text(encoding="utf-8")

# ==============================================================================
# 1. UPDATE SIDEBAR FOR CUSTOMER (Lines around 590)
# ==============================================================================
old_guest_sidebar_regex = re.compile(
    r'<!-- GUEST MENU -->.*?<!-- Bottom Options -->',
    re.DOTALL
)

new_customer_and_guest_sidebar = '''<!-- CUSTOMER MENU (8 Màn hình chính) -->
          <template v-else-if="currentRole === 'customer'">
            <button
              @click="activeNav = 'cust-dashboard'"
              class="w-full flex items-center gap-3.5 px-4 py-3 rounded-2xl text-xs font-semibold transition"
              :class="activeNav === 'cust-dashboard' ? 'bg-[#10b981] text-white font-bold shadow-lg shadow-emerald-500/25' : 'hover:bg-slate-800/40 text-slate-400 hover:text-white'"
            >
              <i class="fa-solid fa-house text-sm w-4"></i>
              <span>Dashboard</span>
            </button>

            <button
              @click="activeNav = 'cust-find-parking'"
              class="w-full flex items-center gap-3.5 px-4 py-3 rounded-2xl text-xs font-semibold transition"
              :class="activeNav === 'cust-find-parking' ? 'bg-[#10b981] text-white font-bold shadow-lg shadow-emerald-500/25' : 'hover:bg-slate-800/40 text-slate-400 hover:text-white'"
            >
              <i class="fa-solid fa-square-parking text-sm w-4"></i>
              <span>Find Parking</span>
            </button>

            <button
              @click="activeNav = 'cust-bookings'"
              class="w-full flex items-center gap-3.5 px-4 py-3 rounded-2xl text-xs font-semibold transition"
              :class="activeNav === 'cust-bookings' ? 'bg-[#10b981] text-white font-bold shadow-lg shadow-emerald-500/25' : 'hover:bg-slate-800/40 text-slate-400 hover:text-white'"
            >
              <i class="fa-solid fa-calendar-check text-sm w-4"></i>
              <span>My Bookings</span>
            </button>

            <button
              @click="activeNav = 'cust-vehicles'"
              class="w-full flex items-center gap-3.5 px-4 py-3 rounded-2xl text-xs font-semibold transition"
              :class="activeNav === 'cust-vehicles' ? 'bg-[#10b981] text-white font-bold shadow-lg shadow-emerald-500/25' : 'hover:bg-slate-800/40 text-slate-400 hover:text-white'"
            >
              <i class="fa-solid fa-car text-sm w-4"></i>
              <span>My Vehicles</span>
            </button>

            <button
              @click="activeNav = 'cust-monthly-pass'"
              class="w-full flex items-center gap-3.5 px-4 py-3 rounded-2xl text-xs font-semibold transition"
              :class="activeNav === 'cust-monthly-pass' ? 'bg-[#10b981] text-white font-bold shadow-lg shadow-emerald-500/25' : 'hover:bg-slate-800/40 text-slate-400 hover:text-white'"
            >
              <i class="fa-solid fa-ticket text-sm w-4"></i>
              <span>Monthly Pass</span>
            </button>

            <button
              @click="activeNav = 'cust-history'"
              class="w-full flex items-center gap-3.5 px-4 py-3 rounded-2xl text-xs font-semibold transition"
              :class="activeNav === 'cust-history' ? 'bg-[#10b981] text-white font-bold shadow-lg shadow-emerald-500/25' : 'hover:bg-slate-800/40 text-slate-400 hover:text-white'"
            >
              <i class="fa-solid fa-clock-rotate-left text-sm w-4"></i>
              <span>Parking History</span>
            </button>

            <button
              @click="activeNav = 'cust-payments'"
              class="w-full flex items-center gap-3.5 px-4 py-3 rounded-2xl text-xs font-semibold transition"
              :class="activeNav === 'cust-payments' ? 'bg-[#10b981] text-white font-bold shadow-lg shadow-emerald-500/25' : 'hover:bg-slate-800/40 text-slate-400 hover:text-white'"
            >
              <i class="fa-solid fa-credit-card text-sm w-4"></i>
              <span>Payments</span>
            </button>

            <button
              @click="activeNav = 'cust-profile'"
              class="w-full flex items-center gap-3.5 px-4 py-3 rounded-2xl text-xs font-semibold transition"
              :class="activeNav === 'cust-profile' ? 'bg-[#10b981] text-white font-bold shadow-lg shadow-emerald-500/25' : 'hover:bg-slate-800/40 text-slate-400 hover:text-white'"
            >
              <i class="fa-solid fa-user-gear text-sm w-4"></i>
              <span>My Profile</span>
            </button>
          </template>

          <!-- GUEST MENU -->
          <template v-else>
            <button
              @click="activeNav = 'guest-home'"
              class="w-full flex items-center gap-3.5 px-4 py-3 rounded-2xl text-xs font-semibold transition"
              :class="activeNav === 'guest-home' ? 'bg-slate-800 text-white font-bold' : 'hover:bg-slate-800/40 text-slate-400 hover:text-white'"
            >
              <i class="fa-solid fa-house text-sm w-4"></i>
              <span>Home</span>
            </button>
            <button
              @click="activeNav = 'parking-map'"
              class="w-full flex items-center gap-3.5 px-4 py-3 rounded-2xl text-xs font-semibold transition"
              :class="activeNav === 'parking-map' ? 'bg-slate-800 text-white font-bold' : 'hover:bg-slate-800/40 text-slate-400 hover:text-white'"
            >
              <i class="fa-solid fa-chart-simple text-sm w-4"></i>
              <span>Parking Availability</span>
            </button>
          </template>
        </nav>
      </div>

      <!-- Bottom Options -->'''

content = old_guest_sidebar_regex.sub(lambda m: new_customer_and_guest_sidebar, content)

# Also update the bottom options so customer only sees Support & Sign Out (no SQL explorer)
old_bottom_options = '''<!-- Bottom Options -->
      <div class="pt-6 border-t border-slate-800/80 space-y-1">
        <a
          href="/db_viewer.html"
          target="_blank"
          class="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-xs text-cyan-400 hover:bg-slate-800/40 transition"
        >
          <i class="fa-solid fa-database w-4"></i>
          <span>SQL Explorer</span>
        </a>
        <button
          @click="handleLogout"
          class="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-xs text-slate-400 hover:text-rose-400 hover:bg-slate-800/40 transition"
        >
          <i class="fa-solid fa-arrow-right-from-bracket w-4"></i>
          <span>Sign Out</span>
        </button>
      </div>'''

new_bottom_options = '''<!-- Bottom Options -->
      <div class="pt-6 border-t border-slate-800/80 space-y-1">
        <button
          @click="showHelpModal = true"
          class="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-xs text-slate-300 hover:bg-slate-800/40 transition text-left cursor-pointer"
        >
          <i class="fa-solid fa-circle-question w-4 text-emerald-400"></i>
          <span>Help &amp; Support</span>
        </button>
        <a
          v-if="currentRole !== 'customer' && !guestMode"
          href="/db_viewer.html"
          target="_blank"
          class="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-xs text-cyan-400 hover:bg-slate-800/40 transition"
        >
          <i class="fa-solid fa-database w-4"></i>
          <span>SQL Explorer</span>
        </a>
        <button
          @click="handleLogout"
          class="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-xs text-slate-400 hover:text-rose-400 hover:bg-slate-800/40 transition cursor-pointer"
        >
          <i class="fa-solid fa-arrow-right-from-bracket w-4"></i>
          <span>Sign Out</span>
        </button>
      </div>'''

content = content.replace(old_bottom_options, new_bottom_options)

# ==============================================================================
# 2. ADD NOTIFICATION DROPDOWN TO HEADER
# ==============================================================================
old_bell_button = '''<!-- Notification Bell -->
          <button class="w-9 h-9 rounded-xl bg-slate-100 hover:bg-slate-200 flex items-center justify-center text-slate-600 relative transition">
            <i class="fa-regular fa-bell text-sm"></i>
            <span class="w-2 h-2 rounded-full bg-rose-500 absolute top-2 right-2 border-2 border-white"></span>
          </button>'''

new_bell_button = '''<!-- Notification Bell & Dropdown -->
          <div class="relative">
            <button
              @click="showNotifDropdown = !showNotifDropdown"
              class="w-9 h-9 rounded-xl bg-slate-100 hover:bg-slate-200 flex items-center justify-center text-slate-600 relative transition cursor-pointer"
            >
              <i class="fa-regular fa-bell text-sm"></i>
              <span class="w-2 h-2 rounded-full bg-rose-500 absolute top-2 right-2 border-2 border-white"></span>
            </button>
            <!-- Dropdown -->
            <div
              v-if="showNotifDropdown"
              class="absolute right-0 mt-2 w-80 bg-white rounded-2xl shadow-2xl border border-slate-100 z-50 p-4 space-y-3"
            >
              <div class="flex items-center justify-between border-b border-slate-100 pb-2">
                <span class="font-bold text-xs text-slate-900">Thông báo ({{ customerNotifications.length }})</span>
                <button @click="showNotifDropdown = false" class="text-xs text-slate-400 hover:text-slate-600 cursor-pointer">
                  <i class="fa-solid fa-xmark"></i>
                </button>
              </div>
              <div class="space-y-2 max-h-64 overflow-y-auto">
                <div
                  v-for="(n, idx) in customerNotifications"
                  :key="idx"
                  class="p-2.5 rounded-xl bg-slate-50 border border-slate-100 text-xs"
                >
                  <div class="font-semibold text-slate-800 flex items-center gap-1.5 mb-0.5">
                    <i :class="n.icon + ' text-emerald-500'"></i> {{ n.title }}
                  </div>
                  <div class="text-[11px] text-slate-500 leading-relaxed">{{ n.body }}</div>
                  <div class="text-[9px] text-slate-400 mt-1">{{ n.time }}</div>
                </div>
              </div>
            </div>
          </div>'''

content = content.replace(old_bell_button, new_bell_button)

index_path.write_text(content, encoding="utf-8")
print("Sidebar & Header updated successfully!")
