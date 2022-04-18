-- 用shell命令导出excel：
-- echo "select * from finance_analysis_20211219db.tbl_d_au_td_gold_data_analysis" | mysql -h127.0.0.1 -uroot -p123456 > C:/Users/xiongyuan/Desktop/gold_data.xlsx
-- 非严格模式 
-- SET @@global.sql_mode= '';

-- select * from temp_gold_data;
-- temp_gold_data
-- 01 删除并创建 tbl_gold_data
-- 去空格，去百分号，去逗号
DROP TABLE IF EXISTS finance_analysis_20211219db.tbl_gold_data;
CREATE TABLE finance_analysis_20211219db.tbl_gold_data LIKE finance_analysis_20211219db.temp_gold_data;
INSERT INTO finance_analysis_20211219db.tbl_gold_data
SELECT 
id, 
replace(item, ".","") as item, 
replace(replace(replace(open," ",""),",",""),"%","") as "open",  
replace(replace(replace(high," ",""),",",""),"%","") as "high",
replace(replace(replace(low," ",""),",",""),"%","") as "low", 
replace(replace(replace(close," ",""),",",""),"%","") as "close", 
replace(up_or_down,"%","") as up_or_down,
version_date 
from finance_analysis_20211219db.temp_gold_data;

-- 02 清空并创建 tbl_au_td_gold_data
truncate table finance_analysis_20211219db.tbl_au_td_gold_data;
insert into finance_analysis_20211219db.tbl_au_td_gold_data
select 
id as id,
version_date as version_date,
item as item,
cast(open as float) as open,
cast(high as float) as high,
cast(low as float) as low,
cast(close as float) as close,
cast(up_or_down as float) as up_or_down
from tbl_gold_data
where item = 'Au9999';

-- 03 清空并创建 tbl_au_td_gold_data_analysis
truncate table finance_analysis_20211219db.tbl_au_td_gold_data_analysis;
insert into finance_analysis_20211219db.tbl_au_td_gold_data_analysis
select 
	id,
	version_date,
    now() as refresh_date,
	item,
    case 
		when open >= 10000 then open/100
        when open >= 1000 then open/10
        else open
        end as open,
	case 
		when high >= 10000 then high/100
        when high >= 1000 then high/10
        else high
        end as high,
    case 
		when low >= 10000 then low/100
        when low >= 1000 then low/10
        else low
        end as low,
	case 
		when close >= 10000 then close/100
        when close >= 1000 then close/10
        else close
        end as close,
	up_or_down,
	case
		when up_or_down > 0 then 1
		when up_or_down =0 then 0
		when up_or_down <0 then -1
		end as mapping,
	date_format(version_date,"%m%d") as date_number,
    date_format(version_date,"%Y") as year_number,
    date_format(version_date,"%m") as month_number,
    date_format(version_date,"%d") as day_number
from finance_analysis_20211219db.tbl_au_td_gold_data;

-- 04 清空并创建 tbl_d_au_td_gold_data_analysis
truncate table finance_analysis_20211219db.tbl_d_au_td_gold_data_analysis;
insert into finance_analysis_20211219db.tbl_d_au_td_gold_data_analysis
select id,date_number, sum(mapping)
from finance_analysis_20211219db.tbl_au_td_gold_data_analysis
group by date_number
order by date_number;

-- 05 清空并插入数据 tbl_y_au_td_gold_data_analysis
truncate table finance_analysis_20211219db.tbl_y_au_td_gold_data_analysis;
insert into finance_analysis_20211219db.tbl_y_au_td_gold_data_analysis
select id, year_number, sum(mapping)
from finance_analysis_20211219db.tbl_au_td_gold_data_analysis
group by year_number
order by year_number;

-- 06 清空并插入 tbl_y_au_td_average_analysis
truncate table finance_analysis_20211219db.tbl_y_au_td_average_analysis;
insert into finance_analysis_20211219db.tbl_y_au_td_average_analysis
select id, year_number, avg(close)
from finance_analysis_20211219db.tbl_au_td_gold_data_analysis
group by year_number
order by year_number;

-- 07 清空并插入 select * from tbl_d_au_td_year_and_month_mapping;
truncate table finance_analysis_20211219db.tbl_d_au_td_year_and_month_mapping;
insert into finance_analysis_20211219db.tbl_d_au_td_year_and_month_mapping
select id,year_number,month_number, sum(mapping) as mapping_sum
from finance_analysis_20211219db.tbl_au_td_gold_data_analysis
group by year_number,month_number
order by year_number, month_number;

-- 08 清空并插入 select * from tbl_m_au_td_gold_data_mapping order by month_number;
truncate table finance_analysis_20211219db.tbl_m_au_td_gold_data_mapping;
insert into finance_analysis_20211219db.tbl_m_au_td_gold_data_mapping
with temp_table_01 as (
select id,month_number, sum(mapping_sum) as sum, avg(mapping_sum) as average
from finance_analysis_20211219db.tbl_d_au_td_year_and_month_mapping
group by month_number
),temp_table_02 as (
select id,month_number, mapping_sum as current_sum_mapping from finance_analysis_20211219db.tbl_d_au_td_year_and_month_mapping
where year_number = (select max(year_number) from finance_analysis_20211219db.tbl_d_au_td_year_and_month_mapping)
)
select a.id, a.month_number, b.current_sum_mapping, a.average, a.sum
from temp_table_01 a
left join temp_table_02 b
on a.month_number = b.month_number;


-- 09 清空并插入数据到 tbl_d_news_cctv_union_all
truncate table finance_analysis_20211219db.tbl_d_news_cctv_union_all;
insert into finance_analysis_20211219db.tbl_d_news_cctv_union_all
with temp_table_02 as (
	select version_date, title, brief, keyword, url, refresh_date,news_type from finance_analysis_20211219db.tbl_d_news_cctv_world
	union all 
	select version_date, title, brief, keyword, url, refresh_date,news_type from finance_analysis_20211219db.tbl_d_news_cctv_china
	union all 
	select version_date, title, brief, keyword, url, refresh_date,news_type from finance_analysis_20211219db.tbl_d_news_cctv_economy
)
select version_date, title, brief, keyword, url, refresh_date,news_type from temp_table_02;





