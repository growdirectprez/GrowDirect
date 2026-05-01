<%
function visitorCurrency() {
  return (currentVisitor().COUNTRY = "USA") ? "$" : "£"
}

// Format credit card date from a general date string format
// to the mm/yy format.
function formatCreditCardDate(dateString) {
    var datetime = new BVI_DateTime(dateString, '0:0:0', null, null);
    if (Error.set || (datetime == null)) return dateString;
    var yearString = ""+datetime.year;
    yearString = yearString.substr(yearString.length-2, 2);
    var retString = datetime.month+'/'+yearString;
    return retString;
}

%>