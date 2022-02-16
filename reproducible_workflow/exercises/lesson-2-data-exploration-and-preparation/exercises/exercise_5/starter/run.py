#!/usr/bin/env python
import os
import argparse
import logging
import pandas as pd
import wandb

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    run = wandb.init(project="exercise_5", job_type="process_data")

    ## YOUR CODE HERE
    # read the file from wandb
    logger.info('read the file frow wandb')
    artifact = run.use_artifact(args.input_artifact)
    path_to_file = artifact.file()
    df = pd.read_parquet(path_to_file)

    # pre-process the file
    logger.info('pre-process the file')
    df = df.drop_duplicates().reset_index(drop=True)
    df['title'].fillna(value=' ', inplace=True)
    df['song_name'].fillna(value=' ', inplace=True)
    df['text_feature'] = df['title'] + ' ' + df['song_name']

    # inspection shows that there are nan in column 'loundness'
    df['loudness'].fillna(df['loudness'].mean(), inplace=True)

    # check there is no nan left
    assert not df.isna().any().any()
    logger.info(f'result of check of nans in df: {df.isna().any().any()}')

    # save the file and upload it to an artifact
    logger.info('save the file as csv')
    file_name = args.artifact_name
    df.to_csv(file_name)

    artifact = wandb.Artifact(
        name=args.artifact_name,
        type=args.artifact_type,
        description=args.artifact_description
    )
    artifact.add_file(file_name)
    logger.info("Logging artifact")
    run.log_artifact(artifact)

    # remove the file created locally
    logger.info('remove the file created locally')
    os.remove(file_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preprocess a dataset",
        fromfile_prefix_chars="@",
    )

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True,
    )

    parser.add_argument(
        "--artifact_name", type=str, help="Name for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_type", type=str, help="Type for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_description",
        type=str,
        help="Description for the artifact",
        required=True,
    )

    args = parser.parse_args()

    go(args)
