# 533_project
# Supermarket System Functions

---

## 1. Product Management (Sub-Package 1)
### **Module 1: Warehouse Management**
- **Description:** Handles product management within the warehouse.
- **Functions:**
 1. **Product Entry (`add_product()`):**
    - **Inputs:** `id`, `name`, `category`, `purchase_price`, `entry_date`, `quantity`
    - Adds new products to the warehouse database with complete details.
 2. **Product Exit (`remove_product()`):**
    - **Inputs:** `id`, `quantity`
    - Ensures stock availability before fulfilling product requests.
 3. **Inventory Display (`display()`):**
    - **Output:** `id`, `name`, `category`, `purchase_price`, `entry_date`, `quantity`
    - Displays details of products in the warehouse, including stock levels and entry information.

### **Module 2: Sales Management**
- **Description:** Manages product movement and display on shelves.
- **Functions:**
 1. **New Product Shelving (`add_newproduct()`):**
    - **Inputs:** `id`, `quantity`, `sale_price`
    - Moves products from the warehouse to the shelves and adjusts stock levels.
 2. **Modify Sale Price (`change_price()`):**
    - **Inputs:** `id`, `new_price`
    - Updates the price of shelved products.

 3. **Adjust Shelf Quantity :**
    - **Inputs:** `id`, `quantity`
    - Increases product quantities on shelves( `increase_quantity()`).
    - Decreases product quantities on shelves(`decrease_quantity()`).

 4. **Products Display (`display_shelves()`):**
    - **Inputs:** `id`, `name`, `quantity`, `sales_price`
    - Shows products currently available on shelves.

---

## 2. Customer Management (Sub-Package 2)
### **Module 1: Purchase Management**
- **Description:** Enables and manages customer shopping activities.
- **Functions:**
 1. **Product Browsing (`display()`):**
    - Allows customers to view available products on shelves.
 2. **Product Selection (`choose()`):**
    - Adds or removes items from the shopping cart.
    - Records customer details (`name`, `sale_price`, `quantity`, `purchase_price`).
 3. **Checkout (`checkout()`):**
    - Processes and finalizes purchases, including:
      - Calculating total and tax-inclusive amounts.
      - Recording the transaction through `add_record()`.
      - Reducing shelved product quantities.

### **Module 2: Records Management**
- **Description:** Tracks customer purchases and generates insights.
- **Functions:**
 1. **Add Record (`add_record()`):**
   - **Inputs:** `id`, `items`, `total_price`, `profit`, `cal_quantity`
    - Logs individual purchase transactions.
 2. **Purchase History (`get_history()`):**
    - Retrieves a customer's shopping records.
 3. **Customer Spending Insights (`get_total()`):**
    - Calculates total purchase counts and spending for each customer.
 4. **Store Profit Analysis (`supermarket_situation()`):**
    - Analyzes total sales, profits, and identifies popular products.
