import pandas as pd
import os
import datetime

def ScZd_T_read(file_name, site_name, time_format):
    data = pd.read_csv(file_name, sep='\t', engine='python')
    data = data.values[1:-1]

    site_id = []
    for temp_data in data:
        site_id.append(temp_data[0][0:5])
        # temp_data = temp_data[0][6:-1]
        # temp_data = re.findall(r'.{19}', temp_data)

    index = site_id.index(site_name)
    data_frame = data[index][0][6::]

    res = []
    while len(data_frame) > 0:
        res.append(data_frame[:6])
        data_frame = data_frame[6:]

    data_result = []
    for temp_data in res:

        if temp_data.isspace():
            temp_data = '-9999.0'
            # print(temp_data)
        else:
            temp_data = temp_data
            # print(temp_data)
        data_result.append(temp_data)

    date = os.path.basename(file_name)[7:-4]

    date_time = []
    for time_i in range(0, 24):
        hours = ('%.2d' % time_i)
        datet = ('%s %s' % (date, hours))
        if time_format == 'UTC':
            datet = datetime.datetime.strptime(datet, '%Y%m%d %H') - datetime.timedelta(hours=8)
        if time_format == 'BJT':
            datet = datetime.datetime.strptime(datet, '%Y%m%d %H')
        date_time.append(datet)

    return date_time, data_result


if __name__ == '__main__':
    file_dir = r'C:\Users\ASUS\Desktop\Liu\ZdDx2020'  # 气象站点数据所在目录
    output_name = r'C:\Users\ASUS\Desktop\Liu\ZdDx2020meteorological_data_precipitation.csv'  # 输出文件路径
    site_data = r'C:\Users\ASUS\Desktop\Liu\scb_site.csv'
    time_format = 'BJT'

    site = pd.read_csv(site_data, sep=',', engine='python')
    site = pd.DataFrame(site)
    site_name = []
    site_city = []
    for temp_site in site['ID']:
        site_name.append(str(temp_site))
    for temp_site in site['NAME']:
        site_city.append(str(temp_site))

    record_book = dict()

    for site_i in range(0, len(site_name)):
        date = []
        data = []
        for filewalks in os.walk(file_dir):
            for file in filewalks[2]:
                if 'ScZd_R' in file:  # ****此处可以根据文件前缀选择日期范围
                    file_name = os.path.join(file_dir, file)
                    date_time, data_result = ScZd_T_read(file_name, site_name[site_i], time_format)
                    for i in range(0, len(date_time)):
                        date.append(date_time[i].strftime('%Y-%m-%d %H:%M'))
                        data.append(data_result[i])

        # 到此处一个站点的循环结束.获取到date和data两个列表
        if site_i == 0:  # 第一次循环往字典中加入日期
            record_book.update([('Date', date)])
        record_book.update([(site_city[site_i], data)])

    df = pd.DataFrame(record_book)
    df.to_csv(output_name, index=False)
    print('处理完毕: %s' % output_name)