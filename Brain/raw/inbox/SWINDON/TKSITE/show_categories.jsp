<HTML>
<HEAD>
<TITLE>Products Categories</TITLE>
</HEAD>

<BODY>

<% 
  var cntmgrObj = new BVI_ContentManager();
  
  if (cntmgrObj != null) {
	
	// Get all the OID's of the top level categories
	var query = "select OID, NAME from BV_CATEGORY where STORE_ID = 102 and PARENT_OID = 0";
	var cntList = cntmgrObj.contentByQuery(query);
	if (cntList != null) {
	  var i;
	  var cntObj;
	  var len = cntList.length;
	  for (i = 0;i < len; i++) {
	    cntObj = cntList.get(i);
		if (cntObj != null) {
		  var oid = cntObj.get("OID");
		  var name = cntObj.get("NAME");
		  Response.write("<A HREF='show_subcategories.jsp?OID=" + oid.stringValue + "&" + Session.Location.linkString() + "'>" + name.stringValue + "</A><BR>");
		}  
	  }
	}
  }
  
%>

</BODY>

</HTML>
