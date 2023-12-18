from datetime import datetime

import pandas as pd

from file_upload.Utils.CountryDataDetail import row_data


def sort_df_header(dataframe):
    '''
    将pandas DataFrame对象的列名按照row_data中的index进行排序, 并返回排序后的顺序列表
    dataframe: pandas DataFrame对象
    '''
    # 输入参数验证，必须是pandas DataFrame对象
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError('dataframe must be a pandas DataFrame object')

    sort_list = []

    for column in dataframe.columns:
        new_column = column.lower().replace(" ", "")

        count = 0
        for row in row_data:
            new_row = row['name'].lower().replace(" ", "")

            if new_column != new_row:
                count += 1
            elif new_column == new_row:
                sort_list.append(row['name'])
                continue

            if count == len(row_data):
                sort_list.append('index')
                count = 0

    dataframe.columns = sort_list
    print(dataframe.columns)
    return sort_list


def convert_to_percentage(dataframe, row_list):
    '''
    转换成保留两位的百分比形式
    '''
    orders_wow = row_list[4]['name']
    turnover = row_list[5]['name']
    turnover_YoY = row_list[7]['name']
    orders_YoY = row_list[8]['name']
    orders_YoY_weekday = row_list[9]['name']
    turnover_YoY_weekday = row_list[10]['name']

    need_to_convert = [orders_wow, turnover, turnover_YoY,
                       orders_YoY, orders_YoY_weekday, turnover_YoY_weekday]
    # 将output中的每一项数据都按照need_to_convert列表中的值，转换成保留两位的百分比形式
    for item in need_to_convert:
        dataframe[item] = dataframe[item].apply(lambda x: '{:.2%}'.format(x))

    return dataframe


def compare_times(time_str1, time_str2):
    '''
    对比时间
    '''
    if pd.notna(time_str1):
        if time_str1 == 0:
            return 0

        time1 = datetime.strptime(str(time_str1), '%H:%M:%S')
        time2 = datetime.strptime(time_str2, '%H:%M:%S')

        if time1 < time2:
            return 1
        elif time1 > time2:
            return 0
        else:
            return 1


def filter_data(dataframe, data_type):
    '''
    筛选数据
    dataframe: pandas DataFrame对象
    data_type: 需要处理的数据类型
    return: output, None
    '''

    orders = row_data[2]['name']
    orders_wow = row_data[4]['name']
    turnover = row_data[5]['name']
    last_time = row_data[6]['name']

    # 定义不同data_type对应的过滤条件
    filters = {
        'increase': (dataframe[orders_wow] > 1) | (dataframe[turnover] > 1),
        'turnover drop': dataframe[turnover] < -0.2,
        'order drop': dataframe[orders_wow] < -0.2,
        'zero order': dataframe[orders] == 0,
        'last time': dataframe[last_time].apply(compare_times, args=('08:00:00',)) == 1,
    }

    try:
        # 根据data_type获取对应的过滤条件
        filter_condition = filters[data_type]
        output = dataframe[filter_condition]
    except KeyError:
        # 如果data_type不存在于字典中，则表示输入的data_type无效，返回相应的失败原因
        return None, f"Invalid data_type: '{data_type}'"

    return output, None


def get_informations(data, row_list, data_type, title):
    '''
    获取信息
    data: pandas DataFrame对象
    row_list: 需要处理的表格的表头
    data_type: 需要处理的数据类型
    title: 需要处理的数据类型对应的标题
    '''

    output, error = filter_data(dataframe=data, data_type=data_type)
    print(error)

    # output = output.drop_duplicates().sort_values(by='index')

    output = convert_to_percentage(dataframe=output, row_list=row_list)

    # 将'Countries with >100% increase:'这句话添加到output的第一行,并加粗
    output = pd.concat([pd.DataFrame([[title]], columns=['index']), output])
    # output = output.style.applymap(lambda x: 'font-weight: bold' if x == title else '')

    return output


def output_to_excel(dataframe):
    '''
    输出成EXCEL
    dataframe: pandas DataFrame对象
    '''
    # dataframe.columns = [row['name'] for row in row_data]
    sort_df_header(dataframe)

    # 将每一项中的NaN替换成0
    dataframe.fillna(0)

    increase = get_informations(data=dataframe, row_list=row_data, data_type='increase',
                                title='Countries with >100% increase:')
    turnover_drop = get_informations(data=dataframe, row_list=row_data, data_type='turnover drop',
                                     title='Countries with <-20% turnover drop:')
    order_drop = get_informations(data=dataframe, row_list=row_data, data_type='order drop',
                                  title='Countries with <-20% order drop:')
    zero_order = get_informations(data=dataframe, row_list=row_data, data_type='zero order',
                                  title='Countries with 0 order:')
    last_time_data = get_informations(data=dataframe, row_list=row_data, data_type='last time',
                                      title='Last order time > 1 hour:')

    # 输出成excel
    merged_data = pd.concat(
        [increase, turnover_drop, order_drop, zero_order, last_time_data], ignore_index=True)

    return merged_data
