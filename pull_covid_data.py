import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys

current_date = datetime.now().date()

# read in latest covid data
covid_data = pd.read_csv('/Users/mateowheeler/Documents/covid data/covid_19_data.csv')

# temp explicit subsets
covid_us = covid_data.where(covid_data['Country/Region']=='US')
covid_china = covid_data.where(covid_data['Country/Region']=='Mainland China')
covid_italy = covid_data.where(covid_data['Country/Region']=='Italy')
covid_s_korea = covid_data.where(covid_data['Country/Region']=='South Korea')

# Create array of all countries in data
cntry_array = covid_data["Country/Region"].unique()
#print(cntry_array)
#TODO: For every country in array, compute average daily percent change in cases, then plot top 10 by Avg Daily % Chg

def group_daily(df):
    daily = df.groupby('ObservationDate', as_index=False).agg({"Confirmed": "sum", "Deaths": "sum", "Recovered": "sum"})
    daily_confirmed = df.groupby('ObservationDate').agg({"Confirmed": "sum"})

    return daily, daily_confirmed

#TODO: dynamically assign DF names for each country
daily_overall, daily_confirmed_overall = group_daily(covid_data)
daily_us, daily_confirmed_us = group_daily(covid_us)
daily_china, daily_confirmed_china = group_daily(covid_china)
daily_italy, daily_confirmed_italy = group_daily(covid_italy)
daily_s_korea, daily_confirmed_s_korea = group_daily(covid_s_korea)


# Avg Daily Case growth globally and by country
def daily_percent_change(df):

    global_case_pct_change = df.pct_change()
    global_case_pct_change['Confirmed_Perc_Chg'] = global_case_pct_change['Confirmed'].astype(float).map("{:.2%}".format)

    return global_case_pct_change

global_case_pct_change = daily_percent_change(daily_confirmed_overall)
us_case_pct_change = daily_percent_change(daily_confirmed_us)
china_case_pct_change = daily_percent_change(daily_confirmed_china)
italy_case_pct_change = daily_percent_change(daily_confirmed_italy)
s_korea_case_pct_change = daily_percent_change(daily_confirmed_s_korea)


def plot_perc_chg_bars(df, country):

    fig = px.bar(df, x=df.index, y= 'Confirmed_Perc_Chg', text="Confirmed_Perc_Chg")

    fig.update_layout(
        title="{0} Daily % Change in Confirmed Cases".format(country),

        xaxis_title="Date",
        yaxis_title="% Change",
        font=dict(
            size=15,
        )
    )

    fig.show()

plot_perc_chg_bars(global_case_pct_change, "Global")
plot_perc_chg_bars(us_case_pct_change, "US")
plot_perc_chg_bars(china_case_pct_change, "China")
plot_perc_chg_bars(italy_case_pct_change, "Italy")
plot_perc_chg_bars(s_korea_case_pct_change, "South Korea")


#TODO average daily case growth for all countries

def plot_time_series(df, title):
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
                    x=df.ObservationDate,
                    y=df['Confirmed'],
                    name="Confirmed",
                    line=dict(
                        color="deepskyblue",
                        width=5
                    ),
                    opacity=0.8))

    fig2.add_trace(go.Scatter(
                    x=df.ObservationDate,
                    y=df['Deaths'],
                    name="Deaths",
                    line=dict(
                        color="darkred",
                        width=5
                    ),
                    opacity=0.8))

    fig2.add_trace(go.Scatter(
                    x=df.ObservationDate,
                    y=df['Recovered'],
                    name="Recovered",
                    line=dict(
                        color="lightgreen",
                        width=5
                    ),
                    opacity=0.8))

    fig2.update_layout(title_text=title)
    fig2.show()

plot_time_series(daily_overall, "Global COVID-19 Data")
plot_time_series(daily_us, "US COVID-19 Data")
plot_time_series(daily_china, "China COVID-19 Data")
plot_time_series(daily_italy, "Italy COVID-19 Data")
plot_time_series(daily_s_korea, "South Korea COVID-19 Data")