import requests
from mv import get_cameras, get_snapshot
from urlalive import url_alive
from datetime import datetime, timedelta
import logging
from pathlib import Path


def main():
    logger = logging.getLogger('get-snapshot')
    file_handler = logging.FileHandler(f'{str(Path.home())}/caterpillar-cam/get-snapshot.log')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info('Getting list of cameras from Meraki...')

    cameras = get_cameras()
    camera_name = cameras[0]['name']
    logger.debug(f'{cameras}')
    timestamp = datetime.now().replace(microsecond=0).isoformat()
    logger.debug(f'{timestamp}')
    logger.info(f'Getting snapshot link from {camera_name}...')
    snapshot = get_snapshot(cameras[0]['networkId'], cameras[0]['serial'])
    url = snapshot['url']
    logger.debug(f'Snapshot URL: {url}')

    if url_alive(url, retries=10, seconds=5, ok=3):
        response = requests.request('GET', url, stream=True)
        with open(f'{str(Path.home())}/caterpillar-cam/images/{timestamp}.jpeg', 'wb') as image:
            for chunk in response:
                image.write(chunk)
        logger.info('Getting snapshot from Meraki successful.')
    else:
        logger.warning('Failed to download image.')

if __name__ == '__main__':
    main()
