import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from statsmodels.tsa.arima.model import ARIMA

# Global dataset
data = None

# ------------------ FUNCTIONS ------------------ #
def load_data():
    global data
    try:
        file_path = filedialog.askopenfilename(
            title="Select Pollution Dataset",
            filetypes=[("CSV files", ".csv"), ("All files", ".*")]
        )
        if not file_path:
            return
        data = pd.read_csv(file_path, parse_dates=["timestamp"])
        messagebox.showinfo("Success", f"Dataset loaded: {file_path}")
        # Populate city dropdown
        city_combo["values"] = sorted(data["city"].unique())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load dataset: {e}")

# ---------- AVG POLLUTANT ---------- #
def avg_pollutant_graph():
    if data is None:
        messagebox.showerror("Error", "No data loaded")
        return
    try:
        city = city_var.get()
        pollutant = pollutant_var.get()
        df = data[data["city"] == city].copy()
        df["date"] = pd.to_datetime(df["timestamp"]).dt.date
        avg_df = df.groupby("date")[pollutant].mean()

        plt.figure(figsize=(8, 4))
        avg_df.plot(marker="o")
        plt.title(f"Avg {pollutant.upper()} per Day in {city}")
        plt.xlabel("Date")
        plt.ylabel(f"{pollutant.upper()} Levels")
        plt.grid(True)
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {e}")

def avg_pollutant_values():
    if data is None:
        messagebox.showerror("Error", "No data loaded")
        return
    try:
        city = city_var.get()
        pollutant = pollutant_var.get()
        df = data[data["city"] == city].copy()
        df["date"] = pd.to_datetime(df["timestamp"]).dt.date
        avg_df = df.groupby("date")[pollutant].mean().round(2)
        messagebox.showinfo("Avg Values", avg_df.to_string())
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {e}")

# ---------- PEAK HOURS ---------- #
def peak_hours_graph():
    if data is None:
        messagebox.showerror("Error", "No data loaded")
        return
    try:
        city = city_var.get()
        pollutant = pollutant_var.get()
        df = data[data["city"] == city].copy()
        df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
        avg_df = df.groupby("hour")[pollutant].mean()

        plt.figure(figsize=(8, 4))
        avg_df.plot(kind="bar", color="orange")
        plt.title(f"Peak Hours of {pollutant.upper()} in {city}")
        plt.xlabel("Hour of Day")
        plt.ylabel(f"{pollutant.upper()} Levels")
        plt.grid(True)
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {e}")

def peak_hours_values():
    if data is None:
        messagebox.showerror("Error", "No data loaded")
        return
    try:
        city = city_var.get()
        pollutant = pollutant_var.get()
        df = data[data["city"] == city].copy()
        df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
        avg_df = df.groupby("hour")[pollutant].mean().round(2)
        messagebox.showinfo("Peak Hours Values", avg_df.to_string())
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {e}")

# ---------- COMPARE REGIONS ---------- #
def compare_regions_graph():
    if data is None:
        messagebox.showerror("Error", "No data loaded")
        return
    try:
        pollutant = pollutant_var.get()
        avg_df = data.groupby("city")[pollutant].mean().sort_values()

        plt.figure(figsize=(8, 4))
        avg_df.plot(kind="bar", color="green")
        plt.title(f"Average {pollutant.upper()} Across Cities")
        plt.xlabel("City")
        plt.ylabel(f"{pollutant.upper()} Levels")
        plt.grid(True)
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {e}")

def compare_regions_values():
    if data is None:
        messagebox.showerror("Error", "No data loaded")
        return
    try:
        pollutant = pollutant_var.get()
        avg_df = data.groupby("city")[pollutant].mean().round(2).sort_values()
        messagebox.showinfo("Compare Regions", avg_df.to_string())
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {e}")

# ---------- FORECAST ---------- #
def forecast_graph():
    if data is None:
        messagebox.showerror("Error", "No data loaded")
        return
    try:
        city = city_var.get()
        pollutant = pollutant_var.get()
        df = data[data["city"] == city].copy()
        df["date"] = pd.to_datetime(df["timestamp"]).dt.date
        ts = df.groupby("date")[pollutant].mean()

        model = ARIMA(ts, order=(2, 1, 2))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=7)

        plt.figure(figsize=(8, 4))
        ts.plot(label="Historical")
        forecast.plot(label="Forecast", color="red")
        plt.title(f"Forecast {pollutant.upper()} for {city} (Next 7 Days)")
        plt.xlabel("Date")
        plt.ylabel(f"{pollutant.upper()} Levels")
        plt.legend()
        plt.grid(True)
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {e}")

def forecast_values():
    if data is None:
        messagebox.showerror("Error", "No data loaded")
        return
    try:
        city = city_var.get()
        pollutant = pollutant_var.get()
        df = data[data["city"] == city].copy()
        df["date"] = pd.to_datetime(df["timestamp"]).dt.date
        ts = df.groupby("date")[pollutant].mean()

        model = ARIMA(ts, order=(2, 1, 2))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=7).round(2)

        messagebox.showinfo("Forecast Values", forecast.to_string())
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {e}")

# ---------- ALERTS ---------- #
def check_alerts():
    if data is None:
        messagebox.showerror("Error", "No data loaded")
        return
    try:
        alerts = []
        thresholds = {"pm25": 100, "pm10": 150, "co2": 1000, "co": 9, "no2": 80, "so2": 80, "o3": 120}

        for pollutant, limit in thresholds.items():
            exceed = data[data[pollutant] > limit]
            if not exceed.empty:
                alerts.append(f"{pollutant.upper()} exceeded safe limit ({limit}) in {exceed['city'].unique()}")

        if alerts:
            messagebox.showwarning("Pollution Alerts", "\n".join(alerts))
        else:
            messagebox.showinfo("Pollution Alerts", "All pollutant levels are within safe limits.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {e}")

# ------------------ GUI ------------------ #
root = Tk()
root.title("AI-Powered Environmental Monitoring System")
root.geometry("600x600")

btn_load = Button(root, text="📂 Load Dataset", command=load_data)
btn_load.pack(pady=5)

frame_sel = Frame(root)
frame_sel.pack(pady=10)

Label(frame_sel, text="City:").grid(row=0, column=0, padx=5)
city_var = StringVar()
city_combo = ttk.Combobox(frame_sel, textvariable=city_var)
city_combo.grid(row=0, column=1, padx=5)

Label(frame_sel, text="Pollutant:").grid(row=1, column=0, padx=5)
pollutant_var = StringVar()
pollutant_combo = ttk.Combobox(frame_sel, textvariable=pollutant_var,
                               values=["co2", "co", "pm25", "pm10", "no2", "so2", "o3"])
pollutant_combo.grid(row=1, column=1, padx=5)

# Buttons with separate graph & values
Button(root, text="📊 Avg Pollutant (Graph)", command=avg_pollutant_graph).pack(pady=5)
Button(root, text="📋 Avg Pollutant (Values)", command=avg_pollutant_values).pack(pady=5)

Button(root, text="⏰ Peak Hours (Graph)", command=peak_hours_graph).pack(pady=5)
Button(root, text="📋 Peak Hours (Values)", command=peak_hours_values).pack(pady=5)

Button(root, text="🌍 Compare Regions (Graph)", command=compare_regions_graph).pack(pady=5)
Button(root, text="📋 Compare Regions (Values)", command=compare_regions_values).pack(pady=5)

Button(root, text="📈 Forecast (Graph)", command=forecast_graph).pack(pady=5)
Button(root, text="📋 Forecast (Values)", command=forecast_values).pack(pady=5)

Button(root, text="⚠ Check Alerts", command=check_alerts).pack(pady=5)

root.mainloop()