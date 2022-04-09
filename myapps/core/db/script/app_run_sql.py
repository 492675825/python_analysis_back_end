import pymysql


def run_query():
    host = 'localhost'
    user = 'root'
    password = '123456'
    port = 3306
    database = 'finance_analysis_20211219db'
    db = pymysql.connect(host=host, user=user, password=password, port=port,
                         database=database)
    print(db.get_host_info())
    print(db.get_server_info())
    cur = db.cursor()
    sql_01 = 'DROP TABLE IF EXISTS tbl_gold_data;'
    cur.execute(sql_01)
    sql_02 = 'CREATE TABLE tbl_gold_data LIKE temp_gold_data;'
    cur.execute(sql_02)
    sql_03 = 'INSERT INTO tbl_gold_data SELECT id, replace(item, ".","") as item, replace(replace(replace(open," ",""),",",""),"%","") as "open",replace(replace(replace(high," ",""),",",""),"%","") as "high",replace(replace(replace(low," ",""),",",""),"%","") as "low", replace(replace(replace(close," ",""),",",""),"%","") as "close", replace(up_or_down,"%","") as up_or_down, version_date from temp_gold_data;'
    cur.execute(sql_03)
    sql_04 = "truncate table tbl_au_td_gold_data;"
    cur.execute(sql_04)
    sql_05 = "insert into tbl_au_td_gold_data select id as id,version_date as version_date,item as item,cast(open as float) as open,cast(high as float) as high,cast(low as float) as low,cast(close as float) as close,cast(up_or_down as float) as up_or_down from tbl_gold_data where item = 'Au9999';"
    cur.execute(sql_05)
    sql_06 = 'truncate table tbl_au_td_gold_data_analysis;'
    cur.execute(sql_06)
    sql_07 = 'insert into tbl_au_td_gold_data_analysis select id,version_date,now() as refresh_date,item,case when open >= 10000 then open/100 when open >= 1000 then open/10 else open end as open,case when high >= 10000 then high/100 when high >= 1000 then high/10 else high end as high, case when low >= 10000 then low/100 when low >= 1000 then low/10 else low end as low, case when close >= 10000 then close/100 when close >= 1000 then close/10 else close end as close, up_or_down, case when up_or_down > 0 then 1 when up_or_down =0 then 0 when up_or_down <0 then -1 end as mapping, date_format(version_date,"%m%d") as date_number, date_format(version_date,"%Y") as year_number, date_format(version_date,"%m") as month_number, date_format(version_date,"%d") as day_number from tbl_au_td_gold_data;'
    cur.execute(sql_07)
    cur.close()

run_query()
