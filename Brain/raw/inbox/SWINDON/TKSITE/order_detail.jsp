<%
  var orderNumber = Request.value("order_number");
  var invoice = null;
  if (!isEmptyString(orderNumber)) {
	 invoice = Session.MRWallet.getInvoice(orderNumber);
	 if (invoice == null) {
	   // add error handler
	   RETURN();
	 }
  } else {
	// add error handler
	RETURN();
  }
%>

<HTML>
<HEAD>
<TITLE>T&K Order History Page</TITLE>
</HEAD>

<BODY>

  <H1><FONT color='#660000'>Order Detail</FONT></H1>
  <BR>
  
  <!--------------------------->
  <!-- Display order details -->
  <!--------------------------->
  <TABLE BORDER=0>
    <TR>
	  <TD ALIGN=right><B>Order Number:</B>
	  <TD ALIGN=left><%=invoice.ORDER_NUMBER%>
    <TR>
	  <TD ALIGN=right><B>Order Date:</B>
	  <TD ALIGN=left><%=invoice.ORDER_DATE%>
  </TABLE>
  <BR>
  
  <TABLE BORDER=0 WIDTH='95%'>
    <TR BGCOLOR='#660000'>
		<TH ALIGN=center><FONT COLOR=white>Product ID
	    <TH ALIGN=center><FONT COLOR=white>Product Name
		<TH ALIGN=center><FONT COLOR=white>Quantity
		<TH ALIGN=center><FONT COLOR=white>Price
  
    <!-- Get the individual items that made up the order -->
	<%
	var items = invoice.PRICED_ITEMS;
	if (items != null) {
	  var bgColor;
	  for (i=0; i<items.length; i++) {
	    var item = items.get(i);
	    bgColor = (i%2) ? "#FF9999" : "#FFCCCC" ;
		%>
		<TR BGCOLOR=<%=bgColor%>>
		  <TD ALIGN=center><%=item.PRODUCT_ID%>
		  <TD ALIGN=center><%=item.PRODUCT_NAME%>
		  <TD ALIGN=center><%=item.QUANTITY%>
		  <TD ALIGN=right><%=item.ADJUSTED_PRICE%>
	    <%
	  }
	  %>
	  </TABLE>
	  
	  <!-- Show all of the sub-totals & grand total -->
	  <%
	  var taxTotal = invoice.TOTAL_TAXES.stringValue;
	  var shpTotal = invoice.TOTAL_SHIPPING.stringValue;
	  var grdTotal = invoice.GRAND_TOTAL.stringValue;
	  %>
	  <TABLE BORDER=0 WIDTH='95%' BGCOLOR='#660000'>
	      <TR><TD WIDTH='85%' ALIGN=right><FONT COLOR=white><B>Total Tax:</B>
	          <TD WIDTH='15%' ALIGN=right><FONT COLOR=white><%=taxTotal%>
	      <TR><TD WIDTH='85%' ALIGN=right><FONT COLOR=white><B>Total Shipping:</B>
	          <TD WIDTH='15%' ALIGN=right><FONT COLOR=white><%=shpTotal%>
	      <TR><TD WIDTH='85%' ALIGN=right><FONT COLOR=white><B>Grand Total:</B>
	          <TD WIDTH='15%' ALIGN=right><FONT COLOR=white><B><%=grdTotal%></B>
	  </TABLE>
	  <BR><BR>
	  
	  <!-- Display the address to which the order was shipped -->
	  <%
	  var destination = invoice.DESTINATION;
	  %>
	  <P>The shipping address used for this order was:</P>
	  <TABLE BORDER=0>
	    <TR><TD ALIGN=right><B>Name:</B>
		    <TD ALIGN=left><%=destination.NAME%>
		<TR><TD ALIGN=right><B>Address:</B>
			<TD ALIGN=left><%=destination.ADDRESS%>
		<TR><TD ALIGN=right><B>City:</B>
			<TD ALIGN=left><%=destination.CITY%>
		<TR><TD ALIGN=right><B>State/County:</B>
			<TD ALIGN=left><%=destination.STATEORPROVINCE%>
		<TR><TD ALIGN=right><B>Zip/Post Code:</B>
			<TD ALIGN=left><%=destination.ZIPORPOSTALCODE%>
		<TR><TD ALIGN=right><B>Country:</B>
			<TD ALIGN=left><%=destination.COUNTRY%>
	  </TABLE>
	  <%
	} else {
	  // add error handler
	}
	%>  
    
</BODY>
</HTML>


