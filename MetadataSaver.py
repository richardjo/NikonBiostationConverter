from BiostationLibrary import MetadataRetriever, MetadataSaver

def metadata_saver(home_directory, output_directory, bf_tools_directory, use_stitching):
    rt_metadata = MetadataRetriever()
    rt_metadata.retrieve_files(home_directory)
    rt_metadata.csv_formatting(use_stitching)
    rt_metadata.retrieve_image_file_list()
    rt_metadata.retrieve_magnification_values()
    rt_metadata.retrieve_delta_T_values()
    rt_metadata.retrieve_position_values()
    image_file_lists = rt_metadata.image_file_lists
    magnification_values_lists = rt_metadata.magnification_values_lists
    delta_T_lists = rt_metadata.delta_T_lists
    position_x_values_lists = rt_metadata.position_x_lists
    position_y_values_lists = rt_metadata.position_y_lists

    for index in range(0,len(image_file_lists)):
        ct_metadata = MetadataSaver(image_file_lists[index], output_directory = output_directory, use_stitching = use_stitching, position_x_list = position_x_values_lists[index], position_y_list = position_y_values_lists[index], 
        magnification_list=magnification_values_lists[index], delta_T_list = delta_T_lists[index], rows = rt_metadata.rows, columns = rt_metadata.columns)
        ct_metadata.convert(bf_tools_directory)
        ct_metadata.magnification_metadata()
        ct_metadata.pixel_size_metadata()
        ct_metadata.delta_T_metadata()
        ct_metadata.save_metadata(bf_tools_directory)

