from pandas import read_csv

def read_zips():
    return read_csv("zips.csv")

def main():
    zips_df = read_zips()
    print(zips_df.head(10))

if __name__ == "__main__":
    main()