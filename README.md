# Delivery Analysis Project
This project is focused on analyzing delivery data to uncover insights into various aspects of the delivery process, including order volume, delivery times, and factors affecting delivery efficiency. The project uses data from a delivery service and aims to provide valuable insights for business, delivery personnel, and restaurants.

## Objective
The main objective of this project is to perform exploratory data analysis (EDA) on delivery data to gain insights into:

* Business operations such as order volume and distribution.
* Delivery personnel performance and conditions.
* Restaurant delivery metrics.

## Key Insights
### Order Volume and Distribution

* The number of orders per day and week.
* Distribution of orders by traffic conditions.
* Comparison of order volume by city and traffic conditions.
   
### Delivery Personnel Analysis

* The age range of delivery personnel.
* Vehicle condition ratings.
* Average ratings per delivery person and by traffic conditions.
* Identification of the fastest and slowest delivery personnel by city.

### Restaurant Delivery Metrics

* The number of unique delivery people.
* Average distance between restaurants and delivery locations.
* Average delivery time by city, type of order, and traffic conditions.
* Impact of festivals on delivery time.

## Data Cleaning
The data was cleaned and preprocessed to ensure accurate analysis. The steps included:

* Converting column names to lowercase.
* Handling missing values and data type conversions.
* Removing extra spaces from object features.
   
## Exploratory Data Analysis (EDA)
**1. Business Insights**

* Quantity Orders Per Day
Visualized the number of orders per day using a bar chart.

* Quantity Orders Per Week
Visualized the number of orders per week using a line chart.

* Orders Distribution Per Traffic
Visualized the distribution of orders by traffic conditions using a pie chart.

* Comparison of Order Volume by City and Traffic
Compared order volumes by city and traffic conditions using a scatter plot.

* Deliveries Quantity by Delivery Person Per Week
Analyzed the number of deliveries per delivery person per week using a line chart.

* Central Localization of Each City by Traffic
Visualized the central locations of deliveries in each city by traffic conditions using a Folium map.

**2. Delivery Person Insights**

* Age of Delivery Personnel
Identified the youngest and oldest delivery personnel.

* Vehicle Condition
Determined the best and worst vehicle conditions.

* Average Rating Per Delivery Person
Calculated the average rating for each delivery person.

* Ratings by Traffic Type
Analyzed the average rating and standard deviation by traffic conditions.

* Ratings by Climatic Conditions
Analyzed the average rating and standard deviation by weather conditions.

* Top 10 Fastest Delivery Persons by City
Identified the top 10 fastest delivery persons in each city.

* Top 10 Slowest Delivery Persons by City
Identified the top 10 slowest delivery persons in each city.

**3. Restaurant Insights**

* Number of Unique Delivery People
Calculated the number of unique delivery personnel.

* Average Distance to Restaurants and Delivery Locations
Calculated the average distance between restaurants and delivery locations.

* Delivery Time by City
Analyzed the average delivery time and standard deviation by city.

* Delivery Time by City and Type of Order
Analyzed the average delivery time and standard deviation by city and type of order.

* Delivery Time by City and Traffic Type
Analyzed the average delivery time and standard deviation by city and traffic conditions.

* Delivery Time During Festivals
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
