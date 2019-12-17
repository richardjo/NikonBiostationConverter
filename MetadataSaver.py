from BiostationLibrary import MetadataRetriever, MetadataSaver

def metadata_saver(home_directory, output_directory, bf_tools_directory, use_stitching):
    y = MetadataRetriever()
    y.retrieve_files(home_directory)
    y.csv_formatting(use_stitching)
    y.retrieve_image_file_list()
    y.retrieve_magnification_values()
    y.retrieve_delta_T_values()
    y.retrieve_position_values()
    image_file_lists = y.image_file_lists
    magnification_values_lists = y.magnification_values_lists
    delta_T_lists = y.delta_T_lists
    position_x_values_lists = y.position_x_lists
    position_y_values_lists = y.position_y_lists

    for index in range(0,len(image_file_lists)):
        x = MetadataSaver(image_file_lists[index], output_directory = output_directory, use_stitching = use_stitching, position_x_list = position_x_values_lists[index], position_y_list = position_y_values_lists[index], 
        magnification_list=magnification_values_lists[index], delta_T_list = delta_T_lists[index], rows = y.rows, columns = y.columns)
        x.convert(bf_tools_directory)
        x.magnification_metadata()
        x.pixel_size_metadata()
        x.delta_T_metadata()
        x.save_metadata(bf_tools_directory)

