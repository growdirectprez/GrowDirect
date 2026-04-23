namespace CRDMSearchableBuilder
{
    using System;
    using System.Data.SqlClient;
    using System.IO;
    using System.Linq;
    using System.Reflection;
    using System.Xml;

    internal class CreateSourceXmlDocuments
    {
        /// <summary>
        /// Calls the method to create the XML files that are used to build the class, searchable and builders.
        /// </summary>
        /// <param name="metadataExists">Boolean which indicates if Metadata can be used.</param>
        /// <param name="path">The path and name which is used to save the xml.</param>
        /// <param name="domain">The domain which the CRDM is being used in - relates to Secure3.</param>
        /// <param name="connectionString">The connection string to be used.</param>
        public static bool CreateXml(bool metadataExists, string path, string domain, string connectionString, string manifest)
        {
            bool success;

            if (metadataExists)
            {
                success = GenerateXmlFile(path, domain, connectionString, manifest);

                if (!success)
                {
                    return false;
                }

                Console.WriteLine("XML for searchable has been created");
            }
            else
            {
                success = GenerateXmlFile(path, domain, connectionString, manifest);

                if (!success)
                {
                    return false;
                }

                Console.WriteLine("XML for searchable has been created");
            }

            return true;
        }

        /// <summary>
        /// Creates an XML file using the SP passed in.
        /// </summary>
        /// <param name="xmlFilePath">The file path and name which the XML file will be saved as.</param>
        /// <param name="domain">The domain which the CRDM is being used in - relates to Secure3.</param>
        /// <param name="connectionString">The connection string to be used.</param>
        /// <param name="manifest">The SQL SP which is to be used.</param>
        public static bool GenerateXmlFile(string xmlFilePath, string domain, string connectionString, string manifest)
        {
            if (!Assembly.GetExecutingAssembly().GetManifestResourceNames().ToList().Contains(manifest))
            {
                string message = string.Format("The SQL script which is being requested is not contained in the solution - {0}.", manifest);

                Utilities.RespondToError(message);
                return false;
            }

            string sql = new StreamReader(Assembly.GetExecutingAssembly().GetManifestResourceStream(manifest)).ReadToEnd();

            SqlConnection activeConnection = new SqlConnection(connectionString);
            activeConnection.Open();

            SqlCommand command = new SqlCommand(string.Format(sql, domain), activeConnection);

            XmlDocument crdmSchema = new XmlDocument();

            crdmSchema.Load(command.ExecuteXmlReader());

            StreamWriter sw = new StreamWriter(xmlFilePath);
            crdmSchema.Save(sw);
            sw.Flush();
            sw.Close();

            activeConnection.Close();

            return true;
        }
    }
}
