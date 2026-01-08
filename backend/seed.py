from database import SessionLocal
from models import Category, Product, ProductImage, User, Order, OrderItem, WishlistItem

def seed_db():
    db = SessionLocal()
    
    try:
        # Check if data exists
        if db.query(Category).first():
            print("Database already contains data. Clearing and reseeding...")
            # Clear existing data in correct order (respecting foreign keys)
            db.query(WishlistItem).delete()
            db.query(OrderItem).delete()
            db.query(Order).delete()
            db.query(ProductImage).delete()
            db.query(Product).delete()
            db.query(Category).delete()
            db.commit()

        print("Seeding database...")

        # Create default user if not exists
        default_user = db.query(User).filter(User.id == "00000000-0000-0000-0000-000000000001").first()
        if not default_user:
            default_user = User(
                id="00000000-0000-0000-0000-000000000001",
                email="test@example.com",
                full_name="Test User"
            )
            db.add(default_user)
            db.flush()

        # Categories
        categories_data = [
            {
                "name": "Mobiles",
                "slug": "mobiles",
                "image_url": "https://rukminim1.flixcart.com/flap/128/128/image/22fddf3c7da4c4f4.png?q=100",
                "parent_slug": None
            },
            {
                "name": "TV & Appliances",
                "slug": "tv-appliances",
                "image_url": "https://rukminim1.flixcart.com/flap/128/128/image/0ff199d1bd27eb98.png?q=100",
                "parent_slug": None
            },
            {
                "name": "Men's Fashion",
                "slug": "mens-fashion",
                "image_url": "https://rukminim1.flixcart.com/flap/128/128/image/82b3ca5fb2301045.png?q=100",
                "parent_slug": None
            },
            {
                "name": "Women's Fashion",
                "slug": "womens-fashion",
                "image_url": "https://rukminim1.flixcart.com/flap/128/128/image/82b3ca5fb2301045.png?q=100",
                "parent_slug": None
            },
            {
                "name": "Furniture",
                "slug": "furniture",
                "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600&auto=format&fit=crop&q=60",
                "parent_slug": None
            },
            # Subcategories
            {
                "name": "Clothing",
                "slug": "mens-clothing",
                "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&auto=format&fit=crop&q=60",
                "parent_slug": "mens-fashion"
            },
            {
                "name": "Footwear",
                "slug": "mens-footwear",
                "image_url": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600&auto=format&fit=crop&q=60",
                "parent_slug": "mens-fashion"
            },
            {
                "name": "Clothing",
                "slug": "womens-clothing",
                "image_url": "https://rukminim2.flixcart.com/image/832/832/xif0q/shirt/z/h/b/s-hswshs23010-bl-high-star-original-imah3j77ctfjbndc.jpeg?q=70",
                "parent_slug": "womens-fashion"
            },
            {
                "name": "Footwear",
                "slug": "womens-footwear",
                "image_url": "https://m.media-amazon.com/images/I/41tZ9T1R6lL._SY625_.jpg",
                "parent_slug": "womens-fashion"
            },
            # TV & Appliances Subcategories
            {
                "name": "Air Conditioners",
                "slug": "air-conditioners",
                "image_url": "https://images.unsplash.com/photo-1614631446506-6927d627038e?w=600&auto=format&fit=crop&q=60",
                "parent_slug": "tv-appliances"
            },
            {
                "name": "Washing Machines",
                "slug": "washing-machines",
                "image_url": "https://images.unsplash.com/photo-1626806819282-2c1dc01a5e0c?w=600&auto=format&fit=crop&q=60",
                "parent_slug": "tv-appliances"
            },
            {
                "name": "Refrigerators",
                "slug": "refrigerators",
                "image_url": "https://images.unsplash.com/photo-1571175443880-49e1d58b794a?w=600&auto=format&fit=crop&q=60",
                "parent_slug": "tv-appliances"
            },
            {
                "name": "Televisions",
                "slug": "televisions",
                "image_url": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=600&auto=format&fit=crop&q=60",
                "parent_slug": "tv-appliances"
            },
        ]

        categories = {}
        # First pass: Create parent categories
        for cat_data in categories_data:
            if cat_data["parent_slug"] is None:
                cat = Category(
                    name=cat_data["name"], 
                    slug=cat_data["slug"], 
                    image_url=cat_data["image_url"]
                )
                db.add(cat)
                db.flush()
                categories[cat_data["slug"]] = cat.id

        # Second pass: Create subcategories
        for cat_data in categories_data:
            if cat_data["parent_slug"]:
                parent_id = categories.get(cat_data["parent_slug"])
                cat = Category(
                    name=cat_data["name"], 
                    slug=cat_data["slug"], 
                    image_url=cat_data["image_url"],
                    parent_id=parent_id
                )
                db.add(cat)
                db.flush()
                categories[cat_data["slug"]] = cat.id


        # Products Data
        products_data = [
            # MOBILES
            {
                "category": "mobiles",
                "name": "Apple iPhone 15 Pro Max (256GB)",
                "slug": "iphone-15-pro-max-256gb",
                "description": "Titanium design, A17 Pro chip. The most powerful iPhone ever.",
                "price": 134900,
                "original_price": 159900,
                "discount_percentage": 16,
                "stock_quantity": 45,
                "brand": "Apple",
                "rating": 4.7,
                "review_count": 8542,
                "images": [
                    "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600&auto=format&fit=crop&q=60",
                ]
            },
            {
                "category": "mobiles",
                "name": "Samsung Galaxy S24 Ultra",
                "slug": "samsung-galaxy-s24-ultra",
                "description": "Galaxy AI is here. Welcome to the era of mobile AI.",
                "price": 119999,
                "original_price": 129999,
                "discount_percentage": 8,
                "stock_quantity": 52,
                "brand": "Samsung",
                "rating": 4.6,
                "review_count": 6234,
                "images": [
                    "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=600&auto=format&fit=crop&q=60"
                ]
            },
            {
                "category": "mobiles",
                "name": "Apple iPhone 17 Pro Max (256GB)",
                "slug": "iphone-17-pro-max-256gb",
                "description": "The future of iPhone. Featuring a revolutionary new design and the A19 Pro chip.",
                "price": 159900,
                "original_price": 169900,
                "discount_percentage": 5,
                "stock_quantity": 100,
                "brand": "Apple",
                "rating": 5.0,
                "review_count": 120,
                "images": [
                    "https://www.mobileana.com/wp-content/uploads/2025/06/Apple-iPhone-17-Pro-Max-Cosmic-Orange.webp",
                    "https://m-cdn.phonearena.com/images/hub/550-wide-two_1200/iPhone-17-Pro-Max-release-date-price-and-features.webp",
                    "https://applepremiumstore.com.ng/wp-content/uploads/2025/07/G0bLx54WEAA6dVj.jpg-large.jpeg"
                ]
            },
            {
                "category": "mobiles",
                "name": "Apple iPhone 16 Pro (Desert Titanium)",
                "slug": "iphone-16-pro-desert-titanium",
                "description": "The ultimate iPhone. Featuring a stunning titanium design, A18 Pro chip, and the best camera system ever in an iPhone.",
                "price": 119900,
                "original_price": 129900,
                "discount_percentage": 8,
                "stock_quantity": 75,
                "brand": "Apple",
                "rating": 4.9,
                "review_count": 2540,
                "images": [
                    "https://idestiny.in/wp-content/uploads/2024/10/iPhone_16_Pro_Desert_Titanium_PDP_Image_Position_1__en-IN-600x600.jpg",
                    "https://www.designinfo.in/wp-content/uploads/2024/09/Apple-iPhone-16-Pro-128GB-Desert-Titanium-2-485x485-optimized.webp",
                    "https://www.designinfo.in/wp-content/uploads/2024/09/Apple-iPhone-16-Pro-128GB-Desert-Titanium-4-485x485-optimized.webp",
                    "https://www.apple.com/newsroom/images/2024/09/apple-debuts-iphone-16-pro-and-iphone-16-pro-max/article/Apple-iPhone-16-Pro-camera-system-240909_inline.jpg.large.jpg"
                ]
            },
            {
                "category": "mobiles",
                "name": "Apple iPhone 15 Pro (Natural Titanium)",
                "slug": "iphone-15-pro-natural-titanium",
                "description": "iPhone 15 Pro. Forged in titanium. Featuring the groundbreaking A17 Pro chip, a customizable Action button, and the most powerful iPhone camera system ever.",
                "price": 129900,
                "original_price": 134900,
                "discount_percentage": 4,
                "stock_quantity": 40,
                "brand": "Apple",
                "rating": 4.8,
                "review_count": 8945,
                "images": [
                    "https://www.apple.com/newsroom/images/2023/09/apple-unveils-iphone-15-pro-and-iphone-15-pro-max/article/Apple-iPhone-15-Pro-lineup-hero-230912_Full-Bleed-Image.jpg.large.jpg",
                    "https://www.apple.com/newsroom/images/2023/09/apple-unveils-iphone-15-pro-and-iphone-15-pro-max/article/Apple-iPhone-15-Pro-lineup-color-lineup-geo-230912_big.jpg.large.jpg",
                    "https://www.apple.com/newsroom/images/2023/09/apple-unveils-iphone-15-pro-and-iphone-15-pro-max/article/Apple-iPhone-15-Pro-lineup-camera-system-230912_big.jpg.large.jpg",
                    "https://www.apple.com/newsroom/images/2023/09/apple-unveils-iphone-15-pro-and-iphone-15-pro-max/article/Apple-iPhone-15-Pro-lineup-USB-C-connector-cable-230912_big.jpg.large.jpg"
                ]
            },
            {
                "category": "mobiles",
                "name": "Samsung Galaxy S25 Ultra (Titanium Silver/Blue)",
                "slug": "samsung-galaxy-s25-ultra-titanium",
                "description": "Galaxy AI is here. The new Galaxy S25 Ultra features a titanium frame, the latest Snapdragon 8 Gen 4, and an unparalleled camera experience.",
                "price": 129999,
                "original_price": 144999,
                "discount_percentage": 10,
                "stock_quantity": 60,
                "brand": "Samsung",
                "rating": 4.9,
                "review_count": 1500,
                "images": [
                    "https://rukminim2.flixcart.com/image/832/832/xif0q/mobile/i/s/g/-original-imahgfmzraymrnrg.jpeg?q=70&crop=false",
                    "https://rukminim2.flixcart.com/image/832/832/xif0q/mobile/f/j/t/-original-imahggetqzszzxqh.jpeg?q=70&crop=false"
                ]
            },
            {
                "category": "mobiles",
                "name": "Google Pixel 10 Pro (Obsidian)",
                "slug": "google-pixel-10-pro-obsidian",
                "description": "Introducing the Pixel 10 Pro. The most advanced Pixel yet, powered by the Google Tensor G5 and Google AI.",
                "price": 109999,
                "original_price": 119999,
                "discount_percentage": 8,
                "stock_quantity": 45,
                "brand": "Google",
                "rating": 4.7,
                "review_count": 850,
                "images": [
                    "https://lh3.googleusercontent.com/OccemUtB0u2IVT5jfAX_Hh6us7y7M3xHJZL0DiIhy632EiU0ZYIEESyJGZ9DtDiqmde5JJn50rziiwZsnrkQSy2knekI7DIXi8I",
                    "https://lh3.googleusercontent.com/rfBtmYnjlisXRpVe1WsdU66fX9NKN-ky5Vyr7C4eX6DRRR1dcy4Q-MCXfqg_3242aToJdKP1_HtF8nNzYUft8UIqjp01xj5mwQ",
                    "https://lh3.googleusercontent.com/4SO0Lj2DVbCAOcUQqAe8KyTw7JkQjPTlubgUIvSbqoGLQ-nfk8hh4EqCbyI5q705aPD78ufcr6eamo6dg5TvLb9IDFqZJsgyPBVd",
                    "https://lh3.googleusercontent.com/juTRBndkTNAEqn4bhzQoG2wp9ojL9gRWNxHdDQCEUoECwsSKdupIrAjEbQ4FAVHiI_rn3Kmq3D0gFGD2rMOySbpOnivxwKHy0w"
                ]
            },
            {
                "category": "mobiles",
                "name": "Google Pixel 10 (Frost)",
                "slug": "google-pixel-10-frost",
                "description": "Meet the Pixel 10. Helpful, powerful, and full of AI features you'll love.",
                "price": 79999,
                "original_price": 89999,
                "discount_percentage": 11,
                "stock_quantity": 55,
                "brand": "Google",
                "rating": 4.6,
                "review_count": 1200,
                "images": [
                    "https://rukminim2.flixcart.com/image/832/832/xif0q/mobile/p/e/2/-original-imahfjsfgu7vjkvw.jpeg?q=70&crop=false",
                    "https://rukminim2.flixcart.com/image/832/832/xif0q/mobile/w/g/3/-original-imahfjsfvkkhav7z.jpeg?q=70&crop=false"
                ]
            },
            {
                "category": "mobiles",
                "name": "Google Pixel 8 Pro",
                "slug": "google-pixel-8-pro",
                "description": "The AI phone from Google.",
                "price": 84999,
                "original_price": 106999,
                "discount_percentage": 21,
                "stock_quantity": 28,
                "brand": "Google",
                "rating": 4.4,
                "review_count": 3124,
                "images": [
                    "https://images.unsplash.com/photo-1598327105666-5b89351aff70?w=600&auto=format&fit=crop&q=60" 
                ]
            },
             # MEN'S CLOTHING
            {
                "category": "mens-clothing",
                "name": "Cotstyle Round Neck Red T-Shirt",
                "slug": "cotstyle-round-neck-red-tshirt",
                "description": "Cotstyle Cotton Fabrics Round Neck Short Length Plain Half Sleeve Casual Daily Wear Men's T-Shirts. Premium cotton comfort.",
                "price": 499,
                "original_price": 999,
                "discount_percentage": 50,
                "stock_quantity": 100,
                "brand": "Cotstyle",
                "rating": 4.5,
                "review_count": 250,
                "images": [
                    "https://www.cotstyle.com/cdn/shop/files/RN01_385554_S_Red_1200x.jpg?v=1685429291",
                    "https://www.cotstyle.com/cdn/shop/files/RN01_385554_S_Red_1.jpg?v=1685429311",
                    "https://www.cotstyle.com/cdn/shop/files/RN01_385554_S_Red_3.jpg?v=1685429313"
                ]
            },
            {
                "category": "mens-clothing",
                "name": "Van-stylo Oversized Graphic T-Shirt (Black)",
                "slug": "van-stylo-oversized-graphic-black-tshirt",
                "description": "Van-stylo Full Sleeve Oversized Tshirt for Men. Round Neck Longline Drop Shoulder Graphic Printed T-Shirt. Trendy and comfortable.",
                "price": 275,
                "original_price": 999,
                "discount_percentage": 72,
                "stock_quantity": 80,
                "brand": "Van-stylo",
                "rating": 4.2,
                "review_count": 120,
                "images": [
                    "https://www.jiomart.com/images/product/original/rvq1gnebgp/van-stylo-full-sleeve-oversized-tshirt-for-men-round-neck-longline-drop-shoulder-graphic-printed-t-shirt-black-color-product-images-rvq1gnebgp-0-202310251053.jpg",
                    "https://www.jiomart.com/images/product/original/rvq1gnebgp/van-stylo-full-sleeve-oversized-tshirt-for-men-round-neck-longline-drop-shoulder-graphic-printed-t-shirt-black-color-product-images-rvq1gnebgp-1-202310251053.jpg",
                    "https://www.jiomart.com/images/product/original/rvq1gnebgp/van-stylo-full-sleeve-oversized-tshirt-for-men-round-neck-longline-drop-shoulder-graphic-printed-t-shirt-black-color-product-images-rvq1gnebgp-2-202310251053.jpg"
                ]
            },
            {
                "category": "mens-clothing",
                "name": "H&M Loose Fit Printed Hoodie",
                "slug": "hm-loose-fit-printed-hoodie",
                "description": "Hoodie in midweight sweatshirt fabric with a soft brushed inside. Dropped shoulders, kangaroo pocket, and ribbing at the cuffs and hem.",
                "price": 2099,
                "original_price": 2699,
                "discount_percentage": 22,
                "stock_quantity": 40,
                "brand": "H&M",
                "rating": 4.6,
                "review_count": 340,
                "images": [
                    "https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/2025/SEPTEMBER/9/derh0o4m_c2ce69ee316b41dfbd9ee2185f101d41.jpg",
                    "https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/2025/SEPTEMBER/9/y9o9Pq79_bbcf0db403ba4a0baf2d6d2974006572.jpg",
                    "https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/2025/SEPTEMBER/9/ixqyY0cP_d38ea9e22f88420987b193a9a8181c11.jpg"
                ]
            },
            {
                "category": "mens-clothing",
                "name": "H&M Regular Fit Hoodie (Brown)",
                "slug": "hm-regular-fit-brown-hoodie",
                "description": "Long-sleeved hoodie in midweight sweatshirt fabric with a soft brushed inside. Kangaroo pocket and double-layered drawstring hood.",
                "price": 2099,
                "original_price": 2699,
                "discount_percentage": 22,
                "stock_quantity": 35,
                "brand": "H&M",
                "rating": 4.7,
                "review_count": 410,
                "images": [
                    "https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/2025/AUGUST/5/0uXIrr3B_124c7aeb454c4d9aaf754fa452b47164.jpg",
                    "https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/2025/AUGUST/5/ZRlXLcQE_30093ed9e8464956854d381164049509.jpg",
                    "https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/2025/AUGUST/5/he1y4o0r_b4c1ee2a278644e18bf40a471bb1dde9.jpg"
                ]
            },
            {
                "category": "mens-clothing",
                "name": "Linaria Loose Fit Men Black Jeans",
                "slug": "linaria-loose-fit-black-jeans",
                "description": "Men Loose Fit Mid Rise Black Jeans. Comfortable baggy fit suitable for casual occasions.",
                "price": 413,
                "original_price": 1999,
                "discount_percentage": 79,
                "stock_quantity": 60,
                "brand": "Linaria",
                "rating": 4.3,
                "review_count": 980,
                "images": [
                    "https://rukminim2.flixcart.com/image/832/832/xif0q/jean/o/t/i/30-11-baggy-bk-41-jeanberry-original-imahfrtuxpcyfaq8.jpeg?q=90&crop=false",
                    "https://rukminim2.flixcart.com/image/832/832/xif0q/jean/y/x/0/30-11-baggy-bk-41-jeanberry-original-imahfrtujqwvf5ez.jpeg?q=90&crop=false",
                    "https://rukminim2.flixcart.com/image/832/832/xif0q/jean/n/w/7/30-11-baggy-bk-41-jeanberry-original-imahfrtukaufw5pq.jpeg?q=90&crop=false"
                ]
            },
            {
                "category": "mens-clothing",
                "name": "Straight Leg Dark Blue Jeans",
                "slug": "straight-leg-dark-blue-jeans",
                "description": "Straight Leg Dark Blue Jeans, Casual Wide Leg Denim. High quality denim suitable for parties and casual wear.",
                "price": 999,
                "original_price": 1499,
                "discount_percentage": 33,
                "stock_quantity": 45,
                "brand": "Generic",
                "rating": 4.4,
                "review_count": 150,
                "images": [
                    "https://m.media-amazon.com/images/I/413ajpbCYEL.jpg",
                    "https://m.media-amazon.com/images/I/41bBPMdg7fL.jpg",
                    "https://m.media-amazon.com/images/I/411epmlGvXL.jpg"
                ]
            },

            # WOMEN'S CLOTHING
            {
                "category": "womens-clothing",
                "name": "High Star Women Oversized Fit Striped Shirt",
                "slug": "high-star-women-striped-shirt",
                "description": "A stylish oversized fit striped casual shirt for women featuring a spread collar, perfect for a modern casual look.",
                "price": 1405,
                "original_price": 2999,
                "discount_percentage": 53,
                "stock_quantity": 40,
                "brand": "High Star",
                "rating": 4.3,
                "review_count": 120,
                "images": [
                    "https://rukminim2.flixcart.com/image/832/832/xif0q/shirt/z/h/b/s-hswshs23010-bl-high-star-original-imah3j77ctfjbndc.jpeg?q=70"
                ]
            },
            {
                "category": "womens-clothing",
                "name": "KOTTY Regular Women Dark Blue Jeans",
                "slug": "kotty-women-dark-blue-jeans",
                "description": "High-rise dark blue jeans with a regular fit for women, offering both style and comfort for everyday wear.",
                "price": 493,
                "original_price": 1999,
                "discount_percentage": 75,
                "stock_quantity": 60,
                "brand": "KOTTY",
                "rating": 4.1,
                "review_count": 350,
                "images": [
                    "https://rukminim2.flixcart.com/image/832/832/xif0q/jean/h/o/2/-original-imahfgakqgvmqmma.jpeg?q=70"
                ]
            },
            {
                "category": "womens-clothing",
                "name": "Sassafras Beige Rib Polo Neck Top",
                "slug": "sassafras-beige-rib-polo-top",
                "description": "Women Beige Rib Polo Neck Top. A chic and comfortable addition to your wardrobe.",
                "price": 524,
                "original_price": 1299,
                "discount_percentage": 60,
                "stock_quantity": 45,
                "brand": "Sassafras",
                "rating": 4.4,
                "review_count": 89,
                "images": [
                    "https://sassafras.in/cdn/shop/files/SFTOPS42068-1_287bfb1e-3ac9-435c-a2b7-6f370f0ea778_1800x.jpg?v=1757493262",
                    "https://sassafras.in/cdn/shop/files/SFTOPS42068-2_606fcd07-f742-4ac9-935c-e4d74278c6d8_1800x.jpg?v=1757493262",
                    "https://sassafras.in/cdn/shop/files/SFTOPS42068-3_582cc730-f3b1-440d-afa3-e3635f814dc5_1800x.jpg?v=1757493262",
                    "https://sassafras.in/cdn/shop/files/SFTOPS42068-4_895839b5-619b-4ca5-9adc-fead81c74406_1800x.jpg?v=1757493262"
                ]
            },
            {
                "category": "womens-clothing",
                "name": "Ada Chikankari Yellow Kurti",
                "slug": "ada-chikankari-yellow-kurti",
                "description": "Indian women ethnic motifs hand embroidered yellow cotton lucknowi chikankari indian women short kurti.",
                "price": 1690,
                "original_price": 2490,
                "discount_percentage": 32,
                "stock_quantity": 30,
                "brand": "Ada",
                "rating": 4.6,
                "review_count": 45,
                "images": [
                    "https://assets0.mirraw.com/images/11118940/A911280_zoom.jpg?1689845364",
                    "https://assets0.mirraw.com/images/11119057/image_zoom.jpeg?1674214673",
                    "https://assets0.mirraw.com/images/11119064/image_zoom.jpeg?1674214701",
                    "https://assets0.mirraw.com/images/11119070/image_zoom.jpeg?1674214719"
                ]
            },
            {
                "category": "womens-clothing",
                "name": "Ecentric Lemon Yellow High Low Top",
                "slug": "ecentric-lemon-yellow-top",
                "description": "Elevate your style and prioritize comfort with our high-low hemline top crafted with natural hemp fabric.",
                "price": 1199,
                "original_price": 1999,
                "discount_percentage": 40,
                "stock_quantity": 25,
                "brand": "Ecentric",
                "rating": 4.7,
                "review_count": 22,
                "images": [
                    "https://ecentric.in/cdn/shop/files/1_dab05050-6dff-48de-b80e-315385111397.jpg?v=1692792186&width=1800",
                    "https://ecentric.in/cdn/shop/files/2.1.jpg?v=1692792186&width=1800",
                    "https://ecentric.in/cdn/shop/files/3_796bf222-23bb-491e-ba62-39ab57bf7dfe.jpg?v=1692792184&width=1800",
                    "https://ecentric.in/cdn/shop/files/4_6487aa6c-a8b1-4abe-9902-78d757bffdd8.jpg?v=1692792185&width=1800"
                ]
            },
            {
                "category": "womens-clothing",
                "name": "Freakins Timeless Blue Straight Jeans",
                "slug": "freakins-blue-straight-jeans",
                "description": "Timeless Blue Women's Straight Jeans. Classic denim style for any occasion.",
                "price": 1449,
                "original_price": 2299,
                "discount_percentage": 37,
                "stock_quantity": 55,
                "brand": "Freakins",
                "rating": 4.5,
                "review_count": 134,
                "images": [
                     "https://freakins.com/cdn/shop/files/4thjuly24_14450_a0ab0b3c-986d-4ace-b5a0-d82a86bb5f1e.jpg?v=1749906884&width=2000",
                     "https://freakins.com/cdn/shop/files/4thjuly24_14439_67199ce9-a202-4112-95a5-a0d8412c9b33.jpg?v=1749906884&width=2000",
                     "https://freakins.com/cdn/shop/files/4thjuly24_14423_15dec3ae-182e-4f55-8fe7-0cda39e6bc12.jpg?v=1749906884&width=2000",
                     "https://freakins.com/cdn/shop/files/4thjuly24_14428_1a975175-58a9-41c1-9dd3-5f833a14a6fe.jpg?v=1749906884&width=2000"
                ]
            },
            # WOMEN'S FOOTWEAR
            {
                "category": "womens-footwear",
                "name": "Shoe Lab Comfort Peach Sandal",
                "slug": "shoe-lab-peach-sandal",
                "description": "Comfortable peach sandals with wedge heels, designed for women seeking both elegance and support.",
                "price": 284,
                "original_price": 999,
                "discount_percentage": 71,
                "stock_quantity": 35,
                "brand": "Shoe Lab",
                "rating": 4.0,
                "review_count": 85,
                "images": [
                    "https://www.jiomart.com/images/product/original/rvpbsqulex/shoe-lab-women-s-comfortable-peach-sandal-footwear-for-women-sandals-for-women-wedges-for-women-heels-for-women-non-returnable-product-images-rvpbsqulex-0-202311071212.jpg"
                ]
            },
            {
                "category": "womens-footwear",
                "name": "Milan Safety Ladies Work Shoes",
                "slug": "milan-ladies-work-shoes",
                "description": "Women Black Formal Shoes. Slip-on closure, narrow width. Professional and comfortable for work.",
                "price": 1285,
                "original_price": 1699,
                "discount_percentage": 24,
                "stock_quantity": 40,
                "brand": "Milan Safety",
                "rating": 4.3,
                "review_count": 15,
                "images": [
                    "https://milansafety.com/cdn/shop/products/61KLwvjZ51L._UL1500.jpg?v=1684568621&width=1946"
                ]
            },
            {
                "category": "womens-footwear",
                "name": "Indifeet Stylish Flat Sandal",
                "slug": "indifeet-stylish-flat-sandal",
                "description": "Stylish tan flat sandals for women featuring a trendy strap design, ideal for casual outings and fancy occasions.",
                "price": 1299,
                "original_price": 2599,
                "discount_percentage": 50,
                "stock_quantity": 25,
                "brand": "Indifeet",
                "rating": 4.4,
                "review_count": 45,
                "images": [
                     "https://m.media-amazon.com/images/I/41tZ9T1R6lL._SY625_.jpg"
                ]
            },
            
            # MEN'S FOOTWEAR
            {
                "category": "mens-footwear",
                "name": "Nike Air Force 3 Low x NIGO 'Blue Void'",
                "slug": "nike-air-force-3-low-nigo",
                "description": "A vibrant collaboration between Japanese designer Nigo and Nike, featuring a mix of premium leather, metallic overlays, and artistic details.",
                "price": 14995,
                "original_price": 16995,
                "discount_percentage": 11,
                "stock_quantity": 25,
                "brand": "Nike",
                "rating": 4.8,
                "review_count": 50,
                "images": [
                    "https://static.nike.com/a/images/w_1280,q_auto,f_auto/4690fd0b-d360-4b54-a105-5a47235804cb/air-force-3-low-x-nigo-blue-void-and-tour-yellow-fq7012-100-release-date.jpg",
                    "https://static.nike.com/a/images/w_1280,q_auto,f_auto/ad72b803-3ad2-49f4-9471-b1e525c454c7/air-force-3-low-x-nigo-blue-void-and-tour-yellow-fq7012-100-release-date.jpg",
                    "https://static.nike.com/a/images/w_1280,q_auto,f_auto/728781e6-14c0-40ad-9a5e-e508995656da/air-force-3-low-x-nigo-blue-void-and-tour-yellow-fq7012-100-release-date.jpg"
                ]
            },
            {
                "category": "mens-footwear",
                "name": "New Balance 550 'Oreo'",
                "slug": "new-balance-550-oreo",
                "description": "A classic 1989 basketball silhouette returned to the spotlight. The 'Oreo' colorway offers a clean black-and-white aesthetic with premium leather construction.",
                "price": 8299,
                "original_price": 11999,
                "discount_percentage": 30,
                "stock_quantity": 30,
                "brand": "New Balance",
                "rating": 4.6,
                "review_count": 85,
                "images": [
                    "https://hypefly.co.in/_next/image?url=https%3A%2F%2Fdjm0962033frr.cloudfront.net%2F845080_01_jpg_1c50df1366.webp&w=3840&q=75",
                    "https://hypefly.co.in/_next/image?url=https%3A%2F%2Fdjm0962033frr.cloudfront.net%2Fsmall_1_2025_12_10_T030848_887_fb3bcdc0b9.webp&w=3840&q=75",
                    "https://hypefly.co.in/_next/image?url=https%3A%2F%2Fdjm0962033frr.cloudfront.net%2Fsmall_5_2025_12_10_T030249_131_e1ca54b6ef.webp&w=3840&q=75"
                ]
            },
            {
                "category": "mens-footwear",
                "name": "Asics Gel-NYC",
                "slug": "asics-gel-nyc",
                "description": "The GEL-NYC™ sneaker sources inspiration from heritage and modern performance running styles.",
                "price": 14500,
                "original_price": 15999,
                "discount_percentage": 9,
                "stock_quantity": 20,
                "brand": "Asics",
                "rating": 4.7,
                "review_count": 42,
                "images": [
                    "https://ik.imagekit.io/ventis/prod/tr:n-product_full_image_zoomable/content/images/prodotti/67/92/679273/20250918112603172.jpg",
                    "https://ik.imagekit.io/ventis/prod/tr:n-product_full_image_zoomable/content/images/prodotti/67/92/679273/20250918112603578.jpg"
                ]
            },

            # TV & APPLIANCES
            # AIR CONDITIONERS (ACs)
            {
                "category": "air-conditioners",
                "name": "Samsung 1.5 Ton 3 Star Split AC",
                "slug": "samsung-1-5-ton-3-star-split-ac",
                "description": "1.5 Ton 3 Star Split AC with Anti Bacterial Filter, Copper Condenser Coil, and Silver Nano Technology. Features fast cooling mode and stabilizer-free operation.",
                "price": 30000,
                "original_price": 45990,
                "discount_percentage": 35,
                "stock_quantity": 20,
                "brand": "Samsung",
                "rating": 4.2,
                "review_count": 150,
                "images": [
                    "https://m.media-amazon.com/images/I/41DsqB+M9vL.jpg",
                    "https://m.media-amazon.com/images/I/41DsqB+M9vL._SX466_.jpg",
                    "https://5.imimg.com/data5/SELLER/Default/2023/10/351834416/UX/SD/SD/26748510233/samsung-air-conditioner-500x500.jpg",
                    "https://images.jdmagicbox.com/quickquotes/images_main/samsung-1-5-ton-3-star-2018-split-ac-ar18mc5ulgm-aluminium-white-164741639-u9x8m.jpg"
                ]
            },
            {
                "category": "air-conditioners",
                "name": "Samsung 1.5 Ton 3 Star Inverter Split AC",
                "slug": "samsung-1-5-ton-inverter-split-ac",
                "description": "Triple inverter-powered by 8 pole digital inverter. Convertible mode, digital display, stabilizer-free. Copper Condenser Coil for better cooling.",
                "price": 44990,
                "original_price": 55990,
                "discount_percentage": 20,
                "stock_quantity": 25,
                "brand": "Samsung",
                "rating": 4.4,
                "review_count": 210,
                "images": [
                    "https://m.media-amazon.com/images/I/61Q3CimBXNL._SX342_.jpg",
                    "https://m.media-amazon.com/images/I/61Q3CimBXNL._SX466_.jpg",
                    "https://m.media-amazon.com/images/I/61Q3CimBXNL._SX385_.jpg",
                    "https://m.media-amazon.com/images/I/61Q3CimBXNL._SX569_.jpg",
                    "https://m.media-amazon.com/images/I/61Q3CimBXNL._SX522_.jpg"
                ]
            },
            {
                "category": "air-conditioners",
                "name": "Blue Star 1 Ton 5 Star Inverter Split AC",
                "slug": "blue-star-1-ton-5-star-inverter-ac",
                "description": "Premium 1 Ton Inverter Split AC with 5 Star Energy Rating (2025 BEE Label). Advanced cooling technology and durable copper condenser.",
                "price": 36990,
                "original_price": 48990,
                "discount_percentage": 24,
                "stock_quantity": 15,
                "brand": "Blue Star",
                "rating": 4.6,
                "review_count": 85,
                "images": [
                    "https://consumer.bluestarindia.com/cdn/shop/files/IC512RNUR01.png",
                    "https://consumer.bluestarindia.com/cdn/shop/files/IC512RNUR02.png",
                    "https://consumer.bluestarindia.com/cdn/shop/files/IC512RNUR03.png",
                    "https://consumer.bluestarindia.com/cdn/shop/files/IC512RNUR04.png",
                    "https://consumer.bluestarindia.com/cdn/shop/files/IC512RNUR05.png"
                ]
            },
            {
                "category": "air-conditioners",
                "name": "Godrej 1.5 Ton 3 Star Inverter Split AC",
                "slug": "godrej-1-5-ton-3-star-inverter-ac",
                "description": "1.5 Ton Split AC with Inverter Compressor. Antibacterial Coating and Dust Filter. Suitable for medium-sized rooms.",
                "price": 34499,
                "original_price": 42900,
                "discount_percentage": 20,
                "stock_quantity": 30,
                "brand": "Godrej",
                "rating": 4.1,
                "review_count": 92,
                "images": [
                    "https://m.media-amazon.com/images/I/31dyODG-EUL.jpg",
                    "https://m.media-amazon.com/images/I/31ZoDElKCCL.jpg",
                    "https://m.media-amazon.com/images/I/31pQ0qoeAFL.jpg",
                    "https://m.media-amazon.com/images/I/51iVrbAbqDL.jpg",
                    "https://m.media-amazon.com/images/I/31up4XcoiZL.jpg"
                ]
            },
            {
                "category": "air-conditioners",
                "name": "Blue Star 0.8 Ton 3 Star Inverter Split AC",
                "slug": "blue-star-0-8-ton-inverter-ac",
                "description": "Compact 0.8 Ton Inverter Split AC perfect for smaller rooms up to 100 sq ft. 3-star rating, 100% copper condenser.",
                "price": 28499,
                "original_price": 35900,
                "discount_percentage": 21,
                "stock_quantity": 18,
                "brand": "Blue Star",
                "rating": 4.3,
                "review_count": 45,
                "images": [
                    "https://www.jiomart.com/images/product/original/581026680/bluestar-0-8-ton-3-star-ic309rbtu-inverter-split-air-conditioner-digital-o581026680-p591013458-0-202511181728.jpeg",
                    "https://www.jiomart.com/images/product/original/581026680/bluestar-0-8-ton-3-star-ic309rbtu-inverter-split-air-conditioner-digital-o581026680-p591013458-1-202511181728.jpeg",
                    "https://www.jiomart.com/images/product/original/581026680/bluestar-0-8-ton-3-star-ic309rbtu-inverter-split-air-conditioner-digital-o581026680-p591013458-2-202511181728.jpeg",
                    "https://www.jiomart.com/images/product/original/581026680/bluestar-0-8-ton-3-star-ic309rbtu-inverter-split-air-conditioner-digital-o581026680-p591013458-3-202511181728.jpeg"
                ]
            },
            {
                "category": "air-conditioners",
                "name": "Godrej 1 Ton 3 Star Inverter Split AC",
                "slug": "godrej-1-ton-3-star-inverter-ac",
                "description": "1 Ton Inverter Split AC featuring 100% Copper Condenser with Nano coated Anti-Viral Filter and Anti-Corrosive Bluefin coating.",
                "price": 28990,
                "original_price": 37900,
                "discount_percentage": 24,
                "stock_quantity": 22,
                "brand": "Godrej",
                "rating": 4.2,
                "review_count": 67,
                "images": [
                    "https://cdn.jiostore.online/v2/jmd-asp/jdprod/wrkr/products/pictures/item/free/original/godrej/600725911/0/3Klhi5c0xC-KMN7_kjRMh-Godrej-600725911-i-1-1200Wx1200H.jpeg",
                    "https://cdn.jiostore.online/v2/jmd-asp/jdprod/wrkr/products/pictures/item/free/original/godrej/581026869/1/HxfD13b8q5-6e7890a2-20c8-4805-b1a9-b9d6b8c79f1e.jpeg",
                    "https://cdn.jiostore.online/v2/jmd-asp/jdprod/wrkr/products/pictures/item/free/original/godrej/581026869/2/NNYjU_Ly4g-ab9f234e-8bdb-46e1-90ca-bb86e923fe71.jpeg",
                    "https://cdn.jiostore.online/v2/jmd-asp/jdprod/wrkr/products/pictures/item/free/original/godrej/581026869/3/hAayltbIM6-7b83ff63-9395-45cb-94c7-be8f8d95209c.jpeg"
                ]
            },

            # WASHING MACHINES
            {
                "category": "washing-machines",
                "name": "Samsung 8kg Front Load Washing Machine",
                "slug": "samsung-8kg-front-load-wm",
                "description": "Fully automatic front-loading washing machine with Artificial Intelligence (AI) Control and Wi-Fi connectivity. Features Hygiene Steam.",
                "price": 35900,
                "original_price": 47200,
                "discount_percentage": 24,
                "stock_quantity": 15,
                "brand": "Samsung",
                "rating": 4.5,
                "review_count": 120,
                "images": [
                    "https://images.unsplash.com/photo-1626806819282-2c1dc01a5e0c?w=1000&q=80",
                    "https://images.unsplash.com/photo-1604335399105-a0c585fd81a1?w=1000&q=80",
                    "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=1000&q=80",
                    "https://images.unsplash.com/photo-1626806749363-2f191222d46c?w=1000&q=80"
                ]
            },
            {
                "category": "washing-machines",
                "name": "IFB Senator MBN 8014K 8kg Front Load",
                "slug": "ifb-senator-mbn-8kg-front-load",
                "description": "8 kg capacity, 5-star energy rating, 1400 RPM spin speed. Features Power Steam, Aqua Energie, and Cradle Wash for delicates.",
                "price": 37900,
                "original_price": 48790,
                "discount_percentage": 22,
                "stock_quantity": 12,
                "brand": "IFB",
                "rating": 4.4,
                "review_count": 89,
                "images": [
                    "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=1000&q=80",
                    "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=1000&q=80",
                    "https://images.unsplash.com/photo-1626806819282-2c1dc01a5e0c?w=1000&q=80",
                    "https://images.unsplash.com/photo-1604335399105-a0c585fd81a1?w=1000&q=80"
                ]
            },
            {
                "category": "washing-machines",
                "name": "IFB Elite Plus SXR 7.5kg Front Load",
                "slug": "ifb-elite-plus-sxr-7-5kg",
                "description": "7.5 kg load capacity, 1200 RPM. Features Crescent Moon Drum, 3D Wash System, and in-built heater for hot wash.",
                "price": 35790,
                "original_price": 39490,
                "discount_percentage": 9,
                "stock_quantity": 20,
                "brand": "IFB",
                "rating": 4.3,
                "review_count": 55,
                "images": [
                    "https://images.unsplash.com/photo-1626806749363-2f191222d46c?w=1000&q=80",
                    "https://images.unsplash.com/photo-1626806819282-2c1dc01a5e0c?w=1000&q=80",
                    "https://images.unsplash.com/photo-1545173168-9f1947eebb8f?w=1000&q=80",
                    "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=1000&q=80"
                ]
            },
            {
                "category": "washing-machines",
                "name": "IFB 8kg Top Load TL801EP1S",
                "slug": "ifb-8kg-top-load-tl801ep1s",
                "description": "Top load fully automatic, 8 kg capacity. Features Power Steam, Aqua Energie, and 360-degree Bi-Axial Rotation. Espresso color.",
                "price": 25979,
                "original_price": 33250,
                "discount_percentage": 22,
                "stock_quantity": 18,
                "brand": "IFB",
                "rating": 4.2,
                "review_count": 40,
                "images": [
                    "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=1000&q=80",
                    "https://images.unsplash.com/photo-1545173168-9f1947eebb8f?w=1000&q=80",
                    "https://images.unsplash.com/photo-1626806819282-2c1dc01a5e0c?w=1000&q=80",
                    "https://images.unsplash.com/photo-1604335399105-a0c585fd81a1?w=1000&q=80"
                ]
            },
            {
                "category": "washing-machines",
                "name": "IFB 7kg Top Load TL-REGS",
                "slug": "ifb-7kg-top-load-tl-regs",
                "description": "7 kg Top Load washing machine with Aqua Energie and Deep Clean technology. Stylish medium grey body with glass top.",
                "price": 21990,
                "original_price": 26990,
                "discount_percentage": 19,
                "stock_quantity": 25,
                "brand": "IFB",
                "rating": 4.1,
                "review_count": 65,
                "images": [
                    "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=1000&q=80",
                    "https://images.unsplash.com/photo-1626806819282-2c1dc01a5e0c?w=1000&q=80",
                    "https://images.unsplash.com/photo-1545173168-9f1947eebb8f?w=1000&q=80",
                    "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=1000&q=80"
                ]
            },
            {
                "category": "washing-machines",
                "name": "Godrej 12kg Semi Automatic WS EDGE RIO",
                "slug": "godrej-12kg-semi-automatic",
                "description": "Heavy duty 12 kg semi-automatic washing machine. Rust-proof body, 600W powerful motor, and toughened glass lid.",
                "price": 18499,
                "original_price": 26500,
                "discount_percentage": 30,
                "stock_quantity": 10,
                "brand": "Godrej",
                "rating": 4.0,
                "review_count": 30,
                "images": [
                    "https://images.unsplash.com/photo-1626806749363-2f191222d46c?w=1000&q=80",
                    "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=1000&q=80",
                    "https://images.unsplash.com/photo-1626806819282-2c1dc01a5e0c?w=1000&q=80",
                    "https://images.unsplash.com/photo-1604335399105-a0c585fd81a1?w=1000&q=80"
                ]
            },

            # REFRIGERATORS
            {
                "category": "refrigerators",
                "name": "Whirlpool Intellifresh 308L 2 Star",
                "slug": "whirlpool-intellifresh-308l",
                "description": "308L Double Door Refrigerator with Convertible Freezer. Intellisense Inverter Technology and 6th Sense NutriLock.",
                "price": 27490,
                "original_price": 32500,
                "discount_percentage": 15,
                "stock_quantity": 15,
                "brand": "Whirlpool",
                "rating": 4.3,
                "review_count": 200,
                "images": [
                    "https://images.unsplash.com/photo-1571175443880-49e1d58b794a?w=1000&q=80",
                    "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=1000&q=80",
                    "https://images.unsplash.com/photo-1536353284924-9220c464e262?w=1000&q=80",
                    "https://images.unsplash.com/photo-1585672957774-4b53ce7af2ec?w=1000&q=80"
                ]
            },
            {
                "category": "refrigerators",
                "name": "Samsung Family Hub Refrigerator",
                "slug": "samsung-family-hub-refrigerator",
                "description": "Smart Refrigerator with Touchscreen Hub. Internal cameras, meal planning, and smart home control. 26.5 cu. ft. capacity.",
                "price": 159990,
                "original_price": 239990,
                "discount_percentage": 33,
                "stock_quantity": 5,
                "brand": "Samsung",
                "rating": 4.8,
                "review_count": 45,
                "images": [
                    "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=1000&q=80",
                    "https://images.unsplash.com/photo-1571175443880-49e1d58b794a?w=1000&q=80",
                    "https://images.unsplash.com/photo-1585672957774-4b53ce7af2ec?w=1000&q=80.jpg",
                    "https://images.unsplash.com/photo-1536353284924-9220c464e262?w=1000&q=80"
                ]
            },
            {
                "category": "refrigerators",
                "name": "Liebherr 245L 2 Star Double Door",
                "slug": "liebherr-245l-double-door",
                "description": "245 Litres Frost Free Double Door Refrigerator. Inverter Compressor and Hot-to-Cool Technology.",
                "price": 27500,
                "original_price": 38860,
                "discount_percentage": 29,
                "stock_quantity": 10,
                "brand": "Liebherr",
                "rating": 4.2,
                "review_count": 30,
                "images": [
                    "https://images.unsplash.com/photo-1571175443880-49e1d58b794a?w=1000&q=80",
                    "https://images.unsplash.com/photo-1584269664266-9e6ca3a32339?w=1000&q=80",
                    "https://images.unsplash.com/photo-1585672957774-4b53ce7af2ec?w=1000&q=80",
                    "https://images.unsplash.com/photo-1536353284924-9220c464e262?w=1000&q=80"
                ]
            },
            {
                "category": "refrigerators",
                "name": "Samsung RT28K3922RZ Double Door",
                "slug": "samsung-rt28k3922rz-double-door",
                "description": "253 Litres Double Door Refrigerator with Digital Inverter. Stabilizer Free Operation and Curd Maestro.",
                "price": 22890,
                "original_price": 28990,
                "discount_percentage": 21,
                "stock_quantity": 25,
                "brand": "Samsung",
                "rating": 4.4,
                "review_count": 150,
                "images": [
                    "https://images.unsplash.com/photo-1584269664266-9e6ca3a32339?w=1000&q=80",
                    "https://images.unsplash.com/photo-1571175443880-49e1d58b794a?w=1000&q=80",
                    "https://images.unsplash.com/photo-1536353284924-9220c464e262?w=1000&q=80",
                    "https://images.unsplash.com/photo-1585672957774-4b53ce7af2ec?w=1000&q=80"
                ]
            },
            
            # TELEVISIONS
            {
                "category": "televisions",
                "name": "Sony Bravia 139 cm (55 inches) 4K Ultra HD Smart LED Google TV KD-55X75L",
                "slug": "sony-bravia-55-inch-4k-kd-55x75l",
                "description": "Resolution: 4K Ultra HD (3840 x 2160) | Refresh Rate: 60 Hertz | 178 Degree wide viewing angle. X1 4K Processor, Google TV, Dolby Audio.",
                "price": 57990,
                "original_price": 99900,
                "discount_percentage": 42,
                "stock_quantity": 10,
                "brand": "Sony",
                "rating": 4.8,
                "review_count": 1250,
                "images": [
                    "https://m.media-amazon.com/images/I/81D8pNF0qPL._SX679_.jpg",
                    "https://m.media-amazon.com/images/I/8195A49fElL._SX679_.jpg",
                    "https://m.media-amazon.com/images/I/814mF0rE0NL._SX679_.jpg",
                    "https://m.media-amazon.com/images/I/71wK7q-i+UL._SX679_.jpg"
                ]
            },
            {
                "category": "televisions",
                "name": "Samsung 80 cm (32 Inches) HD Ready LED Smart TV UA32T4340BKXXL",
                "slug": "samsung-32-inch-t4340-smart-tv",
                "description": "HD Ready (1366x768) | Refresh Rate: 60 Hertz. Smart TV Features: Personal Computer, Screen Share, Music System, Content Guide, Connect Share Movie.",
                "price": 13990,
                "original_price": 18900,
                "discount_percentage": 26,
                "stock_quantity": 40,
                "brand": "Samsung",
                "rating": 4.3,
                "review_count": 2100,
                "images": [
                    "https://images.samsung.com/is/image/samsung/in-hd-tv-t4340-ua32t4340akxxl-frontblack-229654228?$684_547_PNG$",
                    "https://images.samsung.com/is/image/samsung/in-hd-tv-t4340-ua32t4340akxxl-dynamic1black-229654230?$684_547_PNG$",
                    "https://images.samsung.com/is/image/samsung/in-hd-tv-t4340-ua32t4340akxxl-dynamic2black-229654231?$684_547_PNG$"
                ]
            },
            {
                "category": "televisions",
                "name": "Samsung 80 cm (32 inch) HD Ready LED Smart TV, Series 4 32T4900",
                "slug": "samsung-32-inch-t4900-series-4",
                "description": "Series 4 Smart Monitor & TV. Work and learn from home with Personal Computer mode. Ultra Clean View and Contrast Enhancer.",
                "price": 15990,
                "original_price": 22900,
                "discount_percentage": 30,
                "stock_quantity": 25,
                "brand": "Samsung",
                "rating": 4.4,
                "review_count": 890,
                "images": [
                    "https://www.suryatronics.in/image/cache/catalog/Samsung-Television-32-Inch-Black_1_19022024113704180-1000x1000.jpg",
                    "https://www.suryatronics.in/image/cache/catalog/Samsung-Television-32-Inch-Black_2_19022024113713392-1000x1000.jpg",
                    "https://www.suryatronics.in/image/cache/catalog/Samsung-Television-32-Inch-Black_3_19022024113717230-1000x1000.jpg",
                    "https://www.suryatronics.in/image/cache/catalog/Samsung-Television-32-Inch-Black_4_19022024113720601-1000x1000.jpg"
                ]
            },
            {
                "category": "televisions",
                "name": "Apple TV 4K (3rd Generation) Wi-Fi + Ethernet",
                "slug": "apple-tv-4k-3rd-gen",
                "description": "The Apple experience. Cinematic in every sense. 4K Dolby Vision and HDR10+. Powered by the A15 Bionic chip. Siri Remote with touch-enabled clickpad.",
                "price": 16900,
                "original_price": 16900,
                "discount_percentage": 0,
                "stock_quantity": 30,
                "brand": "Apple",
                "rating": 4.9,
                "review_count": 3500,
                "images": [
                    "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/apple-tv-4k-hero-select-202210?wid=1076&hei=1070&fmt=jpeg&qlt=90&.v=1664896361164",
                    "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/apple-tv-4k-remote-select-202210?wid=1076&hei=1070&fmt=jpeg&qlt=90&.v=1664896361482",
                    "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/apple-tv-4k-connect-select-202210?wid=1076&hei=1070&fmt=jpeg&qlt=90&.v=1664896361596"
                ]
            },
            {
                "category": "mens-footwear",
                "name": "Adidas Originals Samba OG",
                "slug": "adidas-samba-og",
                "description": "Born on the pitch, the Samba is a timeless icon of street style. Low-profile look, soft leather upper, and gum rubber outsole.",
                "price": 9500,
                "original_price": 10999,
                "discount_percentage": 13,
                "stock_quantity": 40,
                "brand": "Adidas",
                "rating": 4.5,
                "review_count": 300,
                "images": [
                    "https://www.bonzer.cl/cdn/shop/products/zapatilla-adidas-originals-samba-og-127383.jpg?v=1696535614",
                    "https://www.bonzer.cl/cdn/shop/products/zapatilla-adidas-originals-samba-og-322608.webp?v=1696535614",
                    "https://www.bonzer.cl/cdn/shop/products/zapatilla-adidas-originals-samba-og-543790.webp?v=1696535614"
                ]
            },

            # TV & APPLIANCES
            {
                "category": "tv-appliances",
                "name": "Samsung 55-inch Crystal 4K UHD TV",
                "slug": "samsung-55inch-crystal-4k-tv",
                "description": "Ultra HD visuals with Crystal Processor 4K.",
                "price": 42990,
                "original_price": 54990,
                "discount_percentage": 22,
                "stock_quantity": 34,
                "brand": "Samsung",
                "rating": 4.4,
                "review_count": 5621,
                "images": [
                    "https://images.unsplash.com/photo-1593784991095-a20506948430?w=600&auto=format&fit=crop&q=60"
                ]
            },
             {
                "category": "tv-appliances",
                "name": "LG Washing Machine",
                "slug": "lg-washing-machine",
                "description": "Front load fully automatic washing machine.",
                "price": 34990,
                "original_price": 44990,
                "discount_percentage": 22,
                "stock_quantity": 31,
                "brand": "LG",
                "rating": 4.4,
                "review_count": 3892,
                "images": [
                    "https://images.unsplash.com/photo-1626806819282-2c1dc01a5e0c?w=600&auto=format&fit=crop&q=60"
                ]
            },

            # FASHION
            {
                "category": "mens-fashion",
                "name": "Levi's Men's Jeans",
                "slug": "levis-mens-jeans",
                "description": "Classic fit denim jeans.",
                "price": 1999,
                "original_price": 3499,
                "discount_percentage": 43,
                "stock_quantity": 125,
                "brand": "Levi's",
                "rating": 4.4,
                "review_count": 12543,
                "images": [
                    "https://images.unsplash.com/photo-1542272617-08f08637533d?w=600&auto=format&fit=crop&q=60"
                ]
            },
            {
                "category": "mens-fashion",
                "name": "Nike Running Shoes",
                "slug": "nike-running-shoes",
                "description": "Comfortable running shoes for daily use.",
                "price": 3499,
                "original_price": 5999,
                "discount_percentage": 42,
                "stock_quantity": 87,
                "brand": "Nike",
                "rating": 4.5,
                "review_count": 6543,
                "images": [
                    "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&auto=format&fit=crop&q=60"
                ]
            },
            {
                "category": "womens-fashion",
                "name": "Women's Summer Dress",
                "slug": "womens-summer-dress",
                "description": "Light and breezy summer dress.",
                "price": 1499,
                "original_price": 2999,
                "discount_percentage": 50,
                "stock_quantity": 134,
                "brand": "Zara",
                "rating": 4.3,
                "review_count": 8765,
                "images": [
                    "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600&auto=format&fit=crop&q=60"
                ]
            },
            
            # FURNITURE
             {
                "category": "furniture",
                "name": "Modern Sofa",
                "slug": "modern-sofa",
                "description": "Comfortable 3-seater sofa.",
                "price": 24999,
                "original_price": 44999,
                "discount_percentage": 44,
                "stock_quantity": 18,
                "brand": "Durian",
                "rating": 4.3,
                "review_count": 2345,
                "images": [
                    "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600&auto=format&fit=crop&q=60"
                ]
            }
        ]

        # Create products and images
        for product_data in products_data:
            images_urls = product_data.pop("images")
            category_slug = product_data.pop("category")
            
            # Handle user schema update (specifications)
            product_data["specifications"] = {} # Default specs for simplicity
            
            product = Product(
                category_id=categories[category_slug],
                **product_data,
                is_available=True
            )
            db.add(product)
            db.flush()
            
            # Add product images
            for idx, img_url in enumerate(images_urls):
                img = ProductImage(
                    product_id=product.id,
                    image_url=img_url,
                    display_order=idx,
                    is_primary=(idx == 0)
                )
                db.add(img)
        
        db.commit()
        print(f"Database seeded successfully with {len(products_data)} products!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()