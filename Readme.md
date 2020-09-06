### Link Shrink - API

This repository stores, backend API source code for the Link Shrink Service.

**To run the API Server**

````bash
$ sudo chmod 777 start.sh
$ ./start.sh
````

**End points**

- `/ ` POST request

  ````json
  {
    "url":"www.google.com",
    "todo": "short"
  }
  ````

  **Response**:

  ````json
  {
    "url": "http://0.0.0.0:5000/1e673a4c"
  }
  ````

- `/ ` POST request

  ````
  {
    "url":"http://0.0.0.0:5000/1e673a4c",
    "todo": "long"
  }
  ````

  **Response**:

  ````json
  {
    "url": "www.google.com"
  }
  ````

- `/<short-url-key>` GET request

  ````
  http://0.0.0.0:5000/1e673a4c
  ````

  **Response:**

  Redirected to long URL automatically.

  