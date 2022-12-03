Create  PROCEDURE Insert_USC
@UID int,
@SID int
AS
    INSERT INTO UID_SID_Create
    VALUES(@UID,@SID)
GO


Create  PROCEDURE Insert_UCMC
@UID int,
@CID int,
@MID int
AS
    INSERT INTO UID_CID
    VALUES(@UID,@CID)
	INSERT INTO MID_CID
    VALUES(@MID,@CID)
GO

--音乐人提交音乐
IF OBJECT_ID('submitmusic','P') IS NOT NULL
Drop Procedure submitmusic
GO

Create  PROCEDURE submitmusic
@MNAME NVARCHAR(30),
@MTIME SMALLint,
@MDATE DATE,
@MDIR NVARCHAR(50),
@LID int,
@ANAME NVARCHAR(30),
@MMNAME nvarchar(30)


AS 
    INSERT INTO MUSIC(MNAME,MTIME,MDATE,MDIR,LID)
    VALUES(@MNAME,@MTIME,@MDATE,@MDIR,@LID)

	DECLARE @MID int
	select @MID = MID from Music where MName = @MNAME

IF NOT EXISTS (select * from MusicMaker where MMName = @MMNAME)
        begin 
            insert into MusicMaker
			values(@MMNAME) 
        end 

IF NOT EXISTS (select * from Album where ANAME = @ANAME)
        begin 
            insert into ALBUM(ANAME)
			values(@ANAME) 
        end 

	DECLARE @MMID int
	select @MMID = MMID from MusicMaker where MMName = @MMNAME

	DECLARE @AID int
	select @AID = AID from Album where AName = @ANAME

	insert into MID_AID values(@MID, @AID)

	insert into MID_MMID values(@MID, @MMID)
GO

Create PROCEDURE P$_deleteComment
@CID int
as
    delete COMMENT where CID = @CID
GO

Create PROCEDURE P$_deleteUser
@UID int
as
    delete Account_Password where UID = @UID
GO

IF OBJECT_ID('addvip','P') IS NOT NULL
Drop Procedure addvip
GO

Create  PROCEDURE addvip
@UID INT
AS 
   UPDATE [USERINFO] SET UISVIP=1
   WHERE UID=@UID
GO