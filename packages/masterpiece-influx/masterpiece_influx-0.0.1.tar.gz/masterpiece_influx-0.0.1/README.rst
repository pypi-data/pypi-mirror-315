InfluxDB V3 Plugin for MasterPiece
==================================

This project adds InfluxDB V3 timeseries recording functionality to `MasterPiece` framework.


Usage
-----

To install:

.. code-block:: bash

  pip install masterpiece_influx

Once installed, you can create `config/Influx.json` configuration file to specify
information needed for reading and writing time series data to desired Influx database.

.. code-block:: text
		
  {"token": "your token",
   "org": "your organization",
   "host": "https://eu-central-1-1.aws.cloud2.influxdata.com",
   "database": "your database"
  }


License
-------

This project is licensed under the MIT License - see the `LICENSE` file for details.
