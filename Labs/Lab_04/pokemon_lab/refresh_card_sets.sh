#!/bin/bash
# Loops through all existing JSON files in the lookup directory and re-runs the API call to update the data.

echo "Refreshing all card sets in card_set_lookup/..."

for FILE in card_set_lookup/*.json; do
    if [ -f "$FILE" ]; then
        SET_ID=$(basename "$FILE" .json)
        echo "Updating set: $SET_ID..."
        curl -s "https://api.pokemontcg.io/v2/cards?q=set.id:$SET_ID" -o "$FILE"
        echo "Data written to $FILE"
    fi
done

echo "All card sets have been refreshed."
