"""
HTML Report Generator for Better Data Visualization
Creates formatted HTML reports for gameplan and scouting data
"""

import json
import pandas as pd
from datetime import datetime
import os


class HTMLReportGenerator:
    """Generates formatted HTML reports for MFN analysis"""
    
    def __init__(self, output_dir=None):
        self.output_dir = output_dir or "/Users/jamesjones/personal/game_logs/reports"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.css_styles = """
        <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 20px; 
            background-color: #f5f5f5; 
        }
        .header { 
            background-color: #2c3e50; 
            color: white; 
            padding: 20px; 
            border-radius: 8px; 
            margin-bottom: 20px;
        }
        .section { 
            background-color: white; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 8px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .personnel-section {
            border-left: 4px solid #3498db;
            margin: 15px 0;
        }
        .play-recommendation {
            background-color: #e8f5e8;
            padding: 10px;
            margin: 5px 0;
            border-radius: 4px;
            border-left: 3px solid #27ae60;
        }
        .defensive-tendency {
            background-color: #ffe8e8;
            padding: 10px;
            margin: 5px 0;
            border-radius: 4px;
            border-left: 3px solid #e74c3c;
        }
        .stats { 
            display: inline-block; 
            background-color: #ecf0f1; 
            padding: 5px 10px; 
            margin: 2px; 
            border-radius: 4px; 
            font-weight: bold;
        }
        table { 
            width: 100%; 
            border-collapse: collapse; 
            margin: 10px 0;
        }
        th, td { 
            padding: 8px; 
            text-align: left; 
            border-bottom: 1px solid #ddd; 
        }
        th { 
            background-color: #34495e; 
            color: white; 
        }
        tr:hover { 
            background-color: #f5f5f5; 
        }
        .highlight { 
            background-color: #f39c12; 
            color: white; 
            padding: 2px 6px; 
            border-radius: 3px; 
        }
        .targeting-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }
        .targeting-card {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #e67e22;
        }
        </style>
        """

    def generate_personnel_report(self, gameplan_data, output_filename=None):
        """Generate HTML report for personnel-based gameplan"""
        if not gameplan_data:
            return None
            
        opponent = gameplan_data.get('opponent', 'Unknown')
        league = gameplan_data.get('league', '')
        season = gameplan_data.get('season', '')
        
        if not output_filename:
            output_filename = f"personnel_gameplan_{opponent}_{league}_{season}.html"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Personnel Gameplan vs {opponent}</title>
            {self.css_styles}
        </head>
        <body>
            <div class="header">
                <h1>🏈 Personnel-Based Gameplan</h1>
                <h2>vs {opponent} ({league} {season})</h2>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        """
        
        # Add personnel sections
        recommendations = gameplan_data.get('recommendations', {})
        personnel_defense = gameplan_data.get('personnel_defense', {})
        
        for personnel, plays in recommendations.items():
            if not plays:
                continue
                
            # Get defensive data for this personnel
            def_data = personnel_defense.get(personnel, {})
            total_plays = def_data.get('total_plays', 0)
            defenses = def_data.get('defenses', {})
            
            html_content += f"""
            <div class="section personnel-section">
                <h2>👥 {personnel} Personnel</h2>
                <p><strong>Analysis based on {total_plays} plays</strong></p>
                
                <h3>🛡️ {opponent}'s Defensive Responses:</h3>
                <div class="targeting-grid">
            """
            
            # Show defensive tendencies
            for def_play, frequency in list(defenses.items())[:4]:
                html_content += f"""
                    <div class="defensive-tendency">
                        <strong>{def_play}</strong><br>
                        <span class="highlight">{frequency}%</span> of the time
                    </div>
                """
            
            html_content += """
                </div>
                
                <h3>⚡ Recommended Plays:</h3>
            """
            
            # Group plays by defense
            defense_groups = {}
            for play in plays[:8]:  # Top 8 plays
                defense = play['vs_defense']
                if defense not in defense_groups:
                    defense_groups[defense] = []
                defense_groups[defense].append(play)
            
            for defense, defense_plays in defense_groups.items():
                def_freq = next((d['def_frequency'] for d in defense_plays), 0)
                html_content += f"""
                    <h4>vs {defense} ({def_freq}% frequency):</h4>
                """
                
                for i, play in enumerate(defense_plays[:2], 1):  # Max 2 plays per defense
                    html_content += f"""
                        <div class="play-recommendation">
                            <strong>{i}. {play['play']}</strong> ({play['play_type']})<br>
                            <span class="stats">{play['ypp']:.1f} YPP</span>
                            <span class="stats">{play['any_a']:.1f} ANY/A</span>
                            <span class="stats">{play['sample_size']} plays</span>
                        </div>
                    """
            
            html_content += "</div>"
        
        # Add quick reference section
        html_content += """
            <div class="section">
                <h2>📋 Quick Reference</h2>
                <table>
                    <tr>
                        <th>Personnel</th>
                        <th>Top Play</th>
                        <th>YPP</th>
                        <th>Backup Play</th>
                        <th>YPP</th>
                    </tr>
        """
        
        for personnel, plays in recommendations.items():
            if not plays:
                continue
            top_play = plays[0]
            backup_play = plays[1] if len(plays) > 1 else None
            
            html_content += f"""
                <tr>
                    <td><strong>{personnel}</strong></td>
                    <td>{top_play['play']}</td>
                    <td class="highlight">{top_play['ypp']:.1f}</td>
                    <td>{backup_play['play'] if backup_play else 'N/A'}</td>
                    <td>{backup_play['ypp']:.1f if backup_play else 'N/A'}</td>
                </tr>
            """
        
        html_content += """
                </table>
            </div>
        </body>
        </html>
        """
        
        # Write to file
        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        print(f"📄 HTML report generated: {output_path}")
        return output_path

    def generate_scouting_report_html(self, league, season, team, scouting_data, targeting_data=None):
        """Generate HTML scouting report"""
        output_filename = f"scouting_report_{team}_{league}_{season}.html"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Scouting Report: {team}</title>
            {self.css_styles}
        </head>
        <body>
            <div class="header">
                <h1>🔍 Scouting Report</h1>
                <h2>{team} ({league} {season})</h2>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="section">
                <h2>📊 Offensive Tendencies</h2>
                <p>Plays called at least 2% of the time:</p>
                <table>
                    <tr>
                        <th>Play</th>
                        <th>Frequency</th>
                        <th>Formation</th>
                    </tr>
        """
        
        # Add offensive plays (this would need to be passed from scouting data)
        html_content += """
                </table>
            </div>
            
            <div class="section">
                <h2>🛡️ Defensive Tendencies</h2>
                <table>
                    <tr>
                        <th>Defense</th>
                        <th>Frequency</th>
                        <th>Package</th>
                    </tr>
                </table>
            </div>
        """
        
        # Add targeting analysis if available
        if targeting_data:
            html_content += """
                <div class="section">
                    <h2>🎯 Pass Targeting Analysis</h2>
                    <p>Where to deploy your best defensive players:</p>
                    <div class="targeting-grid">
            """
            
            for position, percentage in targeting_data.get('targeting_percentages', [])[:6]:
                if percentage >= 5:  # Only show significant targets
                    color = "#e74c3c" if percentage > 20 else "#f39c12" if percentage > 15 else "#3498db"
                    html_content += f"""
                        <div class="targeting-card" style="border-left-color: {color}">
                            <h3>{position}</h3>
                            <div class="highlight" style="background-color: {color}">{percentage:.1f}%</div>
                            <p>Target frequency</p>
                        </div>
                    """
            
            html_content += "</div></div>"
        
        html_content += """
        </body>
        </html>
        """
        
        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        print(f"📄 Scouting report generated: {output_path}")
        return output_path

    def open_report_in_browser(self, report_path):
        """Open the generated report in default browser"""
        import webbrowser
        webbrowser.open(f'file://{report_path}')


# Integration functions
def generate_html_personnel_report(gameplan_data):
    """Generate HTML report from personnel gameplan data"""
    generator = HTMLReportGenerator()
    report_path = generator.generate_personnel_report(gameplan_data)
    
    # Auto-open in browser
    if report_path:
        generator.open_report_in_browser(report_path)
    
    return report_path


if __name__ == "__main__":
    # Example usage
    generator = HTMLReportGenerator()
    
    # Test with sample data
    sample_data = {
        'opponent': 'BOS',
        'league': 'USFL', 
        'season': 2002,
        'recommendations': {
            '1RB/1TE/3WR': [
                {
                    'vs_defense': 'Dime Normal Man Cover 1',
                    'def_frequency': 30.0,
                    'play': 'Singleback Slot Strong HB Counter',
                    'ypp': 8.2,
                    'any_a': 9.8,
                    'sample_size': 45,
                    'play_type': 'Outside Run'
                }
            ]
        }
    }
    
    generator.generate_personnel_report(sample_data)