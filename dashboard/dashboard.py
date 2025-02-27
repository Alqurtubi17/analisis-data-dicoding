import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("main_data.csv")
df['dteday'] = pd.to_datetime(df['dteday'])  # Convert to datetime

# Sidebar for date range selection
st.sidebar.header("Filter Data")
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [df["dteday"].min(), df["dteday"].max()])

if len(date_range) != 2:
    st.sidebar.error("Mohon Maaf, harus pilih rentang tanggal!")
else:
    start_date, end_date = date_range
    # Filter data by date range
    df_filtered = df[(df['dteday'] >= pd.Timestamp(start_date)) & (df['dteday'] <= pd.Timestamp(end_date))]

    # Dashboard Title
    st.title("Dashboard Penyewaan Sepeda")

    # Section 1: Tren Penyewaan Sepeda
    df_trend = df_filtered.groupby('dteday')['cnt'].sum().reset_index()
    st.subheader("Tren Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(df_trend['dteday'], df_trend['cnt'], linestyle='-')
    ax.set_title("Tren Dalam Hari", loc="center", fontsize=30)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

    df_trend_hr = df_filtered.groupby('hr')['cnt'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(df_trend_hr['hr'], df_trend_hr['cnt'], linestyle='-')
    ax.set_title("Tren Dalam Per Jam", loc="center", fontsize=30)
    ax.set_xticks(range(0, 24))
    ax.tick_params(axis='x', labelsize=25)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

    # Section 2: Distribusi Penyewaan Berdasarkan Jam dan Hari
    st.subheader("Distribusi Penyewaan Berdasarkan Jam dan Hari")
    day_labels = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    pivot_table = df_filtered.pivot_table(index='hr', columns='weekday', values='cnt', aggfunc='mean')
    fig, ax = plt.subplots(figsize=(20, 15))
    sns.heatmap(pivot_table, cmap="coolwarm", annot=True, fmt=".0f", xticklabels=day_labels, yticklabels=range(0, 24))
    plt.title("Heatmap Penyewaan Sepeda Berdasarkan Jam dan Hari", loc="center", fontsize=30)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=15)
    st.pyplot(fig)

    # Section 3: Pengaruh Faktor Cuaca dan Musim
    # Menghitung korelasi Pearson
    corr_temp = df["temp"].corr(df["cnt"])
    corr_hum = df["hum"].corr(df["cnt"])
    corr_windspeed = df["windspeed"].corr(df["cnt"])
    st.subheader("Pengaruh Faktor Cuaca dan Musim terhadap Penyewaan")
    fig, axes = plt.subplots(1, 3, figsize=(20, 10))
    # Scatter plot temperatur
    sns.regplot(x="temp", y="cnt", data=df, ax=axes[0], scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    axes[0].set_title(f"Temperatur terhadap Penyewaan\nKorelasi: {corr_temp:.2f}", fontsize = 20)
    axes[0].set_ylabel(None)
    axes[0].set_xlabel('Temperatur', fontsize = 20)
    axes[0].tick_params(axis='x', labelsize=20)
    axes[0].tick_params(axis='y', labelsize=20)
    # Scatter plot kelembapan
    sns.regplot(x="hum", y="cnt", data=df, ax=axes[1], scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    axes[1].set_title(f"Kelembapan terhadap Penyewaan\nKorelasi: {corr_hum:.2f}", fontsize = 20)
    axes[1].set_ylabel(None)
    axes[1].set_xlabel('Kelembapan', fontsize = 20)
    axes[1].tick_params(axis='x', labelsize=20)
    axes[1].tick_params(axis='y', labelsize=20)
    # Scatter plot kecepatan angin
    sns.regplot(x="windspeed", y="cnt", data=df, ax=axes[2], scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    axes[2].set_title(f"Kecepatan Angin terhadap Penyewaan\nKorelasi: {corr_windspeed:.2f}", fontsize = 20)
    axes[2].set_ylabel(None)
    axes[2].set_xlabel('Kecepatan Angin', fontsize = 20)
    axes[2].tick_params(axis='x', labelsize=20)
    axes[2].tick_params(axis='y', labelsize=20)
    st.pyplot(fig)

    # Section 4: Perbandingan Penyewaan pada Hari Kerja vs. Akhir Pekan
    st.subheader("Perbandingan Penyewaan pada Hari Kerja vs. Akhir Pekan")
    df_filtered['weekend'] = df_filtered['weekday'].apply(lambda x: 'Weekend' if x in [0, 6] else 'Weekday')
    avg_rentals = df_filtered.groupby('weekend')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(x='weekend', y='cnt', data=avg_rentals, ax=ax)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)


    # Section 5: Rata-rata Penyewaan Berdasarkan Waktu dalam Sehari
    st.subheader("Analisis Cluster")
    bins = [0, 3, 9, 15, 19, 23]
    labels = ["Dini Hari", "Pagi", "Siang", "Sore", "Malam"]
    df_filtered["time_of_day"] = pd.cut(df_filtered["hr"], bins=bins, labels=labels, include_lowest=True, ordered=True)
    time_avg = df_filtered.groupby("time_of_day")["cnt"].mean()
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(x=time_avg.index, y=time_avg.values, palette="coolwarm", ax=ax)
    ax.set_title("Rata-rata Penyewaan Berdasarkan Waktu dalam Sehari", loc="center", fontsize=30)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

    # Section 6: Pola Penyewaan Sepeda Berdasarkan Hari dalam Seminggu
    weekday_labels = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    weekday_avg = df_filtered.groupby("weekday")["cnt"].mean()
    weekday_avg.index = weekday_labels
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(x=weekday_avg.index, y=weekday_avg.values, palette="coolwarm", ax=ax)
    ax.set_title("Pola Penyewaan Sepeda Berdasarkan Hari dalam Seminggu", loc="center", fontsize=30)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

    # Section 7: Distribusi Penyewaan Sepeda Berdasarkan Musim
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.boxplot(x="season", y="cnt", data=df_filtered, ax=ax)
    ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
    ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Musim", loc="center", fontsize=30)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
