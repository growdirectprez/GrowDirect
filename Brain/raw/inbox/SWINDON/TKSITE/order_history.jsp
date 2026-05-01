
<!-- Only registered members can view their purchase history -->
<!-- Need to add code to check if a member & id not to       -->
<!-- re-direct them to the new users registration page       -->


<HTML>
<HEAD>
<TITLE>T&K Order History Page</TITLE>
</HEAD>

<BODY>

  <H1><FONT color='#660000'>Your Previous T&K Purchases</FONT></H1>
  <BR><BR>
  
  <!-- check for user having no previous purchases -->
  <%
   if (Session.MRWallet.getInvoiceSummaryList().length == 0) {
     Response.write("<P>You have not purchased anything with T&K yet !!</P>");
	 RETURN();
   }
  %>
  
  <!-- Table header -->
  <TABLE BORDER=0 WIDTH='95%'>
  
    <TR BGCOLOR='#660000'>
	  <TH ALIGN=center><FONT COLOR=white><B>Order Date</B></FONT>
	  <TH ALIGN=center><FONT COLOR=white><B>Order Number</B></FONT>
	  <TH ALIGN=center><FONT COLOR=white><B>Order Status</B></FONT>
	  <TH ALIGN=center><FONT COLOR=white><B>Order Value</B></FONT>
	  <TH ALIGN=center><FONT COLOR=white><B>More Info</B></FONT>
  
  <!-- Table Contents -->
  <%
    var bgColor;
	var orderList = Session.MRWallet.getInvoiceSummaryList();
	if (orderList != null) {
	  for (i=0; i<orderList.length; i++) {
	    bgColor = (i%2) ? "#FF9999" : "#FFCCCC" ;
		var invoiceSummary = orderList.get(i);
		
		if (invoiceSummary.SERVICE_NAME == "TK") {
		  %>
		    <TR BGCOLOR=<%=bgColor%>>
		    <TD ALIGN=center><%=invoiceSummary.ORDER_DATE%>
		    <TD ALIGN=center><%=invoiceSummary.ORDER_NUMBER%>
		    <TD ALIGN=center><%=invoiceSummary.ORDER_STATE%>
		    <TD ALIGN=right><%=invoiceSummary.TOTAL.stringValue%>
		    <TD ALIGN=center><A HREF="order_detail.jsp?<%=Session.Location.linkString()%>&order_number=<%=invoiceSummary.ORDER_NUMBER%>">Order Details</A>
		  <%
		} else {
		  // ignore all purchases for no n T&K stores
		}  
	  }
	} else {
	  // add error handler
	  Response.write("<P>order_history.jsp : orderList is NULL</P>");
	}
  %>
  </TABLE>
  
  
</BODY>
</HTML>


