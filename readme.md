# Little Lemon Restaurant API

Welcome to the **Little Lemon Restaurant API** documentation. This guide provides an overview of the project's scope, required endpoints, and key implementation notes. Please refer to this document as you develop your API project to ensure its successful completion.

## <span style="color: #800080">Scope</span>

You will create a fully functioning API project for the *Little Lemon* restaurant, enabling client application developers to use the APIs for web and mobile applications. Users with different roles can browse, add, and edit menu items, place and manage orders, assign delivery crew, and complete deliveries.

## <span style="color: #800080">Project Structure</span>

- Create a Django app named `LittleLemonAPI` to house all API endpoints.
- Utilize `pipenv` to manage dependencies within a virtual environment.
- Follow proper naming conventions and use function- or class-based views as appropriate.
- Define user roles and groups as outlined in the project requirements.

## <span style="color: #800080">User Groups</span>

Create the following user groups and assign users to them through the Django admin panel:

1. Manager
2. Delivery Crew

Users not assigned to a group will be considered customers.

## <span style="color: #800080">Error Handling and Status Codes</span>

Implement appropriate error messages accompanied by relevant HTTP status codes. Ensure that the API returns the correct status codes for various scenarios, including successful operations and errors.

## <span style="color: #800080">API Endpoints</span>

The following sections detail the required API endpoints, their roles, methods, and purposes.

### <span style="color: #800080">User Registration and Token Generation</span>

1. **Endpoint**: `/api/users`
   - **Role**: No role required
   - **Method**: POST
   - **Purpose**: Creates a new user with name, email, and password.

2. **Endpoint**: `/api/users/users/me/`
   - **Role**: Anyone with a valid user token
   - **Method**: GET
   - **Purpose**: Displays information about the current user.

3. **Endpoint**: `/token/login/`
   - **Role**: Anyone with a valid username and password
   - **Method**: POST
   - **Purpose**: Generates access tokens for further API calls.

### <span style="color: #800080">Menu Items Management</span>

1. **Endpoint**: `/api/menu-items`
   - **Role**: Customer, Delivery Crew
   - **Method**: GET
   - **Purpose**: Lists all menu items.

2. **Endpoint**: `/api/menu-items/{menuItem}`
   - **Role**: Customer, Delivery Crew
   - **Method**: GET
   - **Purpose**: Displays information about a single menu item.

3. **Endpoint**: `/api/menu-items`
   - **Role**: Manager
   - **Method**: GET
   - **Purpose**: Lists all menu items.

### <span style="color: #800080">User Group Management</span>

1. **Endpoint**: `/api/groups/manager/users`
   - **Role**: Manager
   - **Method**: GET
   - **Purpose**: Return a list of all managers.

2. **Endpoint**: `/api/groups/manager/users`
   - **Role**: Manager
   - **Method**: POST
   - **Purpose**: Assigns a user to the manager group.

3. **Endpoint**: `/api/menu-items`
   - **Role**: Manager
   - **Method**: GET
   - **Purpose**: Lists all menu items.

### <span style="color: #800080">Cart Management</span>

1. **Endpoint**: `/api/cart/menu-items`
   - **Role**: Customer
   - **Method**: GET
   - **Purpose**: Return current items in the customer's cart.

2. **Endpoint**: `/api/cart/menu-items`
   - **Role**: Customer
   - **Method**: POST
   - **Purpose**: Adds a menu item to the cart.

### <span style="color: #800080">Order Management</span>

1. **Endpoint**: `/api/orders`
   - **Role**: Customer
   - **Method**: GET
   - **Purpose**: Return all orders with order items created by a customer.

2. **Endpoint**: `/api/orders`
   - **Role**: Customer
   - **Method**: POST
   - **Purpose**: Creates a new order item for the customer.

3. **Endpoint**: `/api/orders/{orderId}`
   - **Role**: Customer
   - **Method**: GET
   - **Purpose**: Lists all items for a specific order.

4. **Endpoint**: `/api/orders`
   - **Role**: Manager
   - **Method**: GET
   - **Purpose**: Return all orders with order items for all users.

5. **Endpoint**: `/api/orders/{orderId}`
   - **Role**: Manager
   - **Method**: PUT, PATCH
   - **Purpose**: Updates the order, incluiding assigning a delivery crew and updating the order status.

6. **Endpoint**: `/api/orders/{orderId}`
   - **Role**: Manager
   - **Method**: DELETE
   - **Purpose**: Deletes an order.

7. **Endpoint**: `/api/orders/`
   - **Role**: Delivery Crew
   - **Method**: GET
   - **Purpose**: Return all orderds.

8. **Endpoint**: `/api/orders`
   - **Role**: Delivery Crew
   - **Method**: PATCH
   - **Purpose**: Allows a delivery crew to update the order status.

## <span style="color: #800080">Additional Steps</span>

- Implement filtering, pagination, and sorting for `/api/menu-items` and `/api/orders` endpoints.
- Apply throttling to ensure API stability and performance.
