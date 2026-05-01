<!-- #include file="tk/scripts/utilities.jsp" -->

<HTML>
<HEAD>
<TITLE>Products Detail</TITLE>
</HEAD>

<BODY>

<% 
  var oid = Request.value("OID");
  if (oid != null) {
	var cntmgrObj = new BVI_ContentManager();
	if (cntmgrObj != null) {
	  var cntObj = cntmgrObj.contentByOID(oid,"TK","PRODUCT");
	  if (cntObj != null) { %>
	    <TABLE border='1'>
		<TR><TD width='10%'><IMG src=' <%= cntObj.FULL_IMAGE %> '><TD width='90%'> <%= cntObj.NAME %>
		</TABLE>
		<P> <%= cntObj.LONGDESC %> </P>
		<P>Price: <%=visitorCurrency()%><%=cntObj.PRICE%> per item</P>
        
		<!-- Add to Shopping List -->
        <FORM ACTION="shoplist.jsp">
		<%=Session.Location.formString()%>
		<INPUT TYPE="HIDDEN" NAME="oid" VALUE="<%=oid%>">
		<INPUT TYPE="HIDDEN" NAME="action" VALUE="add_item_to_list">
		<INPUT NAME="submit" TYPE="IMAGE" SRC="/tk/images/add_to_shopping_list.jpg">
        </FORM>
	
		<!--  Shopping Cart -->
		<FORM ACTION="shopping_cart.jsp" METHOD=post>
		<%= Session.Location.formString() %>
		<P>Quantity:  </P>
		<INPUT TYPE=hidden NAME=OID VALUE=<%=cntObj.oid%>>
		<INPUT TYPE=hidden NAME=ACTION VALUE='add_item_to_cart'>
		<INPUT TYPE=text NAME=QUANTITY VALUE=1 SIZE=5 MAXLENGTH=5>
		<BR>
		<INPUT TYPE=image src='/tk/images/add-to-basket.gif'>
	    </FORM>
		<%
	  }
	}
  }	
%>

</BODY>

</HTML>
