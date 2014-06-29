drop table if exists settings;
create table settings (
  key text not null,
  val text null
);

-- insert data
insert into settings(key, val) values('IPType','dhcp');
insert into settings(key, val) values('IPAddress','');
insert into settings(key, val) values('IPNetMask','');
insert into settings(key, val) values('IPGateway','');
insert into settings(key, val) values('SoundVolume','50');
insert into settings(key, val) values('LEDBlink','8');
