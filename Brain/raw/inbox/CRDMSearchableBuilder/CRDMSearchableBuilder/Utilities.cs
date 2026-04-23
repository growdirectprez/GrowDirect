using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CRDMSearchableBuilder
{
    using System;
    using System.CodeDom;

    /// <summary>
    /// General utilities or methods for POSTransaction Class creation.
    /// </summary>
    internal class Utilities
    {
        /// <summary>
        /// Takes the SQL data type from the column information and translates to a .NET type.
        /// </summary>
        /// <param name="dataType">The SQL data type from the XML to be converted.</param>
        /// <param name="isNullable">The SQL attribute used to determine if the type can be null.</param>
        /// <param name="maxVal">The maximum value where data type is one of integer types.</param>
        /// <param name="minVal">The minimum value where data type is one of integer types.</param>  
        public static CodeTypeReference ConvertDataType(string dataType, bool isNullable, long? maxVal, long? minVal)
        {
            CodeTypeReference codeType;

            switch (dataType)
            {
                case "text":
                case "ntext":
                case "nvarchar":
                case "nchar":
                case "xml":
                case "char":
                case "timestamp":
                case "varchar":
                case "varbinary":
                case "binary":
                    codeType = new CodeTypeReference(typeof(string));
                    break;
                case "smallmoney":
                case "numeric":
                case "decimal":
                case "float":
                case "money":
                case "real":
                    codeType = new CodeTypeReference(typeof(double));
                    break;
                case "tinyint":
                    codeType = maxVal == null || minVal == null ? new CodeTypeReference(typeof(sbyte)) : ChangeToAppropriateDataType(maxVal, minVal);
                    break;
                case "smallint":
                    codeType = maxVal == null || minVal == null ? new CodeTypeReference(typeof(short)) : ChangeToAppropriateDataType(maxVal, minVal);
                    break;
                case "int":
                    codeType = maxVal == null || minVal == null ? new CodeTypeReference(typeof(int)) : ChangeToAppropriateDataType(maxVal, minVal);
                    break;
                case "bigint":
                    codeType = maxVal == null || minVal == null ? new CodeTypeReference(typeof(long)) : ChangeToAppropriateDataType(maxVal, minVal);
                    break;
                case "uniqueidentifier":
                    codeType = new CodeTypeReference(typeof(Guid));
                    break;
                case "datetime":
                case "date":
                case "datetime2":
                case "smalldatetime":
                    codeType = isNullable ? new CodeTypeReference(typeof(DateTime?)) : new CodeTypeReference(typeof(DateTime));
                    break;
                case "time":
                    codeType = new CodeTypeReference(typeof(TimeSpan));
                    break;
                case "bit":
                    codeType = new CodeTypeReference(typeof(bool));
                    break;
                default:
                    codeType = new CodeTypeReference(typeof(string));
                    break;
            }

            return codeType;
        }


        /// <summary>
        /// Takes the SQL data type from the column information and translates to a .NET type.
        /// </summary>
        /// <param name="maxVal">The maximum value where data type is one of integer types.</param>
        /// <param name="minVal">The minimum value where data type is one of integer types.</param> 
        public static CodeTypeReference ChangeToAppropriateDataType(long? maxVal, long? minVal)
        {
            CodeTypeReference newDataType;

            if (maxVal > int.MaxValue || minVal < int.MinValue)
            {
                newDataType = new CodeTypeReference(typeof(long));
            }
            else if (maxVal > short.MaxValue || minVal < short.MinValue)
            {
                newDataType = new CodeTypeReference(typeof(int));
            }
            else if (maxVal > byte.MaxValue || minVal < sbyte.MinValue)
            {
                newDataType = new CodeTypeReference(typeof(short));
            }
            else if (maxVal < sbyte.MaxValue && minVal > sbyte.MinValue && minVal < 0)
            {
                newDataType = new CodeTypeReference(typeof(sbyte));
            }
            else
            {
                newDataType = new CodeTypeReference(typeof(byte));
            }

            return newDataType;
        }

        /// <summary>
        /// Provide information of arguments required.
        /// </summary>
        /// <param name="message">String with the message to pass back to the user.</param>
        /// <param name="e">Actual error message.</param> 
        public static void RespondToError(string message, Exception e = null)
        {
            Console.WriteLine();
            Console.WriteLine(message);
            Console.WriteLine();
            Console.WriteLine(@"See the AppConfig file for examples.");
            Console.WriteLine(e);
            Console.WriteLine();
            Console.WriteLine("Press any key to continue ...");

            Console.ReadKey();
        }
    }
}
