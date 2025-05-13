import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_query_stats(file_path):
    """Load query statistics from JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def plot_general_stats(stats, output_dir):
    """Plot general query statistics."""
    categories = ['Valid Queries', 'Invalid Queries']
    values = [stats[cat] for cat in categories]
    
    plt.figure(figsize=(8, 5))
    bars = plt.bar(categories, values, color=['green', 'red'])
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{height}', ha='center', va='bottom')
    
    plt.title('Query Statistics Overview')
    plt.ylabel('Count')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(Path(output_dir) / 'query_overview.pdf')
    plt.close()

def plot_top_clauses(stats, output_dir, top_n=None):
    """Plot SQL clauses by frequency (all non-zero)."""
    # Get clause frequencies and sort
    clauses = list(stats['Clause Frequency'].items())
    clauses.sort(key=lambda x: x[1], reverse=False)
    
    # Take all non-zero frequencies
    non_zero_clauses = [(clause, count) for clause, count in clauses if count > 0]
    
    # Use all non-zero clauses instead of just top N
    selected_clauses = non_zero_clauses
    
    # Get the data for plotting
    labels = [clause for clause, _ in selected_clauses]
    counts = [count for _, count in selected_clauses]
    y_pos = np.arange(len(labels))
    
    # Calculate better figure dimensions
    height_per_clause = 0.25  # Reduced from 0.3
    min_height = 6
    fig_height = max(min_height, height_per_clause * len(selected_clauses))
    
    # Create horizontal bar chart with dynamic sizing
    fig, ax = plt.subplots(figsize=(12, fig_height))
    bars = ax.barh(y_pos, counts, color='skyblue')
    
    # Set y-ticks and labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    
    # Add value annotations
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 0.3, bar.get_y() + bar.get_height()/2, 
                f'{width}', ha='left', va='center')
    
    # Set titles and labels
    ax.set_title('Total Frequency of SQL clauses over 10000 queries')
    ax.set_xlabel('Frequency')
    
    # Set x-axis limits to reduce horizontal space
    max_count = max(counts)
    ax.set_xlim(0, max_count * 1.1)  # Only add 10% extra space for annotations
    
    # Set y-axis limits to reduce vertical space
    ax.set_ylim(y_pos.min() - 0.5, y_pos.max() + 0.5)
    
    # Adjust layout with tighter margins
    plt.tight_layout(pad=1.0)  # Reduced padding
    
    # Save the figure
    plt.savefig(Path(output_dir) / 'clause_frequency.pdf')
    plt.close(fig)

def plot_clause_per_query(stats, output_dir):
    """Plot average occurrences of each SQL clause per query."""
    # Get clause frequencies and sort
    clauses = list(stats['Clause Frequency'].items())
    
    # Calculate occurrences per query
    total_queries = stats['Total Queries']  # Using valid queries as denominator
    clauses_per_query = [(clause, count / total_queries) for clause, count in clauses if count > 0]
    
    # Sort by occurrences per query (descending)
    clauses_per_query.sort(key=lambda x: x[1], reverse=True)
    
    # Create lists for plotting (to put highest values at the top)
    plot_labels = [clause for clause, _ in clauses_per_query][::-1]
    plot_frequencies = [freq for _, freq in clauses_per_query][::-1]
    y_pos = np.arange(len(plot_labels))
    
    # Calculate figure dimensions
    height_per_clause = 0.25
    min_height = 6
    fig_height = max(min_height, height_per_clause * len(clauses_per_query))
    
    # Create horizontal bar chart
    fig, ax = plt.subplots(figsize=(12, fig_height))
    bars = ax.barh(y_pos, plot_frequencies, color='skyblue')
    
    # Set y-ticks and labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(plot_labels)
    
    # Add value annotations with conditional formatting: 
    # 5 decimal places for very small values, 3 for others
    for i, bar in enumerate(bars):
        width = bar.get_width()
        # Use 5 decimal places for values that would show as 0.00
        if width < 0.01:
            format_str = f"{width:.4f}"
        else:
            format_str = f"{width:.3f}"
        ax.text(width + 0.01, bar.get_y() + bar.get_height()/2, 
                format_str, ha='left', va='center')
    
    # Set titles and labels
    ax.set_title('Average Frequency of SQL clauses per query over 10000 queries')
    ax.set_xlabel('Occurrences per Query')
    
    # Set x-axis limits
    max_freq = max(plot_frequencies)
    ax.set_xlim(0, max_freq * 1.1)
    
    # Set y-axis limits to reduce vertical space
    ax.set_ylim(y_pos.min() - 0.5, y_pos.max() + 0.5)
    
    # Add grid for better readability
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Adjust layout with tighter margins
    plt.tight_layout(pad=1.0)
    
    # Save the figure
    plt.savefig(Path(output_dir) / 'clause_per_query.pdf')
    plt.close(fig)

def main():
    # Define paths
    input_file = 'query_stat.json'
    output_dir = './plots'  # Current directory
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)
    
    # Load data
    stats = load_query_stats(input_file)
    
    # Generate plots
    plot_general_stats(stats, output_dir)
    plot_top_clauses(stats, output_dir)
    plot_clause_per_query(stats, output_dir)  # Add this line
    
    print(f"Plots generated and saved to {Path(output_dir).absolute()}")

if __name__ == "__main__":
    main()