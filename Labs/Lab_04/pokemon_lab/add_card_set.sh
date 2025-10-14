#!/bin/bash
# Prompts the user for a set ID and fetches the corresponding card data.

read -p "Enter the TCG Card Set ID (e.g., base1): " SET_ID

if [ -z "$SET_ID" ]; then
    echo "Error: Set ID cannot be empty." >&2
    exit 1
fi

echo "Fetching data for set ID: $SET_ID..."
curl "https://api.pokemontcg.io/v2/cards?q=set.id:$SET_ID" -o "card_set_lookup/$SET_ID.json"
