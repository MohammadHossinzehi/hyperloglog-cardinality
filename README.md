# HyperLogLog Cardinality Estimator

## Overview

Production-grade implementation of HyperLogLog — a probabilistic data structure for counting distinct elements in massive datasets with ~1.04 / sqrt(m) standard error while consuming sublinear memory.

## Why HyperLogLog?

Traditional distinct-count algorithms scale linearly with cardinality. Tracking 10 million unique users with a traditional set consumes too much memory. HyperLogLog trades accuracy for space — a 0.01% decrease in accuracy for a 10,000x reduction in memory on cardinality estimates.

## Features

- Fast Cardinality Estimation: O(1) time complexity per element
- Sublinear Memory: O(log log U) space. Default p=14 uses 16,384 bytes
- Configurable Precision: Adjust p from 4-16 to calibrate accuracy
- Merge: Combine multiple HyperLogLog instances without reprocessing
- Bias Corrections: Automatic small/large range adjustments
- Comprehensive Tests: Full unit test coverage included

## Installation

Copy hyperloglog.py into your project. No external dependencies required.

## Usage

from hyperloglog import HyperLogLog

hll = HyperLogLog()
hll.add("alice")
hll.add("bob")
hll.add("alice")  # Duplicate ignored

count = hll.cardinality()  # Returns approximately 2

hll2 = HyperLogLog()
hll2.add("charlie")
merged = hll.merge(hll2)
print(merged.cardinality())  # Returns approximately 3

## API

Constructor: HyperLogLog(p=14)
- p: Precision bits (4-16, default 14)

Methods:
- add(x): Add element
- cardinality(): Get estimated count
- merge(other): Combine two HyperLogLog instances
- clear(): Reset to empty
- size_bytes(): Return memory usage

## Tests

python -m unittest test_hyperloglog.py -v

Tests cover: basic operations, large sets, duplicates, merging, clearing, precision validation, and memory usage.

## Complexity

| Operation | Time | Memory |
|-----------|------|--------|
| add(x) | O(1) | O(1) |
| cardinality() | O(2^p) | O(1) |
| merge() | O(2^p) | O(1) |
