
<%
// Basic session related setup.
initSessionState();

var storeName = "OfficeExpress";
var defaultErrorPage = "/oexpress/scripts/error.jsp";
var loginPage = "/oexpress.html";
var mainFrameSet = "/oexpress/scripts/frameset/main_frame.jsp";

var server_url = Request.SERVER_URL;
if (isEmptyString(server_url)) 
    server_url = "http://" + Request.HTTP_HOST;

var okay = true;
var errorPage = Request.value('errorPage');
if (errorPage == null || errorPage == '') 
    errorPage = defaultErrorPage;
var nextPage = Request.value('nextPage');

// Process login inputs...
 
var username = Request.value('username');
var password = Request.value('password');

var action = Request.value('action');
if (action != null  && !isEmptyString(action))
   Session.MRaction = action;
//
// Authenticate the visitor.
//
if (isEmptyString(username)) {
    okay = false;
    Session.errorMessage = "You must specify both a username and password";
} else if (isEmptyString(password)) {
    okay = false;
    Session.errorMessage = "You must specify both a username and password";
} else {
    visitor = Session.visitorManager.visitor(username);

    if (Error.set || visitor == null) {
	okay = false;
	Session.errorMessage = "Invalid username or password";
    } else if ( visitor.isPasswordValid(password) == 0 ) {
	okay = false;
	Session.errorMessage = "Invalid username or password";
    }
}

if (okay) {

    // Visitor has been authenticated, set up the visitor info
    // for this session.

    // If there are something in the shopping cart, save them. The
    // entire sales rep component will be reset later, thus loosing
    // the cart items. 

    var savedItemList = null;
    var needToRestoreCart = false;
    if (Session.MRSalesRep != null) {
	savedItemList = Session.MRSalesRep.getItemList();
	if (!Error.set && savedItemList.length > 0) {
	    needToRestoreCart = true;
	}
    }

    setCurrentVisitor(visitor);
    Session.userType = "member";

    // Maintain login statistics.
    loginData();

    // Set up the store information for this session.
	
    Session.storeName = storeName;
    setCurrentService(storeName);
    Session.storeID = Session.serviceID;

    // Initialize the Commerce WebApp components.  

    okay = initMRComponents();

    if (okay) {
	// Restore shopping cart items if necessary.
	if (needToRestoreCart) {
	    Session.MRSalesRep.addItemList(savedItemList);
	}
    }
}

if (okay == false) {
    // Login error.  
    if (errorPage == defaultErrorPage) {
	Session.errorMessage += '<P> Please retry the <A HREF="'+server_url+loginPage+'"> Login Page </A> again.';
    } else {
	Request.add_attribute("error", Session.errorMessage);
    }

    visitScript(errorPage);
}

obslogEnterStore(Session.ObservationManager, Session.sessionKey(),
                 Session.visitorID, Session.serviceID,
                 "Entered OfficeExpress");

//
// Done with the login and initialization. Display the next page.
//

// If the nextPage parameter is supplied by the requester, visit
// that page.  
if (nextPage != null)  {
    visitScript(nextPage);

}

// Otherwise, the default home page is presented.
Response.redirect(server_url+makeScriptURL(mainFrameSet));
%>


