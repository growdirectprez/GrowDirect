<!-- #include file="tk/scripts/utilities.jsp" -->

<HTML>
<HEAD>
<TITLE>Product Detail</TITLE>
</HEAD>

<BODY>

<% 
  var oid = Request.value("OID");
  if (oid != null) {
    var cntmgrObj = new BVI_ContentManager();
	if (cntmgrObj != null) {
	  var catObj = cntmgrObj.categoryInfo(oid,"TK","PRODUCT");
	  if (catObj != null) {
		var cntList = catObj.childContent(null);
		if (cntList != null) {
		
		  Response.write("<TABLE>");
		  Response.write("<TD width=100>Product Img");
		  Response.write("<TD width=250>Product Name");
		  Response.write("<TD width=100>Product Price");
		  
		  for (i=0; i<cntList.length; i++) {
		    var cntObj = cntList.get(i);
			if (cntObj != null) {
			  Response.write("<TR>");
			  Response.write("<TD width=100>" + "<IMG src='" + cntObj.PREVIEW_IMAGE + "'>");
			  Response.write("<TD width=250>" + "<A HREF='show_product_detail.jsp?OID=" + cntObj.OID + "&" + Session.Location.linkString() + "'>" + cntObj.NAME + "</A>");
			  Response.write("<TD width=100>" + visitorCurrency() + cntObj.PRICE);
			}
		  }
		  Response.write("</TABLE>");
		}
	  }
	}
  }
%>

</BODY>

</HTML>
