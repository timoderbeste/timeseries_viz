import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr


class TimeseriesVisualizer():
    def __init__(self, 
                 file_path: str, 
                 file_type: str = "csv",
                 plt_style="default"):
        if file_type == "csv":
            self.df = pd.read_csv(file_path)
        else:
            raise NotImplementedError
        
        plt.style.use(plt_style)
        
    def visualize_distribution(self,
                               t_col, d_cols, t_keys,
                               t_key_rule="exact", d_col_pattern=None,
                               t_label="", d_label="", 
                               title=None, save_path=None, show_plot=False):
        num_rows, num_cols = len(t_keys), len(d_cols)
        fig, axs = plt.subplots(num_rows, num_cols, 
                                figsize=(5 * num_rows, 5 * num_cols), squeeze=False)
        for i in range(num_cols):
            d_col = d_cols[i]
            for j in range(num_rows):
                t_key = t_keys[j]
                axs[j, i].set_title("%s %s" % (d_col, t_key))
                axs[j, i].grid(False)
                timeseries_vals = \
                    self.__extract_timeseries_vals(t_col, d_col, 
                                                   t_key, t_key_rule, 
                                                   d_col_pattern)
                valid_idx = np.isfinite(timeseries_vals)
                valid_timeseries_vals = timeseries_vals[valid_idx]
                m, b = np.polyfit(range(len(valid_timeseries_vals)), 
                                  valid_timeseries_vals, 1)
                axs[j, i].scatter(range(len(timeseries_vals)), 
                                  timeseries_vals)
                axs[j, i].plot(range(len(timeseries_vals)), 
                               m * range(len(timeseries_vals)) + b)
        
        if title is None:
            title = "DISTRIBUTION" \
                if not d_col_pattern \
                else "%s DISTRIBUTION" % d_col_pattern.replace("%s", "").strip("-_ ")
        fig.suptitle(title)

        if show_plot:
            fig.show()
        if save_path is not None:
            fig.savefig(save_path)
        fig.clf()
    
    def __extract_timeseries_vals(self, t_col, d_col, t_key, t_key_rule, d_col_pattern):
        if t_key is not None:
            if t_key_rule == "exact":
                df = self.df.loc[self.df[t_col] == t_key]
            elif t_key_rule == "contains":
                df = self.df.loc[self.df[t_col].str.contains(t_key)]
            else:
                raise NotImplementedError
        else:
            df = self.df
            
        if d_col_pattern is not None:
            return np.array(df[d_col_pattern % d_col])
        else:
            return np.array(df[d_col])
    