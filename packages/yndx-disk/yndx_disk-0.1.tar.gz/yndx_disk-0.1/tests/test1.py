import asyncio

from yndx_disk.api.disk import get_disk_info
from yndx_disk.clients import AsyncDiskClient, DiskClient


token = "y0_AgAAAABEv3LAAADLWwAAAAEbu2zjAADsLbpHvl9B348K8P29_rrEx_W1-A"
# token = "y0_AgAAAAB0f9ugAAr16AAAAAD8mVZ6AAAURr55tgpMSoyIqcR3NyxzI9t2zw"

# async def main():
#     client = DiskClient(token)
#     client.update_disk_info()
#
# asyncio.run(main())

client = DiskClient(token)
client.update_disk_info()