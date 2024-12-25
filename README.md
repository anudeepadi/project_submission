### Monarch Butterfly Population Decline Prediction

This summary outlines the key details, approach, and findings of the project aimed at predicting monarch butterfly sightings and analyzing the contributing factors to their population decline. This project was part of the **2024 Rowdy Datathon**, and the focus was to use machine learning and deep learning models to study population trends and factors affecting monarch butterflies.

---

## 1. **Problem Statement**
The project aims to respond to a hypothetical global crisis involving a drastic decline in monarch butterfly populations. Monarch butterflies are crucial pollinators, and their decline has far-reaching implications for biodiversity, agriculture, and human well-being. The task was to:
- Analyze fluctuations in monarch butterfly populations.
- Investigate contributing factors, such as climate change and pesticide use.
- Propose resource allocation strategies to mitigate population decline.
- Perform a focused analysis of migration patterns, particularly through Texas.

This project analyzes the **Monarch Butterfly Population Decline** and aims to provide actionable insights into the causes and potential remedies.

---

## 2. **Data Description**
The data sources included:
- Monarch butterfly migration data from **Journey North**.
- Environmental and air quality data from **EPA AQS**.
- Pesticide data from the **USDA Pesticide Data Program**.
- Various additional datasets related to climate, geography, and crop production.

The dataset faced issues with missing values, particularly in the `Year`, `Month`, `Day`, and `Latitude` columns, which were addressed through data imputation and cleaning techniques.

---

## 3. **Challenges Faced**
### 3.1. Missing Data
- **Year, Month, Day, Latitude**: A significant portion of the data contained missing values.
  - Solution: Missing values were either imputed using the median or dropped to maintain data integrity.
  
### 3.2. Overfitting and Model Complexity
- Initial models showed extremely low loss values, indicating overfitting.
  - Solution: Model complexity was reduced, and regularization techniques such as dropout and L2 regularization were applied.
  - Early stopping was also introduced to prevent the model from overtraining.

### 3.3. Numerical Instabilities
- During training, the model produced `NaN` losses due to issues in data preprocessing and model configuration.
  - Solution: The learning rate was reduced, and gradient clipping was applied to stabilize the training process.

---

## 4. **Modeling Process**

### Step 1: **Preprocessing**
- **Date Handling**: The `Date` column was split into `Year`, `Month`, and `Day` components.
- **Missing Value Handling**: Missing values in the `Year`, `Month`, `Day`, and `Latitude` fields were imputed with the median values or dropped if necessary.
- **Normalization**: All features and the target variable were scaled using MinMaxScaler for improved model performance.

### Step 2: **Model Selection**
- A **hybrid deep learning model** combining **LSTM** (for temporal data) and **CNN** (for spatial data) was used to capture both time-based and location-based dependencies.
- **LSTM** was used for `Year`, `Month`, and `Day` features to capture sequential dependencies.
- **CNN** was used for `Latitude` and `Longitude` to capture spatial relationships.

### Step 3: **Regularization and Optimization**
- **Dropout** was applied to prevent overfitting.
- **L2 regularization** was added to dense layers to control large weight values.
- **Batch Normalization** was introduced to stabilize the training process.
- The **Adam optimizer** was used with a learning rate of `0.00001` and **gradient clipping** to prevent exploding gradients.

### Step 4: **Training and Validation**
- The model was trained over 50 epochs with early stopping applied based on the validation loss.
- Both training and validation loss were monitored to ensure that the model generalized well and did not overfit.

---

## 5. **Key Findings**
- **Population Decline**: There are clear signs of a significant decline in monarch butterfly populations, particularly correlated with pesticide usage and air quality metrics.
- **Temporal Analysis**: The LSTM model was able to capture seasonal patterns in butterfly sightings, highlighting critical migration periods.
- **Geospatial Analysis**: The CNN model successfully identified critical regions for monarch butterfly populations, particularly in Texas and other states.

---

## 6. **Next Steps**
- **Further Feature Engineering**: Investigating additional features such as temperature, land use, and rainfall patterns to improve the model’s accuracy.
- **Fourier Transform for Temporal Data**: Investigating the use of Fourier Transforms to capture cyclical patterns in the temporal data (e.g., migration patterns over seasons).
- **Model Expansion**: Extending the model to include other pollinators and investigating broader ecological impacts.

---

## 7. **Results**
The model provided accurate predictions of monarch butterfly sightings and offered insights into the major contributing factors to their population decline, such as pesticide use and air quality changes. The analysis also identified critical regions and migration periods that need urgent attention for conservation efforts.

---

## 8. **GitHub Repository**
- All source code, data cleaning scripts, and modeling approaches are available in the GitHub repository.
- Follow the instructions in the repository's README file to replicate the results and understand the methodology.
  
**GitHub Repository Link**: [Add link to your repository]

---

## 9. **References**
- **Rowdy Datathon 2024** Data Challenge PDF ([2024DataChallenge.pdf](50)).
- **DevPost Workshop** Guide on project submissions and presentations ([DevPost Workshop](51)).
