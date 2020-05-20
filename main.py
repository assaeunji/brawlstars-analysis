import argparse
from pathlib import Path
import pandas as pd
from bsparser import brawlparser
from datetime import datetime

def get_datetime(fmt="%Y%m%d%H%M"):
    return datetime.strftime(datetime.now(), fmt)

def get_parser(_=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--token_path", type=str, help="path of API token")
    parser.add_argument("--output_dir", type=str, help="output directory")
    parser.add_argument("--tag_path", type=str, help="path of tags")
    parser.add_argument("--tag", type=str, help="initial tag")
    return parser


if __name__ == "__main__":
    args, _ = get_parser().parse_known_args()
    tags = pd.read_csv(Path(args.tag_path).expanduser())['0'].tolist() if args.tag_path else args.tag

    print(args)
    
    # expanduser(): 절대경로로 대체
    init        = brawlparser(Path(args.token_path).expanduser(), args.tag)
    all_logs    = init.parse_all_users(tags)
    
    df_all_logs = pd.DataFrame(all_logs)
    df_all_logs.to_csv(Path(args.output_dir).expanduser().joinpath(f"log_{get_datetime()}.csv"), index=False)
    
