About this module
-----------------

Django commands for reporting code statistics (Classes, KLOCs, etc) from
your django project. Reporting Ruby on Rails' rake stats like stats.

Feature
~~~~~~~

::

    python manage.py matome

this command report something like this.

::

    +----------------------+---------+---------+---------+---------+---------+---------+---------+
    | Name                 |  FILES  |  Lines  |   LOC   | Classes | Methods |   M/C   |  LOC/M  |
    +----------------------+---------+---------+---------+---------+---------+---------+---------+
    | View                 |       1 |       2 |       2 |       1 |       0 |     0.0 |     0.0 |
    | Model                |       0 |       0 |       0 |       0 |       0 |     0.0 |     0.0 |
    | Route                |       1 |      10 |       7 |       0 |       0 |     0.0 |     0.0 |
    | Other Modules        |       4 |     108 |      95 |       0 |       0 |     0.0 |     0.0 |
    | JS                   |       0 |       0 |       0 |       0 |       0 |     0.0 |     0.0 |
    | Coffee               |       0 |       0 |       0 |       0 |       0 |     0.0 |     0.0 |
    +----------------------+---------+---------+---------+---------+---------+---------+---------+
    | Total                |       6 |     120 |     104 |       1 |       0 |     0.0 |     0.0 |
    +----------------------+---------+---------+---------+---------+---------+---------+---------+

TODO
~~~~

Many things.
