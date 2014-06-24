drop table if exists settings;
create table settings (
  id integer primary key autoincrement,
  key text not null,
  val text null
);