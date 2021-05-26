import pandas as pd
import os
import datetime


def ScZd_V_read(file_name, site_name, time_format):
    data = pd.read_csv(file_name, sep='\t', encoding='unicode_escape')
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
        res.append(data_frame[:15])
        data_frame = data_frame[15:]

    ws = []
    wd = []
    for temp_data in res:
        data_result = temp_data.split('(')[0]
        wd.append(data_result[0:3])
        if data_result[0:3] == 'PPC' or data_result[0:3] == '   ':
            ws.append(-9999.0)
        else:
            # print(data_result[3::])
            ws.append(float(data_result[3::]) * 0.1)

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
    # print(file_name)
    # print(wd)
    # print(len(wd))

    return date_time, wd, ws


if __name__ == '__main__':
    file_dir = r'meteorological_data'  # 气象站点数据所在目录
    output_name = r'meteorological_data_windspeed.csv'  # 输出文件路径
    site_data = r'scb_site.csv'
    time_format = 'UTC'

    site = pd.read_csv(site_data, sep=',')
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
        wd_data = []
        ws_data = []
        for filewalks in os.walk(file_dir):
            for file in filewalks[2]:
                if 'ScZd_V_' in file:
                    file_name = os.path.join(file_dir, file)
                    date_time, wd, ws = ScZd_V_read(file_name, site_name[site_i], time_format)
                    # print(type(date_time[0]))
                    for i in range(0, len(date_time)):
                        temp_time = pd.to_datetime(date_time[i])
                        temp_time = temp_time
                        # temp_time = temp_time - datetime.timedelta(hours=8)
                        date.append(temp_time.strftime('%Y-%m-%dT%H:%M:%SZ'))
                        wd_data.append(wd[i])
                        ws_data.append(ws[i])
        # 到此处一个站点的循环结束.获取到date和data两个列表
        if site_i == 0:  # 第一次循环往字典中加入日期
            record_book.update([('Date', date)])
        record_book.update([(site_city[site_i], ws_data)])

    df = pd.DataFrame(record_book)
    df.to_csv(output_name, index=False)
    print('处理完毕: %s' % output_name)