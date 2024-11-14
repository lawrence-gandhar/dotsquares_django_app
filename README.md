# Dotsquares django Ecommerce Application - Assignment

## Requirements

1. Setup Django ecommerce project with apps.Create Authentication for fronted user so logged-in users can see what products have been added to the cart.
2. Create a Products Section in the Backend (Fields: Name, Image, Price, Stock).
3. Create a Category Section in the Backend and establish parent-child relationships between them.
4. Create Product tags and establish relationships between products and tags. A product can have multiple tags, and the same tag can be associated with multiple products.
5. Call the products on the frontend in list view and details view.
6. Enable the addition of products to the cart.
7. Create a cart page to display all products added to the cart and implement functionality to remove products from the cart.
8. Upload the files to a public GIT repository and include a README file for proper setup of the project in a local environment.

## Installation

#### Step 1 :: Setting up a Virtual Environment

Install virtualenv package using pip for creating a virtual environment.

<code>pip install virtualenv</code>

#### Step 2 :: Create a directory and activate venv

<code>mkdir projectA    # creates a directory
cd projectA        # navigate inside the directory     
</code>

The below given command will create a directory `env` inside your `projectA` directory. 

`python3 -m venv env`

Now we will activate the virtual environmrent.
`source env/bin/activate`

To deactivate a virtual environment, use the below given command.

`deactivate`


#### Step 2 :: Installing Django

For installation use the below given command.

`python3 -m pip install Django`

To check the version of django installed, use the below given command

`python3 -m django --version`

<br>

# Project and Application Setup

#### Step 1 :

Clone the repository to your local machine, and activate the virtual environment.

#### Step 2 :

Navigate into the directory structure. you will find a file `manage.py` in the `django_app` folder. Now execute the command given below to create a database. Django by default has integration with sqlite.

`python3 manage.py makemigrations app`

Then we have to execute this command `python3 manage.py migrate`. This command will create the database/schemas and tables.

Now, we can create a superuser using the below given command.

`python3 manage.py createsuperuser`

The above command will ask for email address, because I have made `Email Address` as `username`. Please follow the prompts and the superuser will be created.

We can use the same `email address` and the password for both the `Admin` and the `Frontend`.

Now to in order to start the application, we will use the below given command.

`python3 manage.py runserver 0.0.0.0:8000`

This will start the development server on port 8000.

Open your favorite browser, and put in the below given url.

`http://localhost:8000` This is for `Frontend`
`http://localhost:8000/admin` This is for the `Admin Panel`



