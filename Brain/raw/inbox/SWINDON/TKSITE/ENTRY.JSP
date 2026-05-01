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
<img src="/tk/images/tkonline-store.gif">
<p><b><font face="Arial, Helvetica, sans-serif">Welcome to T&amp;K'S Online Store</font></b></p>
<p>This is the RSC BV development system. Please ask the development team before you have a dabble. Otherwise you run the risk of pissing us off. Big time.</p>
<p><font face="Arial, Helvetica, sans-serif"><b>If you are an existing customer, 
  please enter your details below :-</b></font></p>
<form method="post" action="login.jsp"><%=Session.Location.formString()%>
  <table width="400" border="0">
    <tr> 
      <td><font face="Arial, Helvetica, sans-serif"><b>Username:</b></font></td>
      <td> 
        <input type="text" name="username">
      </td>
      <td rowspan="2">&nbsp;</td>
    </tr>
    <tr> 
      <td><font face="Arial, Helvetica, sans-serif"><b>Password:</b></font></td>
      <td> 
        <input type="password" name="password">
      </td>
    </tr>
  </table>
  <p>
    <input type="submit" name="Submit" value="Let's go shop">
  </p>
  <p><font face="Arial, Helvetica, sans-serif"><a href="dummy.jsp?<%=Session.Location.linkString()%>"><font size="2">Forgotten 
    your username or password? Don't worry, click here for help.</font></a></font></p>
  <p><font face="Arial, Helvetica, sans-serif"><a href="register_form.jsp?<%=Session.Location.linkString()%>">New 
    customer? Click here to register.</a></font></p>
  </form>
<p>&nbsp;</p><p>&nbsp;</p>
<p>&nbsp; </p>
<p>&nbsp; </p>
</body>
</html>

  