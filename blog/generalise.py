import psycopg2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from database import engine as en
from sqlalchemy import text

engine = en.connect()
# Connect to the database
# conn = psycopg2.connect(
#     dbname="review",
#     user="postgres",
#     password="Tanzo",
#     host="172.17.0.1",
#     port="5433"
# )

# Create a cursor
# cur = conn.cursor()

# Alter the table to add a new column
engine.execute(text("ALTER TABLE products ADD COLUMN IF NOT EXISTS generalized_description TEXT"))

# Fetch product descriptions from the products table
result=engine.execute(text("SELECT product_id, description FROM products"))

products = result.fetchall()

# Download stopwords if not already downloaded
# if not stopwords.words("english"):
#     nltk.download("stopwords")
# nltk.download("stopwords")
nltk.download("punkt")
# nltk.download("corpus")


# Remove stop words from descriptions
stop_words = set(stopwords.words("english"))
additional_stopwords = set([':', '('])
stop_words.update(additional_stopwords)


for product in products:
    product_id, description = product
    words = word_tokenize(description.lower())
    filtered_words = [word for word in words if word not in stop_words]
    generalized_description = " ".join(filtered_words)

    # Update the table with the generalized description
    query = text("UPDATE products SET generalized_description=:descrip WHERE product_id=:pid")
    engine.execute(query, {"descrip": generalized_description, "pid": product[0]})

#Drop the table if it exists    
engine.execute(text("""
    DROP TABLE IF EXISTS word_counts
"""))



# Create a new table for word counts if it doesn't exist
engine.execute(text("""
    CREATE TABLE IF NOT EXISTS word_counts (
        id SERIAL PRIMARY KEY,
        word TEXT,
        count INTEGER
    )
"""))

# Fetch generalized descriptions from the products table
des=engine.execute(text("SELECT product_id, generalized_description FROM products"))
descriptions = des.fetchall()
print(description)
# Remove stop words from descriptions and count the occurrences of each word
word_counts = Counter()
for product_id, description in descriptions:
    words = word_tokenize(description.lower())
    word_counts.update(words)

# Insert word counts into the new table
for word, count in word_counts.items():
    query=text("INSERT INTO word_counts (word, count) VALUES (:word,:count)")
    engine.execute(query, {"word":word , "count":count})

# Print the contents of the word_counts table
count=engine.execute(text("SELECT * FROM word_counts"))
word_counts_table = count.fetchall()
for row in word_counts_table:
    print(row)

# Commit the changes and close the connection
print('done')
engine.commit()
engine.close()
