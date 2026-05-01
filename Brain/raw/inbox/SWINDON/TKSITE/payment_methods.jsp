<!-- #include file="tk/scripts/utilities.jsp" -->

<%
var pm;
var pmPaymentMethodName;
var pmPaymentName;
var pmPmttypeId;
var pmCardNumber;
var pmFirstName;
var pmMiddleName;
var pmLastName;;
var pmValidDate;
var pmExpiryDate;
var pmPreference;

var pmPreferredMethodName;
var validMsg = "";

%>

<html>
<body bgcolor="#FFFFFF">
<p><font size="+2" face="Arial, Helvetica, sans-serif"><b>Your Payment Methods</b></font></p>
<form action="" method="post">
<%=Session.Location.formString()%>
<%

var paymentMethodsNameList;
var aPaymentMethodName;
var aPaymentMethod
var action;

if (Request.value('delete_payment_method')) {
   action = 'delete';
} else if (Request.value('add_as_new_payment_method')) {
   action = 'add';
} else if (Request.value('update_existing_payment_method')) {
   action = 'update';
} else if (Request.value('retrieve_payment_method')) {
   action = 'retrieve';
}

pmPaymentMethodName = Request.value('pm_payment_name_select');
pmPreferredMethodName = Session.MRWallet.getPaymentPreference();

var nameList;
if (action == 'delete') {
   Session.MRWallet.removePaymentMethod(pmPaymentMethodName);
   nameList = Session.MRWallet.getPaymentMethodNameList(Session.storeName);
   if (nameList.length()>0) {
      action = 'retrieve';
      pmPaymentMethodName = nameList.get(0);
   } else {
      action = '';
   }
	
}
 
if (action == 'retrieve') {

   pm = Session.MRWallet.getPaymentMethodByName(pmPaymentMethodName);
   pmPaymentName = DecodeGuestPaymentName(pm.PAYMENT_NAME);
   pmPmttypeId = pm.PMTTYPE_ID;
   pmCardNumber = pm.CARD_NUMBER;
   pmFirstName = pm.FIRST_NAME;
   pmMiddleName = pm.MIDDLE_NAME;
   pmLastName = pm.LAST_NAME;
   pmValidDate = formatCreditCardDate(pm.VALID_DATE);
   pmExpiryDate = formatCreditCardDate(pm.EXPIRATION_DATE);
   pmPreferred = (pmPreferredMethodName == pmPaymentMethodName);
} else if ((action =='add') || (action=='update')) {

 
   // applies for both update and new operation
   // get the fields from the form, and validate.
   
   pmPaymentName = Request.value('pm_payment_name');
   pmPmttypeId = Request.value('pm_pmttype_id');
   pmCardNumber = Request.value('pm_card_number');
   pmFirstName = Request.value('pm_first_name');
   pmMiddleName = Request.value('pm_middle_name');
   pmLastName = Request.value('pm_last_name');
   pmValidDate = Request.value('pm_valid_date');
   pmExpiryDate = Request.value('pm_expiry_date');
   pmPreferred = Request.value('pm_preferred');

   //!! need to validate

   // Validate entry
   if (pmPaymentName == '') {
      validMsg += "<br>A <b>Payment Name</b> must be specified.";
   }
   if (pmCardNumber.length != 16) {
      validMsg += "<br>A <b>Card Number</b> must be 16 digits.";
   }
   if (pmFirstName == "") {
      validMsg += "<br>A <b>First Name</b> must be specified.";
   }
   if (pmLastName == "") {
      validMsg += "<br>A <b>Last Name</b> must be specified.";
   }
   if (pmValidDate != pmValidDate.format('strftime:%m/%y')) {
      validMsg += "<br><b>Valid Date</b> must be of the format MM/YY";
   }
   if (pmExpiryDate != pmExpiryDate.format('strftime:%m/%y')) {
      validMsg += "<br><b>Expiry Date</b> must be of the format MM/YY";
   }
	
   
   if (validMsg == "") {
      pm = new BVI_Properties;
   //!!Why??      pm.PAYMENT_LISTNAME= pm_payment_name;
      pm.PAYMENT_NAME    = pmPaymentName;
      pm.STORE_NAME      = Session.storeName;
      pm.PMTTYPE_ID      = parseInt(pmPmttypeId);
      pm.CARD_NUMBER     = pmCardNumber;
      pm.FIRST_NAME      = pmFirstName;
      pm.MIDDLE_NAME     = pmMiddleName;
      pm.LAST_NAME       = pmLastName;
      pm.VALID_DATE      = pmValidDate;
      pm.EXPIRATION_DATE = pmExpiryDate;

      if (action == 'add') {

         Session.MRWallet.insertPaymentMethod(pm);
         if (pmPreferred==1) {
            Session.MRWallet.setPaymentPreference(EncodeGuestPaymentName(pmPaymentName));
         }  
         if (Error.set) {
            Response.write('Add FAILED');
         } 
      } else {

         Session.MRWallet.updatePaymentMethod(pmPaymentName, pm);
         if (pmPreferred==1) {
            Session.MRWallet.setPaymentPreference(EncodeGuestPaymentName(pmPaymentName));
         }  
         if (Error.set) {
            Response.write('Update FAILED');
         }
      }
   }
}   



paymentMethodsNameList = Session.MRWallet.getPaymentMethodNameList(Session.storeName);
if (paymentMethodsNameList.length() > 0) {
%>
<SELECT NAME="pm_payment_name_select">
<%
   for(var i=0; i < paymentMethodsNameList.length(); i++) {
      aPaymentMethodName= paymentMethodsNameList.get(i)
%>

<OPTION NAME="<%=HTMLEncode(aPaymentMethodName)%>" <%=(aPaymentMethodName==pmPaymentName) ? ' SELECTED' : ''%>><%=aPaymentMethodName%><BR>

<%
}
%>
</SELECT>
<input type="submit" name="retrieve_payment_method" value="Retrieve Payment Method">
<%
}
%>
<%=(validMsg=="" ? '':'<FONT COLOR=RED>'+validMsg+'</FONT>')%>
<table width="75%">
  <tr> 
    <td bgcolor="#660000"><b><font color="#FFFFFF" face="Arial, Helvetica, sans-serif">Payment 
      Name</font></b></td>
    <td>
      <input type="text" name="pm_payment_name" value="<%=HTMLEncode(pmPaymentName,0)%>">
    </td>
  </tr>
  <tr> 
    <td bgcolor="#660000"><b><font color="#FFFFFF" face="Arial, Helvetica, sans-serif">Payment 
      Type Id</font></b></td>
    <td>
	<!-- !!Don't like the fact these options are hardcoded! -->
	<INPUT TYPE=RADIO NAME="pm_pmttype_id" <%=(pmPmttypeId==0 || pmPmttypeId==null) ? 'CHECKED':''%> VALUE=0 > Visa
    <INPUT TYPE=RADIO NAME="pm_pmttype_id" <%=pmPmttypeId==1 ? 'CHECKED':''%> VALUE=1 > MasterCard
    <INPUT TYPE=RADIO NAME="pm_pmttype_id" <%=pmPmttypeId==2 ? 'CHECKED':''%> VALUE=2 > Discover
    </td>
  </tr>
  <tr> 
    <td bgcolor="#660000"><b><font color="#FFFFFF" face="Arial, Helvetica, sans-serif">Card 
      Number</font></b></td>
    <td>
      <input type="text" name="pm_card_number" value="<%=HTMLEncode(pmCardNumber,0)%>">
    </td>
  </tr>
  <tr> 
    <td bgcolor="#660000"><b><font color="#FFFFFF" face="Arial, Helvetica, sans-serif">First 
      Name</font></b></td>
    <td>
      <input type="text" name="pm_first_name" value="<%=HTMLEncode(pmFirstName,0)%>">
    </td>
  </tr>
  <tr> 
    <td bgcolor="#660000"><b><font color="#FFFFFF" face="Arial, Helvetica, sans-serif">Middle 
      Name</font></b></td>
    <td>
      <input type="text" name="pm_middle_name" value="<%=HTMLEncode(pmMiddleName,0)%>">
    </td>
  </tr>
  <tr> 
    <td bgcolor="#660000"><b><font color="#FFFFFF" face="Arial, Helvetica, sans-serif">Last 
      Name</font></b></td>
    <td>
      <input type="text" name="pm_last_name" value="<%=HTMLEncode(pmLastName,0)%>">
    </td>
  </tr>
  <tr> 
    <td bgcolor="#660000"><b><font color="#FFFFFF" face="Arial, Helvetica, sans-serif">Valid 
      Date</font></b></td>
    <td>
      <input type="text" name="pm_valid_date" value="<%=HTMLEncode(pmValidDate,0)%>">
    </td>
  </tr>
  <tr> 
    <td bgcolor="#660000"><b><font color="#FFFFFF" face="Arial, Helvetica, sans-serif">Expiration 
      Date</font></b></td>
    <td>
      <input type="text" name="pm_expiry_date" value="<%=HTMLEncode(pmExpiryDate,0)%>">
    </td>
  </tr>
  <tr> 
    <td bgcolor="#660000"><b><font color="#FFFFFF" face="Arial, Helvetica, sans-serif">Make This Your Default? 
      </font></b></td>
    <td>
<!--      <INPUT TYPE=RADIO NAME="pm_preferred" <%=pmPreferred==0 ? 'CHECKED':''%> VALUE=0 > No -->
      <INPUT TYPE=RADIO NAME="pm_preferred" <%=pmPreferred==1 ? 'CHECKED':''%> VALUE=1 > Yes
    </td>
  </tr>
</table>
<input type="submit" name="add_as_new_payment_method" value="Add as new payment method">
<input type="submit" name="update_existing_payment_method" value="Update existing payment method">
<input type="submit" name="delete_payment_method" value="Delete payment method">
</html>
