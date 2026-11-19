# Viva Questions and Answers

## What is Flask?

Flask is a lightweight Python web framework. Here it receives HTTP requests, serves the static page, and connects routes to Python services.

## What is pandas?

pandas is a Python library for tabular data. It reads CSV files into DataFrames, detects duplicates, handles missing values, merges data, and exports CSV results.

## Why use a service layer?

It keeps mathematics separate from web code. The same function can be tested or reused without a browser or Flask request.

## Why does the app use strings for set elements?

CSV values can be numeric or textual. Converting to cleaned strings gives deterministic comparisons and makes `1` and `1.0` consistent.

## What is an equivalence relation?

It is reflexive, symmetric, and transitive. Such a relation divides a set into non-overlapping equivalence classes.

## Why is data not persistent?

The project is a local learning tool. An in-memory store keeps the design simple and avoids database setup. Restarting deliberately clears data.

## What is the difference between a set and a table?

A set removes duplicates and ignores order mathematically. A table keeps rows, including repeated rows. This is why join row counts can differ from distinct-key counts.
