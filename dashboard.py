from flask import Flask, render_template_string
import psutil, platform, datetime

app = Flask(__name__)

# ----------------------- Helper Function -----------------------
def get_system_info():
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    battery = psutil.sensors_battery()
    ip = psutil.net_if_addrs()
    ip_address = next((addr.address for iface in ip.values() for addr in iface if addr.family == 2), "N/A")

    return {
        'os': platform.system() + " " + platform.release(),
        'processor': platform.processor(),
        'boot_time': boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        'uptime': str(uptime).split('.')[0],
        'network_sent': f"{psutil.net_io_counters().bytes_sent / (1024*1024):.2f} MB",
        'network_received': f"{psutil.net_io_counters().bytes_recv / (1024*1024):.2f} MB",
        'cpu_usage': psutil.cpu_percent(interval=1),
        'memory_usage': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'ip_address': ip_address,
        'battery': f"{battery.percent}%" if battery else "N/A"
    }

# ----------------------- Base CSS -----------------------
base_css = """
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');

body {
  margin: 0;
  font-family: 'Poppins', sans-serif;
  background: linear-gradient(135deg, #0a192f, #112240);
  color: #e6f1ff;
  min-height: 100vh;
  overflow-x: hidden;
}
.header {
  background: linear-gradient(90deg, #06102a, #0b1e3d);
  color: #ffffff;
  text-align: center;
  padding: 1rem;
  font-size: 1.5rem;
  font-weight: 550;
  letter-spacing: 1px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.6);
  text-transform: uppercase;
  position: sticky;
  top: 0;
  z-index: 10;
}
.main-content {
  padding: 3rem 8%;
  animation: fadeIn 0.8s ease-in-out;
}
.system-info {
  background: rgba(17, 34, 64, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem 2.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
  margin-bottom: 3rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(8px);
  position: relative;
  overflow: hidden;
}
.system-info::before {
  content: '';
  position: absolute;
  top: -2px; left: -2px; right: -2px; bottom: -2px;
  background: linear-gradient(45deg, #64ffda, #00b4d8, #64ffda);
  background-size: 400%;
  animation: glowingBorder 6s linear infinite;
  z-index: 0;
  border-radius: 16px;
  opacity: 0.08;
}
@keyframes glowingBorder {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.system-info h2 { color: #64ffda; margin-bottom: 1rem; font-weight: 600; position: relative; z-index: 1; }

.info-grid {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 2rem;
  position: relative;
  z-index: 1;
}
.info-section { flex: 1; min-width: 280px; }
.info-section h3 {
  color: #64ffda;
  font-size: 1.1rem;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  margin-bottom: 0.7rem;
  padding-bottom: 0.3rem;
}
.info-section p { margin: 0.3rem 0; color: #ccd6f6; line-height: 1.8; }
.info-section i { color: #64ffda; margin-right: 8px; }

.bar { background: rgba(255,255,255,0.1); border-radius: 6px; overflow: hidden; height: 8px; margin: 6px 0 12px; }
.bar div {
  background: linear-gradient(90deg, #64ffda, #0077b6);
  height: 100%; border-radius: 6px;
  transition: width 0.5s ease;
}

.last-updated { text-align: right; font-size: 0.9rem; color: #64ffda; margin-bottom: 1rem; position: relative; z-index: 1; }

.overview-links {
  display: flex; justify-content: center; flex-wrap: wrap; gap: 2rem; position: relative; z-index: 1;
}
.overview {
  text-align: center; padding: 2rem 1.5rem;
  background: linear-gradient(145deg, #0b1e3d, #132b52);
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0, 255, 255, 0.1);
  transition: all 0.3s ease;
  width: 280px;
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.overview:hover { transform: translateY(-8px) scale(1.03); box-shadow: 0 8px 25px rgba(0, 255, 255, 0.3); }
.overview img { width: 75px; height: 75px; margin-bottom: 0.8rem; filter: drop-shadow(0 0 6px #64ffda); }

.btn {
  background: #64ffda; color: #0a192f;
  padding: 0.7rem 1.5rem; border-radius: 8px;
  text-decoration: none; transition: all 0.3s ease;
  font-weight: 600; letter-spacing: 0.5px;
  box-shadow: 0 3px 10px rgba(100, 255, 218, 0.3);
}
.btn:hover { background: #5ce1c9; box-shadow: 0 5px 20px rgba(100, 255, 218, 0.4); transform: translateY(-3px); }
.back { display: inline-block; margin-top: 1.8rem; }

canvas {
  display: block;
  margin: 2rem auto;
  max-width: 280px;   /* 🔹 chart size reduced */
  max-height: 280px;  /* 🔹 chart size reduced */
}

@keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
</style>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
"""

# ----------------------- Home Page -----------------------
@app.route('/')
def home():
    info = get_system_info()
    return render_template_string(base_css + """
    <header class="header"><h1>System Monitoring Dashboard</h1></header>
    <main class="main-content">
      <section class="system-info">
        <div class="last-updated"><i class="fa-solid fa-rotate"></i> Last updated: {{ datetime }}</div>
        <h2>System Information</h2>
        <div class="info-grid">
          <div class="info-section">
            <h3>System</h3>
            <p><i class="fa-brands fa-windows"></i><strong>OS:</strong> {{ info.os }}</p>
            <p><i class="fa-solid fa-microchip"></i><strong>Processor:</strong> {{ info.processor }}</p>
            <p><i class="fa-solid fa-clock"></i><strong>Boot Time:</strong> {{ info.boot_time }}</p>
            <p><i class="fa-solid fa-hourglass-half"></i><strong>Uptime:</strong> {{ info.uptime }}</p>
            <p><i class="fa-solid fa-battery-half"></i><strong>Battery:</strong> {{ info.battery }}</p>
          </div>
          <div class="info-section">
            <h3>Performance</h3>
            <p><i class="fa-solid fa-microchip"></i><strong>CPU Usage:</strong> {{ info.cpu_usage }}%</p>
            <div class="bar"><div style="width: {{ info.cpu_usage }}%"></div></div>
            <p><i class="fa-solid fa-memory"></i><strong>Memory Usage:</strong> {{ info.memory_usage }}%</p>
            <div class="bar"><div style="width: {{ info.memory_usage }}%"></div></div>
            <p><i class="fa-solid fa-hdd"></i><strong>Disk Usage:</strong> {{ info.disk_usage }}%</p>
            <div class="bar"><div style="width: {{ info.disk_usage }}%"></div></div>
          </div>
          <div class="info-section">
            <h3>Network</h3>
            <p><i class="fa-solid fa-wifi"></i><strong>IP Address:</strong> {{ info.ip_address }}</p>
            <p><i class="fa-solid fa-arrow-up"></i><strong>Network Sent:</strong> {{ info.network_sent }}</p>
            <p><i class="fa-solid fa-arrow-down"></i><strong>Network Received:</strong> {{ info.network_received }}</p>
          </div>
        </div>
      </section>

      <div class="overview-links">
        <div class="overview">
          <img src="https://cdn-icons-png.flaticon.com/512/3003/3003988.png" alt="CPU">
          <h3>CPU Overview</h3>
          <a href="/cpu" class="btn">View Details</a>
        </div>
        <div class="overview">
          <img src="https://cdn-icons-png.flaticon.com/512/1048/1048945.png" alt="Memory">
          <h3>Memory Overview</h3>
          <a href="/memory" class="btn">View Details</a>
        </div>
        <div class="overview">
          <img src="https://cdn-icons-png.flaticon.com/512/2732/2732349.png" alt="Disk">
          <h3>Disk Overview</h3>
          <a href="/disk" class="btn">View Details</a>
        </div>
      </div>
    </main>
    """, info=info, datetime=datetime.datetime.now().strftime("%H:%M:%S"))

# ----------------------- CPU Page -----------------------
@app.route('/cpu')
def cpu():
    cpu_percent = psutil.cpu_percent(interval=1)
    cores = psutil.cpu_count(logical=False)
    logical_cores = psutil.cpu_count(logical=True)
    freq = psutil.cpu_freq()
    current_freq = round(freq.current, 2) if freq else "N/A"
    max_freq = round(freq.max, 2) if freq else "N/A"

    return render_template_string(base_css + """
    <header class="header"><h1>CPU Details</h1></header>
    <main class="main-content">
      <div style="display:flex; gap:2rem; flex-wrap:wrap;">
        <!-- Chart -->
        <div style="flex:1; min-width:280px; text-align:center;">
          <h2>CPU Usage: {{ cpu }}%</h2>
          <canvas id="cpuChart"></canvas>
        </div>

        <!-- Details -->
        <div style="flex:1; min-width:280px; background: rgba(17,34,64,0.9); padding:2rem; border-radius:16px; box-shadow:0 4px 20px rgba(0,0,0,0.4);">
          <h3 style="color:#64ffda; margin-bottom:1rem;">CPU Details</h3>
          <p style="margin:0.7rem 0;"><i class="fa-solid fa-microchip" style="margin-right:10px;"></i><strong>Cores:</strong> {{ cores }}</p>
          <p style="margin:0.7rem 0;"><i class="fa-solid fa-microchip" style="margin-right:10px;"></i><strong>Logical Cores:</strong> {{ logical_cores }}</p>
          <p style="margin:0.7rem 0;"><i class="fa-solid fa-tachometer-alt" style="margin-right:10px;"></i><strong>Current Frequency:</strong> {{ current_freq }} MHz</p>
          <p style="margin:0.7rem 0;"><i class="fa-solid fa-tachometer-alt" style="margin-right:10px;"></i><strong>Max Frequency:</strong> {{ max_freq }} MHz</p>
        </div>
      </div>
      <a href="/" class="btn back" style="margin-top:2rem; display:inline-block;">← Back to Home</a>

      <script>
        const ctx = document.getElementById('cpuChart');
        new Chart(ctx, {
          type: 'doughnut',
          data: { labels: ['Used','Free'], datasets: [{ data: [{{ cpu }}, {{ 100 - cpu }}],
            backgroundColor: ['#007bff','#cce6ff'], borderWidth:0 }]},
          options:{plugins:{legend:{position:'bottom'}}, cutout:'60%'}
        });
      </script>
    </main>
    """, cpu=cpu_percent, cores=cores, logical_cores=logical_cores, current_freq=current_freq, max_freq=max_freq)


# ----------------------- Memory Page -----------------------
@app.route('/memory')
def memory():
    mem = psutil.virtual_memory()
    used = round(mem.used / (1024**3), 2)
    total = round(mem.total / (1024**3), 2)
    free = round(mem.available / (1024**3), 2)
    swap = psutil.swap_memory()
    swap_used = round(swap.used / (1024**3), 2)
    swap_total = round(swap.total / (1024**3), 2)

    return render_template_string(base_css + """
    <header class="header"><h1>Memory Details</h1></header>
    <main class="main-content">
      <div style="display:flex; gap:2rem; flex-wrap:wrap;">
        <!-- Chart -->
        <div style="flex:1; min-width:280px; text-align:center;">
          <h2>Memory Used: {{ used }} GB / {{ total }} GB</h2>
          <canvas id="memChart"></canvas>
        </div>

        <!-- Details -->
        <div style="flex:1; min-width:280px; background: rgba(17,34,64,0.9); padding:2rem; border-radius:16px; box-shadow:0 4px 20px rgba(0,0,0,0.4);">
          <h3 style="color:#64ffda; margin-bottom:1rem;">Memory Details</h3>
          <p style="margin:0.7rem 0;"><i class="fa-solid fa-memory" style="margin-right:10px;"></i><strong>Total Memory:</strong> {{ total }} GB</p>
          <p style="margin:0.7rem 0;"><i class="fa-solid fa-memory" style="margin-right:10px;"></i><strong>Used Memory:</strong> {{ used }} GB</p>
          <p style="margin:0.7rem 0;"><i class="fa-solid fa-memory" style="margin-right:10px;"></i><strong>Free Memory:</strong> {{ free }} GB</p>
          <p style="margin:0.7rem 0;"><i class="fa-solid fa-exchange-alt" style="margin-right:10px;"></i><strong>Swap Used:</strong> {{ swap_used }} GB / {{ swap_total }} GB</p>
        </div>
      </div>
      <a href="/" class="btn back" style="margin-top:2rem; display:inline-block;">← Back to Home</a>

      <script>
        const memCtx = document.getElementById('memChart');
        new Chart(memCtx, {
          type: 'doughnut',
          data: { labels:['Used','Free'], datasets:[{data:[{{ mem.percent }}, {{ 100 - mem.percent }}],
          backgroundColor:['#28a745','#d4edda'], borderWidth:0}]},
          options:{plugins:{legend:{position:'bottom'}}, cutout:'60%'}
        });
      </script>
    </main>
    """, mem=mem, used=used, total=total, free=free, swap_used=swap_used, swap_total=swap_total)


# ----------------------- Disk Page -----------------------
@app.route('/disk')
def disk():
    disk = psutil.disk_usage('/')
    used = round(disk.used / (1024**3), 2)
    total = round(disk.total / (1024**3), 2)
    free = round(disk.free / (1024**3), 2)

    return render_template_string(base_css + """
    <header class="header"><h1>Disk Details</h1></header>
    <main class="main-content">
      <div style="display:flex; gap:2rem; flex-wrap:wrap;">
        <!-- Chart -->
        <div style="flex:1; min-width:280px; text-align:center;">
          <h2>Disk Used: {{ used }} GB / {{ total }} GB</h2>
          <canvas id="diskChart"></canvas>
        </div>

        <!-- Details -->
        <div style="flex:1; min-width:280px; background: rgba(17,34,64,0.9); padding:2rem; border-radius:16px; box-shadow:0 4px 20px rgba(0,0,0,0.4);">
          <h3 style="color:#64ffda; margin-bottom:1rem;">Disk Details</h3>
          <p style="margin:0.7rem 0;"><i class="fa-solid fa-hdd" style="margin-right:10px;"></i><strong>Total Disk:</strong> {{ total }} GB</p>
          <p style="margin:0.7rem 0;"><i class="fa-solid fa-hdd" style="margin-right:10px;"></i><strong>Used Disk:</strong> {{ used }} GB</p>
          <p style="margin:0.7rem 0;"><i class="fa-solid fa-hdd" style="margin-right:10px;"></i><strong>Free Disk:</strong> {{ free }} GB</p>
          <p style="margin:0.7rem 0;"><i class="fa-solid fa-folder-open" style="margin-right:10px;"></i><strong>Usage Percent:</strong> {{ disk.percent }}%</p>
        </div>
      </div>
      <a href="/" class="btn back" style="margin-top:2rem; display:inline-block;">← Back to Home</a>

      <script>
        const diskCtx = document.getElementById('diskChart');
        new Chart(diskCtx, {
          type:'doughnut',
          data:{labels:['Used','Free'],datasets:[{data:[{{ disk.percent }},{{ 100 - disk.percent }}],
          backgroundColor:['#ffc107','#fff3cd'],borderWidth:0}]},
          options:{plugins:{legend:{position:'bottom'}}, cutout:'60%'}
        });
      </script>
    </main>
    """, disk=disk, used=used, total=total, free=free)

# ----------------------- Run App -----------------------
if __name__ == '__main__':
    app.run(debug=True)
