--query code
create view top_10_count as
select t.tag_name, t_count.count
from tags as t
inner join (select tag_id, count(*)
from quote_tag_relation 
group by tag_id
order by count(*) desc) as t_count on t_count.tag_id = t.tag_id
order by count desc
limit 10;