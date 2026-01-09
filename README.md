This project is a task management and self-analysis application developed using PyQt5. Its main goal is to allow users to easily add, edit, and delete tasks, while also analyzing productivity and mood patterns.

The application features a simple and user-friendly interface where users can add tasks, write descriptions, select specific dates, choose their mood, and assign a productivity score. All data is stored in an SQLite database, ensuring that information is persistent and always accessible.

Database operations are handled through a dedicated Database class, which contains all CRUD operations (Create, Read, Update, Delete). These methods are used in the main UI, which is built with PyQt components such as QTableWidget, QPushButton, QLineEdit, and others.

One of the most valuable features of the application is the Statistics tab, which visually displays productivity and mood data using Matplotlib. A bar chart shows which moods are associated with higher productivity, a line chart tracks productivity trends over time, and a pie chart highlights the most frequent moods in the user’s records.

Beyond its technical implementation, the application is designed to provide real value by helping users understand their working patterns. It allows users to identify their most productive days, recognize which moods increase motivation, and understand when rest or change is needed.

From a code structure perspective, the project follows object-oriented design principles and is organized into separate modules:
MainWindow.py handles the UI and application logic, database.py manages data storage, and charts.py is responsible for data visualization.

In summary, this application serves as a personal organization and self-reflection tool that uses technology to help users become more productive and focused.
