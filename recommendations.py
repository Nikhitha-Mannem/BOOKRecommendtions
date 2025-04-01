# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load the data with low_memory=False to avoid DtypeWarning
books_df = pd.read_csv('Books.csv', low_memory=False)
ratings_df = pd.read_csv('Ratings.csv', low_memory=False)

# Drop unnecessary columns from the books dataframe
books_df = books_df.drop(['Image-URL-S', 'Image-URL-M'], axis=1)

# Clean book titles to remove any extra whitespace and make them lowercase
books_df['Book-Title'] = books_df['Book-Title'].astype(str).str.strip().str.lower()

# Filter books with more than 50 ratings
filtered_books = ratings_df.groupby('ISBN')['Book-Rating'].count() > 50
books_with_more_than_50_ratings = filtered_books[filtered_books.values == True]

# Filter users who rated more than 200 books
filtered_users = ratings_df.groupby('User-ID')['Book-Rating'].count() > 200
users_rated_more_than_200_books = filtered_users[filtered_users.values == True]

# Keep only the ratings from the filtered books and users
ratings_df = ratings_df[ratings_df['ISBN'].isin(books_with_more_than_50_ratings.index)]
ratings_df = ratings_df[ratings_df['User-ID'].isin(users_rated_more_than_200_books.index)]

# Merge the books and ratings dataframes
books_with_ratings = books_df.merge(ratings_df, on='ISBN')

# Remove duplicate ratings from the same user for the same book
books_with_ratings = books_with_ratings.drop_duplicates(subset=['User-ID', 'Book-Title'])

# Create a pivot table for collaborative filtering
pivot_matrix = books_with_ratings.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating').fillna(0)

# Calculate cosine similarity between items
item_similarity = cosine_similarity(pivot_matrix)

# Create a dictionary to map normalized titles to original titles
title_mapping = {title.lower().strip(): title for title in pivot_matrix.index}

# Recommendation function
def recommended_books(book_name, no_of_recommended_books=3):
    # Normalize the input book name
    book_name = ' '.join(book_name.strip().lower().split())

    # Check if the normalized book name exists in the title mapping
    if book_name in title_mapping:
        # Get the original title from the mapping
        original_title = title_mapping[book_name]
        
        # Find the index of the original title in the pivot matrix
        book_index = np.where(pivot_matrix.index == original_title)[0][0]

        # Get indices of similar books sorted by similarity score
        similar_books_indexes = item_similarity[book_index].argsort()[::-1][1:no_of_recommended_books+1]

        # Retrieve the book titles using the indices
        recommendations = [pivot_matrix.index[e] for e in similar_books_indexes]
        return recommendations
    else:
        return 'Book Not Found'

# Example usage
#print(recommended_books("Harry Porter"))
#print(recommended_books("The Great Gatsby"))
