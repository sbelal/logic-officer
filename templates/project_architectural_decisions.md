# ⚙️ Project-Specific Decisions

This document lists the concrete, actionable rules and conventions for this project. The goal is to provide a single source of truth for implementation details, ensuring consistency across the codebase.

---

### Decision: Custom Exception Location

* **Reason:** Centralizes error handling within each app for better organization and discoverability.
* **Example:** For a `payments` app, a `PaymentError` exception must be located at `payments/exceptions.py`.
    ```python
    # payments/exceptions.py
    class PaymentError(Exception):
        """Base exception for payment processing errors."""
        pass

    class InsufficientFundsError(PaymentError):
        """Raised when a payment fails due to insufficient funds."""
        pass
    ```

---

### Decision: API URL Structure

* **Reason:** To maintain a consistent, predictable, and versioned API endpoint structure across the project.
* **Example:** All API URLs must be prefixed with `/api/v1/`. The URL should use plural nouns for resource names.
    ```python
    # project/urls.py
    from django.urls import path, include

    urlpatterns = [
        # ... other urls
        path('api/v1/', include('products.urls')),
        path('api/v1/', include('orders.urls')),
    ]

    # products/urls.py
    from django.urls import path
    from .views import ProductListCreateView

    urlpatterns = [
        path('products/', ProductListCreateView.as_view(), name='product-list'),
    ]
    ```

---

### Decision: Standardized Logger Names

* **Reason:** Provides a consistent and traceable logging structure, making it easier to debug issues by identifying the source of a log message.
* **Example:** Loggers should be named using Python's `__name__` convention, which resolves to the app and module path.
    ```python
    # any_app/services.py
    import logging

    logger = logging.getLogger(__name__)

    def some_function():
        logger.info("This is an informational message from any_app.services.")
        try:
            # ... some operation
        except Exception as e:
            logger.error("An error occurred: %s", e, exc_info=True)
    ```

---