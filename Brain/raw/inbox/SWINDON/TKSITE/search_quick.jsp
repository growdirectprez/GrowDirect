<!--------------------------------------------------------------------------->
<!-- Script must be called with "action" flag set to one of the following: -->
<!-- 			 		   				 	  	  	 	 				   -->
<!-- (1) show   : This will cause the search page to be displayed ready    -->
<!--              for the user to input the search criteria. This is the   -->
<!--			  all external scripts should use in calling this script   -->
<!-- (2) search : This action flag value is only set from within this      -->
<!--              script (although it could be used from elsewhere). It    -->
<!--              will take the users search criteria and perform the      -->
<!--              search. Following successfully execution of the search   -->
<!--			  the search results object is stored on the Session object-->
<!--			  as Session.MRSearchResult and the the user will be       -->
<!--			  redirected to the search_results page.	   		   	   -->
<!--------------------------------------------------------------------------->

<!------------------------>
<!-- JavaScript section -->
<!------------------------>

<%
  var action = Request.value("action");
  if (!isEmptyString(action)) {
    switch (action) {
	  case 'show':
	    // continues by default to HTML section below
	    break;
	  case 'search':
	    performSearch();
	    break;
	}
  } else {
    // add error handler
  }
%>


<%
function performSearch() {

  var sAttr = null;  // stores the (DB column) name of the search attribute
  var sOper = null;  // stores the search operand type
  var sSort = null;  // stores the search sort order attributes
  
  //////////////
  // DEBUG ONLY 
  var log = new BVI_Log();
  log.level = "critical";
  
  // set the name of the attribute to search on
  switch (Request.value("search_by")) {
    case 'prod_name':
	  sAttr = "NAME";
	  sOper = Session.MRSearch.LIKE;
	  break;
	case 'prod_desc':
	  sAttr = "LONGDESC";
	  sOper = Session.MRSearch.LIKE;
	  break;
	case 'prod_id':
	  sAttr = "PROD_ID";
	  sOper = Session.MRSearch.EQ;
	  break;
  }
  
  // set the search to return all rows
  Session.MRSearch.maxItems = 0;
  
  // make search case insensitive
  Session.MRSearch.isCaseSensitive = false;
  
  // build the search query
  Session.MRSearch.addStringQuery(sAttr,sOper,Request.value("search_for"));
    
  // set the search sort order
  sSort = new BVI_StringList();
  sSort.append(Request.value("sort_by"));
  Session.MRSearch.setOrderByQuery(sSort,Session.MRSearch.ASC);
  
  // perform the search
  Session.MRSearch.setCategory("/");
  Session.MRSearchResult = Session.MRSearch.getSearchResultList();
  log.send("critical","search_quick: getQueryString = " + Session.MRSearch.getQueryString());
  visitScript("/tk/scripts/search_results.jsp");

}
%>


<!------------------>
<!-- HTML Section -->
<!------------------>

<HTML>
<HEAD>
<TITLE>T&K Quick Search Page</TITLE>
</HEAD>

<BODY>

  <H1><FONT color='#660000'>Quick Search</FONT></H1>
  <BR><BR>
    
  <FORM ACTION="search_quick.jsp" METHOD="post">
  <%=Session.Location.formString()%>
  <INPUT TYPE="hidden" NAME="action" VALUE="search">
  
  <TABLE BORDER=0>
    <TR><TD ALIGN=right><B>Search For:</B>
	    <TD ALIGN=left><INPUT TYPE="text" NAME="search_for" WIDTH=50 MAXLENGTH=20>
	<TR><TD ALIGN=right><B>Search By:</B>
	    <TD ALIGN=left>
		  <SELECT NAME="search_by">
		    <OPTION VALUE=prod_name selected>Product Name</OPTION>
			<OPTION VALUE=prod_desc>Product Description</OPTION>
			<OPTION VALUE=prod_id>Product ID</OPTION>
		  </SELECT>
	<TR><TD ALIGN=right><B>Sorted By:</B>
	    <TD align=left>
		  <SELECT NAME="sort_by">
		    <OPTION VALUE="NAME" selected>Product Name</OPTION>
			<OPTION VALUE="PROD_ID">Product ID</OPTION>
			<OPTION VALUE="PRICE">Product Price</OPTION>
		  </SELECT>	
	<TR><TD>
	    <TD><INPUT TYPE="submit" NAME="searchBtn" VALUE="Lets go find it...">	  
  </TABLE>
  </FORM>
  	
</BODY>
</HTML>


