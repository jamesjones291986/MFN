"""
Draft Board Generator - Creates optimized draft boards and exports results
"""

import csv
import json
from pathlib import Path
from typing import List, Dict
from collections import defaultdict


class DraftBoardGenerator:
    """Generates and exports draft boards based on analyzed player data."""
    
    def __init__(self, verbose: bool = False):
        """Initialize the draft board generator."""
        self.verbose = verbose
        
    def generate_board(self, players: List[Dict], top_n: int = 100) -> List[Dict]:
        """Generate a ranked draft board."""
        if self.verbose:
            print(f"Generating draft board for {len(players)} players")
            
        # Sort players by overall score (descending)
        ranked_players = sorted(players, key=lambda x: x['overall_score'], reverse=True)
        
        # Limit to top N
        if top_n > 0:
            ranked_players = ranked_players[:top_n]
            
        # Add draft rankings
        for i, player in enumerate(ranked_players, 1):
            player['draft_rank'] = i
            
        if self.verbose:
            print(f"Generated draft board with {len(ranked_players)} players")
            
        return ranked_players
        
    def generate_positional_boards(self, players: List[Dict], top_n_per_position: int = 20) -> Dict[str, List[Dict]]:
        """Generate position-specific draft boards."""
        positional_boards = defaultdict(list)
        
        # Group players by position
        for player in players:
            position = player['position'].upper()
            positional_boards[position].append(player)
            
        # Sort each position by overall score and limit
        for position, pos_players in positional_boards.items():
            sorted_players = sorted(pos_players, key=lambda x: x['overall_score'], reverse=True)
            
            if top_n_per_position > 0:
                sorted_players = sorted_players[:top_n_per_position]
                
            # Add positional rankings
            for i, player in enumerate(sorted_players, 1):
                player[f'{position.lower()}_rank'] = i
                
            positional_boards[position] = sorted_players
            
        return dict(positional_boards)
        
    def export(self, players: List[Dict], output_path: Path, format: str = 'csv'):
        """Export draft board to specified format."""
        if format == 'csv':
            self._export_csv(players, output_path)
        elif format == 'json':
            self._export_json(players, output_path)
        elif format == 'html':
            self._export_html(players, output_path)
        else:
            raise ValueError(f"Unsupported export format: {format}")
            
    def _export_csv(self, players: List[Dict], output_path: Path):
        """Export to CSV format."""
        if not players:
            return
            
        # Define the columns we want to export
        columns = [
            'draft_rank', 'name', 'position', 'age', 'college', 'height', 'weight',
            'overall_score', 'draft_grade', 'projected_round',
            'physical_score', 'mental_score', 'position_score', 'size_score',
            'speed', 'acceleration', 'agility', 'strength', 'awareness', 'intelligence', 'durability'
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            
            for player in players:
                # Only write columns that exist
                row = {col: player.get(col, '') for col in columns}
                writer.writerow(row)
                
        if self.verbose:
            print(f"Exported {len(players)} players to CSV: {output_path}")
            
    def _export_json(self, players: List[Dict], output_path: Path):
        """Export to JSON format."""
        # Clean up the data for JSON export
        clean_players = []
        
        for player in players:
            clean_player = player.copy()
            # Remove the raw data
            clean_player.pop('_raw', None)
            clean_players.append(clean_player)
            
        export_data = {
            'draft_board': clean_players,
            'metadata': {
                'total_players': len(players),
                'generated_at': str(pd.Timestamp.now()) if 'pd' in globals() else 'unknown',
                'top_player': players[0]['name'] if players else None,
                'positions_analyzed': list(set(p['position'] for p in players))
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
            
        if self.verbose:
            print(f"Exported {len(players)} players to JSON: {output_path}")
            
    def _export_html(self, players: List[Dict], output_path: Path):
        """Export to HTML format."""
        html_content = self._generate_html_report(players)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        if self.verbose:
            print(f"Exported {len(players)} players to HTML: {output_path}")
            
    def _generate_html_report(self, players: List[Dict]) -> str:
        """Generate HTML report content."""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>MFN Draft Board</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .grade-A { background-color: #d4edda; }
                .grade-B { background-color: #fff3cd; }
                .grade-C { background-color: #f8d7da; }
                .position { font-weight: bold; }
                .score { text-align: center; }
                h1 { color: #333; }
                .summary { margin: 20px 0; padding: 15px; background-color: #e9ecef; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>🏈 MFN Draft Board Analysis</h1>
            
            <div class="summary">
                <h2>Summary</h2>
                <p><strong>Total Players Analyzed:</strong> """ + str(len(players)) + """</p>
                <p><strong>Top Prospect:</strong> """ + (players[0]['name'] if players else 'None') + """</p>
                <p><strong>Positions:</strong> """ + ', '.join(sorted(set(p['position'] for p in players))) + """</p>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Player</th>
                        <th>Pos</th>
                        <th>Age</th>
                        <th>College</th>
                        <th>Size</th>
                        <th>Overall Score</th>
                        <th>Grade</th>
                        <th>Projected Round</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for player in players:
            grade_class = f"grade-{player.get('draft_grade', 'F')[0]}"
            height = player.get('height', 'N/A')
            weight = player.get('weight', 'N/A')
            size_str = f"{height} / {weight}lbs" if height != 'N/A' and weight != 'N/A' else 'N/A'
            
            html += f"""
                    <tr class="{grade_class}">
                        <td class="score">{player.get('draft_rank', '')}</td>
                        <td><strong>{player.get('name', '')}</strong></td>
                        <td class="position">{player.get('position', '')}</td>
                        <td class="score">{player.get('age', '')}</td>
                        <td>{player.get('college', '')}</td>
                        <td>{size_str}</td>
                        <td class="score">{player.get('overall_score', 0):.1f}</td>
                        <td class="score">{player.get('draft_grade', '')}</td>
                        <td>{player.get('projected_round', '')}</td>
                    </tr>
            """
            
        html += """
                </tbody>
            </table>
            
            <div style="margin-top: 30px; font-size: 12px; color: #666;">
                <p>Generated by MFN Draft Analyzer</p>
            </div>
        </body>
        </html>
        """
        
        return html
        
    def generate_team_needs_report(self, players: List[Dict], team_needs: Dict[str, List[str]] = None) -> Dict:
        """Generate a report matching players to team needs."""
        if not team_needs:
            # Default generic team needs
            team_needs = {
                'Team A': ['QB', 'WR', 'OL'],
                'Team B': ['RB', 'DL', 'LB'],
                'Team C': ['TE', 'DB', 'WR']
            }
            
        recommendations = {}
        
        for team, positions in team_needs.items():
            team_recs = []
            
            for position in positions:
                # Get top 5 players at this position
                pos_players = [p for p in players if p['position'].upper() == position.upper()]
                pos_players = sorted(pos_players, key=lambda x: x['overall_score'], reverse=True)[:5]
                
                team_recs.append({
                    'position': position,
                    'recommendations': pos_players
                })
                
            recommendations[team] = team_recs
            
        return recommendations