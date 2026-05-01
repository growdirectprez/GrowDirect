<HTML>
<BODY>
<FONT COLOR="RED" SIZE=+2><%=currentVisitor().NAME%></FONT><P>
<A TARGET="main" HREF="user_profile.jsp?<%=Session.Location.linkString()%>">Edit My Profile</A><BR>
<A TARGET="main" HREF="show_categories.jsp?<%=Session.Location.linkString()%>">I wanna spend my wonga!</A><BR>
<A TARGET="main" HREF="shoplist.jsp?action=list&<%=Session.Location.linkString()%>">List my shopping lists</A><BR>
<A TARGET="main" HREF="shopping_cart.jsp?ACTION=display_cart&<%=Session.Location.linkString()%>">View Shopping Cart</A><BR>
<A TARGET="main" HREF="address_book.jsp?<%=Session.Location.linkString()%>">Do stuff with my address book</A><BR>
<A TARGET="main" HREF="order_history.jsp?<%=Session.Location.linkString()%>">View Purchase History</A><BR>
<A TARGET="main" HREF="search_quick.jsp?<%=Session.Location.linkString()%>&action=show">Quick Search</A><BR>
<BR>
<A TARGET="main" HREF="payment_methods.jsp?<%=Session.Location.linkString()%>">Mess with my payment methods!</A><BR>
<P>
<FORM ACTION="shoplist.jsp" TARGET="main">
<%=Session.Location.formString()%>
<INPUT TYPE="hidden" NAME="action" VALUE="new">
<INPUT TYPE="submit" NAME="submit" VALUE="Create list:">
<INPUT TYPE="text" NAME="listname">
</FORM>
</HTML>