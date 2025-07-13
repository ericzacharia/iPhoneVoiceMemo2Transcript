#!/usr/bin/env python3
"""
Summarize a transcript using OpenAI GPT models.
"""

import argparse
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import the API key from llm_api_token.py first, fallback to env var
try:
    from llm_api_token import openai_api_key
    client = OpenAI(api_key=openai_api_key)
except ImportError:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: No OpenAI API key found. Please set OPENAI_API_KEY environment variable or create llm_api_token.py")
        sys.exit(1)
    client = OpenAI(api_key=api_key)


def summarize_transcript(transcript, style="outline"):
    """
    Summarize the transcript using OpenAI API.
    
    Args:
        transcript (str): The transcript text to summarize
        style (str): The style of summary - "outline" or "paragraph"
    
    Returns:
        str: The summarized text
    """
    if style == "outline":
        style_instruction = "Create a clear, structured outline with main points and sub-points."
    else:
        style_instruction = "Write a coherent paragraph summary."
    
    prompt = f"""
    Please summarize the following transcript. {style_instruction}
    
    Focus on:
    - Key topics discussed
    - Main ideas and insights
    - Important decisions or conclusions
    - Action items or next steps (if any)
    
    Transcript:
    {transcript}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert at summarizing transcripts clearly and concisely."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(description="Summarize a transcript file using OpenAI")
    parser.add_argument("transcript_file", help="Path to the transcript file")
    parser.add_argument("-s", "--style", choices=["outline", "paragraph"], 
                       default="outline", help="Summary style (default: outline)")
    parser.add_argument("-o", "--output", help="Output file path (default: append _summary to input filename)")
    
    args = parser.parse_args()
    
    # Read the transcript
    try:
        with open(args.transcript_file, 'r') as f:
            transcript = f.read()
    except FileNotFoundError:
        print(f"Error: Transcript file '{args.transcript_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading transcript file: {str(e)}")
        sys.exit(1)
    
    if not transcript.strip():
        print("Error: Transcript is empty.")
        sys.exit(1)
    
    # Generate summary
    print(f"Generating {args.style} summary...")
    try:
        summary = summarize_transcript(transcript, args.style)
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        sys.exit(1)
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        base_name = os.path.splitext(args.transcript_file)[0]
        output_path = f"{base_name}_summary.txt"
    
    # Write summary to file
    try:
        with open(output_path, 'w') as f:
            f.write(f"Summary ({args.style} style):\n")
            f.write("=" * 50 + "\n\n")
            f.write(summary)
            f.write("\n")
        print(f"Summary saved to: {output_path}")
    except Exception as e:
        print(f"Error writing summary file: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()