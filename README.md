# Django AnonMarket

## Introduction
<p>
D-A-M (Django Anon Market) is an online shop that users can shop  anonymously. <br><br>
The reason that we call it anonymous is that users can not be tracked by their banking logs cuz they are not using real money, they pay for orders using website currency. <br><br>
Users can create an account and exchange their money to websites digital currency and order items. <br> <br>
This project contains 6 applications. <br>

</p>
<ol>
  <li>Authentication</li>
  <li>Vendor</li>
  <li>Customer</li>
  <li>Forum</li>
  <li>Blog</li>
  <li>Messages</li>
</ol> 

### Authentication
<p>
    This project is using django-allauth package for authentication purposes but they are other functionalities that are stored in Auth app, such as:
</p>
<ol>
  <li>User Profile page</li>
  <li>Exchange Money</li>
  <li>Rate a user</li>
</ol>
<hr>

### Vendor
<p>
    This application is only for Selling purposes. vendors can simply Add product or manage customer orders. other features:   
</p>
<ol>
  <li>Update/Delete Product.</li>
  <li>Rate Products.</li>
  <li>Accept/Decline User Orders</li>
  <li>Other Order Management like send product & list of products.</li>
</ol>
<hr>

### Customer
<p>
       As its obvious from its name, this app is for Selling purposes. Users can Order Products and pay for it.
</p>
<ol>
  <li>Add/Delete Order.</li>
  <li>Pay for Orders.</li>
  <li>Orders list and so on.</li>
</ol>
<hr>

### Message
<p>
       This application is for communicating purposes. Customers can communicate with vendors, in order to ask questions and so on.
</p>
<ol>
  <li>Send Message.</li>
  <li>Update/Delete Message.</li>
  <li>Chat List.</li>
</ol>
<hr>

### Blog
<p>
       This application is a simple blog that vendors can write articles for advertising purposes. <br>
        Also it is possible to create a vip article and people must pay in order to access that article.
</p>
<ol>
  <li>Create/Update/Delete Article.</li>
  <li>Rate/Comment System.</li>
  <li>Chat List.</li>
  <li>Buy Article.</li>
    
</ol>
<hr>

### Forum
<p>
       Users can also create Forums in order to ask questions from people. they can ask about a product or provider for insuring that the provider is reliable. <br>
        Same as articles, forums can be vip too, People needs to purchase that forum in order to access its comments.
</p>
<ol>
  <li>Create/Update/Delete Forum.</li>
  <li>Answer Forums.</li>
  <li>Close forum.</li>
  <li>Purchase forum</li>
    
</ol>
<hr>

## How to use?

### First you have to clone this project and cd to the source folder.

```commandline
$ git clone https://github.com/Ml06py/django-anonmarket.git && cd https://github.com/Ml06py/django-anonmarket.git 
```

### If you have docker installed of your pc, you can run the project with one command

```commandline
   $ docker-compose up --build
```

### Otherwise You have to follow this steps.

```commandline
    $ pip install -r requirement.txt
```

```commandline
    $ python manage.py migrate && python manage.py runserver --insecure
```


<small>Good luck.</small>
