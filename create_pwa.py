import sys
from PIL import Image
import os

# USAGE: pass 2 arguments
# arg 1: directory in which files for index.html,sw,js,app.js and manifest.json will be created
# arg 2: photo which will serve as icon for your pwa, will be resized to dimensions of widths 48,64,192,512

def check_args(args):
  if len(sys.argv) < 3:
    print("Please pass a directory and an img in order to create the icon for your pwa")
    sys.exit(0);
  imgsrc = sys.argv[2]
  if not imgsrc.endswith("png") and not imgsrc.endswith("jpg") and not imgsrc.endsWith("jpeg") and not imgsrc.endswith("svg") and not imgsrc.endswith("gif"):
    print("The second argument is not an img")
    sys.exit(0)
    
def main():
  check_args(sys.argv)
  # assign arguments
  directory = sys.argv[1]
  imgsrc = sys.argv[2]
  # create directory if it doesn't exist
  if not os.path.exists(directory):
    os.makedirs(directory)
  imgext,imgname = imgsrc[::-1].split(".",1)
  imgname = (imgname.split("/",1)[0])[::-1]
  imgext = imgext[::-1]
  basewidths = [512,192,64,48]
  img = Image.open(imgsrc)
  message = """
  {
    "short_name": "createpwa",
    "name": "createpwa",
    "icons": [ """
  for x in range(0,len(basewidths)):
    wpercent = (basewidths[x]/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    new_img = img.resize((basewidths[x],hsize), Image.ANTIALIAS)
    new_name = imgname + '_' + str(basewidths[x]) + '.' + imgext
    new_img.save(directory + "/" + new_name)
    message = message + """
      {
        "src": """ + """ "___""" + new_name + """___",
        "type": "image/""" + imgext + """",
        "sizes": """ + """ "___""" + str(basewidths[x]) + """x"""  + str(basewidths[x]) +  """___"
      }"""
    if(x != len(basewidths) - 1):
      message = message + ""","""
  message = message + """ 
    ],
    "start_url": "index.html",
    "background_color": "#002856",
    "theme_color": "#002856",
    "display": "standalone"
  }
   """
  message = message.replace('___','')
  fm = open(directory + "/" + 'manifest.json','w')
  fm.write(message)
  fm.close()

  fsw = open(directory + "/" + 'sw.js','w')
  message = """
  // Cache ID version
  const cacheID = 'v1';
  // Files to precache
  const cacheFiles = [
    // HTML Files
    './index.html',
    // CSS Files
    // Image Files
    // JS Files
    './sw.js',
    './app.js',
    // Misc. Files
    './manifest.json',
  ];

  // Service Worker Install Event
  self.addEventListener('install', function(event) {
    console.log('Attempting to install service worker and cache static assets');
    event.waitUntil(
      caches.open(cacheID)
      .then(function(cache) {
        return cache.addAll(cacheFiles);
      })
      .catch(function(error) {
        console.log(`Unable to add cached assets: ${error}`);
      })
    );
  });

  // Service Worker Activate Event
  self.addEventListener('activate', function(e) {
    e.waitUntil(
      // Load up all items from cache, and check if cache items are not outdated
      caches.keys().then(function(keyList) {
        return Promise.all(keyList.map(function(key) {
          if (key !== cacheID) {
            console.log('[ServiceWorker] Removing old cache', key);
            return caches.delete(key);
          }
        }));
      })
    );
    return self.clients.claim();
  });

  self.addEventListener('fetch', function(event) {
    event.respondWith(
      caches.open(cacheID).then(function(cache) {
        return cache.match(event.request).then(function (response) {
          return response || fetch(event.request).then(function(response) {
            if (event.request.method != "POST") {
              cache.put(event.request, response.clone());
            }
            return response;
          })
          .catch(function(error) {
            console.log("error: " + error);
            return caches.match('./offline.html');
          });;
        });
      })
    );
  });
  """

  fsw.write(message)
  fsw.close()
  
  fapp = open(directory + "/" + 'app.js','w')
  message = """
  // check if service is supported by users browsers
  if ('serviceWorker' in navigator) {
    try {
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
          // Register the service worker passing our service worker code
          navigator.serviceWorker.register('sw.js').then((registration) => {
            // Registration was successful
            console.log('ServiceWorker registration successful!', registration.scope);
          }, (err) => {
            console.log('ServiceWorker registration failed: ', err);
          });
        });
      }
    } catch (e) {
         console.log(e) // Probably want to use some free JS error tracking tool here like Sentry
    }
  }
  """

  fapp.write(message)
  fapp.close()
  
  findex = open(directory + "/" + 'index.html','w')
  message = """
  <html>
    <head>
      <meta charset="utf-8" />
      <meta name="theme-color" content="#002856" />
      <link rel="manifest" href="manifest.json">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <script src="sw.js" defer></script>
      <script src="app.js" defer></script>
    </head>
    <body>
      <p>Hello World!</p>
    </body>
  </html>"""

  findex.write(message)
  findex.close()
   
main()
