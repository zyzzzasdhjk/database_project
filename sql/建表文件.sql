CREATE DATABASE MMS
CREATE TABLE Account_Password
([UID] INT PRIMARY KEY IDENTITY(1,1),
 Account VARCHAR(10) UNIQUE,
 [Password]  VARCHAR(10))

CREATE TABLE Label
(LID INT PRIMARY KEY IDENTITY(1,1),
 Ltext varchar(10))

CREATE TABLE [UserInfo]
([UID] INT PRIMARY KEY,
 UName nvarchar(10),
 USex varchar(1) check(USex = 1 or USex = 2),
 UIntro nvarchar(300) ,
 UBirthday date,
 UIsVip varchar(1),
 LID INT,
 FOREIGN KEY(UID) REFERENCES Account_Password(UID),
 FOREIGN KEY(LID) REFERENCES Label(LID)
)

-- 音乐库
CREATE TABLE Music
(MID int primary key identity(1,1),
MName nvarchar(30) not null,
MTime smallint,
MDate date,
MDir nvarchar(50) not null,
LID int,
FOREIGN KEY(LID) REFERENCES Label(LID)
)

-- 专辑表
CREATE TABLE Album
(AID int PRIMARY KEY IDENTITY(1,1),
AName nvarchar(30) not null
)
-- 音乐制作人库
CREATE TABLE MusicMaker
(MMID int PRIMARY KEY IDENTITY(1,1),
MMName nvarchar(30) not null
)
-- 评论表
CREATE TABLE Comment
(CID INT PRIMARY KEY IDENTITY(1,1),
 CContent nvarchar(300))

-- 歌单表
CREATE TABLE Sheet
([SID] int primary key IDENTITY(1,1),
 SName nvarchar(30) not null,
 SIntro nvarchar(300),
 SFavor smallint)

CREATE TABLE [UID_SID_Create]
(UID int,
 SID int unique,
 PRIMARY KEY ([UID],[SID]),
 FOREIGN KEY([UID]) REFERENCES Account_Password([UID]),
 FOREIGN KEY([SID]) REFERENCES Sheet([SID])
)

CREATE TABLE [UID_SID_Favor]
(UID int,
 SID int,
 PRIMARY KEY ([UID],[SID]),
 FOREIGN KEY([UID]) REFERENCES Account_Password([UID]),
 FOREIGN KEY([SID]) REFERENCES Sheet([SID])
)

CREATE TABLE UID_CID
(UID INT,
 CID INT,
 PRIMARY KEY([UID],CID),
 FOREIGN KEY([UID]) REFERENCES Account_Password([UID]),
 FOREIGN KEY([CID]) REFERENCES Comment([CID])
)

CREATE TABLE SID_MID
([SID] INT,
 MID INT,
 PRIMARY KEY([SID],MID),
 FOREIGN KEY([SID]) REFERENCES Sheet([SID]),
 FOREIGN KEY([MID]) REFERENCES Music([MID])
)

CREATE TABLE MID_MMID
(MID INT,
 MMID INT,
 PRIMARY KEY(MID,MMID),
 FOREIGN KEY([MID]) REFERENCES Music([MID]),
 FOREIGN KEY([MMID]) REFERENCES MusicMaker([MMID])
)

CREATE TABLE MID_AID
(MID INT,
 AID INT,
 PRIMARY KEY(MID,AID),
 FOREIGN KEY([MID]) REFERENCES Music([MID]),
 FOREIGN KEY([AID]) REFERENCES Album([AID])
)

CREATE TABLE MID_CID
(MID INT,
 CID INT,
 PRIMARY KEY(MID,CID),
 FOREIGN KEY([MID]) REFERENCES Music([MID]),
 FOREIGN KEY([CID]) REFERENCES Comment([CID])
)

