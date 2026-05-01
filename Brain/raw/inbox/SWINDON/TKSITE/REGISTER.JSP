<%

// Register a new user

var thisPage = "/tk/scripts/register.jsp";
var errorPage = "/tk/scripts/error.jsp";
var statusMsg = "";
var visitor = null;
var okay = true;
var username = Request.value('username');
var password = Request.value('password');
var password2 = Request.value('password2');

initSessionState();

Response.write("getCurrentUser:" + Session.getCurrentUser() + "<BR>");
Response.write("getCurrentService:" + Session.getCurrentService() + "<BR>");

visitor = Session.visitorManager.newVisitor(username,password);

if (Error.set) {
   Response.write("Error is set");
}

if (visitor == null) {
   Response.write("visitor is null");
}

if (Error.set || visitor == null) {
   statusMsg = "FAILED to create " + username;
} else {
   statusMsg = "Successfully created " + username;
}



//CurrentVisitor().registerGuest(Request.value('username'), Request.value('password'), true);

//if (Error.set || visitor == null) {
//   Session.errorMessage = "Failed to create new customer";
//   Session.errorReturn(thisPage);
//   visitScript(errorPage);
//}
//visitor = currentVisitor();
//
Session.cheeseType="Edam";
%>
<HTML>
<BODY>
<A HREF="entry.jsp">CLICK ME!</A></BODY>
</HTML>
