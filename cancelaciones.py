import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("ncr_ride_bookings.csv")

# Formato de fecha y hora
df["Date"] = pd.to_datetime(df["Date"])
df["Hour"] = df["Time"].str[:2].astype(int)
df["DayOfWeek"] = df["Date"].dt.day_name()


#Filtro de Cancelaciones

cancel_filter = (
    (df["Cancelled Rides by Customer"].fillna(0) > 0) |
    (df["Cancelled Rides by Driver"].fillna(0) > 0) |
    (df["Booking Status"] == "No Driver Found")
)
df_cancelled = df[cancel_filter].copy()

# Nos quedamos con las cancelaciones que tienen razón de cliente
df_customer_reasons = df_cancelled[df_cancelled["Reason for cancelling by Customer"].notna()]

# Agrupamos por día, hora y razón
grouped_reasons = df_customer_reasons.groupby(
    ["DayOfWeek", "Hour", "Reason for cancelling by Customer"]
).size().reset_index(name="Count")

# Calcular porcentaje dentro de cada (día, hora)
grouped_reasons["TotalInSlot"] = grouped_reasons.groupby(["DayOfWeek", "Hour"])["Count"].transform("sum")
grouped_reasons["Percent"] = 100 * grouped_reasons["Count"] / grouped_reasons["TotalInSlot"]


# Usamos la tabla que armamos antes (grouped_reasons)
# Pivot para tener razones como columnas
pivot_reasons = grouped_reasons.pivot_table(
    index=["DayOfWeek", "Hour"],
    columns="Reason for cancelling by Customer",
    values="Percent",
    fill_value=0
)

# Ordenar días de la semana
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
pivot_reasons = pivot_reasons.reindex(pd.MultiIndex.from_product(
    [days_order, range(24)], names=["DayOfWeek", "Hour"]
))

# Hacemos gráfico de barras apiladas
pivot_reasons.plot(kind="bar", stacked=True, figsize=(18,7), colormap="tab20")

plt.title("Distribución de razones de cancelación de clientes por hora y día")
plt.ylabel("Porcentaje (%)")
plt.xlabel("Día de la semana y hora")
plt.legend(title="Razón de cancelación", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()