<HTML>
<HEAD>
<TITLE>Products Sub-Categories</TITLE>
</HEAD>

<BODY>

<% 
  var oid = Request.value("OID");
  if (oid != null) {
  
    var cntmgrObj = new BVI_ContentManager();
	if (cntmgrObj != null) {
	  var catObj = cntmgrObj.categoryInfo(oid,"TK","PRODUCT");
	  if (catObj != null) {
		if (!catObj.isLeaf) {
		  var childList = catObj.childCategories();
		  if (childList != null) {
			var i;
			var len = childList.length;
			for (i=0; i<len; i++) {
			  var childObj = childList.get(i);
			  if (childObj != null) {
			    if (childObj.isLeaf) {
				  Response.write("<A HREF='show_products.jsp?OID=" + childObj.oid + "&" + Session.Location.linkString() + "'>" + childObj.name + "</A><BR>");
			    } else {
				  Response.write("<A HREF='show_subcategories.jsp?OID=" + childObj.oid + "&" + Session.Location.linkString() + "'>" + childObj.name + "</A><BR>");
				}
			  }
			}
		  }
		}
	  }
	}
  }
%>

</BODY>

</HTML>
