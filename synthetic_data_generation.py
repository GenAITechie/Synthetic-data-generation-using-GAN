import pandas as pd
import boto3
import argparse

def generate_synthetic_data(input_path, output_path):
    # Load real data from S3
    real_data = pd.read_csv(input_path)
    
    # Initialize and train the model
    model = CTGAN()
    model.fit(real_data)
    
    # Generate synthetic data
    synthetic_data = model.sample(len(real_data))
    
    # Save synthetic data to CSV
    synthetic_data.to_csv('synthetic_data.csv', index=False)
    
    # Upload synthetic data to S3
    s3 = boto3.client('s3')
    bucket, key = output_path.replace("s3://", "").split("/", 1)
    s3.upload_file('synthetic_data.csv', bucket, key)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, help='S3 path to input data')
    parser.add_argument('--output_path', type=str, help='S3 path to output data')
    args = parser.parse_args()
    generate_synthetic_data(args.input_path, args.output_path)
