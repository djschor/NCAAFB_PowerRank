# NCAA PowerRank

NCAA PowerRank is a Python project for analyzing and ranking NCAA college football quartback performance by using a number of new metrics that evaluate different areas than traditional measures. These metrics include: 
1. Decision-making index (DMI): A comprehensive evaluation of a quarterback's decision-making ability that considers completed passes, interceptions, sacks, and fumbles.
2. Scramble efficiency index (SEI): A measure of a quarterback's efficiency when scrambling and improvising outside the pocket.
3. Completion Rate Above Expected (CRAE): A metric that compares a quarterback's actual completion rate to their expected completion rate based on the difficulty of the passes they attempt.
4. Time to Throw (TTT): A metric that measures the average amount of time a quarterback holds onto the ball before releasing it.
5. Big play ratio (BPR): A measure of a quarterback's ability to make big plays defined as passes that gain 20 or more yards.
6. Touchdown to Interception Ratio on Deep Passes (TID) - measures a quarterback's success throwing deep passes by comparing the number of touchdowns to interceptions on throws over 20 yards.
7. Red Zone Efficiency Rating (RZER): A metric that evaluates a quarterback's performance inside the red zone.

## Features

- Data collection from multiple APIs
- Data preprocessing and cleaning
- Exploratory data analysis
- Feature engineering
- Machine learning model training and evaluation
- Interactive visualizations

## Installation

1. Clone the repository:
git clone https://github.com/your-username/NCAA-PowerRank.git

2. Change into the project directory:
cd NCAA-PowerRank

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