# Caterpillar Cam
While stuck at home during the COVID-19 pandemic, my wife and daughter started
to keep caterpillars. Their lifecycle is really cool and well known. The pay
off is when they become butterflies, of course. A challenge of this lifecycle
is being present to witness the awesome changes as a caterpillar turns into a
chrysalis and ultimately into a butterfly.

To meet this challenge I employed the use of a Meraki MV12 camera and the
dashboard API. The snapshot API endpoint allowed us to grab a snapshot of every
hour and watch them grow. This way we don't have to watch hours of video
recording to see their growth. I plan on making a time lapse video with the
images after the butterflies emerge.

I used a few tools to make life easier:
 - Python 3
 - Meraki Dashboard API library
 - PHP, JS, CSS, and HTML to make a simple website to show the images captured
 thus far (copied from W3 schools)
 - Raspberry Pi 3 to host the scripts and images
 - Meraki MV12
