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
document.getElementById('dateForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting

    // Get the input value
    var dateInput = document.getElementById('dateInput').value;

    // Regular expression to match the YYYY-MM-DD format
    var regex = /^\d{4}-\d{2}-\d{2}$/;

    // Check if the input matches the regex pattern
    if (regex.test(dateInput)) {
        // Create a Date object from the input
        var date = new Date(dateInput);

        // Check if the Date object is valid
        if (!isNaN(date.getTime())) {
            alert('The date is valid: ' + dateInput);
        } else {
            alert('Invalid date format: ' + dateInput);
        }
    } else {
        alert('Invalid date format: ' + dateInput);
    }
});
