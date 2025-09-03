# Praise's Fruit Nutrition Blog

A simple Flask web application that showcases fruit profiles, nutritional tips, and information about Praise Akinwole. The site features a searchable catalog of fruits, individual fruit detail pages, and an About page.

## Features

- **Home Page:**  
  Browse a catalog of fruits with images, botanical names, and short descriptions.  
  Search for fruits by name, botanical name, or description.

- **Fruit Profile Pages:**  
  View detailed information about each fruit, including harvest time, products, pests, medicinal uses, and more.

- **About Page:**  
  Learn about Praise Akinwole, the author. Contact information and social links are provided.  
  Optionally display a profile image by adding it to `static/uploads/` and setting the filename in the code.

- **Responsive Design:**  
  Uses Bootstrap for a clean, mobile-friendly layout.

## Setup

1. **Clone or Download the Repository**

2. **Create and Activate a Virtual Environment (Windows):**
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```

3. **Install Dependencies**
    ```powershell
    pip install flask
    ```

4. **Run the Application**
    ```powershell
    python fruit_website.py
    ```
    The site will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Customization

- **Add Your Profile Image:**  
  Place your image (e.g., `praise.jpg`) in `static/uploads/` and set the `ABOUT_IMAGE` variable near the top of `fruit_website.py`:
    ```python
    ABOUT_IMAGE = 'praise.jpg'
    ```

- **Add or Edit Fruits:**  
  Update the `FRUITS` list in `fruit_website.py` to add more fruits or edit existing ones.

## Project Structure

```
Fruit Website/
│
├── fruit_website.py
├── static/
│   └── uploads/
│        └── [your image files]
├── venv/
└── README.md
```

## Notes

- The search bar and navigation bar have a green background for a fresh, fruit-inspired look.
- The site is for demonstration and educational purposes. For production, consider using Flask templates in separate files and adding more robust error handling.

---

&copy; 2025 Praise Akinwole — Nutritional tips & fruit knowledge.
