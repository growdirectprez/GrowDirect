 

<%

// Cope with zero addresses case!!

var addressBook = new MR_AddressBook(currentVisitor());
var failureMessage = "";

var addressAlias = Request.value('address_alias');
var action;
if (Request.value('add_as_new_address')) { 
   action="add_as_new_address";
} else if (Request.value('update_existing_address')) {
   action="update_existing_address";
} else if (Request.value('delete_address')) {
   action="delete_address";
} else if (Request.value('retrieve_address')) {
   action="retrieve_address";
}
 

var ab_alias;
var ab_address;
var ab_address2;
var ab_city;
var ab_company_name;
var ab_country;
var ab_email;
var ab_fax;
var ab_name;
var ab_phone;
var ab_shipping_type;
var ab_state;
var ab_zip;
   
if (action == "delete_address") {
   Response.write('RESULT:' + addressBook.removeAddressByAlias(addressAlias));
   addressAlias = (addressBook.getAliases()).get(0);
   action = "retrieve_address";
}

if (action == "retrieve_address") {
  // Retrieve existing address
  var retrievedAddress = addressBook.getAddressByAlias(addressAlias);
  ab_alias = addressAlias;

  ab_name = retrievedAddress.NAME; 
  ab_address = retrievedAddress.ADDRESS;
  ab_address2 = "WHERE IS ADDRESS2 !!??";
  ab_city = retrievedAddress.CITY;
  ab_company_name = retrievedAddress.COMPANYNAME;
  ab_country = retrievedAddress.COUNTRY;
  ab_email = retrievedAddress.EMAIL;
  ab_fax = retrievedAddress.FAX;
  ab_phone_number = retrievedAddress.PHONENUMBER
  //ab_ship
  ab_state = retrievedAddress.STATEORPROVINCE;
  ab_zip = retrievedAddress.ZIPORPOSTALCODE;
} else {
   ab_alias = Request.value('ab_alias');
   ab_address = Request.value('ab_address');
   ab_address2 = Request.value('ab_address2');
   ab_city = Request.value('ab_city');
   ab_company_name = Request.value('ab_company_name');
   ab_country = Request.value('ab_country');
   ab_email = Request.value('ab_email');
   ab_fax = Request.value('ab_fax');
   ab_name = Request.value('ab_name');
   ab_phone = Request.value('ab_phone');
   ab_shipping_type = Request.value('ab_shipping_type');
   ab_state = Request.value('ab_state');
   ab_zip = Request.value('ab_zip');
}
  



if (action == "add_as_new_address") {
   
   if (ab_alias == "") {
      failureMessage += "<BR>You must specify a name for this address";
   }
   if ((ab_address == "") && (ab_address2 == "")) {
      failureMessage += "<BR>You must specify an address";
   }
   if (ab_city == "") {
      failureMessage += "<BR>You must specify a city/town";
   }
   if (ab_name == "") {
      failureMessage += "<BR>You must specify a recipient name";
   }
   if (ab_state == "") {
      failureMessage += "<BR>You must specify a county/state";
   }
   if (ab_zip == "") {
      failureMessage += "<BR>You must specify a post/zip code";
   }
}

if ((action == "add_as_new_address" || action == "update_existing_address") & (failureMessage == "")) {

   var addressObject = new BVI_Properties;
   addressObject.ALIAS = ab_alias;
   addressObject.NAME = ab_name;
   addressObject.ADDRESS = ab_address;
   addressObject.CITY = ab_city;
   addressObject.STATEORPROVINCE = ab_state;
   addressObject.COUNTRY = ab_country;
   addressObject.ZIPORPOSTALCODE = ab_zip;
   addressObject.PHONE = ab_phone;
   addressObject.EMAIL = ab_email;
   addressObject.SHIPPINGTYPE = "";
   if (action == "add_as_new_address") { 
      Response.write("RESULT:" + addressBook.insertNewAddress(addressObject));
   } else {
      Response.write("RESULT:" + addressBook.updateAddress(addressObject));
   }   
   Response.write(addressBook.lastError);
}   
   
%>
<html>
<head>
<title>Untitled Document</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>

<body bgcolor="#FFFFFF">
<p><font size="+2">Your Address Book</font></p>
<form method="post" action="">
<%=Session.Location.formString()%>
<%
var aliases = addressBook.getAliases();
if (aliases.length()>0) {
%>
<table width="75%" border="1">
  <tr>
    <td width="49%">Choose an existing address:</td>
    <td width="51%"> 
      <select name="address_alias" size="1">
<%

for (var i=0; i<aliases.length();i++) {
%>
        <option value="<%=aliases.get(i)%>"<%=aliases.get(i)==addressAlias ? ' SELECTED':''%>><%=aliases.get(i)%></option>
<%
}%></select><INPUT TYPE="SUBMIT" NAME="retrieve_address" VALUE="Retrieve address">

    </td>
  </tr>
</table>
<%
}
%>		


   <FONT COLOR=RED><%=failureMessage%></FONT><P>

  <table width="75%" border="1">
    <tr> 
      <td bgcolor="#660000"><font color="#FFFFFF">Name for this address (e.g. 
        home)</font></td>
      <td> 
        <input type="text" name="ab_alias" maxlength="50" size="50" value="<%=HTMLEncode(ab_alias,0)%>">
      </td>
    </tr>
    <tr> 
      <td bgcolor="#660000"><font color="#FFFFFF">Recipient Name</font></td>
      <td> 
        <input type="text" name="ab_name" maxlength="50" size="50" value="<%=HTMLEncode(ab_name,0)%>">
      </td>
    </tr>
    <tr> 
      <td bgcolor="#660000"><font color="#FFFFFF">Address</font></td>
      <td> 
        <input type="text" name="ab_address" maxlength="50" size="50" value="<%=HTMLEncode(ab_address,0)%>">
      </td>
    </tr>
    <tr> 
      <td bgcolor="#660000"><font color="#FFFFFF">Address (continued)</font></td>
      <td> 
        <input type="text" name="ab_address2" maxlength="50" size="50" value="<%=HTMLEncode(ab_address2,0)%>">
      </td>
    </tr>
    <tr> 
      <td bgcolor="#660000"><font color="#FFFFFF">City</font></td>
      <td> 
        <input type="text" name="ab_city" maxlength="50" size="50" value="<%=HTMLEncode(ab_city,0)%>">
      </td>
    </tr>
    <tr> 
      <td bgcolor="#660000"><font color="#FFFFFF">Company Name</font></td>
      <td> 
        <input type="text" name="ab_company_name" maxlength="50" size="50" value="<%=HTMLEncode(ab_company_name,0)%>">
      </td>
    </tr>
    <tr> 
      <td bgcolor="#660000"><font color="#FFFFFF">Country</font></td>
      <td> 
        <input type="text" name="ab_country" maxlength="20" size="20" value="<%=HTMLEncode(ab_country,0)%>">
      </td>
    </tr>
    <tr> 
      <td bgcolor="#660000"><font color="#FFFFFF">E-Mail</font></td>
      <td> 
        <input type="text" name="ab_email" maxlength="50" size="50" value="<%=HTMLEncode(ab_email,0)%>">
      </td>
    </tr>
    <tr> 
      <td bgcolor="#660000"><font color="#FFFFFF">Fax</font></td>
      <td> 
        <input type="text" name="ab_fax" maxlength="50" size="50" value="<%=HTMLEncode(ab_fax,0)%>">
      </td>
    </tr>
    <tr> 
      <td bgcolor="#660000"><font color="#FFFFFF">Phone Number</font></td>
      <td> 
        <input type="text" name="ab_phone" maxlength="50" size="50" value="<%=HTMLEncode(ab_phone,0)%>">
      </td>
    </tr>
    <tr> 
      <td bgcolor="#660000"><font color="#FFFFFF">Shipping Method (list)</font></td>
      <td> 
        <select name="select">
          <option value="PaperBag" selected>PaperBag</option>
          <option value="TurboBox">TurboBox</option>
        </select>
      </td>
    </tr>
    <tr> 
      <td bgcolor="#660000"><font color="#FFFFFF">County / State</font></td>
      <td> 
        <input type="text" name="ab_state" maxlength="20" size="20" value="<%=HTMLEncode(ab_state,0)%>">
      </td>
    </tr>
    <tr> 
      <td bgcolor="#660000"><font color="#FFFFFF">Post/Zip Code</font></td>
      <td> 
        <input type="text" name="ab_zip" maxlength="20" size="20" value="<%=HTMLEncode(ab_zip,0)%>">
      </td>
    </tr>
  </table>
  <p> 
    <input type="submit" value="Add as new address" name="add_as_new_address">
    <input type="submit" name="update_existing_address" value="Update existing address">
	<input type="submit" name="delete_address" value="Delete">
  </p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
</form>
</body>
</html>

<%

function addAsNewAddress() {

   var validationMessage = null;

   
   // Validate entry
   if (ab_country == "Scottish") {
      validationMessage += "<BR>Ock Eye The Noo!";
   }
   
   if (validationMessage != null) {
      Response.write(validationMessage);
   }
}
   
%>