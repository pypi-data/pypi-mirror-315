import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def create_lineplot(
    df,
    x_axis,
    y_axes,
    x_label,
    y_labels,
    line_labels=None,
    title=None,
    colors=None,
    grid=False,
    figsize=(10, 6),
    legend=True,
    rotation=0,
    style='default',
    marker=None,
    linestyle='-',
    alpha=1.0,
    use_secondary_axis=True,
    fontsize_title=16,
    fontsize_labels=12,
    fontsize_ticks=10,
    fontsize_legend=10
):
    """
    Customised function to create single or multiple line plots using matplotlib.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing data for the plot
        title (str): Title of the plot
        x_axis (str): Column name to use for x-axis
        y_axes (str or list): Column name(s) to plot on y-axis. Can be single column name or list
        x_label (str, optional): Label for x-axis
        y_label (str, optional): Label for y-axis
        line_labels (list, optional): Labels for legend of each line
        colors (list, optional): List of colors for each line
        grid (bool, optional): Whether to show grid. Default True
        figsize (tuple, optional): Size of plot. Default (10, 6)
        legend (bool, optional): Whether to show legend. Default True
        rotation (int, optional): Rotation angle for x-axis ticks. Default 0
        style (str, optional): Matplotlib style to use. Default 'seaborn'
        marker (str, optional): Marker style for data points. Default None
        linestyle (str, optional): Style of the line. Default solid
        alpha (float, optional): Opacity of lines. Default 1.0
        fontsize_title (int, optional): Font size for title. Default 16
        fontsize_labels (int, optional): Font size for axis labels. Default 12
        fontsize_ticks (int, optional): Font size for tick labels. Default 10
        fontsize_legend (int, optional): Font size for legend. Default 10
    
    Returns:
        matplotlib.figure.Figure: The created figure object
    """
    plt.style.use(style)
    df = df.copy()
    
    # Ensure y_axes is a list
    if isinstance(y_axes, str):
        y_axes = [y_axes]
    
    # Handle y_labels
    if y_labels is None:
        y_labels = [None] * len(y_axes)
    elif isinstance(y_labels, str):
        y_labels = [y_labels]
    
    # Ensure we have enough y_labels
    while len(y_labels) < len(y_axes):
        y_labels.append(None)
    
    # Default values for line labels and colors
    if line_labels is None:
        line_labels = y_axes
    if colors is None:
        colors = ['blue', 'red', 'green', 'orange', 'purple']
    
    # Create figure and primary axis
    fig, ax1 = plt.subplots(figsize=figsize)
    
    # Determine if we should use secondary axis
    use_secondary = use_secondary_axis and len(y_axes) == 2
    
    lines = []
    labels = []
    
    # Plot lines
    for i, y_axis in enumerate(y_axes):
        if i == 0 or not use_secondary:
            # First line (and all lines if not using secondary axis)
            line = ax1.plot(
                df[x_axis],
                df[y_axis],
                color=colors[i % len(colors)],
                label=line_labels[i],
                marker=marker,
                linestyle=linestyle,
                alpha=alpha
            )[0]
            if i == 0 and y_labels[0]:
                ax1.set_ylabel(y_labels[0], fontsize=fontsize_labels)
                
        elif i == 1 and use_secondary:
            # Second line on secondary axis
            ax2 = ax1.twinx()
            line = ax2.plot(
                df[x_axis],
                df[y_axis],
                color=colors[i % len(colors)],
                label=line_labels[i],
                marker=marker,
                linestyle=linestyle,
                alpha=alpha
            )[0]
            if y_labels[1]:
                ax2.set_ylabel(y_labels[1], fontsize=fontsize_labels)
        
        lines.append(line)
        labels.append(line_labels[i])
    
    # Add title and x-label
    ax1.set_title(title, fontsize=fontsize_title, pad=20)
    if x_label:
        ax1.set_xlabel(x_label, fontsize=fontsize_labels)
    
    # Customize ticks
    ax1.tick_params(axis='both', labelsize=fontsize_ticks)
    plt.xticks(rotation=rotation)
    
    # Add grid
    if grid:
        ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Add legend if needed
    if legend:
        if use_secondary and len(y_axes) == 2:
            ax1.legend(lines, labels, fontsize=fontsize_legend, 
                      framealpha=0.8, loc='upper left')
        else:
            ax1.legend(fontsize=fontsize_legend, framealpha=0.8)
    
    # Adjust layout
    plt.tight_layout()
    #plt.show()
    plt.close(fig)
    return fig


def create_stacked_barplot_lineplot_overlay(
    df, x_axis, barplot_y_axis_value, lineplot_y_axis, 
    x_axis_label, barplot_y_axis_label, lineplot_y_axis_label, 
    barplot_y_axis_category=None, jump_step=1, barplot_where='upper left', 
    lineplot_where='upper right', barplot_order=None, rotation=45, 
    figsize=(12, 6), title=''
):
    """
    Create a stacked barplot with an overlayed line plot.

    Parameters:
        df (pd.DataFrame): Input dataframe.
        x_axis (str): Column name for x-axis values.
        barplot_y_axis_value (list or str): Column names for the barplot values.
        lineplot_y_axis (list or str): Column name(s) for lineplot values.
        x_axis_label (str): Label for the x-axis.
        barplot_y_axis_label (str): Label for the barplot y-axis.
        lineplot_y_axis_label (str): Label for the lineplot y-axis.
        barplot_y_axis_category (str, optional): Column name for the barplot categories.
        jump_step (int, optional): Step size for x-axis ticks. Default is 1.
        barplot_where (str): Location of the barplot legend.
        lineplot_where (str): Location of the lineplot legend.
        barplot_order (list, optional): Custom order for barplot stacking.
        rotation (int, optional): Rotation angle for x-axis labels. Default is 45.
        figsize (tuple, optional): Figure size. Default is (12, 6).
        title (str): Title of the plot.

    Returns:
        None
    """
    # Ensure lineplot_y_axis is a list
    if isinstance(lineplot_y_axis, str):
        lineplot_y_axis = [lineplot_y_axis]
    
    if isinstance(barplot_y_axis_value, str):
        barplot_y_axis_value = [barplot_y_axis_value]

    # Validate column names
    all_columns = barplot_y_axis_value + lineplot_y_axis
    missing_cols = [col for col in all_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Columns {missing_cols} are not in the dataframe.")
    
    # Pivot data for stacked bar plot
    df_pivot_barplot = df.pivot_table(index=x_axis, columns=barplot_y_axis_category, values=barplot_y_axis_value).fillna(0)
    df_pivot_lineplot = df.pivot_table(index=x_axis, values=lineplot_y_axis, aggfunc='sum').fillna(0)

    # Reorder columns for the desired stacking order
    if barplot_order:
        df_pivot_barplot = df_pivot_barplot[barplot_order]

    fig, ax = plt.subplots(figsize=figsize)

    # Plot the stacked bar chart
    df_pivot_barplot.plot(kind='bar', stacked=True, width=1, ax=ax)

    # Set x-ticks for the bar plot
    ax.set_xticks(range(0, len(df_pivot_barplot), jump_step))
    ax.set_xticklabels(df_pivot_barplot.index[::jump_step], rotation=rotation)

    # Plot overlay line plots with secondary y-axis
    ax2 = ax.twinx()
    colors = ['black','brown','grey']
    for i, col in enumerate(lineplot_y_axis):
        ax2.plot(range(len(df_pivot_lineplot)), df_pivot_lineplot[col].values,color=colors[i], marker='o', label=col)

    # Set axis labels and title
    ax.set_xlabel(x_axis_label)
    ax.set_ylabel(barplot_y_axis_label)
    ax2.set_ylabel(lineplot_y_axis_label)
    plt.title(title)

    # Add legends for both plots
    ax.legend(title=barplot_y_axis_category, loc=barplot_where)
    ax2.legend(loc=lineplot_where)

    # Adjust layout for better spacing
    plt.tight_layout()
    #plt.show()
    plt.close(fig)
    
    return fig