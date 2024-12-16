#!/usr/bin/env python3
"""
Command-line interface for PDF processing.
"""
import sys
import os
import argparse
import json
import re
from pathlib import Path
from typing import Optional, Union, List
from loguru import logger
from .pdf_processor import PDFProcessor, ProcessingResult
from .formats import validate_format, get_supported_formats
from .config import ConfigManager, AigrokConfig
import csv
import io
import glob
from .logging import configure_logging

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Process documents with LLMs",
        usage="%(prog)s [options] PROMPT file ...",
        prog="aigrok"
    )
    
    # Version
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.3.1"
    )
    
    # Required arguments
    parser.add_argument(
        "files",
        nargs="+",
        metavar="PROMPT/file",
        help="prompt followed by files to process"
    )
    
    # Optional arguments
    parser.add_argument(
        "--format",
        "-f",
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        "--configure",
        action="store_true",
        help="Configure the application"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        help="Model to use for analysis"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Path to save the output (defaults to stdout)"
    )
    
    # Format options
    parser.add_argument(
        "--type",
        help=f"Input file type. Supported types: {', '.join(t.strip('.') for t in get_supported_formats())}"
    )
    
    # Additional options
    parser.add_argument(
        "--metadata-only",
        action="store_true",
        help="Only extract and display document metadata"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--easyocr",
        action="store_true",
        help="Enable OCR processing of images in PDFs. This is useful for PDFs with scanned text or embedded images containing text. Example: --easyocr"
    )
    
    parser.add_argument(
        "--ocr-languages",
        type=str,
        default="en",
        help="Comma-separated list of language codes for OCR. Available languages depend on EasyOCR's language packs. Example: --ocr-languages 'en,fr,de' for English, French, and German"
    )
    
    parser.add_argument(
        "--ocr-fallback",
        action="store_true",
        help="Continue processing even if OCR fails. This ensures the document is processed using standard text extraction even if OCR encounters errors. Example: --ocr-fallback"
    )
    
    # TODO(cli): Add --version command
    # - Add version command to CLI parser
    # - Return version from pyproject.toml
    
    return parser

def format_output(result: Union[ProcessingResult, List[ProcessingResult]], format_type: str = "text", show_filenames: bool = False) -> str:
    """Format processing result for output.
    
    Args:
        result: Processing result or list of results to format
        format_type: Output format (text, json, markdown)
        show_filenames: Whether to show filenames in text output (for multiple files)
    
    Returns:
        Formatted output string
    """
    if isinstance(result, list):
        if format_type == "text":
            # Format each result with filename prefix (like grep)
            formatted_results = []
            for r in result:
                if not isinstance(r, ProcessingResult):
                    logger.warning(f"Unexpected result type: {type(r)}")
                    continue
                response = r.llm_response or r.text or ""
                filename = getattr(r, 'filename', None) or r.metadata.get('file_name', 'unknown')
                if response:
                    if show_filenames:
                        formatted_results.append(f"{filename}: {response}")
                    else:
                        formatted_results.append(response)
            return "\n".join(formatted_results)
        
        if format_type == "json":
            return json.dumps([{
                "success": r.success,
                "text": r.text,
                "metadata": r.metadata,
                "page_count": r.page_count,
                "llm_response": r.llm_response,
                "error": r.error,
                "filename": getattr(r, 'filename', None) or r.metadata.get('file_name', 'unknown')
            } for r in result if isinstance(r, ProcessingResult)], indent=2)
        
        if format_type == "markdown":
            all_lines = []
            for r in result:
                if not isinstance(r, ProcessingResult):
                    logger.warning(f"Unexpected result type: {type(r)}")
                    continue
                filename = getattr(r, 'filename', None) or r.metadata.get('file_name', 'unknown')
                lines = [
                    f"# {filename}",
                    f"Text: {r.text or 'N/A'}",
                    f"Page Count: {r.page_count}",
                    f"LLM Response: {r.llm_response or 'N/A'}"
                ]
                if r.metadata:
                    lines.extend([
                        "## Metadata",
                        *[f"{k}: {v}" for k, v in r.metadata.items()]
                    ])
                if r.error:
                    lines.append(f"## Error\n{r.error}")
                all_lines.extend(lines)
                all_lines.append("\n---\n")  # Separator between documents
            return "\n".join(all_lines)
    else:
        if not isinstance(result, ProcessingResult):
            logger.warning(f"Unexpected result type: {type(result)}")
            return ""
        
        if format_type == "text":
            response = result.llm_response or result.text or ""
            filename = getattr(result, 'filename', None) or result.metadata.get('file_name', 'unknown')
            if response:
                if show_filenames:
                    return f"{filename}: {response}"
                return response
            return response
        
        if format_type == "json":
            return json.dumps({
                "success": result.success,
                "text": result.text,
                "metadata": result.metadata,
                "page_count": result.page_count,
                "llm_response": result.llm_response,
                "error": result.error,
                "filename": getattr(result, 'filename', None) or result.metadata.get('file_name', 'unknown')
            }, indent=2)
        
        if format_type == "markdown":
            filename = getattr(result, 'filename', None) or result.metadata.get('file_name', 'unknown')
            lines = [
                f"# {filename}",
                f"Text: {result.text or 'N/A'}",
                f"Page Count: {result.page_count}",
                f"LLM Response: {result.llm_response or 'N/A'}"
            ]
            if result.metadata:
                lines.extend([
                    "## Metadata",
                    *[f"{k}: {v}" for k, v in result.metadata.items()]
                ])
            if result.error:
                lines.append(f"## Error\n{result.error}")
            return "\n".join(lines)

def process_single_file(file_path: Union[str, Path], prompt: str) -> ProcessingResult:
    """Process a single PDF file.
    
    Args:
        file_path: Path to PDF file
        prompt: Processing prompt
    
    Returns:
        Processing result
    
    Raises:
        Exception: If processing fails
    """
    try:
        processor = PDFProcessor()
        result = processor.process_file(file_path, prompt)
        result.filename = str(Path(file_path).name)  # Store just the filename
        return result
    except Exception as e:
        logger.error(f"Failed to process {file_path}: {str(e)}")
        return ProcessingResult(
            success=False,
            error=str(e),
            filename=str(Path(file_path).name)
        )

def process_file(
    files: Union[str, Path, List[Union[str, Path]]],
    prompt: str
) -> Union[ProcessingResult, List[ProcessingResult]]:
    """Process one or more PDF files.
    
    Args:
        files: Path(s) to PDF file(s)
        prompt: Processing prompt
    
    Returns:
        Single result or list of results
    """
    if isinstance(files, (str, Path)):
        return process_single_file(files, prompt)
    
    return [process_single_file(f, prompt) for f in files]

def main():
    """Main entry point for the CLI."""
    try:
        parser = create_parser()
        
        # Show help if no arguments provided
        if len(sys.argv) == 1:
            parser.print_help()
            return 0
            
        args = parser.parse_args()
        
        # Configure logging first
        configure_logging(args.verbose)
        
        # Only log when verbose mode is enabled
        if args.verbose:
            logger.debug(f"Arguments: {args}")
            logger.debug(f"Verbose mode: {args.verbose}")

        config_manager = ConfigManager()
        
        # Handle configuration
        if args.configure:
            config_manager.configure()
            return
            
        # Update configuration if OCR options are provided
        if args.easyocr:
            if not config_manager.config:
                print("Error: PDF processor not properly initialized. Please run with --configure first.")
                return
            config_manager.config.ocr_enabled = True
            if args.ocr_languages:
                config_manager.config.ocr_languages = args.ocr_languages.split(',')
            config_manager.config.ocr_fallback = args.ocr_fallback
            config_manager.save_config()
            if args.verbose:
                logger.debug("Updated OCR configuration")
        
        # First argument is the prompt, rest are files
        if len(args.files) < 2:  # Need at least prompt + one file
            print("Error: Must provide both a prompt and at least one file")
            print("Usage: aigrok PROMPT file [file ...]")
            return
            
        prompt = args.files[0]
        patterns = args.files[1:]

        if not args.configure and not patterns:
            print("Error: No input files specified")
            return

        if args.verbose:
            logger.debug(f"Processing files: {patterns}")

        # Expand glob patterns in file arguments
        files = []
        for pattern in patterns:
            matched_files = glob.glob(pattern)
            if not matched_files:
                print(f"Error: File not found: {pattern}")
                return
            files.extend(matched_files)

        # Initialize processor with verbose setting
        processor = PDFProcessor(config_manager=config_manager, verbose=args.verbose)
        
        # Process files and format output
        results = []
        for file in files:
            result = processor.process_file(file, prompt)
            results.append(result)
        
        # Format output
        output = format_output(results[0] if len(results) == 1 else results, args.format, len(files) > 1)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            if args.verbose:
                logger.debug(f"Output written to {args.output}")
        else:
            print(output)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        if args.verbose:
            logger.exception("An error occurred")
        sys.exit(1)

if __name__ == "__main__":
    main()