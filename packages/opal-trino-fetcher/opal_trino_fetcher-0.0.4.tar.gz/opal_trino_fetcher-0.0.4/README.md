# opal-trino-fetcher

`opal-trino-fetcher` is an OPAL fetch provider designed to bring authorization state from Trino. This package allows you to fetch data from Trino and use it within the OPAL framework.

## Features

- Fetch data from Trino using custom queries.
- Integrate fetched data into OPAL for authorization purposes.
- Supports both basic and advanced configurations.

## Installation

To install the package, you can use pip:

```sh
pip install opal-trino-fetcher
```

## Usage

### Basic Usage

To use the `opal-trino-fetcher`, you need to configure it within your OPAL setup. Below is an example configuration:

```json
    {
   "config":{
      "entries":[
         {
            "url":"localhost",
            "config":{
               "fetcher":"TrinoFetchProvider",
               "query":"SELECT * FROM TABLE_NAME",
               "fetch_key":"table_name",
               "connection_params":{
                  "user":"username",
                  "password":"password",
                  "port":8000
               }
            },
            "topics":[
               "policy_data"
            ],
            "dst_path":"cities",
            "periodic_update_interval":10
         }
      ]
   }
}
```

## Building the Package

To build the package, follow these steps:

1. Ensure you have `build` installed:

    ```sh
    pip install build
    ```

2. Navigate to the root directory of your project and run:

    ```sh
    python -m build
    ```

3. This will create a `dist` directory with the built package.

### Docker Setup

You can also use Docker to run the `opal-trino-fetcher`. Below is an example `Dockerfile`:

```Dockerfile
FROM permitio/opal-client:latest

COPY .\dist\opal_trino_fetcher-$VERSION-py3-none-any.whl /tmp/opal_trino_fetcher-$VERSION-py3-none-any.whl

RUN pip install --user /tmp/opal_trino_fetcher-0.0.2-py3-none-any.whl
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## Contact

For any questions or inquiries, please contact open an issue.
