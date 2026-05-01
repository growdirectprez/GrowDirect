
<HTML>
<HEAD>
<TITLE>T&K Search Results Page</TITLE>
</HEAD>

<BODY>

  <H1><FONT color='#660000'>Search Results</FONT></H1>
  <BR><BR>
  
  <%
  if (Session.MRSearchResult == null) {
    Response.write("<P>DEBUG : MRSearchResult == null</P>");
    Response.write("<P>There were no items matching your search criteria</P>");
	RETURN();
  } else {
    var resultCount = Session.MRSearchResult.getSearchResultCount();
    var message = "There were ";
    message += (resultCount == 0) ? "no" : resultCount
    message += " items matching your search criteria"
    Response.write(message);
  }	
  %>
  
  <TABLE BORDER=0 WIDTH='95%'>
    <TR BGCOLOR='#660000'>
	  <TH><FONT COLOR=white>Product Name</FONT>
	  <TH><FONT COLOR=white>Product ID</FONT>
	  <TH><FONT COLOR=white>Price</FONT>
  </TABLE>
    
</BODY>
</HTML>


