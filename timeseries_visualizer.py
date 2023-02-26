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
                               t_col, t_keys, d_cols,
                               t_key_rule="exact", d_col_pattern=None,
                               x_label="", y_label="", x_ticks=None,
                               title=None, save_path=None, show_plot=False):
        num_rows, num_cols, fig, axs = \
            self.__initialize_2d_subplots(t_keys, d_cols, x_label, y_label)
        for i in range(num_cols):
            d_col = d_cols[i] 
            for j in range(num_rows):
                t_key = t_keys[j]
                axs[j, i].set_title("%s %s" % (d_col, t_key))
                axs[j, i].grid(False)
                timeseries_vals = \
                    self._extract_timeseries_vals(t_col, t_key,
                                                  d_col, t_key_rule, 
                                                  d_col_pattern)
                num_timeseries_vals = len(timeseries_vals)
                
                valid_idx = np.isfinite(timeseries_vals)
                valid_timeseries_vals = timeseries_vals[valid_idx]
                num_valid_timeseries_vals = len(valid_timeseries_vals)
                valid_x_ticks = None
                if x_ticks is not None:
                    valid_x_ticks = x_ticks[:num_timeseries_vals][valid_idx]

                m, b = np.polyfit(valid_x_ticks if valid_x_ticks is not None else \
                                  range(num_valid_timeseries_vals), 
                                  valid_timeseries_vals, 1)
                
                axs[j, i].scatter(x_ticks[:num_timeseries_vals] \
                                  if x_ticks is not None else range(num_timeseries_vals), 
                                  timeseries_vals)
                
                if x_ticks is None:
                    axs[j, i].plot(range(num_timeseries_vals), 
                                   m * range(num_timeseries_vals) + b)
                else:
                    axs[j, i].plot(x_ticks[:num_timeseries_vals],
                                   m * x_ticks[:num_timeseries_vals] + b)
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


    def visualize_outliers(self,
                           t_col, t_keys, d_cols,
                           t_key_rule="exact", d_col_pattern=None,
                           x_label="", y_label="", x_ticks=None,
                           title=None, save_path=None, show_plot=False):
        num_rows, fig, axs = \
            self.__initialize_1d_subplots(d_cols, x_label, y_label)
        
        for i in range(num_rows):
            d_col = d_cols[i]
            axs[i, 0].set_title("%s" % (d_col))
            axs[i, 0].grid(False)
            t_key2timeseries_vals = dict()
            for t_key in t_keys:
                timeseries_vals = \
                    self._extract_timeseries_vals(t_col, t_key,
                                                  d_col, t_key_rule, 
                                                  d_col_pattern)
                t_key2timeseries_vals[t_key] = timeseries_vals
            axs[i, 0].boxplot(x=t_key2timeseries_vals.values(), labels=x_ticks)
            # if x_ticks is not None:
            #     axs[i, 0].set_xticks(np.arange(len(t_keys)), x_ticks)
        
        if title is None:
            title = "OUTLIERS" \
                if not d_col_pattern \
                else "%s OUTLIERS" % d_col_pattern.replace("%s", "").strip("-_ ")
        fig.suptitle(title)

        if show_plot:
            fig.show()
        if save_path is not None:
            fig.savefig(save_path)
        fig.clf()


    def visualize_correlations(self,
                               t_col, t_keys,
                               d_cols1, d_cols2,
                               t_key_rule="exact",
                               d_col_pattern1=None, d_col_pattern2=None,
                               x_label="", y_label="",
                               title=None, save_path=None, show_plot=False):
        def compute_correlations_for_t_key(t_key):
            d_col12data = dict()
            for d_col1 in d_cols1:
                d_col12data[d_col1] = self._extract_timeseries_vals(
                    t_col=t_col,
                    t_key=t_key,
                    d_col=d_col1,
                    t_key_rule="contains",
                    d_col_pattern=d_col_pattern1,
                    drop_na=False
                )
            d_col22data = dict()
            for d_col2 in d_cols2:
                d_col22data[d_col2] = self._extract_timeseries_vals(
                    t_col=t_col,
                    t_key=t_key,
                    d_col=d_col2,
                    t_key_rule="contains",
                    d_col_pattern=d_col_pattern2,
                    drop_na=False
                )
            assert d_col12data.keys() == d_col22data.keys()
            print("d_col12data", d_col12data)
            print("d_col22data", d_col22data)
            valid_d_col1_data = []
            valid_d_col2_data = []

        compute_correlations_for_t_key(t_keys[0])
        pass
    
    def _extract_timeseries_vals(self, t_col, t_key, d_col, 
                                 t_key_rule, d_col_pattern, drop_na=True):
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
            try:
                formatted_d_col = d_col_pattern % d_col
            except TypeError as e:
                print(e)
                print("d_col", d_col)
                print("d_col_pattern", d_col_pattern)
                exit(1)
            return np.array(df[formatted_d_col].dropna()) \
                if drop_na else np.array(df[formatted_d_col].dropna())
        else:
            return np.array(df[d_col].dropna()) \
                if drop_na else np.array(df[d_col])
    
    def __initialize_2d_subplots(self, t_keys, d_cols, x_label, y_label):
        num_rows, num_cols = len(t_keys), len(d_cols)
        fig, axs = plt.subplots(num_rows, num_cols, 
                                figsize=(5 * num_cols, 5 * num_rows), 
                                sharex=True,
                                sharey=True,
                                squeeze=False)
        fig.add_subplot(111, frameon=False)
        plt.tick_params(labelcolor="none", 
                        top=False, bottom=False, left=False, right=False)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        return num_rows,num_cols,fig,axs
    
    def __initialize_1d_subplots(self, items, x_label, y_label):
        num_rows = len(items)
        fig, axs = plt.subplots(num_rows, 
                                figsize=(10, 5 * num_rows), 
                                sharex=True,
                                sharey=True,
                                squeeze=False)
        fig.add_subplot(111, frameon=False)
        plt.tick_params(labelcolor="none", 
                        top=False, bottom=False, left=False, right=False)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        return num_rows, fig, axs