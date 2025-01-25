# Route Finder with A* Algorithm
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Project Description

This project is a route finding application using the A* algorithm, specifically designed for João Pessoa, Paraíba, Brazil. The application provides a web interface to calculate routes between two locations using geographical data.

![Image](https://github.com/user-attachments/assets/cf9940f7-93aa-48e7-9b53-4b05c8b4bdd4)

## Project Structure

```
.
├── app.py                  # Streamlit web application
├── data/
│   ├── joao_pessoa_edges.csv   # Graph edges data
│   └── joao_pessoa_nodes.csv   # Nodes geographical data
├── generate_csvs_script.py # Script to generate CSV files
├── README.MD               # Project documentation
├── requirements.txt        # Python dependencies
└── src/
    ├── api.py              # FastAPI route calculation endpoint
    ├── AStar.py            # A* algorithm implementation
    └── __init__.py         # Package initialization
```

## Prerequisites

- Python 3.8+
- pip

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### API Only
To run only the FastAPI server:
```bash
uvicorn src:app --reload
```

### Web Application
To run the full Streamlit web app:
```bash
streamlit run app.py
```

## Key Features

- Uses A* pathfinding algorithm
- Geocoding with OSMnx
- Interactive map visualization
- Supports locations in João Pessoa, Brazil

## Technologies Used

- FastAPI
- Streamlit
- OSMnx
- Folium
- Haversine distance calculation

## Limitations

- Currently supports only João Pessoa locations
- Does not consider street orientation
- Relies on network graph within 100m of start/end points

## Algorithm Details

The A* algorithm is implemented using:
- Haversine distance as the heuristic function
- Graph representation of city network
- Efficient path finding with minimal computational complexity

## License

This project is licensed under the [MIT License](LICENSE).