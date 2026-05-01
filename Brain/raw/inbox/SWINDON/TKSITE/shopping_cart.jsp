<!-- #include file="tk/scripts/utilities.jsp" -->

<HTML>
<HEAD>
<TITLE>T&K Shopping Cart Page</TITLE>
</HEAD>

<BODY>

<H1><FONT color='#660000'>T&K Shopping Cart</FONT></H1>

<% 
  var action = Request.value("ACTION");

  if (action != null) {
    var sRep = Session.MRSalesRep;
	if (sRep != null) {

      switch (action) {
	    case 'display_cart':
		  displayShoppingCart(sRep);
		  break;
	    case 'add_item_to_cart':
	      addItemToCart(sRep);
		  displayShoppingCart(sRep);
		  break;
		case 'update_quantity':
		  updateQuantity(sRep);
		  displayShoppingCart(sRep);
		  break;  
		case 'delete_item_from_cart':
		  deleteItemFromCart(sRep);
		  displayShoppingCart(sRep);
		  break;    
		default:
		  Response.write("<P>(Default)Action is " + action + "</P>");  
	  }
	} else {
	  // add error handling
	}  
  } else {
    // add error handling
	Response.write("<P>Action is null</P>");
  }
  
%>

</BODY>
</HTML>


<%
function addItemToCart(salesRep) {
  
  var oid = Request.value("OID");
  var qty = Request.value("QUANTITY");
  
  if (oid != null && qty != null) {
    
	// test to see if item is already in cart
	var duplicate = false;
	var cartList = salesRep.getItemList();
	for (i=0; i<cartList.length; i++) {
	  if (oid == cartList.get(i).OID) {
	    %>
		<P><%=cartList.get(i).PRODUCT_NAME%> is already in you shopping cart. Use the Quantity field on this page to change the quantity ordered.</P>
		<%
		duplicate = true;
	  }
	}
	
	if (!duplicate) {
	  // add the product to the cart
	  var item = new BVI_Properties();
	  item.OID = oid;
	  item.QUANTITY = qty;
	  item.CONTENT_TYPE = 0;
	  sRep.addItem(item);
	  if (Error.set) {
	    // add error handling : failed to add item
	  }
	}  
  } else {
    // add error handling : oid or qty was null
  }
}
%>


<%
function updateQuantity(salesRep) {
  
  if (salesRep != null) {
    var cartList = salesRep.subtotal().PRICED_ITEMS;
	for (i=0; i<cartList.length; i++) {
	  var qty = Request.value("QUANTITY_" + i);
	  var item = cartList.get(i);
      salesRep.updateQuantity(item.objectValue,qty);
    }
  }
}
%>


<%
function deleteItemFromCart(salesRep) {
  
  var oid = Request.value("OID");
  var cartList = salesRep.subtotal().PRICED_ITEMS;
  for (i=0; i<cartList.length; i++ ) {
    var cartItem = cartList.get(i);
	if (cartItem.OID == oid) {
	  salesRep.removeItem(cartItem.objectValue);
	  if (Error.set) {
	    // add error handler
	    Response.write("<P>Failed to delete item: error = " + Error.code + "</P>");
	  }
	  break;
	}
  }
}
%>

<%
function displayShoppingCart(salesRep) {
  if (salesRep != null) {
    // Test for cart being emtpy (both current & persistent)	
    if ((salesRep.subtotal().PRICED_ITEMS.length == 0)) {
      Response.write("<P><B>Your shopping cart is empty</B></P>");
	  RETURN();
	} else {
	  displayCartHeader();
	  displayCartContent(salesRep);
	  displayCartFooter(salesRep);
	  displayCartButtons();
	}  
  } else {
    // add error handler
  }
}
%>


<%
function displayCartHeader() {
  %>
  <BR>
  <FORM ACTION="shopping_cart.jsp" method="post">
  <%=Session.Location.formString()%>
  <INPUT TYPE="hidden" NAME="ACTION" VALUE="update_quantity">
  
  <TABLE border=0 width='90%'>
    <TR bgcolor='#660000'>
	  <TH><FONT color=white>Options</TH>
	  <TH><FONT color=white>Product Name</TH>
	  <TH><FONT color=white>Product Id</TH>
	  <TH><FONT color=white>Quantity</TH>
	  <TH><FONT color=white>Unit Price</TH>
	  <TH><FONT color=white>Total Price</TH>
	</TR>
  <%	  
}
%>


<%
function displayCartContent(salesRep) {	  

  if (salesRep != null) {
	
    var bgColor;
    var cartList = salesRep.getItemList();
	
	for (i=0; i<cartList.length; i++) {
	  var cartItem = cartList.get(i);
	  bgColor = (i%2) ? "#FF9999" : "#FFCCCC" ;
    %>	  
	
	  <TR BGCOLOR=<%=bgColor%>>
	    <TD><A HREF="shopping_cart.jsp?<%=Session.Location.linkString()%>&ACTION=delete_item_from_cart&OID=<%=cartItem.OID%>">Delete Item</A>
	    <TD ALIGN=left><%=cartItem.PRODUCT_NAME%>
	    <TD ALIGN=center><%=cartItem.PRODUCT_ID%>
	    <TD ALIGN=center><INPUT TYPE="text" NAME="QUANTITY_<%=i%>" VALUE="<%=cartItem.QUANTITY%>" SIZE=5 MAXLENGTH=5>
	    <TD ALIGN=right><%=visitorCurrency()%><%=cartItem.QUOTED_PRICE%>
    
	  <%  
	  var totalDbl = (cartItem.QUANTITY * cartItem.QUOTED_PRICE.doubleValue);
      %>	  
	    <TD ALIGN=right><%=visitorCurrency()%><%=totalDbl%>  
      <%	  
	}
	%>
	</TABLE>
	<%
  }
}
%>

<%
function displayCartFooter(salesRep) {
  if (salesRep != null) {
  %>
    <TABLE border=0 width='90%'>
    <TR BGCOLOR='#660000'>
	<TD WIDTH='85%' ALIGN=right>
	<FONT COLOR=white>
	<B>Product Sub-Total</B>
	<TD ALIGN=right>
  <%
    var cartTotal = salesRep.subtotal().TOTAL_PRICE.doubleValue;
  %>
    <FONT COLOR=white>
    <B><%=visitorCurrency()%><%=cartTotal%></B>
    </TABLE>
  <%
  } else {
    // add error handler
  }
}
%>

<%
function displayCartButtons() {
  %>
  <BR>
  <TABLE border=0 width="90%">
  <TR>
    <TD width="33%" align="right"><INPUT TYPE="submit" VALUE="Update Cart"></TD>
    </FORM>
	<TD width="33%" align="right"><A HREF="show_categories.jsp?<%=Session.Location.linkString()%>">Continue Shopping</A></TD>
	<TD width="33%" align="right"><A HREF="pay_methods.jsp?<%=Session.Location.linkString()%>">Checkout Now</TD>
  </TR>	
  </TABLE>
  
  <!-- TEST CODE ONLY -->
  <BR><BR>
  <P><B>Test link only</B></P>
  <A href="order_review.jsp?<%=Session.Location.linkString()%>">Order Review Page</A>
  <!-- END OF TEST CODE -->
  
  <%
} 
%>