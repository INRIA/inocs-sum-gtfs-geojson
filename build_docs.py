import subprocess

subprocess.run([
    "pdoc",
    "src/sum_gtfs_geojson",
    "--output-dir", "docs",
    "--docformat", "google",
])
