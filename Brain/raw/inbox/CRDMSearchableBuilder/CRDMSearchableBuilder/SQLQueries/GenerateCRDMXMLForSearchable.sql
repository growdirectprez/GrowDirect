SET NOCOUNT ON

-- First create a temporary table 
CREATE TABLE #columnAliases (	ID BIGINT IDENTITY, 
								ColumnName VARCHAR(100), 
								DataType VARCHAR(100),
								TableID BIGINT)

-- A couple of table variables
DECLARE @tableAliases TABLE (	ID BIGINT IDENTITY, 
								TableName VARCHAR(100))

DECLARE @columnData TABLE (	TableID BIGINT,
							TableName VARCHAR(100), 
							TableAlias VARCHAR(100), 
							ColumnName VARCHAR(100), 
							DataType VARCHAR(100), 
							MaxVal BIGINT,
							MinVal BIGINT,
							Alias VARCHAR(100),
							IncludeInHadouken BIT,
							IsDefaultDisplayColumn BIT,
							IsHidden BIT)

-- Declare the variables we will need
DECLARE @iter INT = 1, 
		@iter2 INT = 1, 
		@maxCount INT,
		@maxCount2 INT,
		@maxVal BIGINT,
		@minVal BIGINT,
		@tableName VARCHAR(100), 
		@columnDataType VARCHAR(100),
		@columnName VARCHAR(100),
		@populatedTableExists BIT = 0,
		@SQL NVARCHAR(MAX),
		@tableID BIGINT,
		@IncludeInHadouken BIT,
		@isDefaultDisplayColumn BIT,
		@isHidden BIT,
		@tableAlias VARCHAR(100)

--Establish if the [pos].[Populated] table exists
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[pos].[Populated]') AND type in (N'U'))
SET @populatedTableExists = 1

--Get Header and insert into @tableAliases
SET @SQL = 
'SELECT [name] ' +
  'FROM sys.tables ' +
 'WHERE [name] IN (''CRDM_Header'') ' +
   'AND SCHEMA_NAME(schema_id) = ''dbo'' ' +
   CASE WHEN @populatedTableExists = 1 
		THEN 'AND [name] COLLATE Latin1_General_BIN IN (SELECT TableName COLLATE Latin1_General_BIN FROM [pos].[Populated] WHERE [ColumnName] IS NULL AND [Populated] = 1) '
		ELSE ''
	END +
 'ORDER BY [name] DESC'

--select @SQL
INSERT INTO @tableAliases
EXEC sp_executesql @SQL

--Do all the tables except Receipt
SET @SQL = 
'SELECT [name] ' +
  'FROM sys.tables ' +
 'WHERE [name] LIKE ''CRDM_%'' ' +
   'AND [name] NOT IN (''CRDM_Header'', ''CRDM_Receipt'') ' +
   'AND SCHEMA_NAME(schema_id) = ''dbo'' ' +
   CASE WHEN @populatedTableExists = 1 
		THEN 'AND [name] COLLATE Latin1_General_BIN IN (SELECT TableName COLLATE Latin1_General_BIN FROM [pos].[Populated] WHERE [ColumnName] IS NULL AND [Populated] = 1) '
		ELSE ''
	END +   
 'ORDER BY [name]'

--select @SQL
INSERT INTO @tableAliases
EXEC sp_executesql @SQL
--select * from @tableAliases

SELECT @maxCount = MAX(ID) FROM @tableAliases

WHILE (@iter <= @maxCount)
BEGIN

	SELECT	@tableName = TableName, @tableAlias = SUBSTRING(TableName, 6, 99)
	  FROM	@tableAliases 
	 WHERE  ID = @iter

	SET @SQL =
	'SELECT c.[name], p.[name], ' + CAST(@iter AS NVARCHAR(10)) +
	  'FROM sys.tables t ' +
	  'LEFT JOIN sys.columns c ' +
	    'ON t.object_id = c.object_id ' +
	  'LEFT JOIN sys.types p ' +
	    'ON c.system_type_id = p.system_type_id ' +
	 'WHERE t.[name] = ''' + @tableName +
	   ''' AND SCHEMA_NAME(t.schema_id) = ''dbo'' ' +
	   'AND p.[name] != ''sysname'' ' +
	CASE WHEN @populatedTableExists = 1 
	 	 THEN ' AND c.[name] COLLATE Latin1_General_BIN IN (SELECT [ColumnName] COLLATE Latin1_General_BIN FROM [pos].[Populated] WHERE [TableName] = ''' + @tableName + ''' AND [ColumnName] IS NOT NULL AND [Populated] = 1)'
		 ELSE ' '
	END +	   
	 'ORDER BY c.[column_id]'

	--select @SQL	 
	INSERT INTO #columnAliases
	EXEC sp_executesql @SQL
	--select * from #columnAliases
	  
	SELECT @maxCount2 = MAX(ID) FROM #columnAliases
	
	--Do the non flags
	WHILE (@iter2 <= @maxCount2)
	BEGIN
		SELECT	@columnName = ColumnName,				
				@columnDataType = DataType,
				@tableID = TableID
		  FROM	#columnAliases 
		 WHERE  ID = @iter2

		IF @columnDataType != 'bit'
		BEGIN
			IF @populatedTableExists = 1 AND @columnDataType IN ('tinyint', 'smallint', 'int', 'bigint')
			BEGIN
				SELECT @maxVal = MaxVal, @minVal = MinVal FROM pos.Populated WHERE ColumnName = @columnName AND TableName = @tableName
			END

			-- Now determine if the field should be used in Hadouken Searchables
			SELECT @IncludeInHadouken = 1, @isDefaultDisplayColumn = 0, @isHidden = 0

			IF @tableName = 'CRDM_Header'
			BEGIN 
				IF @columnName IN ('CheckPointID')
				SET @IncludeInHadouken = 0

				IF @columnName IN ('TransactionID', 'StoreNo', 'POSNo', 'TicketNo', 'EndTransDateTime', 'CashierNo', 'TicketAmount')
				SELECT @isDefaultDisplayColumn = 1, @isHidden = 0
			END
			ELSE
			BEGIN
				IF @columnName IN ('TransactionID', 'StoreNo', 'POSNo', 'TicketNo', 'EndTransDateTime', 'CashierNo', 'CheckPointID', 'TradingDay', 'InsertedDateTime')
				SELECT @IncludeInHadouken = 0, @isHidden = 1
			END

			INSERT INTO @columnData 
			SELECT @tableID, @tableName, @tableAlias, @columnName, @columnDataType, @maxVal, @minVal, @columnName, @IncludeInHadouken, @isDefaultDisplayColumn, @isHidden
		END
		
		SET @iter2 = @iter2 + 1
	END

	-- Now we have to spoof a Transaction Time field for the Unique Constraint - we will populate with the EndTransDateTime cast as a Time
	IF @tableName = 'CRDM_Header'
	BEGIN
		INSERT INTO @columnData
		SELECT @tableID, @tableName, @tableAlias, 'TransactionTime', 'time', 0, 0, 'TransactionTime', 1, 0, 0
	END

	SET @iter2 = 1
	
	--Now do the Flags
	WHILE (@iter2 <= @maxCount2)
	BEGIN
		SELECT	@columnName = ColumnName,
				@columnDataType = DataType,
				@tableID = TableID
		  FROM	#columnAliases 
		 WHERE  ID = @iter2

		IF @columnDataType = 'bit'
		BEGIN
			INSERT INTO @columnData 
			SELECT @tableID, @tableName, @tableAlias, @columnName, @columnDataType, @maxVal, @minVal, @columnName, 1, 0, 0
		END
		
		SET @iter2 = @iter2 + 1
	END

	SET @iter2 = 1
	SET @iter = @iter + 1
	
	TRUNCATE TABLE #columnAliases
	
END

DROP TABLE #columnAliases

--select * from @columnData

SELECT A.TableID AS "@TableId", A.TableName AS "@TableName", A.TableAlias AS "@TableAlias",
	(SELECT ColumnName AS "@ColumnName", DataType AS "@DataType", Alias AS "@Alias", MaxVal AS "@MaxVal", MinVal AS "@MinVal", IncludeInHadouken AS "@IncludeInHadouken", IsDefaultDisplayColumn AS "@IsDefaultDisplayColumn", IsHidden AS "@IsHidden"
	   FROM @columnData T WHERE T.TableName = A.TableName 
	    FOR XML PATH('Column'), TYPE)
  FROM (SELECT distinct TableID, TableName, TableAlias FROM @columnData) AS A
 ORDER BY A.TableID
   FOR XML PATH('Table'), ROOT('Sysrepublic.POSTransaction'), TYPE

