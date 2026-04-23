namespace CRDMSearchableBuilder
{
    using System;
    using System.Collections.Generic;
    using System.Configuration;
    using System.IO;
    using System.Linq;

    /// <summary>
    /// Class containing the entry point for the tool.
    /// </summary>
    public class BuildSearchable
    {
        /// <summary>
        /// The entry point for the tool.
        /// </summary>
        /// <param name="args">Variable length list of arguments with which the entry method is called - we use the AppConfig file.</param> 
        public static void Main(string[] args)
        {
            // The root path for saving the files that get created
            string rootFilePath = ConfigurationManager.AppSettings["rootFilePath"];
            if (string.IsNullOrEmpty(rootFilePath))
            {
                Utilities.RespondToError("The path and name for the xml file which is used to create the class is missing from the AppConfig file.");
                return;
            }

            Directory.CreateDirectory(Path.GetDirectoryName(rootFilePath));

            // Path and name of the searchables files for each table that get produced
            string searchableSaveFilePath = ConfigurationManager.AppSettings["searchableSaveFilePath"];
            if (string.IsNullOrEmpty(searchableSaveFilePath))
            {
                Utilities.RespondToError("The path for the searchables is missing from the AppConfig file.");
                return;
            }

            // Path and name of the searchables files for each table that get produced
            string builderSaveFilePath = ConfigurationManager.AppSettings["builderSaveFilePath"];
            if (string.IsNullOrEmpty(builderSaveFilePath))
            {
                Utilities.RespondToError("The path for the builders is missing from the AppConfig file.");
                return;
            }

            string onlineBuilderSaveFilePath = ConfigurationManager.AppSettings["onlineBuilderSaveFilePath"];
            if (string.IsNullOrEmpty(onlineBuilderSaveFilePath))
            {
                Utilities.RespondToError("The path for the online builders is missing from the AppConfig file.");
                return;
            }

            string inventoryBuilderSaveFilePath = ConfigurationManager.AppSettings["inventoryBuilderSaveFilePath"];
            if (string.IsNullOrEmpty(inventoryBuilderSaveFilePath))
            {
                Utilities.RespondToError("The path for the inventory builders is missing from the AppConfig file.");
                return;
            }

            string verifyBuilderSaveFilePath = ConfigurationManager.AppSettings["verifyBuilderSaveFilePath"];
            if (string.IsNullOrEmpty(verifyBuilderSaveFilePath))
            {
                Utilities.RespondToError("The path for the Verify Return builders is missing from the AppConfig file.");
                return;
            }

            // The server where the database is hosted containg the Metadata and CRDM databases
            string dataSource = ConfigurationManager.AppSettings["dataSource"];
            if (string.IsNullOrEmpty(dataSource))
            {
                Utilities.RespondToError("The data source for the SQL connection string is missing from the AppConfig file");
                return;
            }

            // The name of the CRDM database
            string pointOfSaleDatabaseName = ConfigurationManager.AppSettings["pointOfSaleDatabaseName"];
            if (string.IsNullOrEmpty(pointOfSaleDatabaseName))
            {
                Utilities.RespondToError("The CRDM database name for the SQL connection string is missing from the AppConfig file");
                return;
            }

            string onlineDatabaseName = ConfigurationManager.AppSettings["onlineDatabaseName"];
            if (string.IsNullOrEmpty(onlineDatabaseName))
            {
                Utilities.RespondToError("The CRDM online database name for the SQL connection string is missing from the AppConfig file");
                return;
            }

            string inventoryDatabaseName = ConfigurationManager.AppSettings["inventoryDatabaseName"];
            if (string.IsNullOrEmpty(inventoryDatabaseName))
            {
                Utilities.RespondToError("The CRDM Inventory database name for the SQL connection string is missing from the AppConfig file");
                return;
            }

            string verifyDatabaseName = ConfigurationManager.AppSettings["verifyDatabaseName"];
            if (string.IsNullOrEmpty(verifyDatabaseName))
            {
                Utilities.RespondToError("The Verify Return database name for the SQL connection string is missing from the AppConfig file");
                return;
            }

            // The user name to use to connect to the database
            string userId = ConfigurationManager.AppSettings["userId"];
            if (string.IsNullOrEmpty(userId))
            {
                Utilities.RespondToError("The User ID for the SQL connection string is missing from the AppConfig file");
                return;
            }

            // The password for the user selected to connect to the database
            string password = ConfigurationManager.AppSettings["password"];
            if (string.IsNullOrEmpty(password))
            {
                Utilities.RespondToError("The Password for the SQL connection string is missing from the AppConfig file");
                return;
            }

            // Whether there is Metadata or not
            if (string.IsNullOrEmpty(ConfigurationManager.AppSettings["metadataExists"]))
            {
                Utilities.RespondToError("The indicator for whether a Metadata database exists is missing from the AppConfig file");
                return;
            }

            bool metadataExists = CheckBoolValue(ConfigurationManager.AppSettings["metadataExists"]);

            // The Secure 3 domain name pre-pended to the Metadata DB name
            if ((ConfigurationManager.AppSettings["domain"] == null || ConfigurationManager.AppSettings["domain"] == string.Empty) && metadataExists)
            {
                Utilities.RespondToError("You have indicated that a Metadata database exists but the Domain name is missing from the AppConfig file");
                return;
            }

            // The name of the connection that will be used in the searchables used by Secure4 to connect to the CRDM database
            string sqlConnection = ConfigurationManager.AppSettings["sqlConnection"];
            if (string.IsNullOrEmpty(sqlConnection))
            {
                Utilities.RespondToError("The name of the sql connection that will be used in the searchables is missing from the AppConfig file");
                return;
            }

            // The name of the connection that will be used in the searchables used by Secure4 to connect to the HDK instance
            string hdkConnection = ConfigurationManager.AppSettings["hdkConnection"];
            if (string.IsNullOrEmpty(hdkConnection))
            {
                Utilities.RespondToError("The name of the hdk connection that will be used in the searchables is missing from the AppConfig file");
                return;
            }

            string domain = metadataExists ? ConfigurationManager.AppSettings["domain"] : string.Empty;


            //string locationField = ConfigurationManager.AppSettings["locationPredicate"];
            //if (string.IsNullOrEmpty(locationField))
            //{
            //    Utilities.RespondToError("The locationPredicate is missing from the AppConfig file.");
            //    return;
            //}

            string rootTable = ConfigurationManager.AppSettings["rootTable"];
            if (string.IsNullOrEmpty(rootTable))
            {
                Utilities.RespondToError("The rootTable is missing from the AppConfig file.");
                return;
            }

            string onlineRootTable = ConfigurationManager.AppSettings["onlineRootTable"];
            if (string.IsNullOrEmpty(onlineRootTable))
            {
                Utilities.RespondToError("The onlineRootTable is missing from the AppConfig file.");
                return;
            }

            string inventoryRootTable = ConfigurationManager.AppSettings["inventoryRootTable"];
            if (string.IsNullOrEmpty(onlineRootTable))
            {
                Utilities.RespondToError("The onlineRootTable is missing from the AppConfig file.");
                return;
            }

            string verifyrootTable = ConfigurationManager.AppSettings["verifyrootTable"];
            if (string.IsNullOrEmpty(verifyrootTable))
            {
                Utilities.RespondToError("The verifyrootTable is missing from the AppConfig file.");
                return;
            }

            string joinField = ConfigurationManager.AppSettings["joinField"];
            List<string> joinFields = new List<string>();
            if (string.IsNullOrEmpty(joinField))
            {
                Utilities.RespondToError("The joinField string is missing from the AppConfig file.");
                return;
            }
            else
            {
                joinFields = joinField.Split(',').ToList();
            }

            int topLevelTableCount;
            List<string> topLevelTables = new List<string>();
            bool parseResult = int.TryParse(ConfigurationManager.AppSettings["topLevelTableCount"], out topLevelTableCount);
            if (parseResult)
            {
                for (int j = 1; j <= topLevelTableCount; j++)
                {
                    if (string.IsNullOrEmpty(ConfigurationManager.AppSettings["topLevelTable" + j]))
                    {
                        Utilities.RespondToError("There is a top level table in the AppConfig file which is missing a value.");
                        return;
                    }

                    topLevelTables.Add(ConfigurationManager.AppSettings["topLevelTable" + j]);
                }
            }
            else
            {
                Utilities.RespondToError("The topLevelTableCount is missing or is not a number from the AppConfig file.");
                return;
            }

            Console.WriteLine();

            // Path and name to be used for the xml file that is created to use for building the searchable
            string searchableSourceXmlFilePath = ConfigurationManager.AppSettings["searchableSourceXmlFilePath"];
            if (string.IsNullOrEmpty(searchableSourceXmlFilePath))
            {
                Utilities.RespondToError("The name for the POS xml file which is used to create the searchables is missing from the AppConfig file.");
                return;
            }

            // Create the xml documents we need for the searchable and builder creation
            string path = rootFilePath + searchableSourceXmlFilePath;

            // Path and name to be used for the xml file that is created to use for building the searchable
            string onlineSearchableSourceXmlFilePath = ConfigurationManager.AppSettings["onlineSearchableSourceXmlFilePath"];
            if (string.IsNullOrEmpty(onlineSearchableSourceXmlFilePath))
            {
                Utilities.RespondToError("The name for the Online Searchable xml file which is used to create the searchables is missing from the AppConfig file.");
                return;
            }

            // Create the xml documents we need for the searchable and builder creation
            string onlinePath = rootFilePath + onlineSearchableSourceXmlFilePath;

            // Path and name to be used for the xml file that is created to use for building the searchable
            string inventorySearchableSourceXmlFilePath = ConfigurationManager.AppSettings["inventorySearchableSourceXmlFilePath"];
            if (string.IsNullOrEmpty(inventorySearchableSourceXmlFilePath))
            {
                Utilities.RespondToError("The name for the Inventory Searchable xml file which is used to create the searchables is missing from the AppConfig file.");
                return;
            }

            // Create the xml documents we need for the searchable and builder creation
            string inventoryPath = rootFilePath + inventorySearchableSourceXmlFilePath;


            // Path and name to be used for the xml file that is created to use for building the searchable
            string verifySearchableSourceXmlFilePath = ConfigurationManager.AppSettings["verifySearchableSourceXmlFilePath"];
            if (string.IsNullOrEmpty(verifySearchableSourceXmlFilePath))
            {
                Utilities.RespondToError("The name for the Inventory Searchable xml file which is used to create the searchables is missing from the AppConfig file.");
                return;
            }

            // Create the xml documents we need for the searchable and builder creation
            string verifyPath = rootFilePath + verifySearchableSourceXmlFilePath;

            // Connection strings for all required databases
            string manifest;

            string crdmconnectionString =
                $"Data Source={dataSource};Database={pointOfSaleDatabaseName};Connect Timeout=30;Integrated Security=False;User ID={userId};Password={password};";
            string onlineconnectionString =
                $"Data Source={dataSource};Database={onlineDatabaseName};Connect Timeout=30;Integrated Security=False;User ID={userId};Password={password};";
            string inventoryconnectionString =
                $"Data Source={dataSource};Database={inventoryDatabaseName};Connect Timeout=30;Integrated Security=False;User ID={userId};Password={password};";

            string verifyconnectionString =
                $"Data Source={dataSource};Database={verifyDatabaseName};Connect Timeout=30;Integrated Security=False;User ID={userId};Password={password};";


            if (CheckBoolValue(ConfigurationManager.AppSettings["mssql-target-database"]))
            {
                if (CheckBoolValue(ConfigurationManager.AppSettings["generateForCRDMPointOfSale"]))
                {
                    manifest = "CRDMSearchableBuilder.SQLQueries.GenerateCRDMXMLForSearchableNoMetadata.sql";
                    //manifest = "CRDMSearchableBuilder.SQLQueries.GenerateCRDMXMLForSearchableNoMetadataOldWithFastFact.sql";
                    if (CreateSourceXmlDocuments.CreateXml(metadataExists, path, domain, crdmconnectionString, manifest))
                    {
                        Directory.CreateDirectory(Path.GetDirectoryName(rootFilePath + @"\Sql\Store\"));

                        string buildSqlSavePath = rootFilePath + @"\SQL\Store\" + builderSaveFilePath;
                        string searchSqlSavePath = rootFilePath + @"\SQL\Store\" + searchableSaveFilePath;

                        CreateSearchBuilder.CreateSqlBuilder(path, buildSqlSavePath, sqlConnection, rootTable);
                        CreateSearchable.CreateSqlPosSearchable(path, searchSqlSavePath, rootTable, joinFields);
                        Console.WriteLine("POS XML for Sql builder and searchables have been created");
                    }
                }

                if (CheckBoolValue(ConfigurationManager.AppSettings["generateForCRDMOnline"]))
                {
                    manifest = "CRDMSearchableBuilder.SQLQueries.GenerateCRDMOnlineXMLForSearchableNoMetadata.sql";
                    if (CreateSourceXmlDocuments.CreateXml(metadataExists, onlinePath, domain, onlineconnectionString,
                        manifest))
                    {

                        Directory.CreateDirectory(Path.GetDirectoryName(rootFilePath + @"\Sql\Online\"));

                        string buildSqlSavePath = rootFilePath + @"\SQL\Online\" + onlineBuilderSaveFilePath;
                        string searchSqlSavePath = rootFilePath + @"\SQL\Online\" + searchableSaveFilePath;

                        CreateSearchBuilder.CreateSqlOnlineBuilder(onlinePath, buildSqlSavePath, sqlConnection, onlineRootTable);
                        CreateSearchable.CreateSqlOnlineSearchable(onlinePath, searchSqlSavePath, onlineRootTable, joinFields);
                        Console.WriteLine("Online XML for Sql builder and searchables have been created");
                    }
                }

                if (CheckBoolValue(ConfigurationManager.AppSettings["generateForInventory"]))
                {
                    manifest = "CRDMSearchableBuilder.SQLQueries.GenerateCRDMInventoryXMLForSearchableNoMetadata.sql";
                    if (CreateSourceXmlDocuments.CreateXml(metadataExists, inventoryPath, domain, inventoryconnectionString,
                        manifest))
                    {

                        Directory.CreateDirectory(Path.GetDirectoryName(rootFilePath + @"\Sql\Inventory\"));

                        string buildSqlSavePath = rootFilePath + @"\SQL\Inventory\" + inventoryBuilderSaveFilePath;
                        string searchSqlSavePath = rootFilePath + @"\SQL\Inventory\" + searchableSaveFilePath;

                        CreateSearchBuilder.CreateSqlInventoryBuilder(inventoryPath, buildSqlSavePath, sqlConnection, verifyrootTable);
                        CreateSearchable.CreateSqlInventorySearchable(inventoryPath, searchSqlSavePath, verifyrootTable, joinFields);
                        Console.WriteLine("Inventory XML for Sql builder and searchables have been created");
                    }
                }
            }

            if (CheckBoolValue(ConfigurationManager.AppSettings["postgressql-target-database"]))
            {
                if (CheckBoolValue(ConfigurationManager.AppSettings["generateForCRDMPointOfSale"]))
                {
                    manifest = "CRDMSearchableBuilder.SQLQueries.GenerateCRDMXMLForSearchableNoMetadata.sql";
                    if (CreateSourceXmlDocuments.CreateXml(metadataExists, path, domain, crdmconnectionString, manifest))
                    {
                        Directory.CreateDirectory(Path.GetDirectoryName(rootFilePath + @"\PostGreSQL\Store\"));

                        string buildSqlSavePath = rootFilePath + @"\PostGreSQL\Store\" + builderSaveFilePath;
                        string searchSqlSavePath = rootFilePath + @"\PostGreSQL\Store\" + searchableSaveFilePath;

                        CreateSearchBuilder.CreateSqlBuilder(path, buildSqlSavePath, sqlConnection, rootTable, true);
                        CreateSearchable.CreateSqlPosSearchable(path, searchSqlSavePath, rootTable, joinFields, true);
                        Console.WriteLine("POS XML for PostGreSQL builder and searchables have been created");
                    }
                }


                if (CheckBoolValue(ConfigurationManager.AppSettings["generateForCRDMOnline"]))
                {
                    manifest = "CRDMSearchableBuilder.SQLQueries.GenerateCRDMOnlineXMLForSearchableNoMetadata.sql";
                    if (CreateSourceXmlDocuments.CreateXml(metadataExists, onlinePath, domain, onlineconnectionString,
                        manifest))
                    {
                        Directory.CreateDirectory(Path.GetDirectoryName(rootFilePath + @"\PostGreSQL\Online\"));

                        string buildSqlSavePath = rootFilePath + @"\PostGreSQL\Online\" + onlineBuilderSaveFilePath;
                        string searchSqlSavePath = rootFilePath + @"\PostGreSQL\Online\" + searchableSaveFilePath;

                        CreateSearchBuilder.CreateSqlOnlineBuilder(onlinePath, buildSqlSavePath, sqlConnection,
                            onlineRootTable, true);
                        CreateSearchable.CreateSqlOnlineSearchable(onlinePath, searchSqlSavePath, onlineRootTable,
                            joinFields, true);
                        Console.WriteLine("Online XML for PostGreSQL builder and searchables have been created");
                    }
                }

                if (CheckBoolValue(ConfigurationManager.AppSettings["generateForInventory"]))
                {
                    manifest = "CRDMSearchableBuilder.SQLQueries.GenerateCRDMInventoryXMLForSearchableNoMetadata.sql";
                    if (CreateSourceXmlDocuments.CreateXml(metadataExists, inventoryPath, domain, inventoryconnectionString,
                        manifest))
                    {
                        Directory.CreateDirectory(Path.GetDirectoryName(rootFilePath + @"\PostGreSQL\Inventory\"));

                        string buildSqlSavePath = rootFilePath + @"\PostGreSQL\Inventory\" +
                                                  inventoryBuilderSaveFilePath;
                        string searchSqlSavePath = rootFilePath + @"\PostGreSQL\Inventory\" + searchableSaveFilePath;

                        CreateSearchBuilder.CreateSqlInventoryBuilder(inventoryPath, buildSqlSavePath, sqlConnection,
                            inventoryRootTable, true);
                        CreateSearchable.CreateSqlInventorySearchable(inventoryPath, searchSqlSavePath,
                            inventoryRootTable, joinFields, true);
                        Console.WriteLine("Inventory XML for PostGreSQL builder and searchables have been created");
                    }
                }
            }

            if (CheckBoolValue(ConfigurationManager.AppSettings["verify-target-database"]))
            {
                if (CheckBoolValue(ConfigurationManager.AppSettings["generateForVerify"]))
                {
                    manifest = "CRDMSearchableBuilder.SQLQueries.GenerateVerifyXMLForSearchableNoMetadata.sql";
                    if (CreateSourceXmlDocuments.CreateXml(metadataExists, verifyPath, domain, verifyconnectionString,
                        manifest))
                    {

                        Directory.CreateDirectory(Path.GetDirectoryName(rootFilePath + @"\Sql\verify\return\"));

                        string buildSqlSavePath = rootFilePath + @"\Sql\verify\return\" + verifyBuilderSaveFilePath;
                        string searchSqlSavePath = rootFilePath + @"\Sql\verify\return\" + searchableSaveFilePath;

                        CreateSearchBuilder.CreateSqlVerifyBuilder(verifyPath, buildSqlSavePath, sqlConnection, verifyrootTable);
                        CreateSearchable.CreateSqlVerifySearchable(verifyPath, searchSqlSavePath, verifyrootTable, joinFields);
                        Console.WriteLine("Verify XML for Sql builder and searchables have been created");
                    }
                }
            }

            //if (CheckBoolValue(ConfigurationManager.AppSettings["hdk-target-database"]))
                //{
                //    manifest = "CRDMSearchableBuilder.SQLQueries.GenerateCRDMXMLForSearchable.sql";
                //    if (CreateSourceXmlDocuments.CreateXml(metadataExists, path, domain, crdmconnectionString, manifest))
                //    {
                //        Directory.CreateDirectory(Path.GetDirectoryName(rootFilePath + @"\Hadouken\Store\"));

                //        if (CheckBoolValue(ConfigurationManager.AppSettings["generateForCRDMPointOfSale"]))
                //        {
                //            string buildHadoukenSavePath = rootFilePath + @"\HDK\Store\" + builderSaveFilePath;
                //            string searchHadoukenSavePath = rootFilePath + @"\HDK\Store\" + searchableSaveFilePath;
                //            CreateSearchBuilder.CreateHadoukenBuilder(path, buildHadoukenSavePath, hdkConnection, locationField,
                //                rootTable);
                //            CreateSearchable.CreateHadoukenPosSearchable(path, searchHadoukenSavePath, locationField, rootTable,
                //                topLevelTables);
                //            Console.WriteLine("Hadouken XML for Hadouken builder and searchables have been created");
                //        }
                //    }
                //    else
                //    {
                //        return;
                //    }
                //}

                Console.WriteLine();
            Console.WriteLine("Press any key to continue ...");
            Console.ReadKey();
        }

        /// <summary>
        /// Converts the metadata exists string to boolean.
        /// </summary>
        /// <param name="argText">String indicating value of boolean.</param> 
        private static bool CheckBoolValue(string argText)
        {
            bool boolValue;

            switch (argText.ToLower())
            {
                case "yes":
                case "true":
                case "1":
                    boolValue = true;
                    break;
                case "no":
                case "false":
                case "0":
                    boolValue = false;
                    break;
                default:
                    boolValue = false;
                    break;
            }

            return boolValue;
        }
    }
}
