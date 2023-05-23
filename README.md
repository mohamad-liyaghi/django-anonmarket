## Introduction
Django AnonMarket is an online marketplace that allows users to shop anonymously using website currency instead of real money. 
<br>
As an anonymous marketplace, Django AnonMarket prioritizes the privacy and security of its users, allowing them to enjoy a level of anonymity where nobody can keep track of them by being careful and following best practices.
<br>Users can create an account, exchange real money to website currency, and order products from the website. They can also add their own products for sale. 
<br>

The project consists of several modular and scalable applications: 

- Accounts
- Products
- Orders
- Forums
- Articles
- Chats
- Votes
- Comments
<hr>

## Here's a complete overview of each application:

### Accounts
The Accounts app is responsible for user authentication and includes additional functionalities such as a user profile page, registration, login, and logout. Django Allauth is used for authentication.

- User Profile page: Allows users to view and edit their profile information.
- Registration: Allows new users to register.
- Login: Allows users to log in.
- Logout: Allows users to log out.

### Products
The Products app is responsible for managing products and includes functionalities such as adding, updating, and deleting products, and searching for products.

- Add/Delete Product: Allows vendors to add or delete products .
- Update Product: Allows vendors to update product information.
- Search Products: Allows customers to search for products.

### Orders
The Orders app is responsible for managing user orders and includes functionalities such as adding or deleting orders, paying for orders, and viewing a list of orders.

- Add/Delete Order: Allows users to add or delete orders [Ajax] .
- Pay for Orders: Allows users to pay for their orders using website currency.
- Orders List: Allows users to view a list of their orders.

### Chats
The Chats app is responsible for communication between customers and vendors through a real-time messaging system using Django Channels.

- Send Message: Allows customers to send new messages [Socket].
- Update/Delete Message: Allows customers to update or delete messages [Socket].
- Chat List: Allows customers to view a list of their chats.

### Forums
The Forums app allows users to create and participate in forums to discuss products or providers.

- Create/Update/Delete Forum: Allows users to create, update, or delete forums.
- Answer Forums: Allows users to answer forums.
- Close Forum: Allows users to close forums.

### Articles
The Articles app is a simple blogging platform that vendors can use to write articles for advertising purposes. It includes a rating/comment system and an option for users to purchase access to VIP articles.

- Create/Update/Delete Article: Allows vendors to create, update, or delete articles.
- Rating/Comment System: Allows users to rate and comment on articles.
- Buy Article: Allows users to purchase access to VIP articles.
<hr>

## Generic apps 

### Votes
The Votes app is a generic app that provides functionalities for users to vote on any model in the project.

- Add/Delete Vote: Allows users to add or delete votes [Ajax].

### Comments
The Comments app is a generic app that provides functionalities for users to comment on any model in the project.

- Add/Delete Comment: Allows users to add or delete comments [Ajax].
- Comment list

<hr>

## How to use
To use the project, follow these steps:

1. Clone the repository and navigate to the project directory:
   ```
   git clone https://github.com/mohamad-liyaghi/django-anonmarket.git && cd django-anonmarket
   ```
   
2. Run it via docker:
   ````
   docker-compose up --build
   ```````

5. Go to http://127.0.0.1/ to access the website.


## Shots

### Product List
<img src='https://github.com/mohamad-liyaghi/django-anonmarket/blob/main/shots/sample-product-list.jpg' alt='sample-product-list'>

### Product Detail

<img src='https://github.com/mohamad-liyaghi/django-anonmarket/blob/main/shots/sample-product-detail.jpg' alt='sample-product-detail'>

### Order List

<img src='https://github.com/mohamad-liyaghi/django-anonmarket/blob/main/shots/sample-order-list.jpg' alt='sample-order-list'>

### Article List
<img src='https://github.com/mohamad-liyaghi/django-anonmarket/blob/main/shots/sample-article-list.jpg' alt='sample-order-list'>

### Article Detail

<img src='https://github.com/mohamad-liyaghi/django-anonmarket/blob/main/shots/sample-article-detail.jpg' alt='sample-order-detail'>

### Forum Detail

<img src='https://github.com/mohamad-liyaghi/django-anonmarket/blob/main/shots/sample-forum-detail.jpg' alt='sample-forum-detail'>

### Forum Answer

<img src='https://github.com/mohamad-liyaghi/django-anonmarket/blob/main/shots/sample-forum-answer.jpg' alt='sample-forum-answer'>

### Chat Detail

<img src='https://github.com/mohamad-liyaghi/django-anonmarket/blob/main/shots/sample-real-time-chat.jpg' alt='sample-chat-detail'>
