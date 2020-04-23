'''Utility functions for dealing with Meraki MV cameras and snapshots'''

import meraki
from meraki import APIError
from datetime import datetime, timedelta

dashboard = meraki.DashboardAPI(output_log=False)

def get_orgs():
    return dashboard.organizations.getOrganizations()

def get_cameras(orgs=None):
    """Fetch a list MV cameras given a list of organization IDs.

    Args:
        orgids: A list of dashboard organizations as dictionaries.

    Returns:
        A list of MV camera dictionaries.
    """
    if orgs is None:
        orgs = get_orgs()
    cameras = []
    for org in orgs:
        try:
            devices = dashboard.devices.getOrganizationDevices(org['id'])
            devices = [device for device in devices if 'MV' in device['model']]
            for device in devices:
                device['orgid'] = org['id']
                device['orgname'] = org['name']
                cameras.append(device)
        except APIError as e:
            continue # the Meraki SDK already logs errors
    return cameras

def get_snapshot(networkid, serial, timestamp=None, series=None):
    """Fetch a snapshot link for a given camera and timestamp. Bring back a series of 3 snapshots if series is True.

    Args:
        networkid: Dashboard network ID the camera is a part of.
        serial: Serial number of the MV camera.
        timestamp: Timestamp for the snapshot as a datetime object.
        series: True/False if a series of 3 snapshot links should be returned as a list.

    Returns:
        Dictionary containing a single snapshot url or a list of dictionaries containing snapshot urls.
    """
    if timestamp and isinstance(timestamp, datetime):
        if series:
            snapshot_series = []
            for series in range(1, 4):
                series_timestamp = timedelta(seconds=series) + timestamp
                series_timestamp = series_timestamp.isoformat()
                snapshot = dashboard.cameras.generateNetworkCameraSnapshot(networkid, serial, timestamp=series_timestamp)
                snapshot['timestamp'] = series_timestamp
                snapshot_series.append(snapshot)
            return snapshot_series
        else:
            timestamp = timestamp.isoformat()
            return dashboard.cameras.generateNetworkCameraSnapshot(networkid, serial, timestamp=timestamp)
    else:
        return dashboard.cameras.generateNetworkCameraSnapshot(networkid, serial)

if __name__ == '__main__':
    cameras = get_cameras()
    print(cameras)
    ts = datetime.now() - timedelta(hours=6)
    print(get_snapshot(cameras[0]['networkId'], cameras[0]['serial'], timestamp=ts))
    snapshots = get_snapshot(cameras[0]['networkId'], cameras[0]['serial'], timestamp=ts, series=True)
    for snapshot in snapshots:
        print(snapshot)
