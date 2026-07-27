#!/usr/bin/env python3
"""
Main entry point for Resume Scoring & Optimization Agent
"""

import sys
import os
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agent import ResumeScoringAgent


def main():
    parser = argparse.ArgumentParser(
        description="Resume Scoring & Optimization AI Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Score resume against ATS systems only
  python main.py --resume data/resume.docx

  # Score resume and optimize for specific job
  python main.py --resume data/resume.docx --jd data/job_description.txt

  # Non-interactive mode (skip skill verification)
  python main.py --resume data/resume.docx --jd data/job_description.txt --non-interactive
        """
    )

    parser.add_argument(
        "--resume",
        required=True,
        help="Path to resume .docx file"
    )

    parser.add_argument(
        "--jd",
        help="Path to job description text file"
    )

    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Skip interactive skill verification"
    )

    parser.add_argument(
        "--output",
        default="output",
        help="Output directory for reports (default: output)"
    )

    args = parser.parse_args()

    # Validate resume file exists
    if not os.path.exists(args.resume):
        print(f"❌ Error: Resume file not found: {args.resume}")
        sys.exit(1)

    # Validate JD file if provided
    if args.jd and not os.path.exists(args.jd):
        print(f"❌ Error: Job description file not found: {args.jd}")
        sys.exit(1)

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    # Run agent
    agent = ResumeScoringAgent()
    results = agent.run(
        resume_path=args.resume,
        jd_path=args.jd,
        interactive=not args.non_interactive
    )

    print("\n✅ Analysis complete! Check the output folder for detailed reports.")

    return results


if __name__ == "__main__":
    main()
