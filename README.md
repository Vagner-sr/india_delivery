# Delivery Analysis Project
This project is focused on analyzing delivery data to uncover insights into various aspects of the delivery process, including order volume, delivery times, and factors affecting delivery efficiency. The project uses data from a delivery service and aims to provide valuable insights for business, delivery personnel, and restaurants.

## Objective
The main objective of this project is to perform exploratory data analysis (EDA) on delivery data to gain insights into:

1. Business operations such as order volume and distribution.
2. Delivery personnel performance and conditions.
3. Restaurant delivery metrics.

## Key Insights
### Order Volume and Distribution

1. The number of orders per day and week.
2. Distribution of orders by traffic conditions.
3. Comparison of order volume by city and traffic conditions.
   
### Delivery Personnel Analysis

1. The age range of delivery personnel.
2. Vehicle condition ratings.
3. Average ratings per delivery person and by traffic conditions.
4. Identification of the fastest and slowest delivery personnel by city.

### Restaurant Delivery Metrics

1. The number of unique delivery people.
2. Average distance between restaurants and delivery locations.
3. Average delivery time by city, type of order, and traffic conditions.
4. Impact of festivals on delivery time.

## Data Cleaning
The data was cleaned and preprocessed to ensure accurate analysis. The steps included:

1. Converting column names to lowercase.
2. Handling missing values and data type conversions.
3. Removing extra spaces from object features.
   
## Exploratory Data Analysis (EDA)
1. Business Insights
1.1 Quantity Orders Per Day
Visualized the number of orders per day using a bar chart.

1.2 Quantity Orders Per Week
Visualized the number of orders per week using a line chart.

1.3 Orders Distribution Per Traffic
Visualized the distribution of orders by traffic conditions using a pie chart.

1.4 Comparison of Order Volume by City and Traffic
Compared order volumes by city and traffic conditions using a scatter plot.

1.5 Deliveries Quantity by Delivery Person Per Week
Analyzed the number of deliveries per delivery person per week using a line chart.

1.6 Central Localization of Each City by Traffic
Visualized the central locations of deliveries in each city by traffic conditions using a Folium map.

2. Delivery Person Insights
2.1 Age of Delivery Personnel
Identified the youngest and oldest delivery personnel.

2.2 Vehicle Condition
Determined the best and worst vehicle conditions.

2.3 Average Rating Per Delivery Person
Calculated the average rating for each delivery person.

2.4 Ratings by Traffic Type
Analyzed the average rating and standard deviation by traffic conditions.

2.5 Ratings by Climatic Conditions
Analyzed the average rating and standard deviation by weather conditions.

2.6 Top 10 Fastest Delivery Persons by City
Identified the top 10 fastest delivery persons in each city.

2.7 Top 10 Slowest Delivery Persons by City
Identified the top 10 slowest delivery persons in each city.

3. Restaurant Insights
3.1 Number of Unique Delivery People
Calculated the number of unique delivery personnel.

3.2 Average Distance to Restaurants and Delivery Locations
Calculated the average distance between restaurants and delivery locations.

3.3 Delivery Time by City
Analyzed the average delivery time and standard deviation by city.

3.4 Delivery Time by City and Type of Order
Analyzed the average delivery time and standard deviation by city and type of order.

3.5 Delivery Time by City and Traffic Type
Analyzed the average delivery time and standard deviation by city and traffic conditions.

3.6 Delivery Time During Festivals
Compared delivery times during festivals and non-festivals.

## Conclusion
The analysis provided a comprehensive view of delivery operations, highlighting key areas for improvement and efficiency. The insights can be used by business owners, delivery personnel, and restaurants to optimize their processes and enhance customer satisfaction.

## Technologies Used
Python for data processing and analysis.
Pandas and NumPy for data manipulation.
Seaborn, Plotly Express, and Plotly Graph Objects for data visualization.
Folium for mapping.
Haversine for calculating distances.
Getting Started
To run this project, follow these steps:

Clone the repository.
Install the required packages using pip install -r requirements.txt.
Run the notebook to see the analysis and visualizations.
Acknowledgements
This project was developed as part of a data analysis exercise. Special thanks to the data providers and the open-source community for their invaluable tools and libraries.
