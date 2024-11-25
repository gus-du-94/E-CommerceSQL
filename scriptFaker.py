import mysql.connector
from faker import Faker
import random

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="e-commerce"
)

cursor = conn.cursor()

# Initialisation de Faker
fake = Faker()

def insert_addresses(n):
    for _ in range(n):
        query = """
        INSERT INTO Address (Pays, Ville, CodePostal, Rue)
        VALUES (%s, %s, %s, %s)
        """
        values = (fake.country(), fake.city(), fake.zipcode(), fake.street_name())
        cursor.execute(query, values)
    conn.commit()

# Génération de données pour Product
def insert_products(n):
    for _ in range(n):
        query = """
        INSERT INTO Product (Product, Description, Prix, Dimension)
        VALUES (%s, %s, %s, %s)
        """
        values = (fake.word(), fake.text(max_nb_chars=50), random.randint(10, 1000), f"{random.randint(10, 100)}x{random.randint(10, 100)}x{random.randint(10, 100)}")
        cursor.execute(query, values)
    conn.commit()

# Génération de données pour Utilisateur
def insert_users(n):
    cursor.execute("SELECT IDAddress FROM Address")
    address_ids = [i[0] for i in cursor.fetchall()]
    for _ in range(n):
        query = """
        INSERT INTO Utilisateur (Nom, Prenom, Mdp, Email, IDAddress)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (fake.last_name(), fake.first_name(), fake.password(), fake.email(), random.choice(address_ids))
        cursor.execute(query, values)
    conn.commit()

# Génération de données pour ProductCart
def insert_product_cart(n):
    cursor.execute("SELECT IDProduct FROM Product")
    product_ids = [i[0] for i in cursor.fetchall()]
    for _ in range(n):
        query = """
        INSERT INTO ProductCart (IDCommand, IDProduct, Quantity)
        VALUES (%s, %s, %s)
        """
        values = (None, random.choice(product_ids), random.randint(1, 10))
        cursor.execute(query, values)
    conn.commit()

# Génération de données pour Cart
def insert_carts(n):
    cursor.execute("SELECT IDProductCart FROM ProductCart")
    product_cart_ids = [i[0] for i in cursor.fetchall()]
    for _ in range(n):
        query = """
        INSERT INTO Cart (IDProductCart)
        VALUES (%s)
        """
        values = (random.choice(product_cart_ids),)
        cursor.execute(query, values)
    conn.commit()

# Génération de données pour Command
def insert_commands(n):
    cursor.execute("SELECT IDUser FROM Utilisateur")
    user_ids = [i[0] for i in cursor.fetchall()]
    cursor.execute("SELECT IDCart FROM Cart")
    cart_ids = [i[0] for i in cursor.fetchall()]
    cursor.execute("SELECT IDAddress FROM Address")
    address_ids = [i[0] for i in cursor.fetchall()]
    for _ in range(n):
        query = """
        INSERT INTO Command (IDUser, IDCart, IDAddress)
        VALUES (%s, %s, %s)
        """
        values = (random.choice(user_ids), random.choice(cart_ids), random.choice(address_ids))
        cursor.execute(query, values)
    conn.commit()

# Génération de données pour Invoice
def insert_invoices(n):
    cursor.execute("SELECT IDCommand FROM Command")
    command_ids = [i[0] for i in cursor.fetchall()]
    for _ in range(n):
        query = """
        INSERT INTO Invoice (IDCommand, PrixTotal, MethodPaiement)
        VALUES (%s, %s, %s)
        """
        values = (random.choice(command_ids), random.randint(100, 10000), random.choice(['Carte', 'PayPal', 'Virement']))
        cursor.execute(query, values)
    conn.commit()

# Exécution des fonctions
insert_addresses(10)
insert_products(10)
insert_users(10)
insert_product_cart(20)
insert_carts(10)
insert_commands(10)
insert_invoices(10)

# Fermeture de la connexion
cursor.close()
conn.close()