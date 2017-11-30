# CS410-Project
Final Project for CS410 - Address Standardization and Merging

Potential Master Address Data Available From:
1. it looks like open addresses makes their address data available on github already: https://github.com/openaddresses/
2. https://aws.amazon.com/public-datasets/osm/
3. https://www.data.gov/
4. https://openaddresses.io/

General Reminder Notes:
- install ArcGIS for Python in order to use the TIGER files from the Census Bureau and add city/state information to the open addresses

Approaches for Address Parsing:
1. unigram language model to parse address and match to master data for tagging
2. hidden markov
3. CRF
4. maybe use KNN for matching?
