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

  async function registerUser() {
    // Retrieve user input
    var fullName = document.getElementById("fullName").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirmPassword").value;

    // Validate password and confirm password match
    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    // Hash the password using bcrypt
    var saltRounds = 10;
    var hashedPassword = await bcrypt.hash(password, saltRounds);

    // Send the registration data to your server for further processing
    // For demonstration purposes, this code assumes a server endpoint "/register" that handles user registration
    // Replace this with the actual URL of your server endpoint
    var url = "/register";
    var data = {
      fullName: fullName,
      email: email,
      password: hashedPassword,
    };

    // Make a POST request to your server
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then(responseData => {
        // Handle the server response as needed
        console.log(responseData);
      })
      .catch(error => {
        console.error("There was a problem with the fetch operation:", error);
      });
  }