-- 删除用户时级联删除用户相关所有数据（不包括歌单、不包括评论）
create TRIGGER T$_deleteUserInfo
    ON Account_Password
    INSTEAD OF DELETE -- 在删除之前，因为有外键约束
AS
BEGIN -- 开始事务
    DECLARE @UID int -- 声明变量
    SELECT @UID = UID FROM deleted -- 从被删除表中获取数据
    -- 根据被删除UID 删除其他表
    DELETE from UserInfo where UID = @UID
    -- 根据被删除UID，设置关系连接UID=11（为用户被注销的UID）
    UPDATE UID_CID set UID = 11 where UID = @UID
    UPDATE UID_SID_Create set UID = 11 where UID = @UID
    UPDATE UID_SID_Favor set UID = 11 where UID = @UID
    DELETE from Account_Password where UID = @UID
END -- 结束事务
GO



create trigger T$_deleteSheetData
on Sheet
INSTEAD OF DELETE -- 外键
as
    begin
        DECLARE @SID int -- 声明变量
		SELECT @SID = SID FROM deleted -- 从被删除表中获取数据
		DELETE from UID_SID_Create where SID = @SID
		DELETE from UID_SID_Favor where SID = @SID
		DELETE from SID_MID where SID = @SID
        DELETE from Sheet where SID = @SID
    end
GO

create TRIGGER T$_addfavorSheet
    ON UID_SID_Favor
    after insert
AS
BEGIN
    DECLARE @SID int
    SELECT @SID = [SID] FROM inserted

    UPDATE Sheet set SFavor = SFavor + 1 where SID = @SID
END
GO

create TRIGGER T$_deletefavorSheet
    ON UID_SID_Favor
    after delete
AS
BEGIN
    DECLARE @SID int
    SELECT @SID = SID FROM deleted

    UPDATE Sheet set SFavor = SFavor - 1 where SID = @SID
END
GO


create trigger T$_deleteMID_CID
on MID_CID
after delete
as
	begin
	declare @CID int;
	select @CID =CID from deleted
	delete from UID_CID where CID = @CID
	delete from Comment where CID = @CID
	end
GO

create trigger T$_deleteComment
on Comment
instead of delete
as
	begin
	declare @CID int;
	select @CID =CID from deleted
	delete from UID_CID where CID = @CID
	delete from MID_CID where CID = @CID
    DELETE from Comment where CID = @CID
	end
GO

create TRIGGER T$_deleteMusic
    ON Music
    instead of delete
AS
BEGIN
    DECLARE @MID int
    SELECT @MID = MID FROM deleted

    DELETE MID_AID where MID = @MID
	DELETE MID_MMID where MID = @MID
	DELETE MID_CID where MID = @MID
    DELETE Music where MID = @MID
END
GO


create trigger T$_insertUserInfo
on Account_Password
after Insert
as
	begin
	declare @UID int;
	select @UID =UID from Inserted
	insert into UserInfo values(@UID,'新用户','1','这个用户很懒，什么也没留下。','2000-01-01','0',1)
	end
GO

create Trigger T$_limitCreateSheet
on Sheet
	for insert
as
	Declare @SID int
	Declare @Identity nvarchar(10)
	select @Identity = ORIGINAL_LOGIN()
	select @SID = SID from inserted

	IF((10 >= all(select count(UID) from V$_getUserAllCreateSheet group by UID)) or @Identity = 'MVip')
	BEGIN
		delete Sheet where SID = @SID
	END
GO