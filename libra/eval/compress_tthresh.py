import subprocess
import os
import csv
import numpy as np
import argparse
import re

def compress_with_tthresh(tthresh_path, input_file, dimensions, threshold, compressed_file, decompressed_file):
    command = [
        tthresh_path,
        '-i', input_file,
        '-t', 'float',  # Modify the data type as needed ('uchar' for unsigned char, 'float' for floating-point)
        '-s', f'{dimensions[0]}', f'{dimensions[1]}', f'{dimensions[2]}',
        '-p', str(threshold),
        '-c', compressed_file,
        '-o', decompressed_file
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout

def parse_output(output):
    print("tthresh output:\n", output)  # Print the output for debugging

    old_bits_match = re.search(r'oldbits\s*=\s*([\d,]+)', output)
    new_bits_match = re.search(r'newbits\s*=\s*([\d,]+)', output)
    compression_ratio_match = re.search(r'compressionratio\s*=\s*([\d.]+)', output)
    bpv_match = re.search(r'bpv\s*=\s*([\d.]+)', output)
    psnr_match = re.search(r'psnr\s*=\s*([\d.]+)', output)

    if old_bits_match and new_bits_match and compression_ratio_match and bpv_match and psnr_match:
        old_bits = int(old_bits_match.group(1).replace(',', ''))
        new_bits = int(new_bits_match.group(1).replace(',', ''))
        compression_ratio = float(compression_ratio_match.group(1))
        bpv = float(bpv_match.group(1))
        psnr = float(psnr_match.group(1))
        return old_bits, new_bits, compression_ratio, bpv, psnr
    else:
        raise ValueError("Unable to parse tthresh output")

def main():
    parser = argparse.ArgumentParser(description='Compress a raw file using tthresh with varying thresholds.')
    parser.add_argument('tthresh_path', type=str, help='Path to the tthresh executable')
    parser.add_argument('input_file', type=str, help='Path to the input raw file')
    parser.add_argument('output_dir', type=str, help='Directory to save compressed files')
    parser.add_argument('--dimensions', type=str, required=True, help='Dimensions of the input file, formatted as "x,y,z"')

    args = parser.parse_args()

    tthresh_path = args.tthresh_path
    input_file = args.input_file
    output_dir = args.output_dir
    dimensions = tuple(map(int, args.dimensions.split(',')))

    os.makedirs(output_dir, exist_ok=True)

    # Define thresholds for compression
    thresholds = np.arange(30, 70)

    # Prepare CSV file for writing compression info
    csv_file = os.path.join(output_dir, 'compression_info.csv')
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Threshold', 'Old Bits', 'New Bits', 'Compression Ratio', 'BPV', 'PSNR', 'Compressed File', 'Decompressed File'])

        # Compress the raw file using different thresholds
        for threshold in thresholds:
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            compressed_raw_file = os.path.join(output_dir, f'{base_name}_compressed_psnr_{threshold}tthresh.raw')
            decompressed_raw_file = os.path.join(output_dir, f'{base_name}_decompressed_psnr_{threshold}tthresh.raw')
            output = compress_with_tthresh(tthresh_path, input_file, dimensions, threshold, compressed_raw_file, decompressed_raw_file)

            # Parse the output to get the metrics
            old_bits, new_bits, compression_ratio, bpv, psnr = parse_output(output)

            print(f"Compressed {input_file} with threshold {threshold} to {compressed_raw_file}")
            print(f"Old Bits: {old_bits}, New Bits: {new_bits}, Compression Ratio: {compression_ratio}, BPV: {bpv}, PSNR: {psnr}")

            # Write compression info to CSV
            writer.writerow([threshold, old_bits, new_bits, compression_ratio, bpv, psnr, compressed_raw_file, decompressed_raw_file])

if __name__ == "__main__":
    main()
