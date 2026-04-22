<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Точка Доступних Цін</title>
    <style>
        /* Umumiy sozlamalar */
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f2f5;
        }

        /* Ukraina uslubidagi Banner */
        .hero-section {
            background: linear-gradient(135deg, #0057b7 50%, #ffd700 50%);
            color: white;
            padding: 80px 20px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        .hero-section h1 {
            margin: 0;
            font-size: 45px;
            text-shadow: 2px 2px 5px rgba(0,0,0,0.5);
        }

        .hero-section p {
            font-size: 20px;
            margin-top: 15px;
            font-weight: bold;
            color: #fff;
            background: rgba(0,0,0,0.2);
            display: inline-block;
            padding: 10px 20px;
            border-radius: 50px;
        }

        /* Katalog */
        .shop-container {
            max-width: 1100px;
            margin: 50px auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 25px;
            padding: 0 20px;
        }

        /* Katalog kartalari */
        .category-card {
            background: white;
            border-radius: 15px;
            padding: 30px 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: transform 0.3s ease;
            border-bottom: 5px solid #0057b7;
        }

        .category-card:hover {
            transform: translateY(-10px);
        }

        .icon {
            font-size: 50px;
            margin-bottom: 20px;
            display: block;
        }

        .category-card h2 {
            font-size: 24px;
            color: #333;
            margin: 10px 0;
        }

        .category-card p {
            color: #ff4757;
            font-weight: bold;
            font-size: 14px;
            text-transform: uppercase;
        }

        /* Pastki qism */
        footer {
            text-align: center;
            padding: 40px;
            background: #333;
            color: #ccc;
            margin-top: 50px;
        }
    </style>
</head>
<body>

    <div class="hero-section">
        <h1>Точка Доступних Цін</h1>
        <p>Ласкаво просимо! Найкраща якість за доступною ціною.</p>
    </div>

    <div class="shop-container">
        
        <div class="category-card">
            <span class="icon">👟</span>
            <h2>Взуття</h2>
            <p>Фото з'являться незабаром</p>
        </div>

        <div class="category-card">
            <span class="icon">👕</span>
            <h2>Одяг</h2>
            <p>Фото з'являться незабаром</p>
        </div>

        <div class="category-card">
            <span class="icon">👙</span>
            <h2>Білизна</h2>
            <p>Фото з'являться незабаром</p>
        </div>

        <div class="category-card">
            <span class="icon">👜</span>
            <h2>Сумки</h2>
            <p>Фото з'являться незабаром</p>
        </div>

    </div>

    <footer>
        <p>&copy; 2026 Точка Доступних Цін. Всі права захищені.</p>
        <p style="color: #ffd700;">Скоро відкриття асортименту!</p>
    </footer>

</body>
</html>
