import numpy as np

class OlevesterTransform:
    def __init__(self):
        pass

    @staticmethod
    def normalize_field(field, axis=None):
        """
        Normalize a multidimensional field to preserve energy/amplitude stability, optionally along specific axes.
        
        Args:
            field (np.ndarray): Input field array.
            axis (int or tuple, optional): Axis or axes along which to normalize. Defaults to None (global normalization).
        
        Returns:
            np.ndarray: Normalized field array.
        """
        norm = np.sqrt(np.sum(np.abs(field)**2, axis=axis, keepdims=True))
        norm[norm == 0] = 1  # Avoid division by zero
        return field / norm


    @staticmethod
    def dimensional_expand(field, target_dims):
        """
        Expand a field into a higher-dimensional space by extrapolating.

        Args:
            field (np.ndarray): Input field array.
            target_dims (tuple): Target dimensional shape.

        Returns:
            np.ndarray: Expanded field array.
        """
        current_dims = field.shape
        if len(current_dims) > len(target_dims):
            raise ValueError("Target dimensions must be higher than current dimensions.")
        
        expanded_field = np.zeros(target_dims)
        slices = tuple(slice(0, s) for s in current_dims)
        expanded_field[slices] = field
        return expanded_field


    @staticmethod
    def dimensional_reduce(field, target_dims):
        """
        Reduce a field into a lower-dimensional space by averaging.

        Args:
            field (np.ndarray): Input field array.
            target_dims (tuple): Target dimensional shape.

        Returns:
            np.ndarray: Reduced field array.
        """
        current_dims = field.shape
        if len(current_dims) < len(target_dims):
            raise ValueError("Target dimensions must be lower than current dimensions.")        

        # If target_dims is (1,), collapse all dimensions
        if target_dims == (1,):
            return np.array([np.mean(field)])

        # Otherwise, reduce axes until target shape is achieved
        while len(field.shape) > len(target_dims):
            field = np.mean(field, axis=0, keepdims=False)

        return field


    @staticmethod
    def normalize_fourier_coefficients(A, B, weights=None):
        """
        Normalize Fourier coefficients across dimensions.
        
        Args:
            A (np.ndarray): Fourier coefficients (cosine).
            B (np.ndarray): Fourier coefficients (sine).
            weights (np.ndarray): Optional weight array for dimensions.

        Returns:
            tuple: Normalized coefficients (A_normalized, B_normalized).
        """
        norm_A = np.sqrt(np.sum(A**2, axis=0))
        norm_B = np.sqrt(np.sum(B**2, axis=0))

        if weights is None:
            weights = np.ones(A.shape[0])

        A_normalized = (A / norm_A) * weights[:, None]
        B_normalized = (B / norm_B) * weights[:, None]

        return A_normalized, B_normalized

    @staticmethod
    def analyze_dimension_contributions(A_normalized, B_normalized):
        """
        Analyze contributions from different dimensions.

        Args:
            A_normalized (np.ndarray): Normalized cosine coefficients.
            B_normalized (np.ndarray): Normalized sine coefficients.

        Returns:
            np.ndarray: Dimensional similarity matrix.
        """
        num_dims = A_normalized.shape[0]
        similarity_matrix = np.zeros((num_dims, num_dims))

        for i in range(num_dims):
            for j in range(num_dims):
                similarity_matrix[i, j] = (
                    np.dot(A_normalized[i], A_normalized[j])
                    + np.dot(B_normalized[i], B_normalized[j])
                ) / (
                    np.sqrt(np.sum(A_normalized[i]**2 + B_normalized[i]**2))
                    * np.sqrt(np.sum(A_normalized[j]**2 + B_normalized[j]**2))
                )

        return similarity_matrix
