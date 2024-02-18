<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="description" content="Discount assigner with sales prediction">
    <meta name="keywords" content="discount, sales, prediction, assigner, sale booster, connexa, CONNEXA, Connexa">
    <meta name="author" content="Rumeth Sandinu">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>ConneXa sale booster</title>

  <!-- favicon -->
  <link rel="shortcut icon" href="../static/assets/images/favicon.svg" type="image/svg+xml">

  <!-- custom css link -->
  <link rel="stylesheet" href="../static/assets/css/main.css">
  <link rel="stylesheet" href="../static/assets/css/home.css">

  <!-- google font link-->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link
    href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700&family=Roboto:wght@400;500;700&display=swap"
    rel="stylesheet">

  <title>Sale booster</title>

</head>
<body>
    <h1>Sale Booster Console</h1>
    <br/>
    <h2>
        Items
    </h2>
    <br/>


    <ul class="top-product-list grid-list">

        <li class="top-product-item">
          <div class="product-card top-product-card">

            <figure class="card-banner">
              <img src="../static/assets/images/top-product-1.png" width="100" height="100" loading="lazy"
                   alt="Fresh Orangey">

              <div class="btn-wrapper">
                <button class="product-btn" aria-label="Add to Whishlist">
                  <ion-icon name="heart-outline"></ion-icon>

                  <div class="tooltip">Add to Whishlist</div>
                </button>

                <button class="product-btn" aria-label="Quick View">
                  <ion-icon name="eye-outline"></ion-icon>

                  <div class="tooltip">Quick View</div>
                </button>
              </div>
            </figure>

            <div class="card-content">

              <div class="rating-wrapper">
                <ion-icon name="star"></ion-icon>
                <ion-icon name="star"></ion-icon>
                <ion-icon name="star"></ion-icon>
                <ion-icon name="star"></ion-icon>
                <ion-icon name="star"></ion-icon>
              </div>

              <h3 class="h4 card-title">
                <a href="product-details.html">Fresh Orangey</a>
              </h3>

              <div class="price-wrapper">
                <del class="del">$75.00</del>

                <data class="price" value="85.00">$85.00</data>
              </div>

              <button class="btn btn-primary">Add to Cart</button>

            </div>

          </div>
        </li>
    </ul>
</body>
</html>