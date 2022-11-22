create login MusicUser
with password='123',
default_database = MMS

use MMS;
create user MUser
for login MusicUser
with default_schema = guest;

grant select
on Album
to MUser;

grant select,update,insert,delete
on comment
to MUser;

grant select
on Label
to MUser;

grant select
on MID_AID
to MUser;

grant select,update,insert,delete
on MID_CID
to MUser;

grant select
on MID_MMID
to MUser;

grant select
on Music
to MUser;

grant select
on MusicMaker
to MUser;

grant select,update,insert,delete
on Sheet
to MUser;

grant select,update,insert,delete
on SID_MID
to MUser;

grant select,update,insert,delete
on UID_CID
to MUser;

grant select,update,insert,delete
on UID_SID_Create
to MUser;

grant select,update
on User
to MUser;