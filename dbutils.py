import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARTEMiS main entry point")
    parser.add_argument("--config", "-c", type=str, default="config", help="Configuration folder")
    args = parser.parse_args()