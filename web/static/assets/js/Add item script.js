var selectedRow = null

function onFormSubmit(e) {
	event.preventDefault();
        var formData = readFormData();
        if (selectedRow == null){
            insertNewRecord(formData);
		}
        else{
            updateRecord(formData);
		}
        resetForm();    
}

//Retrieve the data
function readFormData() {
    var formData = {};
    formData["productCode"] = document.getElementById("productCode").value;
    formData["product"] = document.getElementById("product").value;
    formData["qty"] = document.getElementById("qty").value;
    formData["perPrice"] = document.getElementById("perPrice").value;
    formData["category"] = document.getElementById("category").value;
    formData["description"] = document.getElementById("description").value;
    formData["discountrate"] = document.getElementById("discountrate").value;
    formData["productImage"] = document.getElementById("productImage").value;
    return formData;
}

//Insert the data
function insertNewRecord(data) {
    var table = document.getElementById("storeList").getElementsByTagName('tbody')[0];
     // Check if the product code already exists
     var productCodeExists = Array.from(table.rows).some(row => row.cells[0].innerHTML === data.productCode);
    
     if (productCodeExists) {
         alert("Product code already exists!");
         return;
     }

    var newRow = table.insertRow(table.length);
    cell1 = newRow.insertCell(0);
		cell1.innerHTML = data.productCode;
    cell2 = newRow.insertCell(1);
		cell2.innerHTML = data.product;
    cell3 = newRow.insertCell(2);
		cell3.innerHTML = data.qty;
    cell4 = newRow.insertCell(3);
		cell4.innerHTML = data.perPrice;
    cell5 = newRow.insertCell(4);
        cell5.innerHTML = data.category;
    cell6 = newRow.insertCell(5);
        cell6.innerHTML = data.description;
    cell7 = newRow.insertCell(6);
        cell7.innerHTML = data.discountrate;
    cell8 = newRow.insertCell(7);
        cell8.innerHTML = `<img src="${document.getElementById('previewImage').src}" alt="Product Image" style="max-width: 50px; max-height: 50px;">`;
    cell9 = newRow.insertCell(8);
        cell9.innerHTML = `<button onClick="onEdit(this)">Edit</button> <button onClick="onDelete(this)">Delete</button>`;
}

//Edit the data
function onEdit(td) {
    selectedRow = td.parentElement.parentElement;
    document.getElementById("productCode").value = selectedRow.cells[0].innerHTML;
    document.getElementById("product").value = selectedRow.cells[1].innerHTML;
    document.getElementById("qty").value = selectedRow.cells[2].innerHTML;
    document.getElementById("perPrice").value = selectedRow.cells[3].innerHTML;
    document.getElementById("category").value = selectedRow.cells[4].innerHTML;
    document.getElementById("description").value = selectedRow.cells[5].innerHTML;
    document.getElementById("discountrate").value = selectedRow.cells[6].innerHTML;
    document.getElementById("productImage").value = selectedRow.cells[7].innerHTML;
}
function updateRecord(formData) {
    selectedRow.cells[0].innerHTML = formData.productCode;
    selectedRow.cells[1].innerHTML = formData.product;
    selectedRow.cells[2].innerHTML = formData.qty;
    selectedRow.cells[3].innerHTML = formData.perPrice;
    selectedRow.cells[4].innerHTML = formData.category;
    selectedRow.cells[5].innerHTML = formData.description;
    selectedRow.cells[6].innerHTML = formData.discountrate;
    selectedRow.cells[7].innerHTML = formData.productImage;
}

//Delete the data
function onDelete(td) {
    if (confirm('Do you want to delete this record?')) {
        row = td.parentElement.parentElement;
        document.getElementById('storeList').deleteRow(row.rowIndex);
        resetForm();
    }
}

//Reset the data
function resetForm() {
    document.getElementById("productCode").value = '';
    document.getElementById("product").value = '';
    document.getElementById("qty").value = '';
    document.getElementById("perPrice").value = '';
    document.getElementById("category").value = '';
    document.getElementById("description").value = '';
    document.getElementById("discountrate").value = '';
    document.getElementById("productImage").value = '';
    selectedRow = null;
}

// Function to display the preview of the uploaded image
function previewImage() {
    var reader = new FileReader();
    reader.onload = function(e) {
        var imgElement = document.getElementById('previewImage');
        imgElement.src = e.target.result;
        imgElement.style.display = 'block'; // Show the image
    }
    var fileInput = document.getElementById('productImage');
    reader.readAsDataURL(fileInput.files[0]);
}

// Call the previewImage function when a file is selected
document.getElementById('productImage').addEventListener('change', previewImage);

