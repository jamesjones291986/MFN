# Team-Specific Analysis Tools

This directory contains tools for analyzing what plays work best against specific opponents, providing direct actionable scouting recommendations.

## Philosophy

Unlike the general gameplan generator that uses complex statistical adjustments, these tools directly answer:
- "What offensive plays have been most successful against Team X?"
- "What defensive plays have been most successful against Team X's offense?"

## Tools

### `team_specific_success_analyzer.py`
Main analysis tool that provides direct success rates and recommendations.

**Usage:**
```bash
# Analyze what works against MIC
python3 team_specific_success_analyzer.py --league USFL --season 2018 --opponent MIC

# Require more attempts for statistical significance
python team_specific_success_analyzer.py --opponent MIC --league USFL --season 2018 --min-attempts 5
```

**Output:**
- Best offensive plays vs opponent (sorted by yards/attempt)
- Best defensive plays vs opponent's offense (sorted by yards allowed)
- Success rates, completion rates, stop rates
- Run vs pass effectiveness recommendations

## Key Advantages

1. **Direct Results**: Shows actual performance against specific opponents
2. **Actionable**: Clear recommendations on what to call
3. **Simple Logic**: Easy to understand and trust
4. **Team-Focused**: Accounts for opponent-specific weaknesses

## Example Output

```
🏃‍♂️ BEST RUNNING PLAYS vs MIC
   I Formation Normal HB Blast
     7.4 yds/carry, 47 attempts, 65.2% success rate
     Personnel: 2RB/1TE/2WR

🎯 BEST PASSING PLAYS vs MIC  
   Shotgun Normal HB Flare
     14.5 yds/att, 4 attempts, 100.0% success, 100.0% comp
     Personnel: 1RB/1TE/3WR

💡 KEY RECOMMENDATIONS vs MIC
   📈 PASS-HEAVY APPROACH: Passing significantly more effective
```

## Future Enhancements

- Add down and distance specific analysis
- Include red zone specific recommendations  
- Add situational analysis (score differential, time remaining)
- Export results to Google Sheets
- Add comparative analysis vs multiple opponents
