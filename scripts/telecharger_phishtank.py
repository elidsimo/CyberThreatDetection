from __future__ import annotations

from io import StringIO
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd


OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "urls_phishtank_brutes.csv"
PHISHTANK_URL = "https://data.phishtank.com/data/online-valid.csv"
USER_AGENT = "phishtank-download-script/1.0"


def download_phishtank_csv() -> pd.DataFrame:
    request = Request(PHISHTANK_URL, headers={"User-Agent": USER_AGENT})

    try:
        with urlopen(request) as response:
            content = response.read().decode("utf-8", errors="replace")
    except HTTPError as error:
        raise RuntimeError(f"PhishTank returned HTTP {error.code} for the public feed.") from error
    except URLError as error:
        raise RuntimeError(f"Unable to reach PhishTank: {error.reason}.") from error

    if not content.strip():
        raise RuntimeError("PhishTank returned an empty response.")

    df = pd.read_csv(StringIO(content))
    if df.empty:
        raise RuntimeError("PhishTank returned a valid CSV with no rows.")

    return df


def main() -> int:
    try:
        df = download_phishtank_csv()
    except RuntimeError as error:
        print(f"Download failed: {error}")
        return 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(df.shape)
    print(df.head())
    print(f"Saved to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
