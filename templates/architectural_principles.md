# 🏛️ Architectural Guiding Principles

This document outlines the high-level architectural principles for this project. The goal is to ensure consistency, maintainability, and scalability in our codebase. All new code should adhere to these guidelines.

---

### Principle: Service-Oriented Architecture (SOA)

* **Rationale:** To decouple business logic from the presentation layer (views). This keeps views "thin," improves code reusability, and simplifies testing of business logic in isolation from HTTP concerns.
* **Implications:**
    * Business logic **must not** reside in `views.py` or DRF `ViewSets`.
    * Create service classes within `/services` folder in a relevant app (e.g., in `apps/my_app/services/my_services.py`) to encapsulate business operations.
    * Views are responsible only for handling HTTP requests/responses, data serialization, and calling the appropriate services.

---

### Principle: Fat Models, Thin Views

* **Rationale:** To centralize data-related logic within the Django models. This ensures data integrity, promotes DRY (Don't Repeat Yourself), and keeps business rules close to the data they affect.
* **Implications:**
    * Use model methods and properties for derived fields or data-related actions (e.g., `order.calculate_total()`, `user.is_active()`).
    * Use the `QuerySet` manager (`objects`) to create custom reusable queries (e.g., `Product.objects.available()`).
    * Views and services should call these model/manager methods directly rather than reimplementing the logic.

---

### Principle: Configuration via Environment Variables

* **Rationale:** To follow the [Twelve-Factor App](https://12factor.net/config) methodology, which separates configuration from code. This enhances security by keeping secrets out of the codebase and improves portability between environments (development, staging, production).
* **Implications:**
    * **Do not** hardcode sensitive values like API keys, database passwords, or `SECRET_KEY` in `settings.py`.
    * All configuration variables must be loaded from environment variables.
    * Use a `.env` file for local development, and ensure `.env` is listed in `.gitignore`.

---

### Principle: Explicit is Better than Implicit

* **Rationale:** Aligns with the Zen of Python. Code should be clear, readable, and unambiguous. This reduces the cognitive load for developers and minimizes bugs caused by misunderstanding "magical" behavior.
* **Implications:**
    * Avoid overly complex metaprogramming or Django signals where a direct function call would be clearer.
    * Name variables and functions descriptively (e.g., `is_eligible_for_discount` is better than `check_eligibility`).
    * When using Django Rest Framework, explicitly define serializer fields (`fields = ['id', 'name']`) instead of relying on `fields = '__all__'` to avoid accidentally exposing sensitive data.

---