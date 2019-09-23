Once this module is installed, you can assign NACE categories to your partners
by simply adding the corresponding category in the partner's form.

Obtaining updated data
======================
The data imported into Odoo is generated from the files downloaded
from the RAMON service::

    http://ec.europa.eu/eurostat/ramon/nomenclatures/index.cfm?TargetUrl=LST_CLS_DLD&StrNom=NACE_REV2&StrLanguageCode=FR&StrLayoutCode=#

If you want to update the data or add another translation, download the
corresponding file from RAMON in CSV format, using ',' as a separator.
Save it to the directory "data" and name it according to the language
code::

    NACE_REV2_<language code>.csv

Then update the LANGS constant in the script "make_data.py" and run it to
refresh the Odoo data files. Finally, upgrade the module to load the data.
