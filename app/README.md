# House Search Website with Flask

This project is a complete implementation of a house search website using Flask. It provides basic functionality for listing properties, searching, and viewing details.

## Project Structure

```
house_search/
├── app.py                  # Main Flask application
├── templates/
│   ├── base.html           # Base template
│   ├── index.html          # Home page with search
│   ├── listings.html       # Property listings
│   └── property.html       # Single property view
├── static/
│   ├── css/
│   │   └── style.css       # CSS styles
│   └── images/            # Property images
└── README.md               # Project documentation
```

## Features

- Home page with a search form
- Property listing page with search results
- Detailed property view
- Responsive design that works on mobile and desktop
- SQLite database for storing property data
- Search functionality with filters (location, price range, bedrooms, property type)

## How to Run the Application

1. Create the project structure as shown above.
2. Save all the files in their respective directories.
3. Add some property images to `static/images/` (name them according to the sample data in `app.py`).
4. Install the required packages:
   ```
   pip install flask
   ```
5. Run the application:
   ```
   python app.py
   ```
6. Open your browser and visit `http://localhost:5000`.

## Future Enhancements

You can extend this basic implementation by adding features like:
- User authentication
- Favorite properties
- Property comparison
- Map integration
- Admin panel for adding/editing properties