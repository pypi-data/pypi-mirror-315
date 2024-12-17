import pandas as pd
from datetime import datetime, timedelta, time
import sys
import os, time
import exchange_calendars
from datetime import date
from lyylog import log, logerr
Trading_Calendars_cache_file = r"D:\UserData\resource\gui\trader_xshs.pkl"

from cachetools import TTLCache, cached

cache = TTLCache(maxsize=100, ttl=300)  # 最多100项，每项保存300秒


class lyycalendar_class:
    def __init__(self, cache_file=Trading_Calendars_cache_file, debug=False):
        self.cache_file = cache_file 
        expiry_duration = 3600 * 24 * 100
        self.calendar_df = self.get_df_calendars(self.cache_file, expiry_duration=expiry_duration, debug=debug).copy()

        if debug: print(self.calendar_df)
        # 创建DataFrame，并添加dayint列
        # self.calendar_df = pd.DataFrame({'dayint': dayint, 'date': dates})

    def get_df_calendars(self, file_path, expiry_duration, debug=False):
        if debug: log("in get_df_calendars, file_path=", file_path)

        # 检查文件是否存在,expiry_duration=3600意味着1小时。
        if os.path.isfile(file_path):
            if debug: log("file exists, check expiry duration")
            last_modified_time = os.path.getmtime(file_path)
            # 计算当前时间与最后修改时间的差值（秒）
            current_time = time.time()
            time_difference = current_time - last_modified_time
            if time_difference < expiry_duration:
                df_calendars = pd.read_pickle(file_path)
                if debug:
                    log("[get_df_calendars] calendar not expired, return it, good df_calendar=\n", df_calendars)
                return df_calendars

        if debug:
            logerr("[get_df_calendars] calendars cache file not exists or expired, try to upgrade it by exchange_calendars")
        cache_dir = os.path.dirname(file_path)
        if debug: log("dirname=", cache_dir)

        if not os.path.exists(cache_dir) and cache_dir != "":
            log(f"dir create dir <" + cache_dir + ">")
            os.makedirs(cache_dir)
        today = date.today()
        half_year_ago, half_year_later = today - timedelta(days=182), today + timedelta(days=182)
        self.calendar_df = exchange_calendars.get_calendar("XSHG").schedule.loc[half_year_ago:half_year_later]
        if debug:
            log("[get_df_calendars] calendar update successfully, new df_calendar=\n", df_calendars)
                    # 提取日期部分并转换为字符串格式
        self.calendar_df.loc[:, "date"] = self.calendar_df["open"].dt.strftime("%Y-%m-%d")
        # 将date列转换为整数格式
        self.calendar_df.loc[:, "dayint"] = self.calendar_df["date"].str.replace("-", "").astype(int)
        self.calendar_df["sn"] = range(0, len(self.calendar_df))
        self.calendar_df.to_pickle(file_path)
        return self.calendar_df

    def 今天开盘且不完整(self):
        """
        判断今天是不是未结束的交易日，是则返回真。is_today_unfinished_trading_day
        """
        today = datetime.now()
        today_str = today.strftime("%Y%m%d")  # 使用字符串格式，避免转换为整数的潜在问题
        trading_days = self.calendar_df["dayint"].astype(str)  # 确保日期格式一致
        # 检查今天是否为交易日，并且当前时间在9点到15点之间
        if today_str in trading_days and 9 < today.hour < 15:
            return True
        else:
            return False

    def day8to10(self, day8):
        """
        把8位的整数或者Str格式的日期，转换成带分隔符"-"的字符串格式的日期：20221013 to 2022-10-13
        """
        day8 = str(day8)
        return day8[0:4] + "-" + day8[4:6] + "-" + day8[6:8]


    def any_date_to_int_multi(self, *any_dates, debug=False):
        """
        将任意日期转换为前8位整数，支持多个日期输入。
        """
        if debug: log("[any_date_to_int_multi] any_dates=", any_dates, "type=", type(any_dates)   )
        result = []
        for any_date in any_dates:
            # 直接调用 any_date_to_int 函数进行转换
            converted_date = int(str(any_date).replace("-", "")[:8])
            result.append(converted_date)
            if debug: log(f"[any_date_to_int_multi] Converted date: {any_date} to {converted_date}")

        return result[0] if len(result) == 1 else tuple(result)        # 如果 result 只有一个元素，直接返回该元素，否则返回元组


    def get_nearest_trading_date(self, date, debug=False):
        """
        找到交易日历中往前小于且最接近date的日期
        """

        if debug: log("[get_nearest_trading_date] 参数 date=", date, "type=", type(date))
        date_int = self.any_date_to_int_multi(date)
        if debug: log("[get_nearest_trading_date] date_int=", date_int)

        # 创建布尔索引数组
        mask = self.calendar_df["dayint"] <= date_int

        # 使用布尔索引过滤DataFrame
        filtered_df = self.calendar_df[mask]
        if filtered_df.empty:
            logerr("[get_nearest_trading_date] No dates found less than or equal to", date_int)
            return None  # 或者抛出异常，取决于你的需求

        # 找到最接近的日期
        closest_date_int = filtered_df['dayint'].max()
        if debug: log("[get_nearest_trading_date] closest_date_int=", closest_date_int)
        return closest_date_int


    def get_nearest_trading_date_from_datetime(self, date_time_str="now",debug=False):
        """
        区分工作时间，来计算最近收盘日。任意%Y-%m-%d %H:%M:%S时间，找到最接近该时间的完整收盘日,支持字符串格式和日期时间格式
        """

        if date_time_str == "now":
            date_time_str = datetime.now()
            log("now", date_time_str, type(date_time_str))
        elif isinstance(date_time_str, str):
            date_time_str = date_time_str[:19]
            date_time_str = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
            log("date_time_str = ",date_time_str,", type=", type(date_time_str))


        date = date_time_str.date()
        hour = date_time_str.hour
        valid_date = date - timedelta(days=1)        if hour < 15 else date
        if debug:
            log("[get_nearest_trading_date_from_datetime] 考虑到时间问题，valid_date=", valid_date, "hour=", hour)   
        return self.get_nearest_trading_date(valid_date, debug=debug)
        

    def 东财最后数据归属日(self):
        """
        ak库东财模块能获取最后行情。本函数计算该行情属于哪个日期。如果今天是周末，则是上周五。如果昨天是工作日，今天也是，但今天还没开盘，则是昨天。如果今天已经开始有数据了，则是今天。
        """
        now = datetime.now()
        date_int = self.any_date_to_int_multi(now)
        df = self.calendar_df[self.calendar_df["dayint"] <= date_int]
        lastindex = len(df) - 1
        target_time = now.replace(hour=9, minute=25, second=0, microsecond=0)
        if now < target_time and df.iloc[lastindex]["dayint"] == self.any_date_to_int_multi(now):
            lastindex = lastindex - 1
        return df.iloc[lastindex]["dayint"]

    def get_sn_of_date(self, date, debug=False):
        """
        获取日期在日历中的索引，并返回对应的sn列的值。
        如果日期不存在于日历中，将引发一个异常。
        如果直接用[列名]取列，则它是一个包含 sn 值的 pandas.Series 或者 pandas.Index，而不是单个 sn 值。应该使用 .iloc[0] 来获取第一个元素，或者如果只有一个匹配项，直接使用 .values[0] 或 [0] 来获取值。
        """
        date_int = self.any_date_to_int_multi(date)
        date_int = self.get_nearest_trading_date(date_int)  # 假设这是另一个辅助函数
        if debug:
            print("[get_index_of_date] date_int=", date_int)

        # 检查是否存在匹配的索引，并获取sn列的值
        matching_sn_values = self.calendar_df[self.calendar_df["dayint"] == date_int]["sn"]
        
        if matching_sn_values.empty:
            raise ValueError(f"日期 {date} 不在日历中。")
        if debug:
            print("[get_index_of_date] matching_sn_values=", matching_sn_values.iloc[0])

        # 返回第一个匹配的sn值
        return matching_sn_values.iloc[0]  # 或者 matching_sn_values.values[0] 或 matching_sn_values[0]
    
    def get_index_series_of_date(self, date, debug=False):
        """
        获取日期在日历中的索引，并返回对应的sn列的值。
        如果日期不存在于日历中，将引发一个异常。
        如果直接用[列名]取列，则它是一个包含 sn 值的 pandas.Series 或者 pandas.Index，而不是单个 sn 值。应该使用 .iloc[0] 来获取第一个元素，或者如果只有一个匹配项，直接使用 .values[0] 或 [0] 来获取值。
        """
        date_int = self.any_date_to_int_multi(date)
        date_int = self.get_nearest_trading_date(date_int)  # 假设这是另一个辅助函数
        if debug:
            log("[get_index_of_date] date_int=", date_int)

        # 检查是否存在匹配的索引，并获取sn列的值
        matching_sn_values = self.calendar_df[self.calendar_df["dayint"] == date_int]["sn"]      

        # 返回第一个匹配的sn值
        return matching_sn_values  # 或者 matching_sn_values.values[0] 或 matching_sn_values[0]

    def get_trading_day_before_n_days(self, days, get_column="dayint", debug=False):
        """找到df中day为date的数据，并向前找到第{days}个值的dayint字段"""
        # 找到当前日期的dayint
        today_int = self.any_date_to_int_multi(datetime.now())
        index = self.get_sn_of_date(today_int, debug=debug)

        start = index - days
        if debug: log("start=", start, "index=", index, "days=", days)
        # 向前找到第{days}个值的dayint字段
        if start < 0:
            raise ValueError("向前查找的天数超出了DataFrame的范围。考虑修改函数使用绝对值或者事先确保参数为正数。")
      
        # 返回正确索引的dayint字段值
        return self.calendar_df.loc[self.calendar_df.index[start], get_column]
    
    
    @cached(cache)
    def 计算相隔天数(self, start_date, end_date, debug=False):
        """
        计算相隔天数
        """
        start_date, end_date = self.any_date_to_int_multi(start_date, end_date)
        # 找到 start_date 和 end_date 在 calendar_df 中最近的有效日期
        start_dayint = self.get_nearest_trading_date(start_date)
        start_dayint_sn = self.get_sn_of_date(start_dayint, debug=debug)
        end_dayint = self.get_nearest_trading_date(end_date)
        end_dayint_sn = self.get_sn_of_date(end_dayint, debug=debug)

        if debug: log("result = ", abs(start_dayint_sn - end_dayint_sn))
        return abs( start_dayint_sn-end_dayint_sn)
    
    def calc_days(self, start_date, end_date):

        def days_between(date1, date2):
            d1 = datetime.strptime(date1, "%Y%m%d")
            d2 = datetime.strptime(date2, "%Y%m%d")
            log("abs(d2-d1)=", abs(d2 - d1).days)
            return abs((d2 - d1).days)

        today = datetime.now().strftime("%Y%m%d")
        current_time = datetime.now().time()

        if today in self.calendar_df["day"].values:
            if current_time < datetime.time(9, 25):
                result = days_between(self.calendar_df[self.calendar_df["day"] == today].iloc[-1]["dayint"], today)
            else:
                result = days_between(self.calendar_df[self.calendar_df["day"] == today]["dayint"].iloc[0], today)
        else:
            result = days_between(self.calendar_df[self.calendar_df["day"] < today]["dayint"].iloc[-1], today)

        log(result)




    def find_nearest_previous_date(self, date_int: int, return_format="date_int", debug=False):
        """
        找到日历中小于等于给定日期的最接近日期。要注意，跟最近完整收盘数据日期不同，这里只是去日历中匹配最接近日期，而不管这天的时间是否收盘
        :param date_int: 输入日期，格式为整数 YYYYMMDD。
        :param return_format: 返回格式，可以为 "date_int"（默认）、"date_str"（字符串格式日期）或 "sn"（自然序号）。
        :param debug: 是否打印调试信息，默认关闭。
        :return: 最接近的日期，根据 return_format 返回相应格式。
        """
        # 根据 return_format 的值，设置需要返回的列名
        if return_format == "sn":
            filtered_df = self.calendar_df[self.calendar_df["dayint"] <= date_int]
            if filtered_df.empty:
                if debug:
                    log("No dates found less than or equal to", date_int)
                return None
            result = filtered_df.iloc[-1]["sn"]
            if debug:
                log("Nearest previous date (SN) =", result)
            return result
        
        column_name = "dayint" if return_format == "date_int" else "day"
        
        filtered_df = self.calendar_df[self.calendar_df["dayint"] <= date_int]
        if filtered_df.empty:
            if debug:
                log("No dates found less than or equal to", date_int)
            return None
        
        result = filtered_df.iloc[-1][column_name]
        if debug:
            log("Nearest previous date ({}) =".format(return_format), result)
        
        return result
  

    def if_in_notfull_time(self, t=None):
        """
        判断时间是否符合：1.当天开盘 且 2.还未收盘
        """
        if t is None:
            t = datetime.now()

        if isinstance(t, str):
            t = datetime.strptime(t, "%Y-%m-%d %H:%M:%S")

        dayint = t.year * 10000 + t.month * 100 + t.day
        timeint = t.hour * 100 + t.minute
        if dayint in self.calendar_df["dayint"].to_list() and 925 <= timeint <= 1530:
            return True
        else:
            return False
        

    def calculate_stock_time_later(self, current_time, seconds):
        #  转换为datetime对象
        current_time = datetime.strptime(current_time, "%H:%M:%S")

        #  计算当前时间加上秒数后的时间
        future_time = current_time + timedelta(seconds=seconds)

        #  判断是否处于股票开盘时间
        if future_time.hour < 9 or (future_time.hour == 9 and future_time.minute < 30):
            #  如果是，则将其调整为开盘时间
            future_time = future_time.replace(hour=9, minute=30, second=0, microsecond=0)
        else:
            #  如果是下午，且超过15:00，则将其调整为第二天早上9:30
            if future_time.hour >= 15:
                future_time = future_time + timedelta(days=1)
                future_time = future_time.replace(hour=9, minute=30, second=0, microsecond=0)

        return future_time.strftime("%H:%M:%S")

    def get_date_ndays_ago(self, n_days, start_date, debug=False):
        """获取若干天前的自然日期，返回datetime对象。如果未指定开始日期，则默认为当前日期。"""
        if start_date is None:
            start_date = datetime.now()
        date_n_days_ago = start_date - timedelta(days=n_days)
        if debug: log("result date_n_days_ago=", date_n_days_ago)
        return date_n_days_ago

    @cached(cache)
    def 最近有完整收盘数据日期(self, return_format="date_int", debug=False):
        """
        返回小于或等于今天的最近完整收盘日。如果今天是开盘日，则开市时间的完整收盘日为前一开盘日。因为当时并没有完整收盘数据。
        """
        now = datetime.now()        
        target_date = now if now.hour>15 else self.get_date_ndays_ago(1, start_date=now) 
        today_int = int(target_date.strftime("%Y%m%d"))
        closest_date = self.find_nearest_previous_date(today_int, return_format=return_format, debug=debug)
        return closest_date


lyytc = lyycalendar_class(cache_file=Trading_Calendars_cache_file, debug=False)

if __name__ == "__main__":

    
    #result = lyytc.get_nearest_trading_date_from_datetime("2024-07-07 13:58:01",debug=True)
    #print("result=", result)
    #lyytc.get_sn_of_date(20240707, debug=True)
    result = lyytc.get_trading_day_before_n_days(1, debug=False)
    print("get_trading_day_before_n_days main result=", result)
    #result = lyytc.计算相隔天数("2024-07-07", "2024-07-03", debug=True)#done
    result  = lyytc.最近有完整收盘数据日期()
    print("最近有完整收盘数据result=", result)
    #log(lyytc.最近完整收盘日(return_format="date_int"))
    # 调用库中的函数，将参数传递给它们
    #log(lyytc.tc_before_today(0))
    #lyytc.计算相隔天数("2024-04-04", "2024-04-07", debug=True)
    #lyytc.计算相隔天数_byIndex("2024-04-04", "2024-04-07", debug=True)
    # # 创建 lyycalendar_class 的实例并在初始化时获取数据
    # today = datetime.now().date()
    # # 前200天日期
    # previous_date = today - timedelta(days=200)

    # # 后200天日期
    # next_date = today + timedelta(days=200)

    # previous_date_str = previous_date.strftime("%Y-%m-%d")
    # next_date = today + timedelta(days=200)
    # next_date_str = next_date.strftime("%Y-%m-%d")

    # import exchange_calendars as xcals
    # xshg = xcals.get_calendar("XSHG")

    # df = xshg.schedule.loc[previous_date_str:next_date_str]
    # dates = df.index
    # # 将DatetimeIndex转换为整数格式（假设格式为YYYYMMDD）
    # dayint = dates.strftime("%Y%m%d").astype(int)

    # # 创建DataFrame，并添加dayint列
    # df = pd.DataFrame({
    #     'dayint': dayint,
    #     'date': dates
    # })

    # log(lyytc.计算相隔天数_byIndex("2023-10-27", "2023-10-28", debug=True))

    # log("close to 20230101", 日历中最接近某天("2023-01-01"))
    # log("tc=", tc_before_today(50, True))
    # start_date = "2023-01-01"
    # end_date = "2023-02-02"
    # n = 计算相隔天数(start_date, end_date)
    # log(n)
