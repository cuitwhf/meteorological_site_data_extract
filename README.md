# meteorological_site_data_extract

本程序集用于提取叶师兄提供的国控站气象数据要素。

# meteorological_site_data_extract_temperature.py

用于提取温度要素，文件名以`ScZd_T`为前缀的文件。

在`if __name__ == '__main__':`后进行参数输入：

file_dir：气象站点数据文件存放目录。

output_name：输出数据路径。

site_data：气象数据站点信息，本程序中使用其站点ID和站点名称。格式参见scb_site.csv

time_format：此处可选择北京时间`time_format = 'BJT'`或者世界时间`time_format = 'UTC'`。

# metorological_site_data_extract_windspeed.py

用于提取温度要素，文件名以`ScZd_V`为前缀的文件。

在`if __name__ == '__main__':`后进行参数输入：

file_dir：气象站点数据文件存放目录。

output_name：输出数据路径。

site_data：气象数据站点信息，本程序中使用其站点ID和站点名称。格式参见scb_site.csv

time_format：此处可选择北京时间`time_format = 'BJT'`或者世界时间`time_format = 'UTC'`。
