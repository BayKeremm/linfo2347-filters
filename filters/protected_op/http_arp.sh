#!/bin/bash

arp_output=$(arp -n)

elements=$(echo "$arp_output" | awk 'NR>1 {print $3}')

while IFS= read -r pair; do
  $(nft add element arp http_arp_filter authorized { $pair })
done <<< "$elements"
