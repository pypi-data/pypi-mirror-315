import requests
import pickle
import os
import base64
import numpy as np

class ModelUploader:
    def __init__(self, api_key):
        self.api_key = api_key
        self.server_url = "https://viturka.com/upload_model"

    def pad_to_match_shape(self, model1_weights, model2_weights):
        """Pad the smaller array with zeros to match the size of the larger one."""
        if len(model1_weights) > len(model2_weights):
            padded_model2 = np.pad(model2_weights, (0, len(model1_weights) - len(model2_weights)), 'constant')
            return model1_weights, padded_model2
        elif len(model2_weights) > len(model1_weights):
            padded_model1 = np.pad(model1_weights, (0, len(model2_weights) - len(model1_weights)), 'constant')
            return padded_model1, model2_weights
        else:
            return model1_weights, model2_weights

    def aggregate_internal_parameters(self, local_model, global_model):
        """
        Aggregates the internals of the SVD++ model, such as user and item embeddings,
        biases, and latent factors.
        """
        # Aggregate user embeddings (pu)
        for user_id in local_model.pu:
            if user_id in global_model.pu:
                local_model.pu[user_id] = self.aggregate_vector(
                    local_model.pu[user_id], global_model.pu[user_id]
                )

        # Aggregate item embeddings (qi)
        for item_id in local_model.qi:
            if item_id in global_model.qi:
                local_model.qi[item_id] = self.aggregate_vector(
                    local_model.qi[item_id], global_model.qi[item_id]
                )

        # Aggregate user biases (bu)
        for user_id in local_model.bu:
            if user_id in global_model.bu:
                local_model.bu[user_id] = self.aggregate_scalar(
                    local_model.bu[user_id], global_model.bu[user_id]
                )

        # Aggregate item biases (bi)
        for item_id in local_model.bi:
            if item_id in global_model.bi:
                local_model.bi[item_id] = self.aggregate_scalar(
                    local_model.bi[item_id], global_model.bi[item_id]
                )

        # Aggregate item interaction factors (y factors)
        max_items = max(len(local_model.y), len(global_model.y))
        local_model.y = self.aggregate_matrices(local_model.y, global_model.y, max_items)

        print("Aggregation of model internals complete.")

    def aggregate_vector(self, local_vec, global_vec):
        """
        Aggregates two vectors, ensuring padded 0s are replaced with the non-zero
        values from the other vector, and averaging where both have actual values.
        """
        aggregated_vec = []
        for local_val, global_val in zip(local_vec, global_vec):
            if local_val != 0 and global_val != 0:
                aggregated_vec.append((local_val + global_val) / 2)
            elif local_val == 0:
                aggregated_vec.append(global_val)  # Use global value if local is 0
            else:
                aggregated_vec.append(local_val)  # Use local value if global is 0
        return aggregated_vec

    def aggregate_scalar(self, local_val, global_val):
        """
        Aggregates two scalar values, ensuring padded 0s are replaced with the
        non-zero value from the other scalar, and averaging where both have actual values.
        """
        if local_val != 0 and global_val != 0:
            return (local_val + global_val) / 2
        elif local_val == 0:
            return global_val  # Use global value if local is 0
        else:
            return local_val  # Use local value if global is 0

    def aggregate_matrices(self, local_matrix, global_matrix, max_dim):
        """
        Pads and aggregates two matrices (e.g., latent factors) to align their shapes,
        ensuring that padded 0s are replaced with non-zero values from the other matrix,
        and averaging where both have actual values.
        """
        local_padded = np.pad(
            local_matrix,
            ((0, max_dim - local_matrix.shape[0]), (0, max_dim - local_matrix.shape[1])),
            'constant'
        )
        global_padded = np.pad(
            global_matrix,
            ((0, max_dim - global_matrix.shape[0]), (0, max_dim - global_matrix.shape[1])),
            'constant'
        )

        aggregated_matrix = np.zeros_like(local_padded)
        for i in range(local_padded.shape[0]):
            for j in range(local_padded.shape[1]):
                local_val = local_padded[i, j]
                global_val = global_padded[i, j]

                if local_val != 0 and global_val != 0:
                    aggregated_matrix[i, j] = (local_val + global_val) / 2
                elif local_val == 0:
                    aggregated_matrix[i, j] = global_val  # Use global value if local is 0
                else:
                    aggregated_matrix[i, j] = local_val  # Use local value if global is 0

        return aggregated_matrix

    def upload_model(self, model, model_type, vectorizer=None, mappings=None):
        """
        Uploads the model to the server and performs aggregation.
        Includes support for both SVD and SVD++ models based on the presence of model.w_.
        """
        # Serialize the local model
        model_data = pickle.dumps(model)
        v_data = pickle.dumps(vectorizer) if vectorizer else None

        # Send the model to the server and receive the global model
        # Prepare the files dictionary
        files = {
            'model': ('model.pkl', model_data, 'application/octet-stream'),
            'vectorizer': (
                f'{model_type}_vectorizer.pkl', v_data, 'application/octet-stream') if vectorizer else None,
        }

        # Add CSV file to the payload if it exists
        if mappings and os.path.exists(mappings):
            files['mapping'] = ('data.csv', open(mappings, 'rb'), 'text/csv')
            response = requests.post(
                f'{self.server_url}',
                files=files,
                data={'api_key': self.api_key, 'model_type': model_type}
            )
        else:
            response = requests.post(
                f'{self.server_url}',
                files=files,
                data={'api_key': self.api_key, 'model_type': model_type}
            )
        if response.status_code == 200:
            # Deserialize the received global model
            data = response.json()
            if data['model'] == 200:
                global_model = model
            else:
                pickled_model = base64.b64decode(data['model'])  # Decode base64
                global_model = pickle.loads(pickled_model)  # Unpickle the global model

            if hasattr(model, 'w_') and hasattr(global_model, 'w_'):
                # Model is SVD, proceed with the existing logic

                # Pad w_ for matching shape
                model.w_, global_model.w_ = self.pad_to_match_shape(model.w_, global_model.w_)

                # Update w_ (Linear Coefficients)
                for i in range(len(model.w_)):
                    if global_model.w_[i] != 0 and model.w_[i] != 0:
                        model.w_[i] = (model.w_[i] + global_model.w_[i]) / 2  # Average for shared features
                    else:
                        model.w_[i] += global_model.w_[i]  # Directly add non-shared features

                # Align V_ matrices and aggregate
                max_rows = max(model.V_.shape[0], global_model.V_.shape[0])
                max_cols = max(model.V_.shape[1], global_model.V_.shape[1])

                padded_model_V = np.pad(
                    model.V_, ((0, max_rows - model.V_.shape[0]), (0, max_cols - model.V_.shape[1])), 'constant'
                )
                padded_global_V = np.pad(
                    global_model.V_,
                    ((0, max_rows - global_model.V_.shape[0]), (0, max_cols - global_model.V_.shape[1])), 'constant'
                )

                # Update V_ (Latent Factor Matrix)
                for row in range(padded_model_V.shape[0]):
                    for col in range(padded_model_V.shape[1]):
                        if padded_model_V[row, col] != 0 and padded_global_V[row, col] != 0:
                            padded_model_V[row, col] = (padded_model_V[row, col] + padded_global_V[row, col]) / 2
                        else:
                            padded_model_V[row, col] += padded_global_V[row, col]

                model.V_ = padded_model_V

                # Aggregate bias term w0_
                model.w0_ = (model.w0_ + global_model.w0_) / 2

            elif hasattr(model, 'pu') and hasattr(global_model, 'pu'):
                # Model is SVD++, proceed with SVD++ aggregation


                # Aggregate user embeddings (pu)
                for user_id in model.pu:
                    if user_id in global_model.pu:
                        model.pu[user_id] = self.aggregate_vector(
                            model.pu[user_id], global_model.pu[user_id]
                        )

                # Aggregate item embeddings (qi)
                for item_id in model.qi:
                    if item_id in global_model.qi:
                        model.qi[item_id] = self.aggregate_vector(
                            model.qi[item_id], global_model.qi[item_id]
                        )

                # Aggregate user biases (bu)
                for user_id in model.bu:
                    if user_id in global_model.bu:
                        model.bu[user_id] = self.aggregate_scalar(
                            model.bu[user_id], global_model.bu[user_id]
                        )

                # Aggregate item biases (bi)
                for item_id in model.bi:
                    if item_id in global_model.bi:
                        model.bi[item_id] = self.aggregate_scalar(
                            model.bi[item_id], global_model.bi[item_id]
                        )

                # Aggregate item interaction factors (y factors)
                max_items = max(len(model.y), len(global_model.y))
                model.y = self.aggregate_matrices(model.y, global_model.y, max_items)

            else:
                raise ValueError("Model type not recognized or lacks required internals for aggregation.")

            print("Model uploaded and aggregated successfully.")
        else:
            print(f"Failed to upload model: {response.content.decode()}")

        return model



