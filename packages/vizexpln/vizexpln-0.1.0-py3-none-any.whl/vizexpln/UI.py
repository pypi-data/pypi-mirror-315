from typing import Any, List
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output, Markdown
from .generator import PlotGenerator
from .messages import REPORT_CONTENT, REPORT_LOADING_MSG
from .report import ReportGenLLM


class VizUI:
    """
    A user interface for performing data analysis using interactive widgets.

    This class provides options for data analysis, allowing users
    to select variables and plot types to visualize data from a given DataFrame.
    """

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Initializes the AnalysisUI with the provided DataFrame.

        Args:
            dataframe (pd.DataFrame): The DataFrame containing the data to be analyzed.
        """
        self.data = dataframe
        self.plot_generator = PlotGenerator(self.data, plot_height=8, plot_width=6)
        self.report_gen_model = ReportGenLLM()
        self.create_settings_widgets()
        self.create_report_widgets()
        self.create_core_widgets(dataframe)
        self.reset_figure_params()


    def create_core_widgets(self, dataframe: pd.DataFrame) -> None:
        """Create core widgets (analysis type, variable selection, plot type)."""

        self.analysis_type_selector = widgets.Dropdown(
            options=["Single Feature", "Multi Feature"],
            description="Analysis Type:",
            style={"description_width": "initial"},
        )
        self.analysis_type_selector.observe(
            self.display_analysis_widgets, names="value"
        )

        self.column_selector = widgets.Dropdown(
            options=dataframe.columns.tolist(),
            description="Select Variable:",
            style={"description_width": "initial"},
        )

        self.plot_type_selector = widgets.Dropdown(
            options=[
                "Histogram",
                "Box Plot",
                "Violin Plot",
                "Line Plot",
                "Scatter Plot",
                "Bar Plot",
                "Pie Chart",
                "Correlation Plot",
                "Missing Value Plot",
            ],
            description="Plot Type:",
            style={"description_width": "initial"},
        )

        self.variable_selector = widgets.SelectMultiple(
            options=dataframe.columns.tolist(),
            description="Select Variables:",
            style={"description_width": "initial"},
            layout=widgets.Layout(height="300px", width="300px"),
        )

        self.output_plot_selector = widgets.Output()
        self.output_plot_view = widgets.Output()
        self.plot_view_button = widgets.Button(
            description="Load",
            button_style="primary",
            layout=widgets.Layout(width="100px", height="25px", margin="5px"),
        )
        self.plot_view_button.on_click(self.render_plots)
        self.curr_analysis = "univariate"
        self.display_analysis_widgets({"new": "Single Feature"})  # Initial display
        self.plot_display = False  # Added to if any plot is displayed

    def create_report_widgets(self) -> None:
        """Create widgets for AI report generation."""
        self.report_gen_checkbox = widgets.Checkbox(
            value=False, description="AI analysis report"
        )
        self.generate_report_flag = False
        self.report_gen_checkbox.observe(self.on_save_fig_change, names="value")
        self.output_report_view = widgets.Output()

        if not self.report_gen_model.alive:
            self.report_gen_checkbox.disabled = True
            self.report_gen_checkbox.description = "AI analysis report(Not avai. No API KEY Found)"

    def create_settings_widgets(self) -> None:
        """Create widgets for plot settings."""
        self.settings_checkbox = widgets.Checkbox(value=False, description="settings")
        self.settings_checkbox.observe(self.update_settings, names="value")
        self.output_settings = widgets.Output()
        self.settings_display = False  # added to know if settings is displayed

    def render_plots(self, b: widgets.Button) -> None:
        """Generates and displays the plot based on selected parameters."""
        with self.output_plot_view:
            clear_output(wait=True)
            if self.curr_analysis == "univariate":
                self.plot_generator.generate_univariate_plot(
                    self.plot_schema,
                    self.plot_type,
                    width=self.figure_width,
                    height=self.figure_height,
                    title=self.figure_title,
                    x_label=self.x_label,
                    y_label=self.y_label,
                )
            else:
                self.plot_generator.generate_multivariate_plot(
                    self.plot_schema,
                    self.plot_type,
                    width=self.figure_width,
                    height=self.figure_height,
                    title=self.figure_title,
                    x_label=self.x_label,
                    y_label=self.y_label,
                )
            self.reset_figure_params()
            self.plot_display = True
            if self.generate_report_flag:
                self.generate_report()

    def _erase_existing_widgets(self) -> None:
        """Clears existing outputs to prepare for new display when interactive widgets updates"""

        # clear plots before load
        if self.output_plot_view:
            with self.output_plot_view:
                clear_output()

        # clear reports before load
        if self.output_report_view:
            with self.output_report_view:
                clear_output()

        # remove existing setting menu
        if self.settings_display:
            self.settings_menu.close()
            self.settings_checkbox.value = False
            self.settings_display = False

        # plot display is set to False since display is cleared
        self.plot_display = False

    def render_univariate_plot(self, column: str, plot_type: str) -> None:
        """Renders a single feature plot."""
        self.plot_schema = column
        self.plot_type = plot_type
        self.curr_analysis = "univariate"
        self._erase_existing_widgets()

    def render_multivariate_plot(
        self, selected_columns: List[str], plot_type: str
    ) -> None:
        """Renders a multi feature plot."""
        self.plot_schema = selected_columns
        self.plot_type = plot_type
        self.curr_analysis = "multivariate"
        self._erase_existing_widgets()

    def display_analysis_widgets(self, change: dict[str, Any]) -> None:
        """Displays widgets based on selected analysis type."""
        with self.output_plot_selector:
            clear_output(wait=True)
            if change["new"] == "Single Feature":
                self.interactive_plot = widgets.interactive(
                    self.render_univariate_plot,
                    column=self.column_selector,
                    plot_type=self.plot_type_selector,
                )
            elif change["new"] == "Multi Feature":
                self.interactive_plot = widgets.interactive(
                    self.render_multivariate_plot,
                    selected_columns=self.variable_selector,
                    plot_type=self.plot_type_selector,
                )
            display(self.interactive_plot)
            display(self.plot_view_button)

    def reset_figure_params(self) -> None:
        """Resets plot parameters to defaults."""
        self.figure_title = None
        self.x_label = None
        self.y_label = None
        self.figure_width = None
        self.figure_height = None
        # reset settings display vars
        if self.settings_display:
            self.fig_width_widget.value = 10
            self.fig_height_widget.value = 5
            self.fig_title_widget.value = ""
            self.x_label_widget.value = ""
            self.y_label_widget.value = ""

    def on_save_fig_change(self, change: dict[str, bool]) -> None:
        """Handles changes in the report generation checkbox."""
        self.generate_report_flag = change["new"]
        if self.plot_display and self.generate_report_flag:
            self.generate_report()

    def control_widgets(self, disable_mode: bool) -> None:
        """Enables or disables UI widgets."""
        self.variable_selector.disabled = disable_mode
        self.plot_type_selector.disabled = disable_mode
        self.analysis_type_selector.disabled = disable_mode
        self.column_selector.disabled = disable_mode
        self.settings_checkbox.disabled = disable_mode
        self.report_gen_checkbox.disabled = disable_mode
        self.plot_view_button.disabled = disable_mode

    def display_report(self, content: str) -> None:
        """Displays the AI report."""
        with self.output_report_view:
            clear_output()
            display(Markdown(content))

    def generate_report(self) -> None:
        """AI report generation."""
        self.display_report(REPORT_LOADING_MSG)
        self.control_widgets(disable_mode=True)
        content = self.report_gen_model.generate_analysis()
        self.display_report(REPORT_CONTENT.format(analysis=content))
        self.control_widgets(disable_mode=False)

    def update_figure_width(self, change: dict[str, int]) -> None:
        self.figure_width = change["new"]

    def update_figure_height(self, change: dict[str, int]) -> None:
        self.figure_height = change["new"]

    def update_x_label(self, change: dict[str, str]) -> None:
        self.x_label = change["new"]

    def update_y_label(self, change: dict[str, str]) -> None:
        self.y_label = change["new"]

    def update_figure_title(self, change: dict[str, str]) -> None:
        self.figure_title = change["new"]

    def update_settings(self, change: dict[str, bool]) -> None:
        """Updates plot settings based on checkbox state."""
        with self.output_settings:
            if change["new"] and not self.settings_display:
                clear_output(wait=True)
                self.fig_width_widget = widgets.IntSlider(
                    min=4, max=16, step=2, value=10, description="Fig Width:"
                )
                self.fig_height_widget = widgets.IntSlider(
                    min=4, max=16, step=2, value=5, description="Fig Height:"
                )
                self.fig_title_widget = widgets.Text(
                    value="",
                    placeholder="Enter Figure Title",
                    description="Figure Title:",
                )
                self.x_label_widget = widgets.Text(
                    value="", placeholder="Enter X Label", description="X Label:"
                )
                self.y_label_widget = widgets.Text(
                    value="", placeholder="Enter Y Label", description="Y Label:"
                )
                self.settings_menu = widgets.HBox(
                    [
                        widgets.VBox([self.fig_width_widget, self.fig_height_widget]),
                        widgets.VBox([self.x_label_widget, self.y_label_widget]),
                        self.fig_title_widget,
                    ]
                )

                self.fig_width_widget.observe(self.update_figure_width, names="value")
                self.fig_height_widget.observe(self.update_figure_height, names="value")
                self.x_label_widget.observe(self.update_x_label, names="value")
                self.y_label_widget.observe(self.update_y_label, names="value")
                self.fig_title_widget.observe(self.update_figure_title, names="value")
                display(self.settings_menu)
            elif not change["new"] and self.settings_display:
                self.settings_menu.close()
        self.settings_display = change["new"]

    def show(self) -> None:
        """Displays the main UI."""
        ui_box = widgets.VBox(
            [
                widgets.HBox(
                    [
                        self.analysis_type_selector,
                        self.report_gen_checkbox,
                        self.settings_checkbox,
                    ]
                ),
                self.output_settings,
                self.output_plot_selector,
                self.output_plot_view,
                self.output_report_view,
            ]
        )
        display(ui_box)
