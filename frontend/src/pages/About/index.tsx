
import React from 'react';
import './About.css';

const About: React.FC = () => {
  return (
    <div className="about-container">
      <h1 className="about-title">NCAA PowerScore</h1>
      <p className="about-description">
        NCAA PowerScore is a Python project created by <a href="https://www.linkedin.com/in/daniel-schorin-85a626b1/" className="highlight-link">Daniel Schorin</a>  for
        analyzing and ranking NCAA college football quartback performance by
        using a number of new metrics that evaluate different areas than
        traditional measures. These metrics include:
      </p>
      <ol className="about-metrics">
        <li>
          <strong>Adaptive Quarterback Score:</strong> The Adaptive Quarterback
          Score (AQS) is a composite metric that evaluates a quarterback's
          adaptability, timing, and proficiency in various game scenarios. It
          takes into account completion percentage, situational pass success
          rate, third-down conversion efficiency, and weighted throw variety,
          providing a comprehensive view of a quarterback's performance.
        </li>
        <li>
          <strong>Quarterback Passing Index:</strong> The Quarterback Passing Index (QPI) measures a quarterback's passing performance by considering completion percentage, yards per attempt, touchdown ratio, and interception ratio. This index provides a balanced evaluation of a quarterback's ability to complete passes, gain yards, score touchdowns, and avoid interceptions.
        </li>
        <li>
          <strong>Scramble Efficiency Index:</strong> The Scramble Efficiency Index (SEI) quantifies a quarterback's effectiveness in gaining yards during scramble plays. This metric is useful for evaluating a quarterback's ability to make plays with their legs and escape pressure when the pocket collapses.
        </li>
        <li>
          <strong>Completion Rate Above Expected:</strong> The Completion Rate Above Expected (CRAE) measures the difference between a quarterback's actual completion rate and their expected completion rate based on the difficulty of attempted passes. This metric helps assess a quarterback's ability to exceed expectations and complete difficult passes.
        </li>
        <li>
          <strong>Decision-making Index:</strong> Decision-making Index (DMI) evaluates a quarterback's decision-making ability by considering completed passes, interceptions, sacks, and fumbles. This index is useful for understanding a quarterback's ability to make smart decisions under pressure and avoid costly mistakes.
        </li>
        <li>
          <strong>Pocket Presence Index:</strong> The Pocket Presence Index (PPI) evaluates a quarterback's ability to make plays under pressure by considering sack avoidance, completion percentage under pressure, and yards per attempt under pressure. This metric helps assess a quarterback's ability to handle defensive pressure and make accurate throws.
        </li>
        <li>
          <strong>Adjusted Deep Pass Success Rate (ADPSR):</strong> This metric evaluates a quarterback's performance on deep pass plays (20 yards or more) by taking into account touchdowns, interceptions, and the number of deep pass attempts. The formula is adjusted to prevent extreme values when the sample size is small.
        </li>
        <li>
          <strong> Red Zone Efficiency Rating:</strong> The Red Zone Efficiency Rating (RZER) quantifies a quarterback's effectiveness in scoring touchdowns inside the red zone. This rating is useful for evaluating a quarterback's ability to capitalize on scoring opportunities and make critical plays near the end zone.
        </li>
      </ol>
      <footer className="about-footer">
        If you have any questions, critiques, or business inquiries, please contact me at <a href="mailto:djschor@umich.edu">djschor@umich.edu</a>.
        </footer>

    </div>
  );
};

export default About;
