import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



df=pd.read_csv("ncr_ride_bookings.csv")




# Aseguramos formato de fecha y hora
df["Date"] = pd.to_datetime(df["Date"])
df["Hour"] = df["Time"].str[:2].astype(int)
df["DayOfWeek"] = df["Date"].dt.day_name()

# Agrupamos
grouped = df.groupby(["DayOfWeek", "Hour"]).agg(
    total_rides=("Booking ID", "count"),
    driver_cancels=("Cancelled Rides by Driver", "sum"),
    customer_cancels=("Cancelled Rides by Customer", "sum")
).reset_index()

# Calcular porcentajes
grouped["Cancel % Driver"] = 100 * grouped["driver_cancels"] / grouped["total_rides"]
grouped["Cancel % Customer"] = 100 * grouped["customer_cancels"] / grouped["total_rides"]

# Pivot para heatmap (driver)
pivot_driver = grouped.pivot(index="DayOfWeek", columns="Hour", values="Cancel % Driver")

# Pivot para heatmap (customer)
pivot_customer = grouped.pivot(index="DayOfWeek", columns="Hour", values="Cancel % Customer")

# Orden de días
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
pivot_driver = pivot_driver.reindex(days_order)
pivot_customer = pivot_customer.reindex(days_order)

# Graficar ambos heatmaps
fig, axes = plt.subplots(2, 1, figsize=(14, 12), sharex=True)

sns.heatmap(pivot_driver, annot=True, fmt=".1f", cmap="Reds",
            cbar_kws={'label': 'Cancel % (Driver)'}, ax=axes[0])
axes[0].set_title("Porcentaje de cancelación por hora y día (Conductor)")
axes[0].set_ylabel("Día de la semana")

sns.heatmap(pivot_customer, annot=True, fmt=".1f", cmap="Blues",
            cbar_kws={'label': 'Cancel % (Customer)'}, ax=axes[1])
axes[1].set_title("Porcentaje de cancelación por hora y día (Cliente)")
axes[1].set_ylabel("Día de la semana")
axes[1].set_xlabel("Hora del día")

plt.tight_layout()
plt.show()

#TODO ver motivos de cancelación por horarios ej: Lunes 01 am
#TODO molestar a canela

#TODO Pronosticar cancelaciones de viaje
