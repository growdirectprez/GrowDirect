<%
var shopListMgr = Session.MRShopListMgr;
var shopList;
var listName = Request.value('listname');
var visitorId = Session.visitorId;
var cntMgr = Session.serviceCM;
if (cntMgr == null) 
    cntMgr = new BVI_ContentManager();

// If this is the first visit to this script, create a new BVI_MRShopListMgr
if (shopListMgr == null) {
   shopListMgr = new BVI_MRShopListMgr(Session.storeName);
   Session.MRShopListMgr = shopListMgr;
}

function newList() {
   shopList = shopListMgr.newPersonalList(visitorId,listName);
}

function listLists() {
   var shopListNames = shopListMgr.getPersonalListNames(visitorId);
   var aListName;
   var listItems;

%>
<font size=+2>Your Shopping Lists</font><p>
<table width="75%" border="1">
  <tr bgcolor="#660000"> 
    <td><b><font color="#FFFFFF">List Name</font></b></td>
    <td><b><font color="#FFFFFF">Items</font></b></td>
    <td><b><font color="#FFFFFF">Options</font></b></td>
  </tr>
<%
   for (var i=0; i<shopListNames.length(); i++) {
      aListName = shopListNames.get(i);
	  listItems = shopListMgr.getPersonalListByName(visitorId,aListName).getItemList();
%>
  <tr> 
    <td><a href="shoplist.jsp?<%=Session.Location.linkString()%>&action=view_list_contents&list_name=<%=aListName%>"><%=aListName%></a></td>
    <td><%=listItems.length%></td>
    <td><a href="shoplist.jsp?<%=Session.Location.linkString()%>&action=delete_list&list_name=<%=aListName%>">Delete</A>
	    <a href="shoplist.jsp?<%=Session.Location.linkString()%>&action=add_list_to_cart&list_name=<%=aListName%>">Add To Cart</a></td>
  </tr>
<%
   }
%>

  <tr bgcolor="#660000"> 
    <td colspan="3">&nbsp;</td>
  </tr>
</table>

<%  
}

//
//  View/Update List Contents (view_list_contents)
//

function viewListContents() {
   var listName = Request.value('list_name');
   var aList = shopListMgr.getPersonalListByName(visitorId,Request.value('list_name'));
   var listItems = aList.getItemList();
%>
<FORM action="shoplist.jsp">
<%=Session.Location.formString()%>
<INPUT TYPE="hidden" NAME="action" VALUE="update_item_quantity">
<INPUT TYPE="hidden" NAME="list_name" VALUE="<%=listName%>">
<font size=+2>Your List '<%=listName%>'</font><p>
<!-- Table header -->
<TABLE BORDER=1>
  <TR bgcolor="#660000"> 
    <TD><b><font color="#FFFFFF">Quantity</font></b></TD>
    <TD><b><font color="#FFFFFF">Description</font></b></TD>
    <TD><b><font color="#FFFFFF">Options</font></b></TD>
  </tr>
<%
   for (var i=0; i<listItems.length; i++) {
      anItem = listItems.get(i);
      var anItemContent = cntMgr.contentByOID(anItem.OID, Session.storeName, anItem.CONTENT_TYPE);
%>
  <tr> 
    <td> 
      <input type="text" name="quantity_<%=i%>" value="<%=anItem.QUANTITY%>" size=3>
    </td>
    <td><a href=show_product_detail.jsp?<%=Session.Location.linkString()%>&oid=<%=anItem.OID%>><%=anItemContent.NAME%></a></td>
    <td><input type="submit" name="update_<%=i%>" value="Update"><a href="shoplist.jsp?<%=Session.Location.linkString()%>&action=remove_item&index=<%=i%>&list_name=<%=Request.value('list_name')%>">Remove</a> 
      <a href="shopping_cart.jsp?<%=Session.Location.linkString()%>&ACTION=add_item_to_cart&OID=<%=anItem.OID%>&QUANTITY=<%=anItem.QUANTITY%>">Add 
      To Cart</a> </td>
  </tr>
<%
  }
%> <!-- Footer --> 
  <TR bgcolor="#660000"> 
    <TD colspan="3">&nbsp;</TD>
  </TR>
</TABLE>
</FORM>
<P>

<%
}

function addItemToList() {
 
   var oid = Request.value('oid');
   
   if (Request.value('list_name') == null) {
      Response.write("<HTML><BODY><FORM ACTION=shoplist.jsp>" + Session.Location.formString());
	  Response.write("<INPUT TYPE=HIDDEN NAME=oid VALUE=" + oid + ">");
	  Response.write("<INPUT TYPE=HIDDEN NAME=action VALUE=add_item_to_list>");
      Response.write("Add to which list?<P>");
	  Response.write("<SELECT NAME=list_name>");

      var shopListNames = shopListMgr.getPersonalListNames(visitorId);
      var aListName;
   
      for (var i=0; i<shopListNames.length(); i++) {
         aListName = shopListNames.get(i);
         Response.write("<OPTION>" + aListName);
      }
	  Response.write("</SELECT><INPUT TYPE=submit VALUE=Add></FORM></BODY></HTML>");
   } else {
      // List has been chosen
	  Response.write("Adding item " + oid);
	  var aList = Session.MRShopListMgr.getPersonalListByName(visitorId,Request.value('list_name'));
	  var anItem = new BVI_Properties;
	  anItem.OID = oid;
	  anItem.QUANTITY = 1;
	  aList.addItem(anItem);
   }	  
}

function removeItemFromList() {
   var aList = shopListMgr.getPersonalListByName(visitorId,Request.value('list_name'));
   aList.removeItem(Request.value('index'));
}

function addListToCart() { 
// NOT CURRENTLY USED, SINCE WE DECIDED TO LEAVE ITEM IN LIST, LIKE WAL-MART
   var aList = shopListMgr.getPersonalListByName(visitorId,Request.value('list_name'));
   aList.removeItem(Request.value('OID'));
//   Response.redirect("shopping_cart.jsp?" + Session.Location.linkString() + "&OID=" + Request.value("OID") + "&QTY=" + Request.value('quantity_' + Request.value('OID'));
}


function deleteList() {

   var aList = shopListMgr.getPersonalListByName(visitorId, Request.value('list_name'));
   shopListMgr.removeList(aList);
}

function updateItemQuantity() {

   var keys = Request.subkeys("update_",true);
   var tokens = Request.tokenize(keys.get(0),"_");
   var index = parseInt(tokens.get(1));
   var newQuantity = Request.value("quantity_" + index);
   
   var aList = shopListMgr.getPersonalListByName(visitorId, Request.value('list_name'));
   
   if (newQuantity==0) {
      aList.removeItem(index);
   } else {
      var itemList = aList.getItemList();
	  var anItem = itemList.get(index).objectValue;
	  anItem.QUANTITY = newQuantity;
	  aList.updateItem(anItem);
   }
}   

if (Request.value('action') == 'add_list_to_cart') {
   // Move entire list to the cart.
   Response.write("Not implemented yet. Waiting for Shopping Cart to be finished.");
}


switch(Request.value('action')) {
   case 'new' :
      newList();
	  break;

   case 'list' :	  
      listLists();
	  break;
	  
   case 'view_list_contents' :
      viewListContents();
	  break;

   case 'add_item_to_list' : 
      addItemToList();
	  if (Request.value('list_name') != null) { 
         viewListContents();
      }
	  break;
	  
   case 'remove_item' : 
      removeItemFromList();
      viewListContents();
	  break;
	  
   case 'delete_list' :
      deleteList();
      listLists();
	  break;
	  
   case 'update_item_quantity' :
      updateItemQuantity();
	  viewListContents();
	  break;
	  
   default :
      Response.write("!!Unhandled case!!");
}
      
%>