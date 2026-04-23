SET NOCOUNT ON

-- First create a temporary table 
CREATE TABLE #columnAliases (	ID BIGINT IDENTITY, 
								ColumnName VARCHAR(100), 
								MetaItemID UNIQUEIDENTIFIER, 
								DataType VARCHAR(100), 
								Alias VARCHAR(100),
								TableID BIGINT)

-- A couple of table variables
DECLARE @tableAliases TABLE (	ID BIGINT IDENTITY, 
								TableName VARCHAR(100), 
								MetaItemID UNIQUEIDENTIFIER, 
								Alias VARCHAR(100))

DECLARE @columnData TABLE (	TableID BIGINT,
							TableName VARCHAR(100), 
							TableAlias VARCHAR(100), 
							ColumnName VARCHAR(100), 
							MetaItemID UNIQUEIDENTIFIER, 
							DataType VARCHAR(100), 
							MaxVal BIGINT,
							MinVal BIGINT, 
							Alias VARCHAR(100),
							IncludeInHadouken BIT,
							IsDefaultDisplayColumn BIT)

-- Declare the variables we will need
DECLARE @iter INT = 1, 
		@iter2 INT = 1, 
		@maxCount INT,
		@maxCount2 INT,
		@maxLength INT,	
		@maxVal BIGINT,
		@minVal BIGINT,			
		@tableAlias VARCHAR(100), 
		@tableName VARCHAR(100), 
		@columnDataType VARCHAR(100),
		@columnAlias VARCHAR(100), 
		@columnName VARCHAR(100), 
		@tableID UNIQUEIDENTIFIER, 
		@columnMetaItemID UNIQUEIDENTIFIER,
		@populatedTableExists BIT = 0,
		@SQL NVARCHAR(MAX),
		@tableId2 BIGINT,
		@IncludeInHadouken BIT,
		@isDefaultDisplayColumn BIT

--Establish if the [dbo].[Populated] table exists
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Populated]') AND type in (N'U'))
SET @populatedTableExists = 1

--Get Header and FastFact and insert into @tableAliases
SET @SQL =
'SELECT MI.[Value], MI.[MetaItemID], MA.[Value] ' +
  'FROM [{0}_Metadata].[dbo].[Metadata_MetaItem] MI ' +
  'LEFT JOIN [{0}_Metadata].[dbo].[Metadata_MetaAttribute] MA ' +
    'ON MI.[MetaItemID]		= MA.[MetaItemID] ' +
 'WHERE MI.[EntityTypeID]	= ''8EC13462-0538-42A2-A9CC-13A703DAF710'' ' +
   'AND MI.[ParentItemID]	= ''3FE9FA2F-EED2-479D-9143-C7FBA782D044'' ' +
   'AND MI.[Value]			IN (''CRDM_Header'', ''CRDM_FastFact'') ' +
   'AND MA.[AttributeTypeID]	= ''8532BD99-D979-4176-B9D2-0E870EC371E4'' ' +
   CASE WHEN @populatedTableExists = 1 
		THEN 'AND MI.[Value] COLLATE Latin1_General_BIN IN (SELECT TableName COLLATE Latin1_General_BIN FROM [dbo].[Populated] WHERE [ColumnName] IS NULL AND [Populated] = 1) '
		ELSE ''
	END +
 'ORDER BY MI.[Value] DESC'

INSERT INTO @tableAliases
EXEC sp_executesql @SQL

--Do all the other tables except Receipt
SET @SQL = 
'SELECT MI.[Value], MI.[MetaItemID], MA.[Value] ' +
  'FROM [{0}_Metadata].[dbo].[Metadata_MetaItem] MI ' +
  'LEFT JOIN [{0}_Metadata].[dbo].[Metadata_MetaAttribute] MA ' +
    'ON MI.[MetaItemID]		= MA.[MetaItemID] ' +
 'WHERE MI.[EntityTypeID]	= ''8EC13462-0538-42A2-A9CC-13A703DAF710'' ' +
   'AND MI.[ParentItemID]	= ''3FE9FA2F-EED2-479D-9143-C7FBA782D044'' ' +
   'AND MI.[Value]			NOT IN (''CRDM_Header'', ''CRDM_FastFact'',''CRDM_Receipt'') ' +
   'AND MI.[Value]			LIKE ''CRDM_%'' ' +
   'AND MA.[AttributeTypeID]	= ''8532BD99-D979-4176-B9D2-0E870EC371E4'' ' +
   CASE WHEN @populatedTableExists = 1 
		THEN 'AND MI.[Value] COLLATE Latin1_General_BIN IN (SELECT TableName COLLATE Latin1_General_BIN FROM [dbo].[Populated] WHERE [ColumnName] IS NULL AND [Populated] = 1) '
		ELSE ''
	END +
 'ORDER BY MI.[Value]'

 --select @SQL
INSERT INTO @tableAliases
EXEC sp_executesql @SQL
--select * from @tableAliases

SELECT @maxCount = MAX(ID) FROM @tableAliases

WHILE (@iter <= @maxCount)
BEGIN

	SELECT	@tableName = TableName,
			@tableID = MetaItemID,
			@tableAlias = Alias
	  FROM	@tableAliases 
	 WHERE  ID = @iter


	SET @SQL = 
	'SELECT MI.[Value], MI.[MetaItemID], MA.[Value], MA2.[Value], ' + CAST(@iter AS NVARCHAR(10)) +
	  'FROM [{0}_Metadata].[dbo].[Metadata_MetaItem] MI ' +
	  'LEFT JOIN [{0}_Metadata].[dbo].[Metadata_MetaAttribute] MA ' +
	    'ON MI.[MetaItemID] = MA.[MetaItemID] ' +
	  'LEFT JOIN [{0}_Metadata].[dbo].[Metadata_MetaAttribute] MA2 ' +
	    'ON MI.[MetaItemID] = MA2.[MetaItemID] ' +
	 'WHERE MA.[AttributeTypeID] = ''9755F90A-B5B4-4AE6-9100-050EF4C78407'' ' +
	   'AND MA2.[AttributeTypeID] = ''8532BD99-D979-4176-B9D2-0E870EC371E4'' ' +
	   'AND MI.[EntityTypeID] = ''B97E9393-6D80-493F-9565-8E20DC849E8A'' ' +
	   'AND MI.[ParentItemID] = ''' + CAST(@tableID AS NVARCHAR(40)) + 
		CASE WHEN @populatedTableExists = 1 
			THEN ''' AND MI.[Value] COLLATE Latin1_General_BIN IN (SELECT [ColumnName] COLLATE Latin1_General_BIN FROM [dbo].[Populated] WHERE [TableName] = ''' + @tableName + ''' AND [ColumnName] IS NOT NULL AND [Populated] = 1)'
			ELSE ''' '
		END +	   
	 'ORDER BY MA.Value'

	--select @SQL
	INSERT INTO #columnAliases
	EXEC sp_executesql @SQL
	--select * from #columnAliases
	  
	SELECT @maxCount2 = MAX(ID) FROM #columnAliases
	
	--Do the non flags
	WHILE (@iter2 <= @maxCount2)
	BEGIN
		SET @maxVal = 0
		SET @minVal = 0

		SELECT	@columnMetaItemID = MetaItemID,
				@columnName = ColumnName,				
				@columnDataType = DataType,
				@columnAlias = Alias,
				@tableId2 = TableID
		  FROM	#columnAliases 
		 WHERE  ID = @iter2

		IF @columnDataType != 'bit'
		BEGIN		
			SELECT	@maxLength = c.max_length
			  FROM sys.tables t
			  LEFT JOIN sys.columns c
				ON t.[object_id] = c.[object_id]
			  LEFT JOIN #columnAliases CA
				ON c.[name] COLLATE Latin1_General_BIN = CA.[ColumnName] COLLATE Latin1_General_BIN 
			 WHERE t.[name] = @tableName
			   AND c.[system_type_id] != 104
			   AND CA.[ID] = @iter2
			 ORDER BY c.[column_id]
			
			IF @populatedTableExists = 1 AND @columnDataType IN ('tinyint', 'smallint', 'int', 'bigint')
			BEGIN
				SELECT @maxVal = MaxVal, @minVal = MinVal FROM dbo.Populated WHERE ColumnName = @columnName AND TableName = @tableName
			END

			-- Now determine if the field should be used in Hadouken Searchables
			SET @IncludeInHadouken = 1
			SET @isDefaultDisplayColumn = 0

			IF @tableName = 'CRDM_Header'
			BEGIN 
				IF @columnName IN ('CheckPointID')
				SET @IncludeInHadouken = 0

				IF @columnName IN ('TransactionID', 'StoreNo', 'POSNo', 'TicketNo', 'EndTransDateTime', 'CashierNo', 'TicketAmount')
				SET @isDefaultDisplayColumn = 1
			END
			ELSE IF @tableName = 'CRDM_FastFact'
			BEGIN
				IF @columnName IN ('TransactionID', 'StoreNo', 'POSNo', 'TicketNo', 'EndTransDateTime', 'CashierNo', 'CheckPointID', 'TradingDay', 'TicketAmount', 'StartTransDateTime', 'InsertedDateTime', 'UpdatedDateTime')
				SET @IncludeInHadouken = 0
			END
			ELSE
			BEGIN
				IF @columnName IN ('TransactionID', 'StoreNo', 'POSNo', 'TicketNo', 'EndTransDateTime', 'CashierNo', 'CheckPointID', 'TradingDay', 'InsertedDateTime')
				SET @IncludeInHadouken = 0
			END
			
			INSERT INTO @columnData 
			SELECT @tableId2, @tableName, @tableAlias, @columnName, @columnMetaItemID, @columnDataType, @maxVal, @minVal, @columnAlias, @IncludeInHadouken, @isDefaultDisplayColumn	
		END
		
		SET @iter2 = @iter2 + 1
	END

	-- Now we have to spoof a Transaction Time field for the Unique Constraint - we will populate with the EndTransDateTime cast as a Time
	IF @tableName = 'CRDM_Header'
	BEGIN
		INSERT INTO @columnData
		SELECT @tableId2, @tableName, @tableAlias, 'TransactionTime', 'ea5645bb-6297-442e-b0a7-e5b749997387', 'time', 0, 0, 'TransactionTime', 1, 0
	END

	SET @iter2 = 1
	
	--Now do the Flags
	WHILE (@iter2 <= @maxCount2)
	BEGIN
		SELECT	@columnMetaItemID = MetaItemID,
				@columnName = ColumnName,
				@columnDataType = DataType,
				@columnAlias = Alias,
				@tableId2 = TableID
		  FROM	#columnAliases 
		 WHERE  ID = @iter2

		IF @columnDataType = 'bit'
		BEGIN
			SELECT	@maxLength = c.max_length
			  FROM sys.tables t
			  LEFT JOIN sys.columns c
				ON t.[object_id] = c.[object_id]
			  LEFT JOIN #columnAliases CA
				ON c.[name] COLLATE Latin1_General_BIN = CA.[ColumnName] COLLATE Latin1_General_BIN 
			 WHERE t.[name] = @tableName
			   AND c.[system_type_id] = 104
			   AND CA.[ID] = @iter2
			 ORDER BY c.[column_id]
			
			INSERT INTO @columnData 
			SELECT @tableId2, @tableName, @tableAlias, @columnName, @columnMetaItemID, @columnDataType, @maxVal, @minVal, @columnAlias, 1, 0
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
	(SELECT ColumnName AS "@ColumnName", MetaItemID AS "@MetaItemID", DataType AS "@DataType", Alias AS "@Alias", MaxVal AS "@MaxVal", MinVal AS "@MinVal", IncludeInHadouken AS "@IncludeInHadouken", IsDefaultDisplayColumn AS "@IsDefaultDisplayColumn"
	   FROM @columnData T WHERE T.TableName = A.TableName 
	    FOR XML PATH('Column'), TYPE)
  FROM (SELECT distinct TableID, TableName, TableAlias FROM @columnData) AS A
 ORDER BY A.TableID
   FOR XML PATH('Table'), ROOT('Sysrepublic.POSTransaction'), TYPE