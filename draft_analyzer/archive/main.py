#!/usr/bin/env python3
"""
MFN Draft Analyzer - Main Entry Point
Analyzes draft-eligible players and generates optimized draft boards.
"""

import argparse
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from draft_board_generator import DraftBoardGenerator
from player_analyzer import PlayerAnalyzer
from data_processor import DataProcessor


def main():
    """Main entry point for the draft analyzer."""
    parser = argparse.ArgumentParser(description='MFN Draft Analyzer')
    parser.add_argument('--input-file', '-i', required=True, 
                       help='Path to the draft-eligible players CSV file')
    parser.add_argument('--output-dir', '-o', default='output',
                       help='Output directory for results (default: output)')
    parser.add_argument('--position', '-p', 
                       help='Filter by specific position (QB, RB, WR, TE, etc.)')
    parser.add_argument('--top-n', '-n', type=int, default=100,
                       help='Number of top players to include in draft board (default: 100)')
    parser.add_argument('--format', '-f', choices=['csv', 'json', 'html'], default='csv',
                       help='Output format (default: csv)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Process the input data
        if args.verbose:
            print(f"Processing player data from: {args.input_file}")
        
        processor = DataProcessor(args.input_file, verbose=args.verbose)
        players = processor.load_players()
        
        if args.position:
            players = processor.filter_by_position(players, args.position)
            if args.verbose:
                print(f"Filtered to {len(players)} {args.position} players")
        
        # Analyze players
        if args.verbose:
            print("Analyzing player potential and projections...")
            
        analyzer = PlayerAnalyzer(verbose=args.verbose)
        analyzed_players = analyzer.analyze_players(players)
        
        # Generate draft board
        if args.verbose:
            print("Generating optimized draft board...")
            
        draft_board = DraftBoardGenerator(verbose=args.verbose)
        ranked_players = draft_board.generate_board(analyzed_players, top_n=args.top_n)
        
        # Export results
        output_file = output_dir / f"draft_board.{args.format}"
        draft_board.export(ranked_players, output_file, format=args.format)
        
        print(f"✅ Draft board generated successfully!")
        print(f"   📊 Analyzed {len(analyzed_players)} players")
        print(f"   🏆 Top {len(ranked_players)} players ranked")
        print(f"   📁 Results saved to: {output_file}")
        
        # Display top 10 preview
        print(f"\n🔥 TOP 10 DRAFT PICKS:")
        for i, player in enumerate(ranked_players[:10], 1):
            print(f"  {i:2d}. {player['name']:<20} {player['position']:<3} - {player['overall_score']:.1f}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()