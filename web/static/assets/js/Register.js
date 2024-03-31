var staffPassword = "staff";
var adminPassword = "admin";

function showForm() {
    var userType = document.getElementById("userType").value; // Get selected user type
    console.log("Selected User Type:", userType);
    var emailInput = document.getElementById("email");

    // Hide all forms
    var forms = document.querySelectorAll(".Register-container");
    forms.forEach(function(form) {
        form.style.display = "none";
    });

    // Show the selected form based on user type
    if (userType === "customer") {
        document.getElementById("customerForm").style.display = "block";
        emailInput.removeAttribute("pattern"); // Remove pattern for customer
    } else if (userType === "staff" || userType === "admin") {
        var password = prompt("Enter password:");
        var correctPassword = userType === "staff" ? staffPassword : adminPassword;

        if (password === correctPassword) {
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
