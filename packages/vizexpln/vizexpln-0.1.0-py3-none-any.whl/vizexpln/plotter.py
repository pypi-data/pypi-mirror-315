import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Optional, Union


class Plotter:
    """
    A class for creating various types of plots using Matplotlib and Seaborn.
    """

    def __init__(self, width: int = 10, height: int = 5) -> None:
        """Initializes the Plotter class with specified figure dimensions."""
        self.width = width
        self.height = height

    def _set_plot_params(
        self,
        title: Optional[str] = None,
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ):
        """Sets plot parameters like title, labels, and dimensions."""
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        if width is not None and height is not None:
            plt.gcf().set_size_inches(width, height)
        elif width is not None:
            plt.gcf().set_size_inches(width, plt.gcf().get_size_inches()[1])
        elif height is not None:
            plt.gcf().set_size_inches(plt.gcf().get_size_inches()[0], height)

    def violin_plot(
        self,
        df: pd.DataFrame,
        x: str,
        y: Optional[str] = None,
        title: Optional[str] = "Violin Plot",
        x_label: Optional[str] = None,
        y_label: Optional[str] = "Value",
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        """Creates a violin plot."""

        if y is None:
            sns.violinplot(y=df[x], color="skyblue")
            if x_label is None:
                x_label = x  # Default x_label if y is None
        else:
            sns.violinplot(x=x, y=y, data=df)
            if x_label is None:
                x_label = x
            if y_label is None:
                y_label = y

        plt.xticks(rotation=45)
        self._set_plot_params(title, x_label, y_label, width, height)

    def histogram(
        self,
        df: pd.DataFrame,
        columns: List[str],
        title: Optional[str] = "Histogram",
        x_label: Optional[str] = "Value",
        y_label: Optional[str] = "Frequency",
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        """Creates histograms."""

        for column in columns:
            plt.hist(df[column], bins=20, alpha=0.5, label=column)

        if x_label is None and len(columns) == 1:
            x_label = columns[0]  # Default if single column

        self._set_plot_params(title, x_label, y_label, width, height)
        plt.legend()

    def box_plot(
        self,
        df: pd.DataFrame,
        x: str,
        y: Optional[str] = None,
        title: Optional[str] = "Box Plot",
        x_label: Optional[str] = None,
        y_label: Optional[str] = "Value",
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        """Creates a box plot."""

        if y is None:
            sns.boxplot(y=df[x], color="skyblue")
            if x_label is None:
                x_label = x  # Default if y is None
        else:
            sns.boxplot(x=x, y=y, data=df)
            # Default labels for two variables
            if x_label is None:
                x_label = x
            if y_label is None:
                y_label = y

        plt.xticks(rotation=45)
        self._set_plot_params(title, x_label, y_label, width, height)

    def line_plot(
        self,
        df: pd.DataFrame,
        columns: List[str],  # Changed to List[str]
        title: Optional[str] = "Line Plot",
        x_label: Optional[str] = "Index",  # Default x-axis is the index
        y_label: Optional[str] = "Value",
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        """Creates a line plot."""

        for column in columns:
            plt.plot(
                df.index, df[column], marker="o", linestyle="-", label=column
            )  # Plot against index

        if y_label is None and len(columns) == 1:
            y_label = columns[0]  # Default y_label if single column

        self._set_plot_params(title, x_label, y_label, width, height)
        plt.legend()
        plt.grid(axis="y", alpha=0.75)

    def scatter_plot(
        self,
        df: pd.DataFrame,
        column: str,  # Changed type to str for single column
        title: Optional[str] = "Scatter Plot",
        x_label: Optional[str] = "Index",  # Default is index
        y_label: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        """Creates a scatter plot."""

        if len(df[column].unique()) > 1:
            plt.scatter(
                df.index, df[column], color="blue", alpha=0.7
            )  # Plot against index
            if y_label is None:
                y_label = column  # Default y_label

            self._set_plot_params(title, x_label, y_label, width, height)
            plt.grid(axis="y", alpha=0.75)
        else:
            print(
                "Scatter plot requires at least two unique values in the selected column."
            )

    def pair_plot(
        self,
        df: pd.DataFrame,
        columns: List[str],
        title: Optional[str] = "Pair Plot",
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,

    ) -> None:
        """Creates a pair plot."""
        if not isinstance(columns, list) or len(columns) < 2:
            raise ValueError(
                "The 'columns' argument must be a list of at least two column names."
            )

        for column in columns:
            if column not in df.columns:
                raise ValueError(f"Column '{column}' is not in the DataFrame.")

        g = sns.pairplot(df[columns])
        # Set title using the figure's suptitle for better placement with pairplot
        g.fig.suptitle(title, y=1.02)  # Adjust y for title position above the plot
        self._set_plot_params(title, x_label, y_label, width, height)

    def pie_chart(
        self,
        df: pd.DataFrame,
        column: str,
        title: Optional[str] = "Pie Chart",
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        """Generates and displays a pie chart."""
        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

        value_counts = df[column].value_counts()
        plt.pie(
            value_counts, labels=value_counts.index, autopct="%1.1f%%", startangle=140
        )
        plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

        self._set_plot_params(title=title, width=width, height=height)

    def bar_chart(
        self,
        df: pd.DataFrame,
        column: str,
        title: Optional[str] = "Bar Chart",
        x_label: Optional[str] = "Count",  # Default x-label
        y_label: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        """Generates and displays a horizontal bar chart."""

        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

        value_counts = df[column].value_counts()
        value_counts.plot(kind="barh", color="skyblue")
        if y_label is None:
            y_label = column  # default y label
        self._set_plot_params(title, x_label, y_label, width, height)

    def correlation_plot(
        self,
        df: pd.DataFrame,
        columns: List[str],
        title: Optional[str] = "Correlation Plot",
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        """Creates a correlation plot (heatmap)."""

        df_numeric = df[columns].select_dtypes(include=["number"])
        plt.figure(
            figsize=(
                width or self.width + df_numeric.shape[1],
                height or self.height + df_numeric.shape[1],
            )
        )

        corr_matrix = df_numeric.corr()
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")

        plt.title(title)  # Set the title directly on the heatmap

    def missing_value_plot(
        self,
        df: pd.DataFrame,
        columns: List[str],
        title: Optional[str] = "Missing Value Plot",
        width: Optional[int] = None,
        height: Optional[int] = None,
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
    ) -> None:
        """Generates and displays a missing value plot (matrix)."""
        sns.heatmap(df[columns].isnull(), cmap="inferno")
        self._set_plot_params(title, x_label, y_label, width, height)
