drop table if exists settings;
create table settings (
  key text not null,
  val text null
);

-- insert data
insert into settings(key, val) values('Volume','50');
insert into settings(key, val) values('LEDBlink','8');
