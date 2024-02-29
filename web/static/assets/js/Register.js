var staffPassword = "staff";
var adminPassword = "admin";

function togglePasswordVisibility() {
  var passwordInput = document.getElementById("password");
  var confirmPasswordInput = document.getElementById("confirmPassword");

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    confirmPasswordInput.type = "text";
  } else {
    passwordInput.type = "password";
    confirmPasswordInput.type = "password";
  }
}

function validateEmail(email) {
  // Regular expression to validate email with domain "@connexa.com"
  var regex = /^[a-zA-Z0-9._-]+@connexa\.com$/;
  return regex.test(email);
}

function showForm() {
  var userType = document.getElementById("userType").value;
  var emailInput = document.getElementById("email");

  // Hide all forms
  var forms = document.querySelectorAll(".Register-container");
  forms.forEach(function (form) {
    form.style.display = "none";
  });

  // Show the selected form based on user type
  if (userType === "customer") {
    document.getElementById("customerForm").style.display = "block";
    emailInput.removeAttribute("pattern"); // Remove pattern for customer
  } else if (userType === "staff" || userType === "admin") {
    var password = prompt("Enter password:");

    // Check password for Staff and Admin forms
    if (
      (userType === "staff" && password === staffPassword) ||
      (userType === "admin" && password === adminPassword)
    ) {
      // Show the selected form
      document.getElementById(userType + "Form").style.display = "block";
      emailInput.setAttribute("pattern", "[a-zA-Z0-9._-]+@connexa.com"); // Set pattern for staff and admin
    } else {
      alert("Incorrect password for Staff or Admin");
    }
  } else {
    // Display a message or take appropriate action for other user types
    alert("Invalid user type selected");
  }
}
