import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from .GUI import show_my_info
import os

def prep_data(data, length_per_pixel, seconds_per_frame):
    pix_lengths = data['length']
    data = data.drop(columns='length')
    actual_lengths = pix_lengths * length_per_pixel
    actual_lengths = actual_lengths.to_numpy()

    data = data.to_numpy()
    data = data[:, 1:]

    number_frames = data.shape[1]
    times = np.arange(number_frames) * seconds_per_frame

    # normalize data to [0, 1] range based on each column
    data = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))
    data = data.T

    return data, actual_lengths, times

def half_point_calc(times, data, actual_lengths):
    half_intensity_points = []
    for time, time_point in zip(times, data):
        half_intensity_point = np.argmin(time_point >= 0.5)
        actual_length = actual_lengths[half_intensity_point]
        half_intensity_points.append((time, actual_length))

    print("(Time, Length)")
    for time, length in half_intensity_points:
        print(int(time), int(length))

    return half_intensity_points

def fitting_half_point(half_intensity_points, times):
    def model_func(t, D, C):
        return np.sqrt(2 * D * t) + C

    times_hp = [time for time, length in half_intensity_points]
    lengths_hp = [length for time, length in half_intensity_points]
    popt, pcov = curve_fit(model_func, times_hp, lengths_hp)

    model_func_vec = np.vectorize(model_func)

    lower_bound_prediction = model_func_vec(times, popt[0] - np.sqrt(pcov[0, 0]), popt[1] - np.sqrt(pcov[1, 1]))
    upper_bound_prediction = model_func_vec(times, popt[0] + np.sqrt(pcov[0, 0]), popt[1] + np.sqrt(pcov[1, 1]))
    predictions = model_func_vec(times, *popt)

    print(f"D: {popt[0]} pm {np.sqrt(pcov[0, 0])}")
    print(f"C: {popt[1]} pm {np.sqrt(pcov[1, 1])}")

    # print(times_hp, lengths_hp, predictions, times)

    return times_hp, lengths_hp, predictions, lower_bound_prediction, upper_bound_prediction, popt, pcov, model_func

def plot_data(path, data, actual_lengths, times, half_intensity_points, times_hp, lengths_hp, predictions, lower_bound_prediction, upper_bound_prediction, popt, pcov, rows, model_func): 
    print(f'Saving plots to {path}')

    data = data.T
    # heat map
    fig, ax = plt.subplots(figsize=(10, 8))
    suptext = "Length over Time with Prediction and Measurement of Half Intensity Point"
    fig.suptitle(suptext, position=(0.5, 0.92))
    suptxts =[suptext]
    ax.imshow(data, cmap='viridis', interpolation='none', aspect='auto', origin='lower', extent=[times.min(), times.max(), actual_lengths.min(), actual_lengths.max()])
    cbar = fig.colorbar(ax.imshow(data, cmap='viridis', interpolation='none', aspect='auto', origin='lower', extent=[times.min(), times.max(), actual_lengths.min(), actual_lengths.max()]), ax=ax)
    cbar.set_label("Normalized Intensity")
    ax.plot(times_hp, lengths_hp, 'ro-', label="Half intensity point")
    ax.plot(times, predictions, 'b-', label="Prediction")
    ax.fill_between(times, lower_bound_prediction, upper_bound_prediction, color='gray', alpha=0.5)
    ax.set_ylabel("Length [µm]")
    ax.set_xlabel("Time [s]")
    ax.legend()

    title = 'heatmap'
    title = title.replace(" ", "_").replace(":", "_")
    save_path_loc = os.path.join(path, f"{title}.svg")
    fig.savefig(save_path_loc, bbox_inches='tight', dpi=300)

    data = data.T
    plots_per_row = (len(data)+1) // rows + 1

    # plot intensity over length per time 
    fig, axs = plt.subplots(rows, plots_per_row, figsize=(12, 8))
    axs = axs.flatten()
    suptxt = "Intensity over Length at Time Points with Prediction and Half Intensity Point"
    fig.suptitle("Intensity over Length at Time Points with Prediction and Half Intensity Point")
    
    for i, (time, time_point) in enumerate(zip(times, data)):
        axs[i].plot(actual_lengths, time_point, label="Measurement")
        axs[i].plot(model_func(time, *popt), 0.5, 'bo', label="Prediction")
        error = np.sqrt(np.diag(pcov))
        axs[i].errorbar(model_func(time, *popt), 0.5, xerr=error[0]+error[1], fmt='bo', capsize=5)
        axs[i].plot(half_intensity_points[i][1], 0.5, 'ro', label="Half intensity Point")
        axs[i].set_ylabel("Intensity")
        axs[i].set_xlabel("Length [µm]")
        axs[i].set_title(f"Time: {time}")
        if i == 0:
            handles, labels = axs[i].get_legend_handles_labels()

    axs[i+1].clear()
    axs[i+1].axis('off')
    axs[i+1].legend(handles, labels, loc='center')

    # remove unused axes
    for i in range(len(data)+1, rows * plots_per_row):
        fig.delaxes(axs[i])
    plt.tight_layout()

    title = "single plots"
    title = title.replace(" ", "_").replace(":", "_")
    save_path_loc = os.path.join(path, f"{title}.svg")
    fig.savefig(save_path_loc, bbox_inches='tight', dpi=300)

    # plot half intensity point over time
    fig, ax = plt.subplots(figsize=(8, 8))
    suptxt = "Length over Time with Prediction and Measurement of Half Intensity Point"
    fig.suptitle(suptxt, position=(0.5, 0.92))
    suptxts.append(suptxt)
    ax.plot(times_hp, lengths_hp,'ro-', label="Half intensity point")
    ax.plot(times, predictions, 'b-', label="Prediction")
    ax.fill_between(times, lower_bound_prediction, upper_bound_prediction, color='b', alpha=0.5)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Length [µm]")
    ax.legend()

    title = "half intensity point over time"
    title = title.replace(" ", "_").replace(":", "_")
    save_path_loc = os.path.join(path, f"{title}.svg")
    fig.savefig(save_path_loc, bbox_inches='tight', dpi=300)

   
    # print("!!!Save the plots via the GUI and then close them to continue!!!")
    # show_my_info("INFO", "!!!Save the plots via the GUI and then close them to continue!!!")
    plt.show()
    plt.close()

def plot_master(df, length_per_pixel, seconds_per_frame, rows, path):
    data, actual_lengths, times = prep_data(df, length_per_pixel, seconds_per_frame)
    half_intensity_points = half_point_calc(times, data, actual_lengths)
    times_hp, lengths_hp, predictions, lower_bound_prediction, upper_bound_prediction, popt, pcov, model_func = fitting_half_point(half_intensity_points, times)
    plot_data(path, data, actual_lengths, times, half_intensity_points, times_hp, lengths_hp, predictions, lower_bound_prediction, upper_bound_prediction, popt, pcov, rows, model_func)

    uncertainties = np.sqrt(np.diag(pcov))
    # print(f"Uncertainties: {uncertainties}")
        
    results_dict = {
        'times': times.tolist(),
        'times_hp': times_hp,
        'lengths_hp': lengths_hp,
        'predictions': predictions.tolist(),
        'lower_bound_prediction': lower_bound_prediction.tolist(),
        'upper_bound_prediction': upper_bound_prediction.tolist(),
        'param_opt': popt.tolist(),
        'param_covmatrix': pcov.tolist(),
        'model_func': "y = np.sqrt(2 * param0 * t) + param1",
        'seconds_per_frame': seconds_per_frame,
        'length_per_pixel (um)': length_per_pixel,
        'rows': rows,
        'uncertainties': uncertainties.tolist()
    }
    return results_dict

def plot_length_over_time(path, results_dicts):
    if os.path.isfile(path):
        path = os.path.dirname(path)
    
    path = os.path.join(path, "plots")
    os.makedirs(path, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    titletext = "Length over Time with Prediction and Measurement of Half Intensity Point"
    fig.suptitle(titletext, position=(0.5, 0.92))

    for i, results_dict in enumerate(results_dicts):
        times = np.array(results_dict['times'])
        times_hp = results_dict['times_hp']
        lengths_hp = results_dict['lengths_hp']
        predictions = np.array(results_dict['predictions'])
        lower_bound_prediction = np.array(results_dict['lower_bound_prediction'])
        upper_bound_prediction = np.array(results_dict['upper_bound_prediction'])

        ax.plot(times_hp, lengths_hp,'o-', label=f"Half intensity point_{i}")
        line, = ax.plot(times, predictions, '-', label=f"Prediction_{i}")
        ax.fill_between(times, lower_bound_prediction, upper_bound_prediction, color=line.get_color(), alpha=0.5)

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Length [µm]")
    ax.legend()

    title = "combined bboxs"
    title = title.replace(" ", "_").replace(":", "_")
    save_path_loc = os.path.join(path, f"{title}.svg")
    fig.savefig(save_path_loc, bbox_inches='tight', dpi=300)#

    plt.show()
    plt.close()