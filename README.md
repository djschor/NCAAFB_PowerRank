# NCAA PowerScore

NCAA PowerScore is a Python project created by Daniel Schorin for analyzing and ranking NCAA college football quartback performance by using a number of new metrics that evaluate different areas than traditional measures. These metrics include: 
1. Adaptive Quarterback Score: The Adaptive Quarterback Score (AQS) is a composite metric that evaluates a quarterback's adaptability, timing, and proficiency in various game scenarios. It takes into account completion percentage, situational pass success rate, third-down conversion efficiency, and weighted throw variety, providing a comprehensive view of a quarterback's performance.
2. Quarterback Passing Index: The Quarterback Passing Index (QPI) measures a quarterback's passing performance by considering completion percentage, yards per attempt, touchdown ratio, and interception ratio. This index provides a balanced evaluation of a quarterback's ability to complete passes, gain yards, score touchdowns, and avoid interceptions.
3. Scramble Efficiency Index: The Scramble Efficiency Index (SEI) quantifies a quarterback's effectiveness in gaining yards during scramble plays. This metric is useful for evaluating a quarterback's ability to make plays with their legs and escape pressure when the pocket collapses.
4. Completion Rate Above Expected: The Completion Rate Above Expected (CRAE) measures the difference between a quarterback's actual completion rate and their expected completion rate based on the difficulty of attempted passes. This metric helps assess a quarterback's ability to exceed expectations and complete difficult passes.
5. Decision-making Index: The Decision-making Index (DMI) evaluates a quarterback's decision-making ability by considering completed passes, interceptions, sacks, and fumbles. This index is useful for understanding a quarterback's ability to make smart decisions under pressure and avoid costly mistakes.
6. Pocket Presence Index (PPI): This metric evaluates a quarterback's ability to make plays under pressure by considering sack avoidance, completion percentage under pressure, and yards per attempt under pressure. This metric helps assess a quarterback's ability to handle defensive pressure and make accurate throws.
7. Adjusted Deep Pass Success Rate (ADPSR): This metric evaluates a quarterback's performance on deep pass plays (20 yards or more) by taking into account touchdowns, interceptions, and the number of deep pass attempts. The formula is adjusted to prevent extreme values when the sample size is small.
8. Red Zone Efficiency Rating: The Red Zone Efficiency Rating (RZER) quantifies a quarterback's effectiveness in scoring touchdowns inside the red zone. This rating is useful for evaluating a quarterback's ability to capitalize on scoring opportunities and make critical plays near the end zone.
## Features

- Data collection from multiple APIs
- Data preprocessing and cleaning
- Exploratory data analysis
- Feature engineering
- Machine learning model training and evaluation
- Interactive visualizations

## Installation

1. Clone the repository:
git clone https://github.com/your-username/NCAA-PowerScore.git

2. Change into the project directory:
cd NCAA-PowerScore

3. Create a virtual environment:
python3 -m venv venv

4. Activate the virtual environment:
source venv/bin/activate # For Linux and macOS
.\venv\Scripts\activate # For Windows

5. Install the required dependencies:
pip install -r requirements.txt

## Usage

1. Collect and preprocess the data:

python data_collection.py
python data_preprocessing.py

2. Train and evaluate the machine learning models:

python model_training.py

3. Generate visualizations and reports:

python visualization.py

- 

## Contributing

If you would like to contribute to the project, please submit a pull request or open an issue for discussion.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [NCAA Football Data API](https://api.collegefootballdata.com/)
- [Pandas](https://pandas.pydata.org/)
- [Scikit-learn](https://scikit-learn.org/)
- [Matplotlib](https://matplotlib.org/)
- [The University of Michigan Football Team](https://mgoblue.com/sports/football)