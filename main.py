from timeseries_visualizer import TimeseriesVisualizer


def main():
    vizer = TimeseriesVisualizer(
        "/Users/timowang/Downloads/time-series-canadian-climate-history/Canadian_climate_history.csv")
    
    vizer.visualize_distribution("LOCAL_DATE",
                                 ["CALGARY", "TORONTO"],
                                 ["01-Jan", "01-Feb"],
                                 t_key_rule="contains",
                                 d_col_pattern="MEAN_TEMPERATURE_%s")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
