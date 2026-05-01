<%
var username = Request.value('username');
var password = Request.value('password');
var visitor = null;
var resultMessage = "No Message";
var loggedIn = false;

// Attempt to log user in
visitor = Session.visitorManager.visitor(username);

if (Error.set || visitor == null) {
   resultMessage = "Username bad.";
} else {
   if (visitor.isPasswordValid(password) == 0) {
      resultMessage = "Username OK, but that's the wrong password";
   } else {
	  loggedIn = true;
      setCurrentVisitor(visitor);
	  Session.setCurrentUser(visitor.ID);
	  Session.visitorId = visitor.ID;
	  Session.storeName="TK";
	  setCurrentService("TK");
	  Session.MRSearch = new BVI_MRParamSearch(Session.storeName,"PRODUCT");
	  if (initMRComponents() != false) {
	      // Restore persistent shopping cart
		  var sRep = Session.MRSalesRep;
	      if (sRep.getItemListFromPersistentCart().length != 0) {
		    sRep.restoreFromPersistentCart();
		    sRep.clearPersistentCart();
		  }
	      // Set shopping cart persistence on
	      sRep.saveShoppingCart = true;
		  sRep.saveShoppingCartInRealtime = true;
	      Response.redirect("main_frameset.jsp?" + Session.Location.linkString());
	  } else {
	     resultMessage = "Failed to create shopping cart";
	  }
	  
      resultMessage += "<p><b>Welcome to T&K's ";
      resultMessage += visitor.NAME;
      resultMessage += "</b>";

   }

}


%>

<HTML>
<FONT COLOR="GREEN"><%=resultMessage%></FONT><BR>
<%
if (loggedIn) {
%>
<A HREF="user_profile.jsp?<%=Session.Location.linkString()%>">Edit My Profile</A><BR>
<A HREF="show_categories.jsp?<%=Session.Location.linkString()%>">I wanna spend my wonga!</A><BR>
<A HREF="shoplist.jsp?action=list&<%=Session.Location.linkString()%>">List my shopping lists</A><BR>
<P>
<FORM ACTION="shoplist.jsp">
<%=Session.Location.formString()%>
<INPUT TYPE="hidden" NAME="action" VALUE="new">
<INPUT TYPE="submit" NAME="submit" VALUE="Create a new list called:">
<INPUT TYPE="text" NAME="listname">
</FORM>
<%
}
%>
</HTML>