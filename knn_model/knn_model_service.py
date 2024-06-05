import pickle
from typing import List
from dto.product_dto import ProductDto
from dto.product_result import ProductResult

# Importing packages
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Loading dataset
products_data = pd.read_csv('../knn_model/shopping_behavior_updated.csv', index_col='Customer ID')
products_data['Gender'] = products_data['Gender'].replace({'Male': 0.68, 'Female': 0.32})
products_data['Category'] = products_data['Category'].replace({'Clothing': 0.42, 'Accessories': 0.30, 'Footwear': 0.2, 'Outerwear':0.08})
products = products_data[['Age', 'Gender', 'Category', 'Purchase Amount (USD)', 'Item Purchased']]

feature_cols = products.drop(['Item Purchased'], axis=1)
X = feature_cols

async def suggest_product(suggestions: List[ProductDto]) -> List[ProductResult]:
    
    # Extract features from suggestions
    post_data = [[suggestion.Age, suggestion.Gender, suggestion.Category, suggestion.PurchaseAmount] for suggestion in suggestions]
    the_post = pd.DataFrame(data=post_data, index=[1])
    
    # Using NearestNeighbors model and kneighbors() method to find k neighbors.
    # Setting n_neighbors = 3 to find 3 similar products
    # Using brute force due to small sample size (30) and few dimensions (11)

    neigh = NearestNeighbors(n_neighbors=3, algorithm='brute')
    neigh.fit(X)
    distances, indices = neigh.kneighbors(the_post)

    # Predict scores
    # predicted_scores = model.predict(features)

    # Create LocationResult objects
    product_results = []
    
        
    for i in range(len(distances.flatten())):
        product_results.append(ProductResult(ItemPurchased=products['Item Purchased'].iloc[indices.flatten()[i]]))
    
    # for suggestion, score in zip(suggestions, predicted_scores):
    #     location_results.append(LocationResult(LocationId=suggestion.LocationId, Score=score))

    return product_results
