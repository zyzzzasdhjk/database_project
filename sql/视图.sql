create view V$_getPlaylistMusicData
as
	select Sheet.SID,Music.MID,MName,MTime,MDate,MMName,MDir
	from Sheet,SID_MID,Music,MID_MMID,MusicMaker
	where Sheet.SID = SID_MID.SID and Music.MID = SID_MID.MID
	and Music.MID = MID_MMID.MID and MusicMaker.MMID = MID_MMID.MMID


create view V$_getMusicComment
as
	select Music.MID,CContent
	from Music,MID_CID,Comment
	where Music.MID = MID_CID.MID and Comment.CID = MID_CID.CID


create view V$_getSheetMusicNum
as
	select Sheet.SID, count(Music.MID) as MusicNum
	from Sheet, SID_MID, Music
	where Sheet.SID = SID_MID.SID and Music.MID = SID_MID.MID
	group by Sheet.SID


create view V$_getUserInformation
as
    select Account_Password.UID, Account, Password, UName, USex, UIntro, UBirthday, UIsVip, Ltext
    from Account_Password, UserInfo, Label
    where Account_Password.UID = UserInfo.UID and UserInfo.LID = Label.LID


create view V$_getSheetUserCreateInfo
as
	select Sheet.SID, SName, SIntro, SFavor, UName
	from Sheet,UID_SID_Create,UserInfo
	where Sheet.SID = UID_SID_Create.SID and UserInfo.UID = UID_SID_Create.UID


create view V$_getMusicData
as
	select Music.MID, MName,MMName,MDate,AName,MDir
	from Music,MID_MMID,MusicMaker,MID_AID,Album
	where Music.MID = MID_MMID.MID and MID_MMID.MMID = MusicMaker.MMID
	and Music.MID = MID_AID.AID and Album.AID = MID_AID.AID


create view V$_getUserAllCreateSheet
as
	select Sheet.SID, Sheet.SName,UserInfo.UID
	from Sheet, UID_SID_Create, UserInfo
	where Sheet.SID = UID_SID_Create.SID and UserInfo.UID = UID_SID_Create.UID


create view V$_getUserAllFavorSheet
as
	select Sheet.SID, Sheet.SName,UserInfo.UID
	from Sheet, UID_SID_Favor, UserInfo
	where Sheet.SID = UID_SID_Favor.SID and UserInfo.UID = UID_SID_Favor.UID
