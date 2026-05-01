<%
initSessionState();
Session.setCurrentService(102);
%>
<HTML>
<FORM ACTION="login.jsp">
<%=Session.Location.formString()%>
Login as an existing user<BR>
Username: <INPUT TYPE="text" NAME="username"><BR>
Password: <INPUT TYPE="text" NAME="password"><BR>
<INPUT TYPE="submit" NAME="submit">
</FORM>
<p>
<FORM ACTION="register.jsp">
<%=Session.Location.formString()%>
Create a new user<BR>
Username: <INPUT TYPE="text" NAME="username"><BR>
Password: <INPUT TYPE="text" NAME="password"><BR>
Password: <INPUT TYPE="text" NAME="password2"><BR>
<INPUT TYPE="submit" NAME="submit">
</FORM>

</HTML>