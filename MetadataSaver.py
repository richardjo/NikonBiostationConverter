from BiostationLibrary import MetadataRetriever, MetadataSaver

def metadata_saver(home_directory, output_directory, bf_tools_directory, use_stitching, use_channels):
    rt_metadata = MetadataRetriever()
    rt_metadata.retrieve_files(home_directory, use_channels)
    rt_metadata.csv_formatting(use_stitching)
    rt_metadata.retrieve_image_file_lists()
    rt_metadata.retrieve_magnification_values()
    rt_metadata.retrieve_delta_T_values()
    rt_metadata.retrieve_position_values()
    rt_metadata.retrieve_channel_values()

    image_file_lists = rt_metadata.image_file_lists
    magnification_lists = rt_metadata.magnification_lists
    delta_T_lists = rt_metadata.delta_T_lists
    position_x_lists = rt_metadata.position_x_lists
    position_y_lists = rt_metadata.position_y_lists
    channels_lists = rt_metadata.channels_lists

    for index in range(0,len(image_file_lists)):
        ct_metadata = MetadataSaver(image_file_lists[index], output_directory = output_directory, use_stitching = use_stitching, well = index, channel_list = channels_lists[index], position_x_list = position_x_lists[index], position_y_list = position_y_lists[index], 
        magnification_list=magnification_lists[index], delta_T_list = delta_T_lists[index], rows = rt_metadata.rows, columns = rt_metadata.columns)
        ct_metadata.convert(bf_tools_directory)
        ct_metadata.magnification_metadata()
        ct_metadata.pixel_size_metadata()
        ct_metadata.delta_T_metadata()
        ct_metadata.save_metadata(bf_tools_directory)

