import os

from timeseries_visualizer import TimeseriesVisualizer


def main():
    data_dir = "/Users/timowang/Data/data/time-series-canadian-climate-history/"
    data_path = os.path.join(data_dir, "Canadian_climate_history.csv")
    time_viz = TimeseriesVisualizer(data_path, plt_style="ggplot")
    time_viz.visualize_distribution(
        t_col="LOCAL_DATE", 
        d_cols=["CALGARY", "TORONTO"], 
        t_keys=["01-Jan", "02-Feb"],
        t_key_rule="contains",
        d_col_pattern="MEAN_TEMPERATURE_%s",
        save_path=os.path.join(data_dir, "distribution_plot.png"),
        show_plot=True,
    )
    


if __name__ == "__main__":
    main()
