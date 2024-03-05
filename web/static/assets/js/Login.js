var staffEmailDomain = "@connexa.com";
var adminEmailDomain = "@connexa.com";

function login() {
  var email = document.getElementById("username").value;
  var password = document.getElementById("password").value;

  // Check if the email is valid based on the user type
  if (validateEmail(email)) {
    var userType = getUserType(email);

    // Simulate a server-side authentication check
    // In a real-world scenario, this check should be done on the server
    authenticateUser(userType, password);
  } else {
    alert("Invalid email format");
  }
}

function validateEmail(email) {
  // Regular expression to validate email with domain "@connexa.com"
  var regex = /^[a-zA-Z0-9._-]+@connexa\.com$/;
  return regex.test(email);
}

function getUserType(email) {
  // Extract the domain from the email address
  var domain = email.substring(email.lastIndexOf("@") + 1);

  // Determine the user type based on the domain
  if (domain === staffEmailDomain) {
    return "staff";
  } else if (domain === adminEmailDomain) {
    return "admin";
  } else {
    return "customer"; // Assuming other domains are customers
  }
}

function authenticateUser(userType, password) {
  // Simulate a server-side authentication check
  // In a real-world scenario, this check should be done on the server
  if (userType === "staff" && password === "staffPasswordHash") {
    alert("Login successful as Staff");
    // Redirect to staff dashboard or perform additional actions for staff login
  } else if (userType === "admin" && password === "adminPasswordHash") {
    alert("Login successful as Admin");
    // Redirect to admin dashboard or perform additional actions for admin login
  } else {
    alert("Incorrect email or password");
  }
}

function togglePasswordVisibility() {
  var passwordInput = document.getElementById("password");
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
  } else {
    passwordInput.type = "password";
  }
}