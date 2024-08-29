
import requests

#TODO to be used for mp4 like files
def fetch_data(download_url: str, session: requests.Session, timeout: int, file_path: str, http2: bool):
    """
    Fetch Data from Url.

    Parameters
    ----------
    download_url : str
        The url that hosts the .ts file

    session : requests.Session
        The session using which we can make a request

    timeout : int
        The time period after which the request expires

    file_path : str
        The path where the file needs to be stored

    http2: bool
        A boolean to specify the need for http2 support

    Returns
    -------
    Optional[str]
        Returns a string containing the download link that failed
    """
    try:
        if http2:
            if ":path" in session.headers:
                parsed_suffix = urlparse(download_url).path
                session.headers[":path"] = parsed_suffix

        with session.get(download_url, timeout=timeout, stream=True) as request_data:
            request_data.raise_for_status()
            if request_data.status_code == 302:
                request_data = redirect_handler(session, request_data)

            file = open(file_path, "ab")

            for chunk in request_data.iter_content(10485760):
                if not chunk:
                    break

                file.write(chunk)
            
            file.close()

    except (ConnectionResetError, ConnectionRefusedError, ConnectionError,
            TimeoutError, ConnectionAbortedError, OSError):
        return download_url


<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
<video id="video"></video>
<script>
  if(Hls.isSupported()) {
    var video = document.getElementById('video');
    var hls = new Hls();
    hls.loadSource('http://cdncities.com/deranalive/deranalive/playlist.m3u8');
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED,function() {
      video.play();
  });
 }
 // hls.js is not supported on platforms that do not have Media Source Extensions (MSE) enabled.
 // When the browser has built-in HLS support (check using `canPlayType`), we can provide an HLS manifest (i.e. .m3u8 URL) directly to the video element throught the `src` property.
 // This is using the built-in support of the plain video element, without using hls.js.
  else if (video.canPlayType('application/vnd.apple.mpegurl')) {
    video.src = 'http://cdncities.com/deranalive/deranalive/playlist.m3u8';
    video.addEventListener('canplay',function() {
      video.play();
    });
  }
</script>