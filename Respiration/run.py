import data, utils, processing, metric
import numpy as np

root = 'E:/Deep_Learning/Respiration/'
data_root = f"{root}DATA/"
result_root = f"{root}RESULTS/"

num_attempts = 3 # MTG_{number}

"""PLOT"""
plot_mode = True
if plot_mode: import plot

while True:
    proceed = int(input("Please enter '1' if you want to proceed, or enter '0': "))
    print()
    if proceed == 0: break
    treatment = input("Desired Treatment Method [Type 'STATIC' or 'ARC']: ")
    print()
    breath = input("Desired Breath Type: [Type 'Breathhold' or 'FULL']: ")
    print()

    patient_path, num_fx = data.patient_path(data_root, treatment, breath)
    patient_ID = utils.extract_patientID(patient_path)
    result_folder = f"{result_root}MTG_{num_attempts}/{patient_ID}/"
    utils.createFolder(result_folder)

    with open(f"{result_folder}metric.txt", "w") as f:
        patient_path, num_fx = data.patient_path(data_root, treatment, breath)
        total_levels, total_errors = [], []

        for fx in range(1, num_fx+1):
            f.write(f"\t\t\t\t=====Fraction{fx}=====\n\n")
            fraction_path, num_fld = data.fraction_path(patient_path, fx)
            fx_lvls, fx_errs = [], []

            for field in range(1, num_fld+1):
                f.write(f"\t\t\t\t =====Field{field}=====\n")
                (data_Times, data_Amps), (beam_Times, beam_Amps) = data.read_field_data(fraction_path, field)
                beam_Times = processing.beam_modification(beam_Times)
                cutted_Amps = processing.cut_by_beams(data_Times, data_Amps, beam_Times)
                enabled_intervals, num_intvs = processing.beam_enabling_intervals(data_Times, data_Amps, beam_Times)

                for intv in range(num_intvs):
                    avg_lvl = metric.avg_lvl_per_interval(enabled_intervals[intv])
                    fitted_line = processing.regression_line(enabled_intervals[intv])
                    error = metric.error_per_interval(enabled_intervals[intv])
                    fx_lvls.append(avg_lvl)
                    fx_errs.append(error)
                    f.write(f"[Interval{intv}] Average Level (mm): {10*avg_lvl:.4f}\tVertical Distance (mm): {10*error:.4f}\n")  # cm -> mm
                
                f.write("\n")

            fx_level = np.mean(np.array(fx_lvls))
            fx_error = np.mean(np.array(fx_errs))
            total_levels.append(fx_level)
            total_errors.append(fx_error)
            f.write(f"Fraction Level (mm): {10*fx_level:.4f}\tMean Distance (mm): {10*fx_error:.4f}\n\n")     # cm -> mm

        f.write("\t\t\t\t=====Total Analysis=====\n")
        f.write(f"Reproducibility (mm): {10*metric.reproducibility(total_levels):.4f}\tStability (mm): {10*metric.stability(total_errors):.4f}\n")
        f.write("\t\t\t\t=====CV=====\n")
        f.write(f"Average Level (mm): {10*metric.coeff_var(total_levels):.4f}\tVertical Distance (mm): {10*metric.coeff_var(total_errors):.4f}\n\n")
        plot.metric_plot(result_folder, total_levels, "Avg_lvl", savefig=True)
        plot.metric_plot(result_folder, total_errors, "Vert_dist", savefig=True)
    
    print(f"Analysis on [{patient_ID}] is complete.")
    print()

print("Program terminated.")