# PureFlix Account Checker 🔍🔒

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green)

This Python script verifies PureFlix accounts using a list of email and password pairs from a text file (`accounts.txt`). It checks credentials by sending HTTP requests to PureFlix's API and saves valid accounts to a file (`hits.txt`).

## Features 🚀

- **Parallel Verification**: Utilizes threads to verify multiple accounts simultaneously, improving processing speed.
- **Real-time Writing**: Valid accounts are written directly to `hits.txt` as they are found.
- **Configurable and Efficient**: Uses a reusable HTTP session to handle requests efficiently and manage network errors.
