import matplotlib.pyplot as plt
import pandas as pd
from typing import List
from .plotter import Plotter


class PlotGenerator:
    def __init__(
        self,
        dataframe: pd.DataFrame,
        plot_height,
        plot_width,
    ):
        """
        Initializes the PlotGenerator with a given DataFrame.

        Parameters:
            dataframe (pd.DataFrame): The DataFrame containing the data to be plotted.
        """
        self.df: pd.DataFrame = dataframe
        self.frame_plotter = Plotter(width=plot_width, height=plot_height)
        self.fig_save_progress = False

    def _clear_figure(self) -> None:
        """
        Clears the current figure in Matplotlib to prepare for a new plot.
        """
        plt.clf()  # Clear the current figure

    def _save_fig(self) -> None:
        """
        saves the plot locally
        """
        fig = plt.gcf()
        plt.tight_layout()
        fig.savefig("./tmp.png", bbox_inches="tight")

    def _validate_columns(self, columns: List[str]) -> bool:
        """
        Validates that the provided columns list contains at least two variables.

        Parameters:
            columns (List[str]): A list of column names to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        if len(columns) < 2:
            print("Please select at least two variables for multivariate analysis.")
            return False
        return True

    def generate_univariate_plot(
        self,
        column: str,
        plot_type: str,
        title: str = None,
        width: int = None,
        height: int = None,
        x_label: str = None,
        y_label: str = None,
    ) -> Exception:
        """
        Generates a univariate plot.

        Args:
            column: The column to plot.
            plot_type: The type of plot.
            title: The plot title.
            width: The plot width.
            height: The plot height.
            x_label: The x-axis label.
            y_label: The y-axis label.
        """

        plot_methods = {
            "Histogram": lambda: self.frame_plotter.histogram(
                columns=[column],
                df=self.df,
                title=title or "Histogram",
                width=width,
                height=height,
                x_label=x_label or "Value",
                y_label=y_label or "Frequency",
            ),
            "Box Plot": lambda: self.frame_plotter.box_plot(
                x=column,
                df=self.df,
                title=title or "Box Plot",
                width=width,
                height=height,
                x_label=x_label,
                y_label=y_label or "Value",
            ),
            "Violin Plot": lambda: self.frame_plotter.violin_plot(
                x=column,
                df=self.df,
                title=title or "Violin Plot",
                width=width,
                height=height,
                x_label=x_label,
                y_label=y_label or "Value",
            ),
            "Line Plot": lambda: self.frame_plotter.line_plot(
                columns=[column],
                df=self.df,
                title=title or "Line Plot",
                width=width,
                height=height,
                x_label=x_label,
                y_label=y_label or "Value",
            ),
            "Scatter Plot": lambda: self.frame_plotter.scatter_plot(
                column=column,
                df=self.df,
                title=title or "Scatter Plot",
                width=width,
                height=height,
                x_label=x_label,
                y_label=y_label,
            ),
            "Bar Plot": lambda: self.frame_plotter.bar_chart(
                column=column,
                df=self.df,
                title=title or "Bar Plot",
                width=width,
                height=height,
                x_label=x_label,
                y_label=y_label or "Count",
            ),
            "Pie Chart": lambda: self.frame_plotter.pie_chart(
                column=column, df=self.df, title=title or "Pie Chart"
            ),
            "Missing Value Plot": lambda: self.frame_plotter.missing_value_plot(
                columns=[column],
                df=self.df,
                title=title or "Missing Value Plot",
                x_label=x_label,
                y_label=y_label,
            ),
        }

        try:
            self._generate_plot(plot_type, plot_methods)
        except Exception as e:
            return Exception(
                "Error plotting!!! please check the plot type and feature.."
            )

    def generate_multivariate_plot(
        self,
        selected_columns: List[str],
        plot_type: str,
        title: str = None,
        width: int = None,
        height: int = None,
        x_label: str = None,
        y_label: str = None,
    ) -> Exception | None:
        """
        Generates a multivariate plot.

        Args:
            selected_columns: The columns to plot.
            plot_type: The type of plot.
            title: The plot title.
            width: The plot width.
            height: The plot height.
            x_label: The x-axis label.
            y_label: The y-axis label.
        """
        if not self._validate_columns(selected_columns):
            return

        melted_df: pd.DataFrame = self.df.melt(
            value_vars=list(selected_columns), value_name="melted_value"
        )

        plot_methods = {
            "Scatter Plot": lambda: self.frame_plotter.pair_plot(
                columns=list(selected_columns),
                df=self.df,
                title=title or "Scatter Plot",
                width=width,
                height=height,
                x_label=x_label,
                y_label=y_label or "Value"

            ),  # Pair plot might not use all args
            "Box Plot": lambda: self.frame_plotter.box_plot(
                x="variable",
                y="melted_value",
                df=melted_df,
                title=title or "Box Plot",
                width=width,
                height=height,
                x_label=x_label,
                y_label=y_label or "Value",
            ),
            "Violin Plot": lambda: self.frame_plotter.violin_plot(
                x="variable",
                y="melted_value",
                df=melted_df,
                title=title or "Violin Plot",
                width=width,
                height=height,
                x_label=x_label,
                y_label=y_label or "Value",
            ),
            "Histogram": lambda: self.frame_plotter.histogram(
                columns=list(selected_columns),
                df=self.df,
                title=title or "Histogram",
                width=width,
                height=height,
                x_label=x_label or "Value",
                y_label=y_label or "Frequency",
            ),
            "Line Plot": lambda: self.frame_plotter.line_plot(
                columns=list(selected_columns),
                df=self.df,
                title=title or "Line Plot",
                width=width,
                height=height,
                x_label=x_label,
                y_label=y_label or "Value",
            ),
            "Correlation Plot": lambda: self.frame_plotter.correlation_plot(
                columns=list(selected_columns),
                df=self.df,
                title=title or "Correlation plot",
            ),  # Correlation might not need all args
            "Missing Value Plot": lambda: self.frame_plotter.missing_value_plot(
                columns=list(selected_columns),
                df=self.df,
                title=title or "Missing Value Plot",
            ),
        }
        try:
            self._generate_plot(plot_type, plot_methods)
        except Exception as e:
            return Exception(
                "Error plotting!!! please check the plot type and feature.."
            )

    def _generate_plot(self, plot_type: str, plot_methods: dict) -> None:
        """Helper method to handle common plot generation logic."""
        plot_method = plot_methods.get(plot_type)
        if plot_method:
            plot_method()
            self._save_fig()
            plt.show()

        else:
            print(
                f"Plot type '{plot_type}' not available for this feature/analysis type."
            )
