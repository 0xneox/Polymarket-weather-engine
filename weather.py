import requests
import time
import threading
from datetime import datetime
import tkinter as tk

# Coordinates Configuration
LKO_LAT, LKO_LON = 26.85, 80.95
SEL_LAT, SEL_LON = 37.469, 126.451  # Incheon Intl Airport Station Area
HKG_LAT, HKG_LON = 22.302, 114.174  # Hong Kong Observatory Hill (Kowloon)

LKO_TZ = "Asia/Kolkata"
SEL_TZ = "Asia/Seoul"
HKG_TZ = "Asia/Hong_Kong"

class WeatherWidgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Global Weather Alpha Terminal")
        self.root.geometry("500x850")
        self.root.resizable(False, False)
        self.root.configure(bg="#11111b")
        self.root.attributes("-topmost", True)
        
        self.last_temps = {"lko": None, "sel": None, "hkg": None}
        self.last_times = {"lko": None, "sel": None, "hkg": None}
        
        # EXACT POLYMARKET MATCHED LADDERS
        self.lko_brackets = [39, 40, 41, 42, 43]
        self.sel_brackets = [25, 26, 27, 28, 29] 
        self.hkg_brackets = [29, 30, 31, 32, 33]
        
        self.setup_ui()
        
        self.running = True
        self.worker_thread = threading.Thread(target=self.background_loop, daemon=True)
        self.worker_thread.start()
        
    def setup_ui(self):
        tk.Label(self.root, text="⚡ TRIPLE-ZONE WEATHER ORDER ENGINE", font=("Arial", 11, "bold"), fg="#cba6f7", bg="#11111b").pack(pady=(12, 2))
        self.lbl_timestamp = tk.Label(self.root, text="Initializing Pipeline...", font=("Arial", 8), fg="#a6adc8", bg="#11111b")
        self.lbl_timestamp.pack(pady=(0, 6))
        
        stats_frame = tk.Frame(self.root, bg="#1e1e2e")
        stats_frame.pack(fill="x", padx=15, pady=5)
        
        # LKO View
        self.lbl_lko_current = tk.Label(stats_frame, text="📍 LKO AIRPORT: --°C", font=("Arial", 10, "bold"), fg="#89b4fa", bg="#1e1e2e")
        self.lbl_lko_current.pack(anchor="w", padx=12, pady=(6, 1))
        self.lbl_lko_vector = tk.Label(stats_frame, text="🚀 VECTOR: --°C/hr", font=("Arial", 8, "bold"), fg="#a6e3a1", bg="#1e1e2e")
        self.lbl_lko_vector.pack(anchor="w", padx=12, pady=(0, 4))
        
        # SEL View
        self.lbl_sel_current = tk.Label(stats_frame, text="📍 SEOUL INCHEON: --°C", font=("Arial", 10, "bold"), fg="#b4befe", bg="#1e1e2e")
        self.lbl_sel_current.pack(anchor="w", padx=12, pady=(2, 1))
        self.lbl_sel_vector = tk.Label(stats_frame, text="🚀 VECTOR: --°C/hr", font=("Arial", 8, "bold"), fg="#a6e3a1", bg="#1e1e2e")
        self.lbl_sel_vector.pack(anchor="w", padx=12, pady=(0, 4))

        # HKG View
        self.lbl_hkg_current = tk.Label(stats_frame, text="📍 HK OBSERVATORY: --°C", font=("Arial", 10, "bold"), fg="#f5e0dc", bg="#1e1e2e")
        self.lbl_hkg_current.pack(anchor="w", padx=12, pady=(2, 1))
        self.lbl_hkg_vector = tk.Label(stats_frame, text="🚀 VECTOR: --°C/hr", font=("Arial", 8, "bold"), fg="#a6e3a1", bg="#1e1e2e")
        self.lbl_hkg_vector.pack(anchor="w", padx=12, pady=(0, 6))
        
        tk.Label(self.root, text="📊 REAL-TIME ORDER SIGNALS", font=("Arial", 9, "bold"), fg="#f5e0dc", bg="#11111b").pack(anchor="w", padx=15, pady=(8, 2))
        
        # Matrix Output Area
        self.txt_matrix = tk.Text(self.root, font=("Consolas", 9, "bold"), fg="#cdd6f4", bg="#181825", bd=0, padx=12, pady=10, wrap="word")
        self.txt_matrix.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.txt_matrix.tag_config("buy_yes", foreground="#a6e3a1")   
        self.txt_matrix.tag_config("buy_no", foreground="#89b4fa")    
        self.txt_matrix.tag_config("sell_yes", foreground="#f38ba8")   
        self.txt_matrix.tag_config("scalping", foreground="#f9e2af")   
        self.txt_matrix.tag_config("neutral", foreground="#6c7086")    
        self.txt_matrix.tag_config("section", foreground="#cba6f7")    

        self.txt_matrix.config(state="disabled")

    def fetch_zone_data(self, lat, lon, tz):
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m&daily=temperature_2m_max&timezone={tz}&forecast_days=3"
            res = requests.get(url, timeout=10)
            return res.json() if res.status_code == 200 else None
        except: return None

    def calculate_vector(self, key, current_val, timestamp):
        velocity = 0.0
        if self.last_temps[key] is not None and self.last_times[key] is not None:
            t_delta = (timestamp - self.last_times[key]).total_seconds() / 3600.0
            if t_delta > 0: 
                velocity = (current_val - self.last_temps[key]) / t_delta
        self.last_temps[key], self.last_times[key] = current_val, timestamp
        return velocity

    def background_loop(self):
        while self.running:
            lko_data = self.fetch_zone_data(LKO_LAT, LKO_LON, LKO_TZ)
            sel_data = self.fetch_zone_data(SEL_LAT, SEL_LON, SEL_TZ)
            hkg_data = self.fetch_zone_data(HKG_LAT, HKG_LON, HKG_TZ)
            
            now = datetime.now()
            payload = {'now': now, 'lko': None, 'sel': None, 'hkg': None}
            
            if lko_data:
                curr = lko_data['current']['temperature_2m']
                vel = self.calculate_vector('lko', curr, now)
                payload['lko'] = (curr, lko_data['current']['relative_humidity_2m'], lko_data['daily']['temperature_2m_max'][0], lko_data['daily']['temperature_2m_max'][1], vel)
                
            if sel_data:
                curr = sel_data['current']['temperature_2m']
                vel = self.calculate_vector('sel', curr, now)
                payload['sel'] = (curr, sel_data['current']['relative_humidity_2m'], sel_data['daily']['temperature_2m_max'][0], sel_data['daily']['temperature_2m_max'][1], vel)
                
            if hkg_data:
                curr = hkg_data['current']['temperature_2m']
                vel = self.calculate_vector('hkg', curr, now)
                payload['hkg'] = (curr, hkg_data['current']['relative_humidity_2m'], hkg_data['daily']['temperature_2m_max'][0], hkg_data['daily']['temperature_2m_max'][1], hkg_data['daily']['temperature_2m_max'][2], vel)

            if lko_data or sel_data or hkg_data:
                self.root.after(0, self.update_display, payload)
                
            time.sleep(900)

    def update_display(self, payload):
        now = payload['now']
        self.lbl_timestamp.config(text=f"Sync: {now.strftime('%H:%M:%S')}")
        
        self.txt_matrix.config(state="normal")
        self.txt_matrix.delete("1.0", tk.END)
        
        # ----------------------------------------------------
        # ZONE 1: LUCKNOW AREA (IST)
        # ----------------------------------------------------
        if payload['lko']:
            curr, hum, t_max, tom_max, vel = payload['lko']
            sign = "+" if vel >= 0 else ""
            self.lbl_lko_current.config(text=f"📍 LKO AIRPORT: {curr}°C ({hum}%)")
            self.lbl_lko_vector.config(text=f"🚀 VECTOR: {sign}{vel:.2f}°C / hr", fg="#a6e3a1" if vel >= 0 else "#f38ba8")
            
            self.txt_matrix.insert(tk.END, "--- LUCKNOW TODAY ---\n", "section")
            lko_time_float = now.hour + (now.minute / 60.0)
            is_lko_peak = 12.5 <= lko_time_float < 15.0
            
            for target in self.lko_brackets:
                dist = target - curr
                
                # Case 1: Target was successfully reached or passed
                if curr >= target or t_max >= target:
                    self.txt_matrix.insert(tk.END, f"[-] {target}°C -> OUT: Reached\n", "neutral")
                
                # Case 2: Time window has expired, target was NOT reached
                elif lko_time_float >= 15.0:
                    self.txt_matrix.insert(tk.END, f"[🚫] {target}°C -> CLOSED: Unreached\n", "neutral")
                
                # Case 3: We are inside the active peak market hours
                elif is_lko_peak:
                    if dist <= 0.6 and vel >= 0.2: 
                        self.txt_matrix.insert(tk.END, f"[⚡] {target}°C -> BUY YES\n", "buy_yes")
                    elif dist <= 0.3 and vel <= 0.05: 
                        self.txt_matrix.insert(tk.END, f"[🔄] {target}°C -> SCALP SPREAD\n", "scalping")
                    elif dist > 0.8 or vel <= -0.05: 
                        self.txt_matrix.insert(tk.END, f"[🛑] {target}°C -> BUY NO / SELL YES\n", "buy_no")
                    else: 
                        self.txt_matrix.insert(tk.END, f"[⏳] {target}°C -> HOLD / MONITOR\n", "scalping")
                
                # Case 4: Early morning / pre-market state
                else:
                    self.txt_matrix.insert(tk.END, f"[•] {target}°C -> NEUTRAL\n", "neutral")
                    
            # RESTORED: Tomorrow Predictive Logic
            self.txt_matrix.insert(tk.END, "🔮 LKO TOMORROW STRATEGY:\n", "section")
            for target in self.lko_brackets:
                if tom_max >= target + 0.5: 
                    self.txt_matrix.insert(tk.END, f"[🟢] {target}°C -> BUY YES TONIGHT\n", "buy_yes")
                elif tom_max < target - 0.5: 
                    self.txt_matrix.insert(tk.END, f"[🔵] {target}°C -> BUY NO TONIGHT\n", "buy_no")
                else: 
                    self.txt_matrix.insert(tk.END, f"[•] {target}°C -> HOLD OFF\n", "neutral")

        # --- SINGLE CLEAR SEPARATOR BETWEEN LKO AND SEL ---
        if payload['lko'] and payload['sel']:
            self.txt_matrix.insert(tk.END, "\n" + "="*34 + "\n\n")

        # ----------------------------------------------------
        # ZONE 2: SEOUL INCHEON INTL AIRPORT (KST)
        # ----------------------------------------------------
        if payload['sel']:
            curr, hum, t_max, tom_max, vel = payload['sel']
            sign = "+" if vel >= 0 else ""
            self.lbl_sel_current.config(text=f"📍 SEOUL INCHEON: {curr}°C ({hum}%)")
            self.lbl_sel_vector.config(text=f"🚀 VECTOR: {sign}{vel:.2f}°C / hr", fg="#a6e3a1" if vel >= 0 else "#f38ba8")
            
            self.txt_matrix.insert(tk.END, "--- SEOUL TODAY (Closed) ---\n", "section")
            for target in self.sel_brackets:
                if curr >= target or t_max >= target: self.txt_matrix.insert(tk.END, f"[-] {target}°C -> OUT: Reached\n", "neutral")
                else: self.txt_matrix.insert(tk.END, f"[❌] {target}°C -> BUY NO\n", "buy_no")
                    
            self.txt_matrix.insert(tk.END, "🔮 SEOUL TOMORROW HIGH-PROBABILITY LADDER:\n", "section")
            for target in self.sel_brackets:
                if 27 <= target <= 29:
                    if target == 28: self.txt_matrix.insert(tk.END, f"[🟢] {target}°C -> BUY YES TONIGHT (Apex Target)\n", "buy_yes")
                    else: self.txt_matrix.insert(tk.END, f"[🔄] {target}°C -> BUY YES / HEDGE SPREAD\n", "scalping")
                elif tom_max >= target + 2.0 or target < 27:
                    self.txt_matrix.insert(tk.END, f"[🔵] {target}°C -> BUY NO TONIGHT (Under-target out)\n", "buy_no")
                else:
                    self.txt_matrix.insert(tk.END, f"[•] {target}°C -> HOLD OFF\n", "neutral")

        if payload['sel'] and payload['hkg']:
            self.txt_matrix.insert(tk.END, "\n" + "="*34 + "\n\n")

        # ----------------------------------------------------
        # ZONE 3: HONG KONG OBSERVATORY (HKT)
        # ----------------------------------------------------
        if payload['hkg']:
            curr, hum, t_max, jun28_max, jun29_max, vel = payload['hkg']
            sign = "+" if vel >= 0 else ""
            self.lbl_hkg_current.config(text=f"📍 HK OBSERVATORY: {curr}°C ({hum}%)")
            self.lbl_hkg_vector.config(text=f"🚀 VECTOR: {sign}{vel:.2f}°C / hr", fg="#a6e3a1" if vel >= 0 else "#f38ba8")
            
            self.txt_matrix.insert(tk.END, "--- HONG KONG JUN 28 LADDER ---\n", "section")
            for target in self.hkg_brackets:
                if target in [30, 31]:
                    if abs(jun28_max - target) <= 0.7:
                        self.txt_matrix.insert(tk.END, f"[🟢] {target}°C -> BUY YES (High Probability Cluster)\n", "buy_yes")
                    else:
                        self.txt_matrix.insert(tk.END, f"[🔄] {target}°C -> RISK ACCUMULATE / SPREAD\n", "scalping")
                elif target <= 28 or target >= 33:
                    self.txt_matrix.insert(tk.END, f"[🔵] {target}°C -> BUY NO (Statistical Improbability)\n", "buy_no")
                else:
                    self.txt_matrix.insert(tk.END, f"[•] {target}°C -> HOLD / LEAVE OPEN\n", "neutral")
            
            self.txt_matrix.insert(tk.END, "\n🔮 HONG KONG JUN 29 STRATEGY:\n", "section")
            for target in self.hkg_brackets:
                if target in [30, 31, 32]:
                    if abs(jun29_max - target) <= 0.5:
                        self.txt_matrix.insert(tk.END, f"[⚡] {target}°C -> ACCUMULATE YES TONIGHT\n", "buy_yes")
                    else:
                        self.txt_matrix.insert(tk.END, f"[⏳] {target}°C -> MONITOR SPREAD VOL\n", "scalping")
                elif target <= 28:
                    self.txt_matrix.insert(tk.END, f"[🔵] {target}°C -> BUY NO (Clear Skew Out)\n", "buy_no")
                else:
                    self.txt_matrix.insert(tk.END, f"[•] {target}°C -> NEUTRAL STRAT\n", "neutral")

        self.txt_matrix.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherWidgetApp(root)
    root.mainloop()
