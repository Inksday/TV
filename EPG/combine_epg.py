import gzip
import xml.etree.ElementTree as ET
import requests
from collections import defaultdict
import io

# List of .xml.gz URLs
file_urls = [
    "https://epgshare01.online/epgshare01/epg_ripper_AR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_AU1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_BEIN1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_BG1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_BR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_CA1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_CL1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_CO1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_CR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_CY1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_DE1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_DK1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_ES1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_FANDUEL1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_FR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_GR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_HR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_IL1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_IN4.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_IT1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_MX1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_MY1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_NL1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_NZ1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_PK1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_PL1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_PT1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_RO1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_RO2.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_SA1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_SE1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_TR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_UK1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_US1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_US_LOCALS2.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_UY1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_ZA1.xml.gz"
]

# Remove duplicate URLs
file_urls = list(dict.fromkeys(file_urls))

# Dictionaries to store unique channels and programmes
channels = {}
programmes = defaultdict(list)

# Process each file
for url in file_urls:
    try:
        # Download and decompress the file
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with gzip.GzipFile(fileobj=io.BytesIO(response.content), mode='rb') as f:
            tree = ET.parse(f)
            root = tree.getroot()

            # Extract channels
            for channel in root.findall('channel'):
                channel_id = channel.get('id')
                if channel_id and channel_id not in channels:
                    channels[channel_id] = channel

            # Extract programmes
            for programme in root.findall('programme'):
                title = programme.find('title').text if programme.find('title') is not None else ''
                programme_key = (
                    programme.get('channel', ''),
                    programme.get('start', ''),
                    title
                )
                programmes[programme_key].append(programme)

    except Exception as e:
        print(f"Error processing {url}: {e}")

# Create a new XML tree
combined_root = ET.Element('tv')

# Add unique channels
for channel in channels.values():
    combined_root.append(channel)

# Add unique programmes (first occurrence of each)
for programme_key, programme_list in programmes.items():
    combined_root.append(programme_list[0])

# Save to a compressed .xml.gz file
combined_tree = ET.ElementTree(combined_root)
with io.BytesIO() as buffer:
    combined_tree.write(buffer, encoding='utf-8', xml_declaration=True)
    buffer.seek(0)
    with gzip.open('DDL_EPG_COMBINED.xml.gz', 'wb') as f:
        f.write(buffer.read())
