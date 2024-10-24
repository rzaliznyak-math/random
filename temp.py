import plotly.subplots as sp
import pandas as pd
import plotly.express as px
from math import ceil
from numpy import where


df = pd.DataFrame(control_simulated_results, columns=["value"])
running_total_df = df.copy()

# Count occurrences and create a running total
running_total_df["count"] = running_total_df["value"].map(
    running_total_df["value"].value_counts()
)
running_total_df["running_total"] = running_total_df.groupby("value").cumcount() + 1

# Rearranging to match the running total of occurrences
running_total_df = running_total_df[["value", "count", "running_total"]]
running_total_df["new_column"] = where(running_total_df["value"] > 110, "blue", "red")


number_experiments_list = [
    1,
    50,
    200,
    400,
    800,
    2500,
    10000,
    number_simulated_experiments,
]
subplot_titles = tuple([f"# sims = {value}" for value in number_experiments_list])
number_experiments_list_length = len(number_experiments_list)


number_cols = 4
number_rows = ceil(number_experiments_list_length / number_cols)

fig = sp.make_subplots(
    rows=number_rows,
    cols=number_cols,
    subplot_titles=subplot_titles,
    vertical_spacing=0.1,
)

for j in range(len(number_experiments_list)):
    number = number_experiments_list[j]
    fig_0 = px.scatter(
        running_total_df[0:number],
        x="value",
        y="running_total",
        color="new_column",
        color_discrete_sequence=["red", "blue"],
    )

    row = 1 + int(j / number_cols)
    col = 1 + j - (row - 1) * number_cols
    fig.add_trace(fig_0.data[0], row=row, col=col)


fig.update_layout(height=600)
x_ticks = [80, 100, 120]
for j in range(len(number_experiments_list)):
    row = 1 + int(j / number_cols)
    col = 1 + j - (row - 1) * number_cols

    fig.update_xaxes(
        tickvals=x_ticks if j > 0 else [int(df["value"].iloc[0])], row=row, col=col
    )

fig.show()
