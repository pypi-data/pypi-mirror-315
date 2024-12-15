import pandas as pd
from surprise import SVDpp, Dataset, Reader, accuracy
from surprise.model_selection import train_test_split
import numpy as np
import hashlib


class SVDPPModel:
    def __init__(self, n_epochs=20, lr_all=0.005, reg_all=0.02):
        """
        Initialize the SVD++ model with specified hyperparameters.

        :param n_epochs: Number of epochs for training.
        :param lr_all: Learning rate for all parameters.
        :param reg_all: Regularization term for all parameters.
        """
        self.model = SVDpp(n_epochs=n_epochs, lr_all=lr_all, reg_all=reg_all)
        self.global_item_to_index = {}  # Global mapping for item IDs
        self.global_index_to_item = {}  # Reverse mapping
        self.next_item_index = 0  # Tracks the next available index

    def update_global_mappings(self, items):
        """
        Updates global item mappings with new items encountered during training.
        """
        for item in items:
            if item not in self.global_item_to_index:
                self.global_item_to_index[item] = self.next_item_index
                self.global_index_to_item[self.next_item_index] = item
                self.next_item_index += 1

    def encode_items(self, items):
        """
        Encodes item IDs using the global mapping.
        """
        return [self.global_item_to_index[item] for item in items]

    def decode_items(self, indices):
        """
        Decodes indices back to item IDs using the global mapping.
        """
        return [self.global_index_to_item[idx] for idx in indices]

    def obfuscate_user_id(self, user_id, client_key):
        """
          Obfuscates or encrypts a user ID into a unique string.

          Parameters:
          user_id (str): The user ID to obfuscate.
          client_key (str): A unique key for the client (serves as a salt).

          Returns:
          str: The obfuscated user ID as a unique string.
        """
        # Combine the user_id and client_key to create a unique input
        combined = f"{client_key}:{user_id}"

        # Use a cryptographic hash function (e.g., SHA-256) to generate a unique hash
        hash_object = hashlib.sha256(combined.encode('utf-8'))

        # Convert the hash to a hexadecimal string
        obfuscated_id = hash_object.hexdigest()

        return obfuscated_id

    def preprocess_data(self, data, user_col, item_col, rating_col, client_key, rating_scale=(1, 5), encrypt=False):
        """
        Preprocess the data to prepare it for training.

        :param csv_path: Path to the CSV file.
        :param user_col: Name of the user ID column.
        :param item_col: Name of the item ID column.
        :param rating_col: Name of the rating column.
        :return: Surprise Dataset object.
        """

        # Ensure required columns are present
        if not all(col in data.columns for col in [user_col, item_col, rating_col]):
            raise ValueError("CSV file must contain user, item, and rating columns.")

        # Rename columns for Surprise compatibility
        data = data[[user_col, item_col, rating_col]]
        data.columns = ['userID', 'itemID', 'rating']

        item_ids = data['itemID'].unique()
        self.update_global_mappings(item_ids)

        # Encode item IDs
        data['itemID'] = data['itemID'].map(self.global_item_to_index)
        if encrypt == True:
            data['userID'] = data['userID'].apply(lambda x: self.obfuscate_user_id(x, client_key))

        # Define the reader for Surprise
        reader = Reader(rating_scale=(data['rating'].min(), data['rating'].max()))

        # Load the data into Surprise format
        dataset = Dataset.load_from_df(data[['userID', 'itemID', 'rating']], reader)
        return dataset

    def train_model(self, csv_path, user_col, item_col, rating_col, rating_scale=(1, 5), client_key="unique_key",
                    encrypt=False):
        """
        Train the SVD++ model using the training set.

        :param dataset: Surprise Dataset object.
        """
        # Load the CSV file
        data = pd.read_csv(csv_path)
        data = data.dropna()

        # Preprocess data
        dataset = self.preprocess_data(data, user_col, item_col, rating_col, client_key, rating_scale, encrypt)

        # Split the dataset into training and test sets
        trainset, testset = train_test_split(dataset, test_size=0.2)

        # Train the model on the training set
        self.model.fit(trainset)

        # Store the test set for evaluation
        self.testset = testset

        return self.model

    def evaluate_model(self, trained_model=None):
        """
        Evaluate the trained model on the test set.

        :return: Dictionary of evaluation metrics.
        """
        if not hasattr(self, 'testset'):
            raise ValueError("Model must be trained before evaluation.")

        if trained_model is None:
            predictions = self.model.test(self.testset)

            # Calculate evaluation metrics
            metrics = {
                'RMSE': accuracy.rmse(predictions, verbose=False),
                'MAE': accuracy.mae(predictions, verbose=False)
            }
            return metrics
        else:
            predictions = trained_model.test(self.testset)

            # Calculate evaluation metrics
            metrics = {
                'RMSE': accuracy.rmse(predictions, verbose=False),
                'MAE': accuracy.mae(predictions, verbose=False)
            }
            return metrics

    def save_mappings(self, filepath):
        """
        Saves global mappings to a file for reuse.
        """
        pd.DataFrame({
            'item_id': list(self.global_item_to_index.keys()),
            'encoded_id': list(self.global_item_to_index.values())
        }).to_csv(filepath, index=False)

    def load_mappings(self, filepath):
        """
        Loads global mappings from a file.
        """
        mapping_df = pd.read_csv(filepath)
        self.global_item_to_index = dict(zip(mapping_df['item_id'], mapping_df['encoded_id']))
        self.global_index_to_item = {v: k for k, v in self.global_item_to_index.items()}
        self.next_item_index = max(self.global_item_to_index.values()) + 1
