

using Sysrepublic.Secure.Core.Data.Contract.Search;
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
    /// Class which creates the Search Builder object.
    /// </summary>
    internal class CreateSearchBuilder
    {
        /// <summary>
        /// Creates a series of XML searchable files using the XML passed in.
        /// </summary>
        /// <param name="sqlXmlFilePath">The file path and name for the XML which is used as the source for the searchable.</param>
        /// <param name="builderFilePath">The file path and name which the XML file will be saved as.</param>
        /// <param name="connectionName">The name of the connection to be used.</param> 
        public static void CreateSqlBuilder(string sqlXmlFilePath, string builderFilePath, string connectionName, string rootTable, bool postGreSqlFlag = false)
        {
            XElement xml = XElement.Load(sqlXmlFilePath);

            SearchBuilderDef sqlBuilder = new SearchBuilderDef();

            sqlBuilder.EntityName = !postGreSqlFlag ? "dbo." + rootTable : "dbo." + rootTable.ToLower();
            sqlBuilder.ConnectionName = connectionName;
            sqlBuilder.Category = "sql-crdm";
            sqlBuilder.Icon = "&#xf1c0;";
            sqlBuilder.RepoTag = "sqlcrdm";
            sqlBuilder.OriginUrl = "explorer/area#/?builderpath=/system/indieapps/securestore/pos/sql/builder/crdm.builder&searchpath=$(ssrpath)";

            SearchableEntities sent = new SearchableEntities();

            sqlBuilder.SearchableEntities = sent;
            sqlBuilder.Views = new List<ViewDefinition>();
            sqlBuilder.Tracks = new Tracks();
            sqlBuilder.DefaultDisplayFields = new DisplayFields();
            sqlBuilder.Tracks.TrackList = new List<Track>();


            foreach (XElement tableDetails in xml.Elements())
            {
                string tableName = tableDetails.Attribute("TableName").Value;

                foreach (XElement columnDetails in tableDetails.Elements())
                {
                    if (columnDetails.Attribute("IsDefaultDisplayColumn").Value == "1")
                    {
                        long? maxVal = null;
                        long? minVal = null;

                        if (columnDetails.Attribute("MaxVal") != null && columnDetails.Attribute("MinVal") != null)
                        {
                            maxVal = long.Parse(columnDetails.Attribute("MaxVal").Value);
                            minVal = long.Parse(columnDetails.Attribute("MinVal").Value);
                        }

                        bool isCommon = false;
                        if (columnDetails.HasAttribute("IsCommon"))
                        {
                            string commonValue = columnDetails.Attribute("IsCommon").Value;
                            isCommon = (commonValue == "0") ? false : true;
                        }

                        sqlBuilder.DefaultDisplayFields.Add(CreateDisplayField(
                                                                columnDetails.Attribute("ColumnName").Value,
                                                                columnDetails.Attribute("DataType").Value,
                                                                SortOrderOption.none,
                                                                tableName,
                                                                postGreSqlFlag,
                                                                minVal,
                                                                maxVal,
                                                                isCommon));
                    }
                }
            }

            sqlBuilder.Views.Add(CreateView("Grid"));
            sqlBuilder.Views.Add(CreateView("Stack"));
            sqlBuilder.Views.Add(CreateView("Panel"));

            Track tr = new Track();
            tr.Id = "transactionviewer";
            tr.Name = "transactionviewer";
            tr.Url = "expo#/txviewer?transactionid={transactionid}&storeno={storeno}&posno={posno}&cashierno={cashierno}";
            tr.ActionType = TrackActionType.Drilldown;
            tr.IconImage = "&#xf016;";

            sqlBuilder.Tracks.TrackList.Add(tr);

            XmlDocument posBuilderDoc = new XmlDocument();
            posBuilderDoc.LoadXml(sqlBuilder.ToXml());

            string prefix = !postGreSqlFlag ? "SQL" : "PostGreSQL";

            StreamWriter sw = new StreamWriter(string.Format(builderFilePath, prefix));
            posBuilderDoc.Save(sw);
            sw.Flush();
            sw.Close();
        }

        public static void CreateSqlOnlineBuilder(string sqlXmlFilePath, string builderFilePath, string connectionName, string rootTable, bool postGreSqlFlag = false)
        {
            XElement xml = XElement.Load(sqlXmlFilePath);

            SearchBuilderDef sqlBuilder = new SearchBuilderDef();

            sqlBuilder.EntityName = !postGreSqlFlag ? "online." + rootTable : "online." + rootTable.ToLower();
            sqlBuilder.ConnectionName = connectionName;
            sqlBuilder.Category = "sql-crdm-online";
            sqlBuilder.Icon = "&#xf1c0;";
            sqlBuilder.RepoTag = "sqlcrdmonline";
            sqlBuilder.OriginUrl = "explorer/area#/?builderpath=/system/indieapps/securestore/online/sql/builder/online.builder&searchpath=$(ssrpath)";

            SearchableEntities sent = new SearchableEntities();

            sqlBuilder.SearchableEntities = sent;
            sqlBuilder.Views = new List<ViewDefinition>();
            sqlBuilder.Tracks = new Tracks();
            sqlBuilder.DefaultDisplayFields = new DisplayFields();
            sqlBuilder.Tracks.TrackList = new List<Track>();


            foreach (XElement tableDetails in xml.Elements())
            {
                string tableName = tableDetails.Attribute("TableName").Value;

                foreach (XElement columnDetails in tableDetails.Elements())
                {
                    if (columnDetails.Attribute("IsDefaultDisplayColumn").Value == "1")
                    {
                        long? maxVal = null;
                        long? minVal = null;

                        if (columnDetails.Attribute("MaxVal") != null && columnDetails.Attribute("MinVal") != null)
                        {
                            maxVal = long.Parse(columnDetails.Attribute("MaxVal").Value);
                            minVal = long.Parse(columnDetails.Attribute("MinVal").Value);
                        }

                        bool isCommon = false;
                        if (columnDetails.HasAttribute("IsCommon"))
                        {
                            string commonValue = columnDetails.Attribute("IsCommon").Value;
                            isCommon = (commonValue == "0") ? false : true;
                        }

                        sqlBuilder.DefaultDisplayFields.Add(CreateDisplayField(
                                                                columnDetails.Attribute("ColumnName").Value,
                                                                columnDetails.Attribute("DataType").Value,
                                                                SortOrderOption.none,
                                                                "online_" + tableName,
                                                                postGreSqlFlag,
                                                                minVal,
                                                                maxVal,
                                                                isCommon));
                    }
                }
            }

            sqlBuilder.Views.Add(CreateView("Grid"));
            sqlBuilder.Views.Add(CreateView("Stack"));
            sqlBuilder.Views.Add(CreateView("Panel"));

            Track tr = new Track();
            tr.Id = "transactionviewer";
            tr.Name = "transactionviewer";
            tr.Url = "expo#/txviewer?orderid={orderid}&customerid={customerid}";
            tr.ActionType = TrackActionType.Drilldown;
            tr.IconImage = "&#xf016;";

            sqlBuilder.Tracks.TrackList.Add(tr);

            XmlDocument posBuilderDoc = new XmlDocument();
            posBuilderDoc.LoadXml(sqlBuilder.ToXml());

            string prefix = !postGreSqlFlag ? "SQL" : "PostGreSQL";

            StreamWriter sw = new StreamWriter(string.Format(builderFilePath, prefix));
            posBuilderDoc.Save(sw);
            sw.Flush();
            sw.Close();
        }


        public static void CreateSqlInventoryBuilder(string sqlXmlFilePath, string builderFilePath, string connectionName, string rootTable, bool postGreSqlFlag = false)
        {
            XElement xml = XElement.Load(sqlXmlFilePath);

            SearchBuilderDef sqlBuilder = new SearchBuilderDef();

            sqlBuilder.EntityName = !postGreSqlFlag ? "inventory." + rootTable : "inventory." + rootTable.ToLower();
            sqlBuilder.ConnectionName = connectionName;
            sqlBuilder.Category = "sql-crdm-inventory";
            sqlBuilder.Icon = "&#xf1c0;";
            sqlBuilder.RepoTag = "sqlcrdminventory";
            sqlBuilder.OriginUrl = "explorer/area#/?builderpath=/system/indieapps/securestore/inventory/sql/builder/inventory.builder&searchpath=$(ssrpath)";

            SearchableEntities sent = new SearchableEntities();

            sqlBuilder.SearchableEntities = sent;
            sqlBuilder.Views = new List<ViewDefinition>();
            sqlBuilder.Tracks = new Tracks();
            sqlBuilder.DefaultDisplayFields = new DisplayFields();

            foreach (XElement tableDetails in xml.Elements())
            {
                string tableName = tableDetails.Attribute("TableName").Value;

                foreach (XElement columnDetails in tableDetails.Elements())
                {
                    if (columnDetails.Attribute("IsDefaultDisplayColumn").Value == "1")
                    {
                        long? maxVal = null;
                        long? minVal = null;

                        if (columnDetails.Attribute("MaxVal") != null && columnDetails.Attribute("MinVal") != null)
                        {
                            maxVal = long.Parse(columnDetails.Attribute("MaxVal").Value);
                            minVal = long.Parse(columnDetails.Attribute("MinVal").Value);
                        }

                        bool isCommon = false;
                        if (columnDetails.HasAttribute("IsCommon"))
                        {
                            string commonValue = columnDetails.Attribute("IsCommon").Value;
                            isCommon = (commonValue == "0") ? false : true;
                        }

                        sqlBuilder.DefaultDisplayFields.Add(CreateDisplayField(
                                                                columnDetails.Attribute("ColumnName").Value,
                                                                columnDetails.Attribute("DataType").Value,
                                                                SortOrderOption.none,
                                                                "inventory_" + tableName,
                                                                postGreSqlFlag,
                                                                minVal,
                                                                maxVal,
                                                                isCommon));
                    }
                }
            }

            sqlBuilder.Views.Add(CreateView("Grid"));
            sqlBuilder.Views.Add(CreateView("Stack"));
            sqlBuilder.Views.Add(CreateView("Panel"));

            Track tr = new Track();
            tr.Id = "transactionviewer";
            tr.Name = "transactionviewer";
            tr.Url = "expo#/txviewer?recordid={recordid}";
            tr.ActionType = TrackActionType.Drilldown;
            tr.IconImage = "&#xf016;";

            sqlBuilder.Tracks.TrackList.Add(tr);

            XmlDocument posBuilderDoc = new XmlDocument();
            posBuilderDoc.LoadXml(sqlBuilder.ToXml());

            string prefix = !postGreSqlFlag ? "SQL" : "PostGreSQL";

            StreamWriter sw = new StreamWriter(string.Format(builderFilePath, prefix));
            posBuilderDoc.Save(sw);
            sw.Flush();
            sw.Close();
        }

        public static void CreateSqlVerifyBuilder(string sqlXmlFilePath, string builderFilePath, string connectionName, string rootTable, bool postGreSqlFlag = false)
        {
            XElement xml = XElement.Load(sqlXmlFilePath);

            SearchBuilderDef sqlBuilder = new SearchBuilderDef();

            sqlBuilder.EntityName = !postGreSqlFlag ? "dbo." + rootTable : "dbo." + rootTable.ToLower();
            sqlBuilder.ConnectionName = connectionName;
            sqlBuilder.Category = "sql-verify";
            sqlBuilder.Icon = "&#xf1c0;";
            sqlBuilder.RepoTag = "sqlverify";
            sqlBuilder.OriginUrl = "explorer/area#/?builderpath=/system/verify/sql/builder/verify.builder&searchpath=$(ssrpath)";
            sqlBuilder.CategoryDisplayName = "Appriss Verify";
            SearchableEntities sent = new SearchableEntities();

            sqlBuilder.SearchableEntities = sent;
            sqlBuilder.Views = new List<ViewDefinition>();
            sqlBuilder.Tracks = new Tracks();
            sqlBuilder.DefaultDisplayFields = new DisplayFields();
            sqlBuilder.Tracks.TrackList = new List<Track>();

            foreach (XElement tableDetails in xml.Elements())
            {
                string tableName = tableDetails.Attribute("TableName").Value;

                foreach (XElement columnDetails in tableDetails.Elements())
                {
                    if (columnDetails.Attribute("IsDefaultDisplayColumn").Value == "1")
                    {
                        long? maxVal = null;
                        long? minVal = null;

                        if (columnDetails.Attribute("MaxVal") != null && columnDetails.Attribute("MinVal") != null)
                        {
                            maxVal = long.Parse(columnDetails.Attribute("MaxVal").Value);
                            minVal = long.Parse(columnDetails.Attribute("MinVal").Value);
                        }

                        bool isCommon = false;
                        if (columnDetails.HasAttribute("IsCommon"))
                        {
                            string commonValue = columnDetails.Attribute("IsCommon").Value;
                            isCommon = (commonValue == "0") ? false : true;
                        }

                        sqlBuilder.DefaultDisplayFields.Add(CreateDisplayField(
                            columnDetails.Attribute("ColumnName").Value,
                            columnDetails.Attribute("DataType").Value,
                            SortOrderOption.none,
                            "dbo_" + tableName,
                            postGreSqlFlag,
                            minVal,
                            maxVal,
                            isCommon));
                    }
                }
            }

            sqlBuilder.Views.Add(CreateView("Grid"));
            sqlBuilder.Views.Add(CreateView("Stack"));
            sqlBuilder.Views.Add(CreateView("Panel"));

            Track tr = new Track();
            tr.Id = "transactionviewer";
            tr.Name = "transactionviewer";
            tr.Url = "expo#/txviewer?recordid={recordid}";
            tr.ActionType = TrackActionType.Drilldown;
            tr.IconImage = "&#xf016;";

            sqlBuilder.Tracks.TrackList.Add(tr);

            XmlDocument posBuilderDoc = new XmlDocument();
            posBuilderDoc.LoadXml(sqlBuilder.ToXml());

            string prefix = !postGreSqlFlag ? "SQL" : "PostGreSQL";

            StreamWriter sw = new StreamWriter(string.Format(builderFilePath, prefix));
            posBuilderDoc.Save(sw);
            sw.Flush();
            sw.Close();
        }

        /// <summary>
        /// Creates a series of XML searchable files using the XML passed in.
        /// </summary>
        /// <param name="hadoukenXmlFilePath">The file path and name for the XML which is used as the source for the searchable.</param>
        /// <param name="builderFilePath">The file path and name which the XML file will be saved as.</param>
        /// <param name="connectionName">The name of the connection to be used.</param>
        /// <param name="locationField">The field which is used as the Location Predicate.</param> 
        public static void CreateHadoukenBuilder(string hadoukenXmlFilePath, string builderFilePath, string connectionName, string locationField, string rootTable, bool postGreSqlFlag = false)
        {
            XElement xml = XElement.Load(hadoukenXmlFilePath);

            SearchBuilderDef sqlBuilder = new SearchBuilderDef();

            sqlBuilder.EntityName = rootTable;
            sqlBuilder.ConnectionName = connectionName;
            sqlBuilder.Category = "hadouken-crdm";
            sqlBuilder.Icon = "&#xf1c0;";
            sqlBuilder.RepoTag = "hadoukencrdm";
            sqlBuilder.OriginUrl = "explorer/area#/?builderpath=/system/crdm/sql/builder/crdm.builder&searchpath=$(ssrpath)";

            SearchableEntities sent = new SearchableEntities();

            sqlBuilder.SearchableEntities = sent;
            sqlBuilder.Views = new List<ViewDefinition>();
            sqlBuilder.Tracks = new Tracks();
            sqlBuilder.DefaultDisplayFields = new DisplayFields();
            sqlBuilder.Tracks.TrackList = new List<Track>();


            foreach (XElement tableDetails in xml.Elements())
            {
                string tableName = tableDetails.Attribute("TableName").Value;

                foreach (XElement columnDetails in tableDetails.Elements())
                {
                    if (columnDetails.Attribute("IsDefaultDisplayColumn").Value == "1")
                    {
                        long? maxVal = null;
                        long? minVal = null;

                        if (columnDetails.Attribute("MaxVal") != null && columnDetails.Attribute("MinVal") != null)
                        {
                            maxVal = long.Parse(columnDetails.Attribute("MaxVal").Value);
                            minVal = long.Parse(columnDetails.Attribute("MinVal").Value);
                        }

                        string columnName = columnDetails.Attribute("ColumnName").Value;
                        string dataType = columnName == locationField ? "varchar" : columnDetails.Attribute("DataType").Value;

                        bool isCommon = false;
                        if (columnDetails.HasAttribute("IsCommon"))
                        {
                            string commonValue = columnDetails.Attribute("IsCommon").Value;
                            isCommon = (commonValue == "0") ? false : true;
                        }

                        sqlBuilder.DefaultDisplayFields.Add(CreateDisplayField(
                                                                columnName,
                                                                dataType,
                                                                SortOrderOption.none,
                                                                tableName,
                                                                postGreSqlFlag,
                                                                minVal,
                                                                maxVal,
                                                                isCommon));
                    }
                }

                if (tableName == "CRDM_FastFact")
                {
                    continue;
                }
            }

            sqlBuilder.Views.Add(CreateView("Grid"));
            sqlBuilder.Views.Add(CreateView("Stack"));
            sqlBuilder.Views.Add(CreateView("Panel"));

            Track tr = new Track();
            tr.Id = "transactionviewer";
            tr.Name = "transactionviewer";
            tr.Url = "expo#/txviewer?transactionid={transactionid}&storeno={storeno}&posno={posno}&cashierno={cashierno}";
            tr.ActionType = TrackActionType.Drilldown;
            tr.IconImage = "&#xf016;";

            sqlBuilder.Tracks.TrackList.Add(tr);

            XmlDocument posBuilderDoc = new XmlDocument();
            posBuilderDoc.LoadXml(sqlBuilder.ToXml());

            StreamWriter sw = new StreamWriter(string.Format(builderFilePath, "HDK"));
            posBuilderDoc.Save(sw);
            sw.Flush();
            sw.Close();
        }

        /// <summary>
        /// Creates a series of XML searchable files using the XML passed in.
        /// </summary>
        /// <param name="name">The name for the field.</param>
        /// <param name="dataType">The SQL data type of the field.</param>
        /// <param name="sortOrder">The sort order for the field.</param>
        /// <param name="tableName">The table name to drive the searchable ID.</param>
        /// <param name="minVal">The minimum value the field takes in the source DB.</param>
        /// <param name="maxVal">The maximum value the field takes in the source DB.</param>
        private static DisplayField CreateDisplayField(string name, string dataType, SortOrderOption sortOrder, string tableName, bool postGreSqlFlag, long? minVal, long? maxVal, bool isCommon)
        {
            string convertedDataType = CreateSearchable.ConvertDataType(dataType, maxVal, minVal);

            DisplayField df = new DisplayField();
            df.ID = name.ToLower();
            df.DataType = convertedDataType;
            df.DisplayName = name;
            df.SortOrder = sortOrder;
            df.SearchableId = tableName.ToLower();

            if (name == "TransactionID")
            {
                df.IsMandatory = true;
            }

            Expression ex = new Expression();
            ExpressionField exf = new ExpressionField();
            exf.DataType = convertedDataType;
            exf.Description = !postGreSqlFlag ? name : name.ToLower();
            exf.CommonField = isCommon;

            df.Expression = new Expression();
            df.Expression.Add(exf);

            return df;
        }

        /// <summary>
        /// Creates a view class for the builder.
        /// </summary>
        /// <param name="name">The name for the field.</param>
        private static ViewDefinition CreateView(string name)
        {
            ViewDefinition vd1 = new ViewDefinition();
            vd1.ActualView = string.Empty;
            vd1.Name = name;

            return vd1;
        }
    }
}
