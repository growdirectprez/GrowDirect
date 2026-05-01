<html>
<%
initSessionState();
Session.setCurrentService(102);
%>
<head>
<title>Untitled Document</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>

<body bgcolor="#FFFFFF">
<p><b><font face="Arial, Helvetica, sans-serif">Welcome to T&amp;K'S Online </font></b></p>
<p><font face="Arial, Helvetica, sans-serif"><b>Please enter your details below.</b></font></p>
<form method="post" action="register.jsp"><%=Session.Location.formString()%>
  <table width="400" border="0">
    <tr> 
      <td><font face="Arial, Helvetica, sans-serif"><b>Username:</b></font></td>
      <td> 
        <input type="text" name="username">
      </td>
      <td rowspan="3">&nbsp;</td>
    </tr>
    <tr> 
      <td><font face="Arial, Helvetica, sans-serif"><b>Password:</b></font></td>
      <td> 
        <input type="password" name="password">
      </td>
    </tr>
    <tr> 
      <td><font face="Arial, Helvetica, sans-serif"><b>Password:</b></font></td>
      <td>
        <input type="password" name="password2">
      </td>
    </tr>
    <tr>
      <td>&nbsp;</td>
      <td>&nbsp;</td>
      <td>&nbsp;</td>
    </tr>
  </table>
  <p> 
    <input type="submit" name="Submit" value="Register">
  </p>
  <p>&nbsp;</p>
  </form>
<p>&nbsp;</p><p>&nbsp;</p>
<p>&nbsp; </p>
<p>&nbsp; </p>
</body>
</html>

  