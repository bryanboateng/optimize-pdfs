import argparse
import logging
import pathlib
import subprocess


def optimize_pdf(input_file_path: pathlib.Path, quality: str):
    if input_file_path.suffix != ".pdf":
        logging.warning(f"Skipping non-PDF file '{input_file_path}'")
        return

    output_file_path = input_file_path.with_stem(
        f"{input_file_path.stem}_optimized_q_{quality}"
    )

    ghostscript_command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{quality}",
        "-dNOPAUSE",
        "-dBATCH",
        f"-sOutputFile={output_file_path}",
        input_file_path,
    ]

    try:
        logging.info(f"Starting with optimization of '{input_file_path}'")
        subprocess.run(ghostscript_command, check=True)
        logging.info(f"Optimized '{input_file_path}' to '{output_file_path}'")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error optimizing '{input_file_path}': {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    argument_parser = argparse.ArgumentParser(prog="Optimize PDF filesize")
    argument_parser.add_argument("files", type=pathlib.Path, nargs="+")
    argument_parser.add_argument(
        "-q",
        "--quality",
        type=str,
        choices=["screen", "ebook", "printer", "prepress", "default"],
        default="ebook"
    )
    arguments = argument_parser.parse_args()
    for file in arguments.files:
        optimize_pdf(file, arguments.quality)
