
<%
//User Profile editor

var userProp = new BVI_Properties;
var visitor = currentVisitor();

if (Request.value('action_type') == "save_update") {
   userProp.NAME = Request.value('user_name');
   userProp.ADDRESS = Request.value('user_address');
   userProp.CITY = Request.value('user_city');
   userProp.EMAIL = Request.value('user_email');
   userProp.COUNTRY = Request.value('user_country');
   visitor.updateProperties(userProp);
   if (Error.set) {
       Response.write("ERROR! " + Error.reason);
   } else {

       Response.localRedirect('/tk/scripts/show_categories.jsp');
	   RETURN();
   }
} else {
%>
<body bgcolor="#FFFFFF">
<form method="post" action="user_profile.jsp">
  <%=Session.Location.formString()%>
  <H1>Your Profile:</H1>
  <table width="300" border="1">
    <tr>
      <td>Name:</td>
      <td> 
        <input type="text" name="user_name" value="<%=visitor.NAME%>">
      </td>
    </tr>
    <tr>
      <td>Address:</td>
      <td>
        <input type="text" name="user_address" value="<%=visitor.ADDRESS%>">
      </td>
    </tr>
    <tr>
      <td>City:</td>
      <td>
        <input type="text" name="user_city" value="<%=visitor.CITY%>">
      </td>
    </tr>
    <tr>
      <td>E-Mail:</td>
      <td>
        <input type="text" name="user_email" value="<%=visitor.EMAIL%>">
      </td>
    </tr>
    <tr>
      <td>Country:</td>
      <td>
	    <select name="user_country">
<%
if (visitor.COUNTRY == "USA") {
   Response.write('<option value="UK">UK</option><option selected value="USA">USA</option>');
} else {
   Response.write('<option selected value="UK">UK</option><option value="USA">USA</option>');
}
%>
		</select>
      </td>
    </tr>
    <tr>
      <td>&nbsp;</td>
      <td>&nbsp;</td>
    </tr>
  </table>
  <p>
    <input type="submit" name="action_type" value="save_update">
  </p>
</form>
<%
}%>
