"""Script for start spiders from code. Useful for testing and debugging."""
import sys

from scrapy import cmdline

cmdline.execute(sys.argv[1].split())
