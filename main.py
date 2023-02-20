import os

from timeseries_visualizer import TimeseriesVisualizer


def main():
    data_dir = "/Users/timowang/Data/data/time-series-canadian-climate-history/"
    data_path = os.path.join(data_dir, "Canadian_climate_history.csv")
    time_viz = TimeseriesVisualizer(data_path, plt_style="ggplot")
    time_viz.visualize_distribution(
        t_col="LOCAL_DATE", 
        t_keys=["01-Jan", "02-Feb"],
        d_cols=["CALGARY", "TORONTO", "VANCOUVER"], 
        t_key_rule="contains",
        d_col_pattern="MEAN_TEMPERATURE_%s",
        x_label="Year",
        y_label="Mean Temperature",
        save_path=os.path.join(data_dir, "distribution_plot.png"),
        show_plot=True,
    )

    time_viz.visualize_outliers(
        t_col="LOCAL_DATE",
        t_keys=["01-Jan", "01-Feb", "01-Mar", "01-Apr", "01-May", "01-Jun",
                "01-Jul", "01-Aug", "01-Sep", "01-Oct", "01-Nov", "01-Dec"],
        d_cols=[
        "TORONTO", 
        "VANCOUVER", 
        "CALGARY",
        "HALIFAX"
        ],
        t_key_rule="contains",
        d_col_pattern="MEAN_TEMPERATURE_%s",
        x_label="Month of the year",
        y_label="Mean Temperatures",
        save_path=os.path.join(data_dir, "outliers_plot.png"),
    )

    


if __name__ == "__main__":
    main()
