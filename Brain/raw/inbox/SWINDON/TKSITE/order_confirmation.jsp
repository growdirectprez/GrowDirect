<HTML>
<HEAD>
  <TITLE>T&K Order Confitrmation Page</TITLE>
</HEAD>

<BODY>
<H1><FONT color='#660000'>Order Confirmation</FONT></H1>
<BR>

<%
  // get the system assigned order number
  var salesRep = Session.MRSalesRep;
  var orderNumber = salesRep.getOrderNumber();
  if (!Error.set && !isEmptyString(orderNumber)) {
    // get the payment type to be used (from previous page)
	var pmtMethod = Request.value("payment-type");
	if (!isEmptyString(pmtMethod)) {
	  // perform the checkout
	  salesRep.checkout(EncodeGuestPaymentName(pmtMethod));
	  if (!Error.set) {
	    // Display message
		%>
		<P>#include 'standard corporate bullshit.h'<BR>
		   Your order has been received & you should shortly receive an e-mail with your order details.
		   Thanks for buying through T&K's on-line store... etc...  
		   <BR><BR>
		   <TABLE BORDER=0>
		     <TR><TD><B>Order Number: </B>
			     <TD><%=salesRep.total().ORDER_NUMBER%> </B>
		     <TR><TD><B>Order Date:</B>
			     <TD><%=salesRep.total().ORDER_DATE%>
		   </TABLE>	 
		</P>   
		<%
	    // Increment the BOUGHT counter for this product
		// Log the buy event
	  } else {
	    // add error handler
		Response.write("<P>Failed to checkout via MRSalesRep</P>");
	  }
	} else {
	  // add error handler
	  Response.write("<P>payment-type parameter not passed</P>");
	}
  } else {
    // add error handler
	Response.write("<P>Failed to get an order number for the shopping cart</P>");
  }
  
%>


</BODY>
</HTML>

