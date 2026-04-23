using Sysrepublic.Secure.Core.Extensions;

namespace CRDMSearchableBuilder
{
    using System.Collections.Generic;
    using System.IO;
    using System.Xml;
    using System.Xml.Linq;

    using Sysrepublic.Foundation.Data.Search;
    using Sysrepublic.Foundation.Search;

    /// <summary>
    /// Class which creates the Searchable object.
    /// </summary>
    internal class CreateSearchable
    {
        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator equals = new SearchableOperator { Name = "equal" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator notequals = new SearchableOperator { Name = "notequal" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator lessthan = new SearchableOperator { Name = "lessthan" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator lessthanequal = new SearchableOperator { Name = "lessthanequal" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator greaterthan = new SearchableOperator { Name = "greaterthan" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator greaterthanequal = new SearchableOperator { Name = "greaterthanequal" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator between = new SearchableOperator { Name = "between" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator notbetween = new SearchableOperator { Name = "notbetween" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator match = new SearchableOperator { Name = "match" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator notmatch = new SearchableOperator { Name = "notmatch" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator inlist = new SearchableOperator { Name = "in" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator notin = new SearchableOperator { Name = "notin" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator startswith = new SearchableOperator { Name = "startswith" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator notstartswith = new SearchableOperator { Name = "notstartswith" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator endswith = new SearchableOperator { Name = "endswith" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator notendswith = new SearchableOperator { Name = "notendswith" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator contains = new SearchableOperator { Name = "contains" };

        /// <summary>
        /// Creates a new searchable operator.
        /// </summary>
        private static SearchableOperator notcontains = new SearchableOperator { Name = "notcontains" };

        /// <summary>
        /// Creates a new searchable operator - used with datetime only.
        /// </summary>
        private static SearchableOperator within = new SearchableOperator { Name = "within" };

        /// <summary>
        /// Creates a new searchable operator - used with datetime only.
        /// </summary>
        private static SearchableOperator on = new SearchableOperator { Name = "on" };

        /// <summary>
        /// Creates a series of XML searchable files using the XML passed in.
        /// </summary>
        /// <param name="sqlXmlFilePath">The file path and name for the XML which is used as the source for the searchable.</param>
        /// <param name="searchableFilePath">The file path and name which the XML file will be saved as.</param>
        /// <param name="rootTable">The root table for the schema.</param>
        /// <param name="joinField">The field used to join to the root table.</param>   
        public static void CreateSqlPosSearchable(string sqlXmlFilePath, string searchableFilePath, string rootTable, List<string> joinFields, bool postGreSqlFlag = false)
        {
            XElement xml = XElement.Load(sqlXmlFilePath);

            foreach (XElement tableDetails in xml.Elements())
            {
                Searchable posSearchable = new Searchable();
                string tableName = tableDetails.Attribute("TableName").Value;

                posSearchable.Label = tableDetails.Attribute("TableAlias").Value;

                foreach (XElement columnDetails in tableDetails.Elements())
                {
                    SearchableField field = new SearchableField();
                    FieldDescription fd = new FieldDescription();

                    string hiddenValue = columnDetails.Attribute("IsHidden").Value;
                    bool hidden = (hiddenValue == "0") ? false : true;

                    fd.Hidden = hidden;
                    field.FieldDescription = fd;

                    if (columnDetails.HasAttribute("IsCommon"))
                    {
                        string commonValue = columnDetails.Attribute("IsCommon").Value;
                        field.CommonField = (commonValue == "0") ? false : true;
                    }

                    if (tableName == rootTable)
                    {
                        field.DataType = ConvertDataType(columnDetails.Attribute("DataType").Value, null, null);
                        field.Label = columnDetails.Attribute("Alias").Value;
                        field.ID = columnDetails.Attribute("ColumnName").Value.ToLower();
                    }
                    else
                    {
                        field.DataType = ConvertDataType(columnDetails.Attribute("DataType").Value, null, null);
                        field.Label = columnDetails.Attribute("Alias").Value;
                        field.ID = tableName.Substring(5).ToLower() + "_" + columnDetails.Attribute("ColumnName").Value.ToLower();

                        //field.CollectionDescription = CreateRelationship(tableName, rootTable, joinField);
                    }

                    List<SearchableOperator> operators = GetSearchableOperatorsForDatatype(field.DataType);
                    field.Operators = operators;

                    Expression le = new Expression();
                    ExpressionField ef = new ExpressionField();
                    ef.DataType = field.DataType;

                    if (columnDetails.HasAttribute("IsCommon"))
                    {
                        string commonValue = columnDetails.Attribute("IsCommon").Value;
                        ef.CommonField = (commonValue == "0") ? false : true;
                    }

                    // Now define the relationship between this table and Header
                    // It is just TransactionID for all tables - in the Hadouken world, ItemDiscount is a subcollection of Item,
                    if (tableName == rootTable)
                    {
                        ef.Description = !postGreSqlFlag ? columnDetails.Attribute("ColumnName").Value : columnDetails.Attribute("ColumnName").Value.ToLower();
                    }
                    else
                    {
                        ef.Description = !postGreSqlFlag ? columnDetails.Attribute("ColumnName").Value : columnDetails.Attribute("ColumnName").Value.ToLower();
                        ef.CollectionDescription = CreateRelationship("dbo." + tableName, "dbo." + rootTable, joinFields, postGreSqlFlag, true);
                    }

                    le.Add(ef);
                    field.LeftExpression = le;

                    posSearchable.Fields.Add(field);
                }

                string tablePrefix = !postGreSqlFlag ? "SQL" : "PostGreSQL";

                //if (tableName == rootTable)
                //{
                //    posSearchable.MandatoryConditionGroup = CreateMandatoryFilters(tablePrefix, postGreSqlFlag);
                //}

                XmlDocument posSearchableDoc = new XmlDocument();
                posSearchableDoc.LoadXml(posSearchable.ToXml());

                StreamWriter sw = new StreamWriter(string.Format(searchableFilePath, tablePrefix, tableName));
                posSearchableDoc.Save(sw);
                sw.Flush();
                sw.Close();
            }
        }

        public static void CreateSqlOnlineSearchable(string sqlXmlFilePath, string searchableFilePath, string rootTable, List<string> joinFields, bool postGreSqlFlag = false)
        {
            XElement xml = XElement.Load(sqlXmlFilePath);

            foreach (XElement tableDetails in xml.Elements())
            {
                Searchable posSearchable = new Searchable();
                string tableName = tableDetails.Attribute("TableName").Value;

                posSearchable.Label = tableDetails.Attribute("TableAlias").Value;

                foreach (XElement columnDetails in tableDetails.Elements())
                {
                    SearchableField field = new SearchableField();

                    if (tableName == rootTable)
                    {
                        field.DataType = ConvertDataType(columnDetails.Attribute("DataType").Value, null, null);
                        field.Label = columnDetails.Attribute("Alias").Value;
                        field.ID = columnDetails.Attribute("ColumnName").Value.ToLower();
                    }
                    else
                    {
                        field.DataType = ConvertDataType(columnDetails.Attribute("DataType").Value, null, null);
                        field.Label = columnDetails.Attribute("Alias").Value;
                        field.ID = tableName.ToLower() + "_" + columnDetails.Attribute("ColumnName").Value.ToLower();

                        //field.CollectionDescription = CreateRelationship(tableName, rootTable, joinField);
                    }

                    List<SearchableOperator> operators = GetSearchableOperatorsForDatatype(field.DataType);
                    field.Operators = operators;

                    Expression le = new Expression();
                    ExpressionField ef = new ExpressionField();
                    ef.DataType = field.DataType;

                    // Now define the relationship between this table and Header
                    // It is just TransactionID for all tables - in the Hadouken world, ItemDiscount is a subcollection of Item,
                    if (tableName == rootTable)
                    {
                        ef.Description = !postGreSqlFlag ? columnDetails.Attribute("ColumnName").Value : columnDetails.Attribute("ColumnName").Value.ToLower();
                    }
                    else
                    {
                        ef.Description = !postGreSqlFlag ? columnDetails.Attribute("ColumnName").Value : columnDetails.Attribute("ColumnName").Value.ToLower();
                        ef.CollectionDescription = CreateRelationship("online." + tableName, "online." + rootTable, joinFields, postGreSqlFlag, false);
                    }

                    le.Add(ef);
                    field.LeftExpression = le;

                    posSearchable.Fields.Add(field);
                }

                string tablePrefix = !postGreSqlFlag ? "SQL" : "PostGreSQL";

                //if (tableName == rootTable)
                //{
                //    posSearchable.MandatoryConditionGroup = CreateMandatoryOnlineFilters(tablePrefix, postGreSqlFlag);
                //}

                XmlDocument posSearchableDoc = new XmlDocument();
                posSearchableDoc.LoadXml(posSearchable.ToXml());

                StreamWriter sw = new StreamWriter(string.Format(searchableFilePath, tablePrefix, tableName));
                posSearchableDoc.Save(sw);
                sw.Flush();
                sw.Close();
            }
        }

        public static void CreateSqlInventorySearchable(string sqlXmlFilePath, string searchableFilePath, string rootTable, List<string> joinFields, bool postGreSqlFlag = false)
        {
            XElement xml = XElement.Load(sqlXmlFilePath);

            foreach (XElement tableDetails in xml.Elements())
            {
                Searchable posSearchable = new Searchable();
                string tableName = tableDetails.Attribute("TableName").Value;

                posSearchable.Label = tableDetails.Attribute("TableAlias").Value;

                foreach (XElement columnDetails in tableDetails.Elements())
                {
                    SearchableField field = new SearchableField();

                    if (tableName == rootTable)
                    {
                        field.DataType = ConvertDataType(columnDetails.Attribute("DataType").Value, null, null);
                        field.Label = columnDetails.Attribute("Alias").Value;
                        field.ID = columnDetails.Attribute("ColumnName").Value.ToLower();
                    }
                    else
                    {
                        field.DataType = ConvertDataType(columnDetails.Attribute("DataType").Value, null, null);
                        field.Label = columnDetails.Attribute("Alias").Value;
                        field.ID = tableName.ToLower() + "_" + columnDetails.Attribute("ColumnName").Value.ToLower();

                        //field.CollectionDescription = CreateRelationship(tableName, rootTable, joinField);
                    }

                    List<SearchableOperator> operators = GetSearchableOperatorsForDatatype(field.DataType);
                    field.Operators = operators;

                    Expression le = new Expression();
                    ExpressionField ef = new ExpressionField();
                    ef.DataType = field.DataType;

                    // Now define the relationship between this table and Header
                    // It is just TransactionID for all tables - in the Hadouken world, ItemDiscount is a subcollection of Item,
                    if (tableName == rootTable)
                    {
                        ef.Description = !postGreSqlFlag ? columnDetails.Attribute("ColumnName").Value : columnDetails.Attribute("ColumnName").Value.ToLower();
                    }
                    else
                    {
                        ef.Description = !postGreSqlFlag ? columnDetails.Attribute("ColumnName").Value : columnDetails.Attribute("ColumnName").Value.ToLower();
                        ef.CollectionDescription = CreateRelationship("inventory." + tableName, "inventory." + rootTable, joinFields, postGreSqlFlag, false);
                    }

                    le.Add(ef);
                    field.LeftExpression = le;

                    posSearchable.Fields.Add(field);
                }

                string tablePrefix = !postGreSqlFlag ? "SQL" : "PostGreSQL";

                //if (tableName == rootTable)
                //{
                //    posSearchable.MandatoryConditionGroup = CreateMandatoryInventoryFilters(tablePrefix, postGreSqlFlag);
                //}

                XmlDocument posSearchableDoc = new XmlDocument();
                posSearchableDoc.LoadXml(posSearchable.ToXml());

                StreamWriter sw = new StreamWriter(string.Format(searchableFilePath, tablePrefix, tableName));
                posSearchableDoc.Save(sw);
                sw.Flush();
                sw.Close();
            }
        }


        public static void CreateSqlVerifySearchable(string sqlXmlFilePath, string searchableFilePath, string rootTable, List<string> joinFields, bool postGreSqlFlag = false)
        {
            XElement xml = XElement.Load(sqlXmlFilePath);

            foreach (XElement tableDetails in xml.Elements())
            {
                Searchable posSearchable = new Searchable();
                string tableName = tableDetails.Attribute("TableName").Value;

                posSearchable.Label = tableDetails.Attribute("TableAlias").Value;

                foreach (XElement columnDetails in tableDetails.Elements())
                {
                    SearchableField field = new SearchableField();

                    if (tableName == rootTable)
                    {
                        field.DataType = ConvertDataType(columnDetails.Attribute("DataType").Value, null, null);
                        field.Label = columnDetails.Attribute("Alias").Value;
                        field.ID = columnDetails.Attribute("ColumnName").Value.ToLower();
                    }
                    else
                    {
                        field.DataType = ConvertDataType(columnDetails.Attribute("DataType").Value, null, null);
                        field.Label = columnDetails.Attribute("Alias").Value;
                        field.ID = tableName.ToLower() + "_" + columnDetails.Attribute("ColumnName").Value.ToLower();

                        //field.CollectionDescription = CreateRelationship(tableName, rootTable, joinField);
                    }

                    List<SearchableOperator> operators = GetSearchableOperatorsForDatatype(field.DataType);
                    field.Operators = operators;

                    Expression le = new Expression();
                    ExpressionField ef = new ExpressionField();
                    ef.DataType = field.DataType;

                    // Now define the relationship between this table and Header
                    // It is just TransactionID for all tables - in the Hadouken world, ItemDiscount is a subcollection of Item,
                    if (tableName == rootTable)
                    {
                        ef.Description = !postGreSqlFlag ? columnDetails.Attribute("ColumnName").Value : columnDetails.Attribute("ColumnName").Value.ToLower();
                    }
                    else
                    {
                        ef.Description = !postGreSqlFlag ? columnDetails.Attribute("ColumnName").Value : columnDetails.Attribute("ColumnName").Value.ToLower();
                        ef.CollectionDescription = CreateRelationship("dbo." + tableName, "dbo." + rootTable, joinFields, postGreSqlFlag, false);
                    }

                    le.Add(ef);
                    field.LeftExpression = le;

                    posSearchable.Fields.Add(field);
                }

                string tablePrefix = !postGreSqlFlag ? "SQL" : "PostGreSQL";

                //if (tableName == rootTable)
                //{
                //    posSearchable.MandatoryConditionGroup = CreateMandatoryInventoryFilters(tablePrefix, postGreSqlFlag);
                //}

                XmlDocument posSearchableDoc = new XmlDocument();
                posSearchableDoc.LoadXml(posSearchable.ToXml());

                StreamWriter sw = new StreamWriter(string.Format(searchableFilePath, tablePrefix, tableName));
                posSearchableDoc.Save(sw);
                sw.Flush();
                sw.Close();
            }
        }

        /// <summary>
        /// Creates a series of XML searchable files using the XML passed in.
        /// </summary>
        /// <param name="hadoukenXmlFilePath">The file path and name for the XML which is used as the source for the searchable.</param>
        /// <param name="searchableFilePath">The file path and name which the XML file will be saved as.</param>
        /// <param name="locationField">The field which is used as the Location Predicate.</param>
        /// <param name="rootTable">The root table for the schema.</param>
        /// <param name="topLevelTables">The list of top level tables which have a one to one relationship with the root table.</param>
        public static void CreateHadoukenPosSearchable(string hadoukenXmlFilePath, string searchableFilePath, string locationField, string rootTable, List<string> topLevelTables)
        {
            XElement xml = XElement.Load(hadoukenXmlFilePath);

            foreach (XElement tableDetails in xml.Elements())
            {
                Searchable posSearchable = new Searchable();
                string tableName = tableDetails.Attribute("TableName").Value;

                if (topLevelTables.Contains(tableName))
                //if (tableName == "CRDM_FastFact")
                {
                    continue;
                }

                posSearchable.Label = tableDetails.Attribute("TableAlias").Value;

                foreach (XElement columnDetails in tableDetails.Elements())
                {
                    if (columnDetails.Attribute("IncludeInHadouken").Value == "0")
                    {
                        continue;
                    }

                    SearchableField field = new SearchableField();

                    long? maxVal = null;
                    long? minVal = null;

                    if (columnDetails.Attribute("MaxVal") != null && columnDetails.Attribute("MinVal") != null)
                    {
                        maxVal = long.Parse(columnDetails.Attribute("MaxVal").Value);
                        minVal = long.Parse(columnDetails.Attribute("MinVal").Value);
                    }

                    if (tableName == rootTable)
                    {
                        field.DataType = ConvertDataType(columnDetails.Attribute("DataType").Value, null, null);
                        field.Label = columnDetails.Attribute("Alias").Value;
                        field.ID = columnDetails.Attribute("ColumnName").Value.ToLower();
                    }
                    else
                    {
                        field.DataType = ConvertDataType(columnDetails.Attribute("DataType").Value, maxVal, minVal);
                        field.Label = columnDetails.Attribute("Alias").Value;
                        field.ID = tableName.Substring(5).ToLower() + "_" + columnDetails.Attribute("ColumnName").Value.ToLower();
                    }

                    List<SearchableOperator> operators = GetSearchableOperatorsForDatatype(field.DataType);
                    field.Operators = operators;

                    Expression le = new Expression();
                    ExpressionField ef = new ExpressionField();
                    ef.DataType = field.DataType;
                    ef.Description = columnDetails.Attribute("ColumnName").Value;

                    le.Add(ef);
                    field.LeftExpression = le;

                    posSearchable.Fields.Add(field);
                }

                // Keep it open and add in FastFact
                if (tableName == rootTable)
                {
                    foreach (XElement tableDetails2 in xml.Elements())
                    {
                        tableName = tableDetails2.Attribute("TableName").Value;

                        if (!topLevelTables.Contains(tableName))
                        //if (tableName != "CRDM_FastFact")
                        {
                            continue;
                        }

                        foreach (XElement columnDetails in tableDetails2.Elements())
                        {
                            if (columnDetails.Attribute("IncludeInHadouken").Value == "0")
                            {
                                continue;
                            }

                            SearchableField field = new SearchableField();

                            long? maxVal = null;
                            long? minVal = null;

                            if (columnDetails.Attribute("MaxVal") != null && columnDetails.Attribute("MinVal") != null)
                            {
                                maxVal = long.Parse(columnDetails.Attribute("MaxVal").Value);
                                minVal = long.Parse(columnDetails.Attribute("MinVal").Value);
                            }

                            field.DataType = ConvertDataType(columnDetails.Attribute("DataType").Value, maxVal, minVal);
                            field.Label = columnDetails.Attribute("Alias").Value;
                            field.ID = columnDetails.Attribute("ColumnName").Value.ToLower();

                            List<SearchableOperator> operators = GetSearchableOperatorsForDatatype(field.DataType);
                            field.Operators = operators;

                            Expression le = new Expression();
                            ExpressionField ef = new ExpressionField();
                            ef.DataType = field.DataType;

                            le.Add(ef);
                            field.LeftExpression = le;

                            posSearchable.Fields.Add(field);
                        }
                    }

                    posSearchable.MandatoryConditionGroup = CreateMandatoryFilters("Hadouken", false);

                    tableName = rootTable;
                }

                XmlDocument posSearchableDoc = new XmlDocument();
                posSearchableDoc.LoadXml(posSearchable.ToXml());

                StreamWriter sw = new StreamWriter(string.Format(searchableFilePath, "HDK", tableName));
                posSearchableDoc.Save(sw);
                sw.Flush();
                sw.Close();
            }
        }

        /// <summary>
        /// Returns the Secure data type for the SQL data type passed in.
        /// </summary>
        /// <param name="dataType">The SQL data type of the field.</param>
        /// <param name="maxVal">The maximum value the field takes in the source DB.</param>
        /// <param name="minVal">The minimum value the field takes in the source DB.</param>  
        public static string ConvertDataType(string dataType, long? maxVal, long? minVal)
        {
            string dt;

            switch (dataType)
            {
                case "char":
                case "nchar":
                    dt = "System.Char";
                    break;
                case "varchar":
                case "nvarchar":
                case "timestamp":
                case "text":
                case "ntext":
                case "varbinary":
                case "binary":
                case "xml":
                    dt = "System.String";
                    break;
                case "uniqueidentifier":
                    dt = "System.Guid";
                    break;
                case "smallmoney":
                case "numeric":
                case "decimal":
                case "float":
                case "money":
                case "real":
                    dt = "System.Double";
                    break;
                case "tinyint":
                    dt = (maxVal != null && minVal != null) ? ChangeToAppropriateDataType(maxVal, minVal) : "System.Byte";
                    break;
                case "smallint":
                    dt = (maxVal != null && minVal != null) ? ChangeToAppropriateDataType(maxVal, minVal) : "System.Int16";
                    break;
                case "int":
                    dt = (maxVal != null && minVal != null) ? ChangeToAppropriateDataType(maxVal, minVal) : "System.Int32";
                    break;
                case "bigint":
                    dt = (maxVal != null && minVal != null) ? ChangeToAppropriateDataType(maxVal, minVal) : "System.Int64";
                    break;
                case "datetime":
                case "date":
                case "datetime2":
                case "smalldatetime":
                    dt = "System.DateTime";
                    break;
                case "time":
                    dt = "System.TimeSpan";
                    break;
                case "bit":
                    dt = "System.Boolean";
                    break;
                default:
                    dt = "System.String";
                    break;
            }

            return dt;
        }

        /// <summary>
        /// Creates the relationship or join details for the table.
        /// </summary>
        /// <param name="tableName">The table name for which the relationship is to be defined.</param>
        /// <param name="rootTable">The root table for the schema.</param>
        /// <param name="joinField">The field used to join to the root table.</param>/// 
        /// <param name="postGreSqlFlag"></param>/// 
        /// <param name="relatedFieldsCommon">If all Related Fields can be optimized</param>/// 
        private static CollectionDescription CreateRelationship(string tableName, string rootTable, List<string> joinFields, bool postGreSqlFlag, bool relatedFieldsCommon)
        {
            Relationship relationship = new Relationship();

            relationship.Parent = !postGreSqlFlag ? rootTable : rootTable.ToLower();
            relationship.RelatedFields = new List<RelatedField>();

            for (int j = 0; j < joinFields.Count; j++)
            {
                RelatedField relatedField = new RelatedField();
                relatedField.From = !postGreSqlFlag ? joinFields[j] : joinFields[j].ToLower();
                relatedField.To = !postGreSqlFlag ? joinFields[j] : joinFields[j].ToLower();
                relatedField.CommonToField = relatedFieldsCommon;
                relationship.RelatedFields.Add(relatedField);
            }

            CollectionDescription collection = new CollectionDescription();
            collection.Collection = !postGreSqlFlag ? tableName : tableName.ToLower();

            collection.Relationships = new List<Relationship>();
            collection.Relationships.Add(relationship);

            return collection;
        }

        /// <summary>
        /// Creates the relationship or join details for the table.
        /// </summary>
        /// <param name="source">The table name for which the relationship is to be defined.</param>
        private static ConditionGroup CreateMandatoryFilters(string source, bool postGreSqlFlag)
        {
            ConditionGroup mcg = new ConditionGroup();
            mcg.LogicalOperator = LogicalOperator.And;

            source = !postGreSqlFlag ? source : source.ToLower();

            Condition c1 = new Condition();
            c1.AllowMandatorySelection = true;
            c1.DataType = "System.DateTime";
            c1.SearchComposerDisplayValue = "Date";
            c1.FieldId = "endtransdatetime";
            c1.LogicalOperator = LogicalOperator.And;
            c1.SearchableId = !postGreSqlFlag ? source + "_CRDM_Header" : source + "_crdm_header";
            c1.OmitOnNull = false;

            ExpressionField ef1 = new ExpressionField();
            ef1.DataType = "System.DateTime";
            ef1.Description = !postGreSqlFlag ? "EndTransDateTime" : "endtransdatetime";

            c1.LeftExpression.Add(ef1);

            c1.Operator = Operators.Equal;

            ExpressionVariable ev = new ExpressionVariable();
            ev.Name = "p1";
            ev.DataType = "System.DateTime";

            c1.RightExpression.Add(ev);

            mcg.Conditions.Add(c1);

            Condition c2 = new Condition();
            c2.AllowMandatorySelection = true;
            c2.DataType = "System.String";
            c2.SearchComposerDisplayValue = "Store Number";
            c2.FieldId = "storeno";
            c2.LogicalOperator = LogicalOperator.And;
            c2.SearchableId = !postGreSqlFlag ? source + "_CRDM_Header" : source + "_crdm_header";
            c2.OmitOnNull = false;

            ExpressionField ef2 = new ExpressionField();
            ef2.DataType = "System.String";
            ef2.Description = !postGreSqlFlag ? "StoreNo" : "storeno";

            c2.LeftExpression.Add(ef2);

            c2.Operator = Operators.Equal;

            ExpressionVariable ev2 = new ExpressionVariable();
            ev2.Name = "p2";
            ev2.DataType = "System.String";

            c2.RightExpression.Add(ev2);

            mcg.Conditions.Add(c2);

            return mcg;
        }

        private static ConditionGroup CreateMandatoryOnlineFilters(string source, bool postGreSqlFlag)
        {
            ConditionGroup mcg = new ConditionGroup();
            mcg.LogicalOperator = LogicalOperator.And;

            source = !postGreSqlFlag ? source : source.ToLower();

            Condition c1 = new Condition();
            c1.AllowMandatorySelection = true;
            c1.DataType = "System.DateTime";
            c1.SearchComposerDisplayValue = "Date";
            c1.FieldId = "checkoutdate";
            c1.LogicalOperator = LogicalOperator.And;
            c1.SearchableId = !postGreSqlFlag ? source + "_OrderHeader" : source + "_orderheader";
            c1.OmitOnNull = false;

            ExpressionField ef1 = new ExpressionField();
            ef1.DataType = "System.DateTime";
            ef1.Description = !postGreSqlFlag ? "EndTransDateTime" : "endtransdatetime";

            c1.LeftExpression.Add(ef1);

            c1.Operator = Operators.Equal;

            ExpressionVariable ev = new ExpressionVariable();
            ev.Name = "p1";
            ev.DataType = "System.DateTime";

            c1.RightExpression.Add(ev);

            mcg.Conditions.Add(c1);

            Condition c2 = new Condition();
            c2.AllowMandatorySelection = true;
            c2.DataType = "System.String";
            c2.SearchComposerDisplayValue = "Order ID";
            c2.FieldId = "orderid";
            c2.LogicalOperator = LogicalOperator.And;
            c2.SearchableId = !postGreSqlFlag ? source + "_OrderHeader" : source + "_orderheader";
            c2.OmitOnNull = false;

            ExpressionField ef2 = new ExpressionField();
            ef2.DataType = "System.String";
            ef2.Description = !postGreSqlFlag ? "OrderID" : "orderid";

            c2.LeftExpression.Add(ef2);

            c2.Operator = Operators.Equal;

            ExpressionVariable ev2 = new ExpressionVariable();
            ev2.Name = "p2";
            ev2.DataType = "System.String";

            c2.RightExpression.Add(ev2);

            mcg.Conditions.Add(c2);

            return mcg;
        }

        private static ConditionGroup CreateMandatoryInventoryFilters(string source, bool postGreSqlFlag)
        {
            ConditionGroup mcg = new ConditionGroup();
            mcg.LogicalOperator = LogicalOperator.And;

            source = !postGreSqlFlag ? source : source.ToLower();

            Condition c1 = new Condition();
            c1.AllowMandatorySelection = true;
            c1.DataType = "System.DateTime";
            c1.SearchComposerDisplayValue = "Date";
            c1.FieldId = "endtransdatetime";
            c1.LogicalOperator = LogicalOperator.And;
            c1.SearchableId = !postGreSqlFlag ? source + "_CRDM_Header" : source + "_crdm_header";
            c1.OmitOnNull = false;

            ExpressionField ef1 = new ExpressionField();
            ef1.DataType = "System.DateTime";
            ef1.Description = !postGreSqlFlag ? "EndTransDateTime" : "endtransdatetime";

            c1.LeftExpression.Add(ef1);

            c1.Operator = Operators.Equal;

            ExpressionVariable ev = new ExpressionVariable();
            ev.Name = "p1";
            ev.DataType = "System.DateTime";

            c1.RightExpression.Add(ev);

            mcg.Conditions.Add(c1);

            Condition c2 = new Condition();
            c2.AllowMandatorySelection = true;
            c2.DataType = "System.String";
            c2.SearchComposerDisplayValue = "Store Number";
            c2.FieldId = "storeno";
            c2.LogicalOperator = LogicalOperator.And;
            c2.SearchableId = !postGreSqlFlag ? source + "_CRDM_Header" : source + "_crdm_header";
            c2.OmitOnNull = false;

            ExpressionField ef2 = new ExpressionField();
            ef2.DataType = "System.String";
            ef2.Description = !postGreSqlFlag ? "StoreNo" : "storeno";

            c2.LeftExpression.Add(ef2);

            c2.Operator = Operators.Equal;

            ExpressionVariable ev2 = new ExpressionVariable();
            ev2.Name = "p2";
            ev2.DataType = "System.String";

            c2.RightExpression.Add(ev2);

            mcg.Conditions.Add(c2);

            return mcg;
        }

        /// <summary>
        /// Gets the appropriate operators for the data type of the field.
        /// </summary>
        /// <param name="dataType">The field type of the field for which the operators are required.</param>
        private static List<SearchableOperator> GetSearchableOperatorsForDatatype(string dataType)
        {
            List<SearchableOperator> operators = new List<SearchableOperator>();

            switch (dataType)
            {
                case "System.Boolean":
                    operators.Add(equals);
                    operators.Add(notequals);
                    break;
                case "System.Char":
                case "System.String":
                case "System.Guid":
                    operators.Add(equals);
                    operators.Add(notequals);
                    operators.Add(match);
                    operators.Add(notmatch);
                    operators.Add(inlist);
                    operators.Add(notin);
                    operators.Add(startswith);
                    operators.Add(notstartswith);
                    operators.Add(endswith);
                    operators.Add(notendswith);
                    operators.Add(contains);
                    operators.Add(notcontains);
                    break;
                case "System.DateTime":
                case "System.TimeSpan":
                    operators.Add(on);
                    operators.Add(greaterthan);
                    operators.Add(lessthan);
                    operators.Add(lessthanequal);
                    operators.Add(greaterthanequal);
                    operators.Add(within);
                    break;
                case "System.Byte":
                case "System.SByte":
                case "System.Int16":
                case "System.UInt16":
                case "System.Int32":
                case "System.UInt32":
                case "System.Int64":
                case "System.UInt64":
                case "System.Single":
                case "System.Double":
                case "System.Decimal":
                    operators.Add(equals);
                    operators.Add(notequals);
                    operators.Add(greaterthan);
                    operators.Add(greaterthanequal);
                    operators.Add(lessthan);
                    operators.Add(lessthanequal);
                    operators.Add(between);
                    operators.Add(notbetween);
                    //operators.Add(inlist);
                    //operators.Add(notin);
                    break;
                default:
                    operators.Add(equals);
                    break;
            }

            return operators;
        }

        /// <summary>
        /// Takes the SQL data type from the column information and translates to a .NET type.
        /// </summary>
        /// <param name="maxVal">The maximum value where data type is one of integer types.</param>
        /// <param name="minVal">The minimum value where data type is one of integer types.</param> 
        private static string ChangeToAppropriateDataType(long? maxVal, long? minVal)
        {
            string newDataType;

            if (maxVal > int.MaxValue || minVal < int.MinValue)
            {
                newDataType = "System.Int64";
            }
            else if (maxVal > short.MaxValue || minVal < short.MinValue)
            {
                newDataType = "System.Int32";
            }
            else if (maxVal > byte.MaxValue || minVal < sbyte.MinValue)
            {
                newDataType = "System.Int16";
            }
            else if (maxVal < sbyte.MaxValue && minVal > sbyte.MinValue && minVal < 0)
            {
                newDataType = "System.SByte";
            }
            else
            {
                newDataType = "System.Byte";
            }

            return newDataType;
        }
    }
}