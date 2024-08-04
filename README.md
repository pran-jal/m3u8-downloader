# TS Downloader

Download all .ts parts and .m3u8 file from .m3u8 link that can be played in VLC.

# TODO
    download .ts using ffmpeg
    .ts are not merged properly

## TRY

    Some TS files do not start with SyncByte 0x47, they can not be played after merging,
        
        Need to remove the bytes before the SyncByte 0x47(71).

        https://en.wikipedia.org/wiki/MPEG_transport_stream