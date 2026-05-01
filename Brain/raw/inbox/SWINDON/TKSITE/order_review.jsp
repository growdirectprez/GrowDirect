<!-- #include file="utilities.jsp" -->

<HTML>
<HEAD>
  <TITLE>T&K Order Review Page</TITLE>
</HEAD>

<BODY>
<H1><FONT color='#660000'>Order Review</FONT></H1>
<BR>

<!-- Verify shopper has payment method -->
<!-- Verify shopper has shipping address -->
<!-- Order Summary -->

<%
  displayCartContents();
  displayShippingAddress();
  displayPaymentMethod();
  displayBuyButton();
%>

</BODY>
</HTML>


<%
function displayCartContents() {

  %>
  <H3><FONT color='#660000'>Order Summary</FONT>
  <BR><BR>
 
  <!-- Cart Header -->
  <TABLE border=0 width='90%'>
    <TR bgcolor='#660000'>
	  <TH><FONT color=white>Product Name</TH>
	  <TH><FONT color=white>Product Id</TH>
	  <TH><FONT color=white>Quantity</TH>
	  <TH><FONT color=white>Unit Price</TH>
	  <TH><FONT color=white>Total Price</TH>
	</TR>
	
  <!-- Cart Content -->
  <%
  var bgColor;
  var cartList = Session.MRSalesRep.subtotal().PRICED_ITEMS;
  for (i=0; i<cartList.length; i++) {
  	var cartItem = cartList.get(i);
	bgColor = (i%2) ? "#FF9999" : "#FFCCCC" ;
    %>	  
	
	<TR BGCOLOR=<%=bgColor%>>
	  <TD ALIGN=left><%=cartItem.PRODUCT_NAME%>
	  <TD ALIGN=center><%=cartItem.PRODUCT_ID%>
	  <TD ALIGN=center><%=cartItem.QUANTITY%>
	  <TD ALIGN=right><%=visitorCurrency()%><%=cartItem.QUOTED_PRICE%>
    
	  <%  
	  var totalDbl = (cartItem.QUANTITY * cartItem.QUOTED_PRICE.doubleValue);
      %>	  
	  <TD ALIGN=right><%=visitorCurrency()%><%=totalDbl%>  
	</TR>  
    <%	
  }
  %>
  </TABLE>
  
  <%
    var total = Session.MRSalesRep.total();
    var subTotal = total.TOTAL_PRICE.stringValue;
	var taxTotal = total.TOTAL_TAXES.stringValue;
	var shpTotal = total.TOTAL_SHIPPING.stringValue;
	var grdTotal = total.GRAND_TOTAL.stringValue;
  %>
  
  <!-- Cart Footer -->
  <TABLE BORDER=0 WIDTH='90%' BGCOLOR='#660000'>
    <TR><TD WIDTH='85%' ALIGN=right><FONT COLOR=white><B>Order Sub-Total</B>
	    <TD WIDTH='15%' ALIGN=right><FONT COLOR=white><%=subTotal%>
	<TR><TD WIDTH='85%' ALIGN=right><FONT COLOR=white><B>Total Tax</B>
	    <TD WIDTH='15%' ALIGN=right><FONT COLOR=white><%=taxTotal%>
	<TR><TD WIDTH='85%' ALIGN=right><FONT COLOR=white><B>Total Shipping</B>
	    <TD WIDTH='15%' ALIGN=right><FONT COLOR=white><%=shpTotal%>
	<TR><TD WIDTH='85%' ALIGN=right><FONT COLOR=white><B>Grand Total</B>
	    <TD WIDTH='15%' ALIGN=right><FONT COLOR=white><B><%=grdTotal%></B>
  </TABLE>
  
  <%	
}
%>

<!-- Shipping Address -->
<%
function displayShippingAddress() {

  var destination = Session.MRSalesRep.total().DESTINATION;
  
  %>
  <BR>
  <HR ALIGN=left WIDTH='90%'>
  <H3><FONT color='#660000'>Shipping Address</FONT>
  <BR><BR>
  
  <TABLE BORDER=0>
    <TR><TD ALIGN=right><B>Name:</B>
	    <TD><%= destination.NAME %>
	<TR><TD ALIGN=right><B>Address:</B>
	    <TD><%= destination.ADDRESS %>
	<TR><TD ALIGN=right><B>City:</B>
	    <TD><%= destination.CITY %>
	<TR><TD ALIGN=right><B>State/County:</B>
	    <TD><%= destination.STATEORPROVINCE %>
	<TR><TD ALIGN=right><B>Country:</B>
	    <TD><%= destination.COUNTRY %>
	<TR><TD ALIGN=right><B>Zip/Post Code:</B>
	    <TD><%= destination.ZIPORPOSTALCODE %>
	<TR><TD ALIGN=right><B>Phone Number:</B>
	    <TD><%= destination.PHONE %>
	<TR><TD ALIGN=right><B>E-Mail Address:</B>
	    <TD><%= destination.EMAIL %>
	<TR><TD ALIGN=right><B>Shipping Method:</B>
	    <TD><%= destination.SHIPPINGTYPE %>
  </TABLE>
  
  <%
}
%>

<!-- Payment Method -->
<%
function displayPaymentMethod() {
  %>
  <BR>
  <HR ALIGN=left WIDTH='90%'>
  <H3><FONT color='#660000'>Payment Method</FONT>
  <BR><BR>
  
  <FORM ACTION="order_confirmation.jsp" METHOD="post">
  <%=Session.Location.formString()%>
  
  <TABLE BORDER=0>
    <TR>
	<TD ALIGN=right><B>Choose a payment method:</B>
	<TD ALIGN=left>
	  <SELECT NAME="payment-type">
	<%
	  // generate the list from the visitors stored payment methods
	  var paymentName = null;
	  var preferredPM = Session.MRWallet.getPaymentPreference();
	  var paymentList = Session.MRWallet.getPaymentMethodNameList("TK");
	  for (i=0; i<paymentList.length(); i++) {
	    var tmpName = paymentList.get(i);
		var selected='';
		if (tmpName == preferredPM) {
		  selected = 'SELECTED'
		}
		paymentName = DecodeGuestPaymentName(tmpName);
		%>
		<OPTION VALUE="<%=HTMLEncode(paymentName)%>" <%=selected%>> <%=paymentName%>
		<%
	  }
	  
	%>
  </TABLE>
  <%
}
%>

<!-- Buy it now -->
<%
function displayBuyButton() {
  %>
  <BR>
  <INPUT TYPE="submit" VALUE="Don't delay - Buy right away...">
  </FORM>
  <%
}
%>