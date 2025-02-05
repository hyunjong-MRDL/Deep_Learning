import os, data, utils, processing, metrics

root = "D:/Datasets/CT_Recon/Breast/"

plot_mode = False

exit_flag = 1
while True:
    exit_flag = int(input("If you want to terminate this program, please enter 0, or else enter 1: "))
    if exit_flag == 0: break
    id_idx = int(input(f"Select the patient number (there are {len(os.listdir(root))} patients currently): "))
    print()
    print("Reference data\n")
    recon_1 = input("Desired Reconstruction Method [Type 'Aice' or 'AIDR']: ")
    seg_1 = input("Desired Segmentation Method: [Type 'Breast' or 'Onco']: ")
    print()
    print("Comparative data\n")
    recon_2 = input("Desired Reconstruction Method [Type 'Aice' or 'AIDR']: ")
    seg_2 = input("Desired Segmentation Method: [Type 'Breast' or 'Onco']: ")
    print()

    path_1 = data.get_RT_path(root, id_idx, recon_1, seg_1)  # ID1_Aice_manual
    ID1 = path_1.split("/")[4]
    path_2 = data.get_RT_path(root, id_idx, recon_2, seg_2)  # ID1_AIDR_manual
    ID2 = path_2.split("/")[4]

    structures_1 = data.get_ROI_structures(path_1)
    contours_1 = data.get_ROI_contours(path_1)

    structures_2 = data.get_ROI_structures(path_2)
    contours_2 = data.get_ROI_contours(path_2)

    total_contours_1 = data.get_contour_data(contours_1)
    total_contours_2 = data.get_contour_data(contours_2)

    roi_namedict_1 = utils.get_ROI_names(path_1)
    roi_namedict_2 = utils.get_ROI_names(path_2)
    print("AI_Manual:")
    utils.print_ROI_names(roi_namedict_1)
    print("IR_Manual:")
    utils.print_ROI_names(roi_namedict_2)

    # matched_roi_names = utils.match_ROIs(roi_namedict_1, roi_namedict_2)
    # utils.print_ROI_names(matched_roi_names)

    # ROI_num = int(input("Interested ROI number: "))
    # print()

    if plot_mode:
        utils.plot_coordinates(ID1, recon_1, seg_1, total_contours_1)
        utils.plot_coordinates(ID2, recon_2, seg_2, total_contours_2)

print("Program terminated.")