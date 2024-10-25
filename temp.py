import plotly.graph_objects as go
from scipy import stats


BLUE = "#0177c9"
RED = "#bd0707"
number_points = 250
pdf = stats.gaussian_kde(control_simulated_results)
X = linspace(
    min(control_simulated_results), max(control_simulated_results), number_points
)
estimated_density = pdf.evaluate(X)
cumulative_density = cumsum(estimated_density)
cumulative_density /= cumulative_density[-1]
cdf_list = list(cumulative_density)
fx_list = estimated_density

hover_string = "True Baseline"
is_rate = False
text_list = [
    f"Pr( {hover_string} > { round((100 if is_rate else 1)*X[j],3 if is_rate else 2) }{'%' if is_rate else ''}) = {'{0:.2%}'.format(1 - cdf_list[j])}"
    for j in range(len(X))
]

distribution_figure = sp.make_subplots(
    rows=1,
    cols=3,
    subplot_titles=(
        "85 conversions or less",
        "115 conversions or more",
        "Between 85 and 115 conversions",
    ),
    vertical_spacing=0.1,
)

lower_bound_list = [85, None, 85]
upper_bound_list = [None, 115, 115]


line_color_left = BLUE
line_color_right = BLUE
all_graph_elements_extra = []
for j in range(3):
    lower_bound_position = 0
    upper_bound_position = number_points - 1
    lower_bound = lower_bound_list[j]
    upper_bound = upper_bound_list[j]

    if lower_bound is not None:
        lower_bound_position = where(array(X) > lower_bound)[0][0]
    if upper_bound is not None:
        upper_bound_position = where(array(X) > upper_bound)[0][0]

    prob = None
    if lower_bound is not None and upper_bound is not None:
        line_color_left = BLUE
        line_color_right = BLUE
        prob = mean(
            where(
                (control_simulated_results > lower_bound)
                & (control_simulated_results < upper_bound),
                1,
                0,
            )
        )
        x_axis_title = f"{prob:.2%} of outcomes shaded"
        probability = stats.norm.cdf(
            upper_bound / number_of_visitors, loc=conversion_rate, scale=standard_error
        ) - stats.norm.cdf(
            lower_bound / number_of_visitors, loc=conversion_rate, scale=standard_error
        )
        print(probability)
    elif lower_bound is not None and upper_bound is None:
        line_color_left = RED
        prob = mean(where(control_simulated_results <= lower_bound, 1, 0))
        x_axis_title = f"{prob:.2%} of outcomes shaded"

        probability = stats.norm.cdf(
            lower_bound / number_of_visitors, loc=conversion_rate, scale=standard_error
        )
        print(probability)
    elif upper_bound is not None and lower_bound is None:
        line_color_right = RED
        prob = mean(where(control_simulated_results >= upper_bound, 1, 0))
        x_axis_title = f"{prob:.2%} of outcomes shaded"
        probability = 1 - stats.norm.cdf(
            upper_bound / number_of_visitors, loc=conversion_rate, scale=standard_error
        )
        print(probability)
    else:
        pass
    x_axis_title = f"{prob:.2%} of outcomes shaded" if prob is not None else None

    line_color_middle = RED if line_color_left == BLUE else BLUE
    distribution_figure.add_trace(
        go.Scatter(
            x=X[0:lower_bound_position],
            y=fx_list[0:lower_bound_position],
            hoverinfo="skip",
            # marker_symbol="square",
            name="< 0 ",
            marker=dict(size=50),
            showlegend=False,
            line_color=line_color_left,
            # hovertext=text_list[:positive_position],
            # fill = "blue",
            line=dict(width=0.05),
            stackgroup="1",
        ),
        row=1,
        col=j + 1,
    )
    distribution_figure.add_trace(
        go.Scatter(
            x=X[lower_bound_position:upper_bound_position],
            y=fx_list[lower_bound_position:upper_bound_position],
            hoverinfo="skip",
            # marker_symbol="square",
            name="< 0 ",
            marker=dict(size=50),
            showlegend=False,
            line_color=line_color_middle,
            # hovertext=text_list[:positive_position],
            # fill = "blue",
            line=dict(width=0.05),
            stackgroup="1",
        ),
        row=1,
        col=j + 1,
    )
    distribution_figure.add_trace(
        go.Scatter(
            x=X[upper_bound_position:],
            y=fx_list[upper_bound_position:],
            hoverinfo="skip",
            # marker_symbol="square",
            name="< 0 ",
            marker=dict(size=50),
            showlegend=False,
            line_color=line_color_right,
            # hovertext=text_list[:positive_position],
            # fill = "blue",
            line=dict(width=0.05),
            stackgroup="1",
        ),
        row=1,
        col=j + 1,
    )
    distribution_figure.add_trace(
        go.Scatter(
            x=X,
            y=fx_list,
            hoverinfo="text",
            # fill='tozeroy',
            mode="lines",
            # name = "+" ,
            showlegend=False,
            line_color="black",
            hovertext=text_list,
            line=dict(width=1.5),
        ),
        row=1,
        col=j + 1,
    )

    distribution_figure.update_xaxes(
        title_text=x_axis_title,
        row=1,
        col=j + 1,
    )


tick_values = [85, 100, 115]

distribution_figure.update_xaxes(
    zeroline=False,
    tickangle=0,
    # title = "" if x_axis_title is None else x_axis_title,
    tickvals=tick_values,
    title_font=dict(size=12),
    ticks="inside",  # Default is 'outside'
    ticklen=6,
)
distribution_figure.update_yaxes(
    title="",
    visible=False,
    showticklabels=False,
)
distribution_figure.update_traces(hoverlabel=dict(font=dict(size=18)))


distribution_figure.update_layout(height=300)
distribution_figure.update_layout(
    annotations=[
        dict(
            text="85 conversions or less",
            x=0.15,
            y=1.05,
            font=dict(size=12),
            showarrow=False,
        ),
        dict(
            text="115 conversions or more",
            x=0.5,
            y=1.05,
            font=dict(size=12),
            showarrow=False,
        ),
        dict(
            text="Between 85 and 115 conversions",
            x=0.85,
            y=1.05,
            font=dict(size=12),
            showarrow=False,
        ),
    ]
)


distribution_figure.show()
