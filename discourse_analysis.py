"""
Milei Securitization Discourse Analysis
========================================

Main analysis script for quantitative discourse analysis of Javier Milei's Twitter
securitization patterns (2022-2025).

This script implements systematic keyword-counting methodology to measure securitization
intensity across enemy categories and economic threat frames.

Author: [Your Name]
Thesis: "Building the Enemy: Populism and the Construction of Security Narratives 
         in Contemporary Argentina (2022-2025)"
"""


import pandas as pd
import re
from datetime import datetime
import numpy as np


# ============================================================================
# KEYWORD DICTIONARIES - Spanish Language
# ============================================================================


# Enemy Categories
ENEMY_KEYWORDS = {
    'la_casta': [
        'casta', 'políticos', 'corruptos', 'privilegiados', 'parásitos',
        'degenerados fiscales', 'clase política', 'establishment'
    ],
    'kirchnerismo': [
        'kirchnerismo', 'kirchneristas', 'cristina', 'cfk', 'fernández',
        'kicillof', 'massa', 'máximo', 'peronismo'
    ],
    'state_apparatus': [
        'estado', 'funcionarios', 'ñoquis', 'empleados públicos',
        'burocracia', 'ministerios', 'banco central', 'bcra', 'afip'
    ],
    'progressives': [
        'feminismo', 'feministas', 'progresismo', 'zurdos', 'izquierda',
        'socialismo', 'comunismo', 'marxismo', 'colectivismo', 'género'
    ],
    'social_movements': [
        'piqueteros', 'movimientos sociales', 'organizaciones sociales',
        'planes sociales', 'vagos', 'planeros'
    ],
    'media': [
        'periodistas', 'medios', 'prensa', 'televisión', 'ensobrados',
        'periodismo militante'
    ],
    'international': [
        'china', 'foro de são paulo', 'brasil', 'lula', 'venezuela',
        'maduro', 'cuba', 'socialismo internacional'
    ]
}


# Economic Securitization Frames
ECONOMIC_KEYWORDS = {
    'fiscal_terrorism': [
        'terrorismo fiscal', 'robo', 'saqueo', 'expropiación', 'confiscación',
        'inflación', 'impuesto', 'emisión', 'déficit'
    ],
    'emergency': [
        'urgente', 'inmediato', 'ya', 'crisis', 'emergencia'
    ],
    'existential': [
        'catástrofe', 'destrucción', 'ruina', 'colapso', 'abismo', 'desastre'
    ]
}


# War and Military Language
WAR_KEYWORDS = [
    'batalla', 'guerra', 'lucha', 'enemigo', 'combate', 'victoria'
]


# Liberty Frames
LIBERTY_KEYWORDS = [
    'libertad', 'libre', 'propiedad privada', 'mercado', 'liberalismo', 'libertario'
]


# ============================================================================
# KEYWORD COUNTING FUNCTIONS
# ============================================================================


def count_keywords(text, keywords):
    """
    Count occurrences of keywords in text using word-boundary detection.
    
    Parameters:
    -----------
    text : str
        The tweet text to analyze
    keywords : list
        List of Spanish keywords to search for
        
    Returns:
    --------
    int
        Total count of keyword occurrences
        
    Notes:
    ------
    - Case-insensitive matching
    - Uses word boundaries (\\b) to prevent false matches
    - Example: "socialismo" won't match "socialismos"
    """
    if pd.isna(text):
        return 0
    
    text_lower = text.lower()
    count = 0
    
    for keyword in keywords:
        # Use word boundaries to match complete words only
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        matches = re.findall(pattern, text_lower)
        count += len(matches)
    
    return count




def calculate_security_intensity(row):
    """
    Calculate the security intensity score for a single tweet.
    
    Security Intensity = Total Enemy Keywords + Total Economic Keywords + War Keywords
    
    Parameters:
    -----------
    row : pandas.Series
        Row from the DataFrame containing keyword counts
        
    Returns:
    --------
    int
        Security intensity score
    """
    enemy_total = sum([
        row.get('la_casta', 0),
        row.get('kirchnerismo', 0),
        row.get('state_apparatus', 0),
        row.get('progressives', 0),
        row.get('social_movements', 0),
        row.get('media', 0),
        row.get('international', 0)
    ])
    
    economic_total = sum([
        row.get('fiscal_terrorism', 0),
        row.get('emergency', 0),
        row.get('existential', 0)
    ])
    
    war_total = row.get('war_language', 0)
    
    return enemy_total + economic_total + war_total




# ============================================================================
# MAIN ANALYSIS FUNCTION
# ============================================================================


def analyze_tweets(input_file, output_file=None):
    """
    Main function to analyze tweets and code for securitization frames.
    
    Parameters:
    -----------
    input_file : str
        Path to Excel/CSV file containing tweets
        Expected columns: 'text', 'timeParsed', 'likes', 'retweets', 'replies'
    output_file : str, optional
        Path to save the coded results (default: adds '_analyzed' to input filename)
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with all coded variables
    """
    
    print(f"Loading data from {input_file}...")
    
    # Read the data
    if input_file.endswith('.xlsx'):
        df = pd.read_excel(input_file)
    elif input_file.endswith('.csv'):
        df = pd.read_csv(input_file)
    else:
        raise ValueError("Input file must be .xlsx or .csv")
    
    print(f"Loaded {len(df)} tweets")
    
    # Parse dates
    print("Parsing timestamps...")
    df['date'] = pd.to_datetime(df['timeParsed'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter
    
    # Calculate total engagement
    print("Calculating engagement metrics...")
    df['total_engagement'] = df['likes'] + df['retweets'] + df['replies']
    
    # Code enemy categories
    print("Coding enemy categories...")
    for category, keywords in ENEMY_KEYWORDS.items():
        print(f"  - {category}")
        df[category] = df['text'].apply(lambda x: count_keywords(x, keywords))
    
    # Code economic frames
    print("Coding economic securitization frames...")
    for frame, keywords in ECONOMIC_KEYWORDS.items():
        print(f"  - {frame}")
        df[frame] = df['text'].apply(lambda x: count_keywords(x, keywords))
    
    # Code war language
    print("Coding war/military language...")
    df['war_language'] = df['text'].apply(lambda x: count_keywords(x, WAR_KEYWORDS))
    
    # Code liberty frames
    print("Coding liberty frames...")
    df['liberty'] = df['text'].apply(lambda x: count_keywords(x, LIBERTY_KEYWORDS))
    
    # Calculate totals
    print("Calculating aggregate metrics...")
    df['total_enemies'] = df[[cat for cat in ENEMY_KEYWORDS.keys()]].sum(axis=1)
    df['total_economic'] = df[[frame for frame in ECONOMIC_KEYWORDS.keys()]].sum(axis=1)
    
    # Calculate security intensity
    print("Calculating security intensity scores...")
    df['security_intensity'] = df.apply(calculate_security_intensity, axis=1)
    
    # Save results
    if output_file is None:
        output_file = input_file.replace('.xlsx', '_analyzed.csv').replace('.csv', '_analyzed.csv')
    
    print(f"Saving results to {output_file}...")
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    # Print summary statistics
    print("\n" + "="*80)
    print("ANALYSIS SUMMARY")
    print("="*80)
    print(f"Total tweets analyzed: {len(df)}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"\nTweets with security frames: {len(df[df['security_intensity'] > 0])} ({len(df[df['security_intensity'] > 0])/len(df)*100:.1f}%)")
    print(f"Average security intensity: {df['security_intensity'].mean():.2f}")
    print(f"Total security intensity: {df['security_intensity'].sum()}")
    
    print(f"\n--- ENEMY CATEGORIES ---")
    for category in ENEMY_KEYWORDS.keys():
        total = df[category].sum()
        print(f"{category.replace('_', ' ').title()}: {total}")
    
    print(f"\n--- ECONOMIC FRAMES ---")
    for frame in ECONOMIC_KEYWORDS.keys():
        total = df[frame].sum()
        print(f"{frame.replace('_', ' ').title()}: {total}")
    
    print(f"\n--- OTHER FRAMES ---")
    print(f"War/Military Language: {df['war_language'].sum()}")
    print(f"Liberty Frames: {df['liberty'].sum()}")
    
    print(f"\n--- QUARTERLY BREAKDOWN ---")
    quarterly = df.groupby('quarter').agg({
        'security_intensity': ['mean', 'sum'],
        'total_engagement': 'sum'
    }).round(2)
    print(quarterly)
    
    print("\n✓ Analysis complete!")
    
    return df




# ============================================================================
# ADDITIONAL ANALYSIS FUNCTIONS
# ============================================================================


def analyze_event_period(df, start_date, end_date, event_name):
    """
    Analyze a specific event period.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The analyzed tweets DataFrame
    start_date : str
        Start date in format 'YYYY-MM-DD'
    end_date : str
        End date in format 'YYYY-MM-DD'
    event_name : str
        Name of the event for reporting
    """
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    event_df = df[mask]
    
    print(f"\n{'='*80}")
    print(f"EVENT ANALYSIS: {event_name}")
    print(f"Period: {start_date} to {end_date}")
    print(f"{'='*80}")
    print(f"Total tweets: {len(event_df)}")
    print(f"Average security intensity: {event_df['security_intensity'].mean():.2f}")
    print(f"Average engagement: {event_df['total_engagement'].mean():.0f}")
    
    print(f"\nTop enemy categories:")
    for category in ENEMY_KEYWORDS.keys():
        total = event_df[category].sum()
        if total > 0:
            print(f"  {category.replace('_', ' ').title()}: {total}")
    
    print(f"\nTop economic frames:")
    for frame in ECONOMIC_KEYWORDS.keys():
        total = event_df[frame].sum()
        if total > 0:
            print(f"  {frame.replace('_', ' ').title()}: {total}")




def export_high_intensity_tweets(df, output_file, threshold=3):
    """
    Export tweets with high security intensity for qualitative analysis.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The analyzed tweets DataFrame
    output_file : str
        Path to save high-intensity tweets
    threshold : int
        Minimum security intensity score (default: 3)
    """
    high_intensity = df[df['security_intensity'] >= threshold].copy()
    high_intensity = high_intensity.sort_values('security_intensity', ascending=False)
    
    # Select relevant columns
    columns = ['date', 'text', 'security_intensity', 'total_engagement',
               'la_casta', 'kirchnerismo', 'fiscal_terrorism', 'war_language']
    
    high_intensity[columns].to_excel(output_file, index=False)
    print(f"Exported {len(high_intensity)} high-intensity tweets to {output_file}")




# ============================================================================
# USAGE EXAMPLE
# ============================================================================


if __name__ == "__main__":
    """
    Example usage of the analysis script.
    
    To run this script:
    1. Ensure your tweet data is in Excel or CSV format
    2. Update the input_file path below
    3. Run: python discourse_analysis.py
    """
    
    # Example for 2022 analysis
    input_file = 'data/raw_data/tweets_2022.xlsx'
    output_file = 'data/processed_data/tweets_2022_analyzed.csv'
    
    # Run the analysis
    df = analyze_tweets(input_file, output_file)
    
    # Optional: Analyze specific event period
    # Example: IMF negotiations (March 2022)
    analyze_event_period(
        df,
        start_date='2022-03-01',
        end_date='2022-03-18',
        event_name='IMF Negotiations March 2022'
    )
    
    # Optional: Export high-intensity tweets for qualitative analysis
    export_high_intensity_tweets(
        df,
        output_file='results/high_intensity_tweets_2022.xlsx',
        threshold=3
    )
    
    print("\n✓ All analyses complete!")
