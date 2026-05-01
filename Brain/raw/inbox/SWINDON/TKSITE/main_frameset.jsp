<HTML>
<FRAMESET COLS="200,*">
  <FRAME NAME="sidebar" SRC="sidebar.jsp?<%=Session.Location.linkString()%>">
  <FRAME NAME="main" SRC="show_categories.jsp?<%=Session.Location.linkString()%>">
</FRAMESET>
</HTML>