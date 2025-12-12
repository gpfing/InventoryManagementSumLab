# Mock database using array to simulate inventory storage

# In-memory database simulating inventory storage
# Each item contains data similar to OpenFoodFacts API structure
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar, sea salt, sunflower lecithin, gellan gum, natural flavor, vitamin A palmitate, vitamin D2, D-alpha-tocopherol",
        "quantity": 50,
        "price": 4.99,
        "barcode": "025293600270"
    },
    {
        "id": 2,
        "product_name": "Organic Peanut Butter",
        "brands": "Justin's",
        "ingredients_text": "Dry roasted peanuts, palm oil, sea salt",
        "quantity": 30,
        "price": 8.99,
        "barcode": "894700010014"
    },
    {
        "id": 3,
        "product_name": "Greek Yogurt",
        "brands": "Chobani",
        "ingredients_text": "Cultured nonfat milk, cane sugar, water, strawberries, natural flavors, fruit pectin, guar gum, beet juice concentrate",
        "quantity": 75,
        "price": 1.49,
        "barcode": "894700010052"
    }
]

# Counter for generating new IDs
next_id = 4
